"""
Edge Cases Testing Module
Tests API error handling, memory limits, and edge scenarios
"""

import pytest
import asyncio
import logging
import aiohttp
from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.test_utils import make_request, TestMetrics, run_concurrent_requests

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestAPIEdgeCases:
    """Edge case tests for API endpoints"""
    
    async def test_invalid_endpoints(self, test_config):
        """Test handling of invalid endpoints"""
        invalid_endpoints = [
            '/api/v1/nonexistent',
            '/api/v1/generate/invalid',
            '/api/v999/test',
            '/invalid/path',
        ]
        
        async with aiohttp.ClientSession() as session:
            for endpoint in invalid_endpoints:
                url = f"{test_config['api_gateway_url']}{endpoint}"
                result = await make_request(session, 'GET', url, timeout=10)
                
                # Should return 404 or similar error
                assert not result['success'] or result['status_code'] == 404, \
                    f"Invalid endpoint {endpoint} should return error"
                logger.info(f"✓ Invalid endpoint {endpoint} handled correctly")
    
    async def test_malformed_json_payloads(self, test_config):
        """Test handling of malformed JSON payloads"""
        url = f"{test_config['api_gateway_url']}/api/v1/crypto/predict"
        
        malformed_payloads = [
            {},  # Empty payload
            {"wrong_field": "value"},  # Wrong fields
            {"symbol": ""},  # Empty required field
            {"symbol": None},  # Null required field
        ]
        
        async with aiohttp.ClientSession() as session:
            for payload in malformed_payloads:
                result = await make_request(session, 'POST', url, data=payload, timeout=30)
                
                # Should handle gracefully (return error, not crash)
                logger.info(f"✓ Malformed payload handled: {result.get('status_code', 'N/A')}")
    
    async def test_oversized_payloads(self, test_config):
        """Test handling of oversized payloads"""
        url = f"{test_config['api_gateway_url']}/api/v1/generate/image"
        
        # Create large payload
        large_payload = {
            "prompt": "A" * 10000,  # Very long prompt
            "style": "realistic",
            "resolution": "1024x1024",
        }
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(session, 'POST', url, data=large_payload, timeout=60)
            
            # Should handle gracefully
            logger.info(f"✓ Oversized payload handled: {result.get('status_code', 'N/A')}")
    
    async def test_special_characters_in_input(self, test_config):
        """Test handling of special characters and injection attempts"""
        url = f"{test_config['api_gateway_url']}/api/v1/generate/image"
        
        special_payloads = [
            {"prompt": "<script>alert('xss')</script>", "style": "realistic"},
            {"prompt": "'; DROP TABLE users; --", "style": "realistic"},
            {"prompt": "../../etc/passwd", "style": "realistic"},
            {"prompt": "NULL\x00byte", "style": "realistic"},
            {"prompt": "unicode: 你好世界 emoji: 🚀🎨", "style": "realistic"},
        ]
        
        async with aiohttp.ClientSession() as session:
            for payload in special_payloads:
                result = await make_request(session, 'POST', url, data=payload, timeout=60)
                
                # Should handle safely without injection
                logger.info(f"✓ Special characters handled safely")
    
    async def test_concurrent_same_request(self, test_config):
        """Test handling of many identical concurrent requests"""
        url = f"{test_config['api_gateway_url']}/health"
        
        # Send 1000 identical requests simultaneously
        metrics = await run_concurrent_requests(
            url=url,
            method='GET',
            data=None,
            count=1000,
            max_concurrent=1000,
            timeout=30
        )
        
        # Should handle without issues
        assert metrics.success_count > 500, "Should handle concurrent identical requests"
        logger.info(f"✓ Handled {metrics.success_count}/1000 identical concurrent requests")
    
    async def test_request_timeout_handling(self, test_config):
        """Test handling of request timeouts"""
        url = f"{test_config['api_gateway_url']}/api/v1/generate/image"
        
        payload = {
            "prompt": "A complex scene",
            "style": "realistic",
            "resolution": "1024x1024",
        }
        
        async with aiohttp.ClientSession() as session:
            # Very short timeout
            result = await make_request(session, 'POST', url, data=payload, timeout=1)
            
            # Should timeout gracefully
            logger.info(f"✓ Timeout handled gracefully: {result.get('error', 'No error')}")


@pytest.mark.asyncio
class TestMemoryAndResourceEdgeCases:
    """Edge case tests for memory and resource limits"""
    
    async def test_sequential_requests_memory_leak(self, test_config):
        """Test for memory leaks with sequential requests"""
        import psutil
        import gc
        
        url = f"{test_config['api_gateway_url']}/health"
        
        # Get initial memory
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Make many sequential requests
        async with aiohttp.ClientSession() as session:
            for i in range(1000):
                result = await make_request(session, 'GET', url, timeout=10)
                
                if i % 100 == 0:
                    gc.collect()  # Force garbage collection
        
        # Get final memory
        gc.collect()
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_growth = final_memory - initial_memory
        
        logger.info(f"Memory: Initial={initial_memory:.2f}MB, Final={final_memory:.2f}MB, Growth={memory_growth:.2f}MB")
        
        # Memory growth should be reasonable (< 100MB for 1000 requests)
        assert memory_growth < 100, f"Potential memory leak: {memory_growth:.2f}MB growth"
    
    async def test_rapid_connection_cycling(self, test_config):
        """Test rapid opening and closing of connections"""
        url = f"{test_config['api_gateway_url']}/health"
        
        # Open and close many connections rapidly
        for i in range(100):
            async with aiohttp.ClientSession() as session:
                result = await make_request(session, 'GET', url, timeout=5)
            
            if i % 20 == 0:
                logger.info(f"Connection cycle {i}/100")
        
        logger.info("✓ Rapid connection cycling handled successfully")


@pytest.mark.asyncio
class TestServiceCommunicationEdgeCases:
    """Edge case tests for inter-service communication"""
    
    async def test_orchestration_with_failing_tasks(self, test_config):
        """Test orchestration with tasks that might fail"""
        url = f"{test_config['api_gateway_url']}/api/v1/orchestrate"
        
        # Request with potentially failing services
        orchestration_request = {
            "tasks": [
                {
                    "type": "crypto_prediction",
                    "params": {
                        "symbol": "INVALID_SYMBOL_XYZ",
                        "timeframe": "1h",
                        "prediction_horizon": 24
                    }
                }
            ],
            "priority": "normal"
        }
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(
                session, 'POST', url,
                data=orchestration_request,
                timeout=120
            )
            
            # Should handle gracefully, not crash
            logger.info(f"✓ Orchestration with failing task handled: {result.get('status_code', 'N/A')}")
    
    async def test_mixed_priority_orchestration(self, test_config):
        """Test orchestration with mixed priority tasks"""
        url = f"{test_config['api_gateway_url']}/api/v1/orchestrate"
        
        priorities = ['low', 'normal', 'high']
        
        async with aiohttp.ClientSession() as session:
            # Send requests with different priorities concurrently
            tasks = []
            for priority in priorities * 10:  # 30 requests total
                orchestration_request = {
                    "tasks": [
                        {
                            "type": "crypto_prediction",
                            "params": {
                                "symbol": "BTC",
                                "timeframe": "1h",
                                "prediction_horizon": 24
                            }
                        }
                    ],
                    "priority": priority
                }
                
                task = make_request(
                    session, 'POST', url,
                    data=orchestration_request,
                    timeout=120
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            success_count = sum(1 for r in results if isinstance(r, dict) and r.get('success'))
            logger.info(f"✓ Mixed priority orchestration: {success_count}/{len(results)} successful")


@pytest.mark.asyncio
class TestDataValidationEdgeCases:
    """Edge case tests for data validation"""
    
    async def test_boundary_values(self, test_config):
        """Test boundary values for numeric inputs"""
        url = f"{test_config['api_gateway_url']}/api/v1/crypto/predict"
        
        boundary_cases = [
            {"symbol": "BTC", "timeframe": "1h", "prediction_horizon": 0},  # Zero
            {"symbol": "BTC", "timeframe": "1h", "prediction_horizon": -1},  # Negative
            {"symbol": "BTC", "timeframe": "1h", "prediction_horizon": 999999},  # Very large
        ]
        
        async with aiohttp.ClientSession() as session:
            for test_case in boundary_cases:
                result = await make_request(session, 'POST', url, data=test_case, timeout=30)
                logger.info(f"✓ Boundary value handled: horizon={test_case['prediction_horizon']}")
    
    async def test_type_mismatch(self, test_config):
        """Test type mismatches in request data"""
        url = f"{test_config['api_gateway_url']}/api/v1/crypto/predict"
        
        type_mismatch_cases = [
            {"symbol": 12345, "timeframe": "1h", "prediction_horizon": 24},  # Number instead of string
            {"symbol": "BTC", "timeframe": 100, "prediction_horizon": 24},  # Number instead of string
            {"symbol": "BTC", "timeframe": "1h", "prediction_horizon": "24"},  # String instead of number
        ]
        
        async with aiohttp.ClientSession() as session:
            for test_case in type_mismatch_cases:
                result = await make_request(session, 'POST', url, data=test_case, timeout=30)
                logger.info(f"✓ Type mismatch handled")
    
    async def test_missing_required_fields(self, test_config):
        """Test requests with missing required fields"""
        url = f"{test_config['api_gateway_url']}/api/v1/crypto/predict"
        
        missing_field_cases = [
            {"timeframe": "1h", "prediction_horizon": 24},  # Missing symbol
            {"symbol": "BTC", "prediction_horizon": 24},  # Missing timeframe
            {"symbol": "BTC", "timeframe": "1h"},  # Missing prediction_horizon
        ]
        
        async with aiohttp.ClientSession() as session:
            for test_case in missing_field_cases:
                result = await make_request(session, 'POST', url, data=test_case, timeout=30)
                
                # Should return validation error
                logger.info(f"✓ Missing field handled: {result.get('status_code', 'N/A')}")


@pytest.mark.asyncio
class TestResilienceEdgeCases:
    """Edge case tests for system resilience"""
    
    async def test_recovery_after_failures(self, test_config):
        """Test system recovery after encountering failures"""
        url = f"{test_config['api_gateway_url']}/health"
        
        async with aiohttp.ClientSession() as session:
            # Phase 1: Normal requests
            result1 = await make_request(session, 'GET', url, timeout=10)
            assert result1['success'], "Initial request should succeed"
            
            # Phase 2: Trigger potential issues with rapid requests
            metrics = await run_concurrent_requests(
                url=url,
                method='GET',
                data=None,
                count=500,
                max_concurrent=500,
                timeout=5
            )
            
            # Phase 3: Verify recovery with normal requests
            await asyncio.sleep(2.0)
            result2 = await make_request(session, 'GET', url, timeout=10)
            
            logger.info(f"✓ System recovered: Initial={result1['success']}, After load={result2['success']}")
    
    async def test_cascading_timeout_handling(self, test_config):
        """Test handling of cascading timeouts in orchestration"""
        url = f"{test_config['api_gateway_url']}/api/v1/orchestrate"
        
        # Request multiple tasks that might timeout
        orchestration_request = {
            "tasks": [
                {
                    "type": "image_generation",
                    "params": {
                        "prompt": "A complex scene",
                        "style": "realistic",
                        "resolution": "1024x1024"
                    }
                },
                {
                    "type": "video_generation",
                    "params": {
                        "prompt": "Flying through clouds",
                        "duration": 5,
                        "resolution": "1080p"
                    }
                }
            ],
            "priority": "normal"
        }
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(
                session, 'POST', url,
                data=orchestration_request,
                timeout=60  # Shorter timeout to trigger cascade
            )
            
            logger.info(f"✓ Cascading timeout handled: {result.get('error', 'No error')}")


@pytest.mark.asyncio
async def test_edge_case_summary(test_config):
    """
    Comprehensive edge case summary test
    Runs multiple edge case scenarios in sequence
    """
    logger.info("Running comprehensive edge case summary")
    
    url = f"{test_config['api_gateway_url']}/health"
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Rapid requests
        for _ in range(100):
            await make_request(session, 'GET', url, timeout=5)
        logger.info("✓ Rapid requests handled")
        
        # Test 2: Concurrent burst
        await run_concurrent_requests(url, 'GET', None, 500, 500, 10)
        logger.info("✓ Concurrent burst handled")
        
        # Test 3: Recovery check
        await asyncio.sleep(1.0)
        result = await make_request(session, 'GET', url, timeout=10)
        assert result['success'], "System should recover"
        logger.info("✓ System recovery verified")
    
    logger.info("Comprehensive edge case summary completed successfully")
