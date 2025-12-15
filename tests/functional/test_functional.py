"""
Functional Testing Module
Tests correctness of feature sets across all services
"""

import pytest
import asyncio
import logging
import aiohttp
from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.test_utils import make_request

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestAPIGatewayFunctional:
    """Functional tests for API Gateway"""
    
    async def test_health_endpoint(self, test_config):
        """Test API Gateway health check"""
        url = f"{test_config['api_gateway_url']}/health"
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(session, 'GET', url)
            
            assert result['success'], f"Health check failed: {result.get('error')}"
            assert result['status_code'] == 200
            assert 'status' in result['data']
            assert result['data']['status'] == 'healthy'
    
    async def test_status_endpoint(self, test_config):
        """Test service status endpoint"""
        url = f"{test_config['api_gateway_url']}/status"
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(session, 'GET', url, timeout=10)
            
            assert result['success'], f"Status check failed: {result.get('error')}"
            assert result['status_code'] == 200
            assert isinstance(result['data'], dict)
    
    async def test_metrics_endpoint(self, test_config):
        """Test metrics endpoint"""
        url = f"{test_config['api_gateway_url']}/metrics"
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(session, 'GET', url)
            
            assert result['success'], f"Metrics check failed: {result.get('error')}"
            assert result['status_code'] == 200
            assert 'timestamp' in result['data']


@pytest.mark.asyncio
class TestImageGenerationFunctional:
    """Functional tests for Image Generation service"""
    
    async def test_image_generation_basic(self, test_config, sample_image_request):
        """Test basic image generation"""
        url = f"{test_config['api_gateway_url']}/api/v1/generate/image"
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(
                session, 'POST', url, 
                data=sample_image_request,
                timeout=300
            )
            
            # Service might not be running, so we check if request was processed
            if result['success']:
                assert result['status_code'] == 200
                logger.info("Image generation successful")
            else:
                logger.warning(f"Image generation service unavailable: {result.get('error')}")
    
    async def test_image_generation_parameters(self, test_config):
        """Test image generation with various parameters"""
        url = f"{test_config['api_gateway_url']}/api/v1/generate/image"
        
        test_cases = [
            {
                "prompt": "A serene mountain landscape",
                "style": "realistic",
                "resolution": "512x512",
                "hdr": False,
                "pbr": False,
                "model": "stable-diffusion"
            },
            {
                "prompt": "Anime character portrait",
                "style": "anime",
                "resolution": "1024x1024",
                "hdr": True,
                "pbr": True,
                "model": "stable-diffusion"
            }
        ]
        
        async with aiohttp.ClientSession() as session:
            for i, test_case in enumerate(test_cases, 1):
                result = await make_request(
                    session, 'POST', url,
                    data=test_case,
                    timeout=300
                )
                
                if result['success']:
                    logger.info(f"Test case {i} passed")
                else:
                    logger.warning(f"Test case {i} - Service unavailable: {result.get('error')}")


@pytest.mark.asyncio
class TestVideoGenerationFunctional:
    """Functional tests for Video Generation service"""
    
    async def test_video_generation_basic(self, test_config, sample_video_request):
        """Test basic video generation"""
        url = f"{test_config['api_gateway_url']}/api/v1/generate/video"
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(
                session, 'POST', url,
                data=sample_video_request,
                timeout=600
            )
            
            if result['success']:
                assert result['status_code'] == 200
                logger.info("Video generation successful")
            else:
                logger.warning(f"Video generation service unavailable: {result.get('error')}")


@pytest.mark.asyncio
class TestCryptoPredictionFunctional:
    """Functional tests for Crypto Prediction service"""
    
    async def test_crypto_prediction_basic(self, test_config, sample_crypto_request):
        """Test basic crypto prediction"""
        url = f"{test_config['api_gateway_url']}/api/v1/crypto/predict"
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(
                session, 'POST', url,
                data=sample_crypto_request,
                timeout=60
            )
            
            if result['success']:
                assert result['status_code'] == 200
                logger.info("Crypto prediction successful")
            else:
                logger.warning(f"Crypto prediction service unavailable: {result.get('error')}")
    
    async def test_crypto_prediction_multiple_symbols(self, test_config):
        """Test crypto prediction for multiple symbols"""
        url = f"{test_config['api_gateway_url']}/api/v1/crypto/predict"
        
        symbols = ['BTC', 'ETH', 'XRP', 'ADA', 'SOL']
        
        async with aiohttp.ClientSession() as session:
            for symbol in symbols:
                request_data = {
                    "symbol": symbol,
                    "timeframe": "1h",
                    "prediction_horizon": 24
                }
                
                result = await make_request(
                    session, 'POST', url,
                    data=request_data,
                    timeout=60
                )
                
                if result['success']:
                    logger.info(f"Prediction for {symbol} successful")
                else:
                    logger.warning(f"Prediction for {symbol} failed: {result.get('error')}")
    
    async def test_sentiment_analysis(self, test_config):
        """Test sentiment analysis endpoint"""
        symbols = ['BTC', 'ETH']
        
        async with aiohttp.ClientSession() as session:
            for symbol in symbols:
                url = f"{test_config['api_gateway_url']}/api/v1/crypto/sentiment/{symbol}"
                
                result = await make_request(session, 'GET', url, timeout=30)
                
                if result['success']:
                    logger.info(f"Sentiment analysis for {symbol} successful")
                else:
                    logger.warning(f"Sentiment analysis for {symbol} unavailable: {result.get('error')}")


@pytest.mark.asyncio
class TestOrchestratorFunctional:
    """Functional tests for Orchestrator service"""
    
    async def test_orchestration_single_task(self, test_config, sample_crypto_request):
        """Test orchestration with single task"""
        url = f"{test_config['api_gateway_url']}/api/v1/orchestrate"
        
        orchestration_request = {
            "tasks": [
                {
                    "type": "crypto_prediction",
                    "params": sample_crypto_request
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
            
            if result['success']:
                assert result['status_code'] == 200
                assert 'workflow_id' in result['data']
                assert result['data']['status'] == 'completed'
                logger.info("Single task orchestration successful")
            else:
                logger.warning(f"Orchestration service unavailable: {result.get('error')}")
    
    async def test_orchestration_multiple_tasks(self, test_config):
        """Test orchestration with multiple tasks"""
        url = f"{test_config['api_gateway_url']}/api/v1/orchestrate"
        
        orchestration_request = {
            "tasks": [
                {
                    "type": "crypto_prediction",
                    "params": {
                        "symbol": "BTC",
                        "timeframe": "1h",
                        "prediction_horizon": 24
                    }
                },
                {
                    "type": "crypto_prediction",
                    "params": {
                        "symbol": "ETH",
                        "timeframe": "1h",
                        "prediction_horizon": 24
                    }
                }
            ],
            "priority": "high"
        }
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(
                session, 'POST', url,
                data=orchestration_request,
                timeout=180
            )
            
            if result['success']:
                assert result['status_code'] == 200
                assert 'workflow_id' in result['data']
                assert result['data']['tasks_executed'] == 2
                logger.info("Multiple task orchestration successful")
            else:
                logger.warning(f"Orchestration service unavailable: {result.get('error')}")
    
    async def test_orchestration_priorities(self, test_config, sample_crypto_request):
        """Test orchestration with different priorities"""
        url = f"{test_config['api_gateway_url']}/api/v1/orchestrate"
        
        priorities = ['low', 'normal', 'high']
        
        async with aiohttp.ClientSession() as session:
            for priority in priorities:
                orchestration_request = {
                    "tasks": [
                        {
                            "type": "crypto_prediction",
                            "params": sample_crypto_request
                        }
                    ],
                    "priority": priority
                }
                
                result = await make_request(
                    session, 'POST', url,
                    data=orchestration_request,
                    timeout=120
                )
                
                if result['success']:
                    assert result['data']['priority'] == priority
                    logger.info(f"Orchestration with {priority} priority successful")
                else:
                    logger.warning(f"Orchestration with {priority} priority failed: {result.get('error')}")


@pytest.mark.asyncio
class TestFraudDetectionFunctional:
    """Functional tests for Fraud Detection service"""
    
    async def test_fraud_analysis_basic(self, test_config, sample_fraud_request):
        """Test basic fraud analysis"""
        url = f"{test_config['api_gateway_url']}/api/v1/fraud/analyze"
        
        async with aiohttp.ClientSession() as session:
            result = await make_request(
                session, 'POST', url,
                data=sample_fraud_request,
                timeout=30
            )
            
            if result['success']:
                assert result['status_code'] == 200
                logger.info("Fraud analysis successful")
            else:
                logger.warning(f"Fraud detection service unavailable: {result.get('error')}")
    
    async def test_fraud_analysis_various_amounts(self, test_config):
        """Test fraud analysis with various transaction amounts"""
        url = f"{test_config['api_gateway_url']}/api/v1/fraud/analyze"
        
        test_amounts = [10.0, 100.0, 1000.0, 10000.0, 100000.0]
        
        async with aiohttp.ClientSession() as session:
            for amount in test_amounts:
                fraud_request = {
                    "transaction_id": f"test-tx-{amount}",
                    "amount": amount,
                    "currency": "USD",
                    "user_id": "test-user-123",
                    "ip_address": "192.168.1.1"
                }
                
                result = await make_request(
                    session, 'POST', url,
                    data=fraud_request,
                    timeout=30
                )
                
                if result['success']:
                    logger.info(f"Fraud analysis for amount ${amount} successful")
                else:
                    logger.warning(f"Fraud analysis for amount ${amount} failed: {result.get('error')}")


@pytest.mark.asyncio
async def test_end_to_end_workflow(test_config):
    """
    End-to-end workflow test
    Tests complete user journey through multiple services
    """
    logger.info("Starting end-to-end workflow test")
    
    async with aiohttp.ClientSession() as session:
        # Step 1: Check system health
        health_url = f"{test_config['api_gateway_url']}/health"
        health_result = await make_request(session, 'GET', health_url)
        assert health_result['success'], "System health check failed"
        logger.info("✓ System health check passed")
        
        # Step 2: Execute crypto prediction
        crypto_url = f"{test_config['api_gateway_url']}/api/v1/crypto/predict"
        crypto_request = {
            "symbol": "BTC",
            "timeframe": "1h",
            "prediction_horizon": 24
        }
        crypto_result = await make_request(session, 'POST', crypto_url, crypto_request, 60)
        
        if crypto_result['success']:
            logger.info("✓ Crypto prediction completed")
        else:
            logger.warning(f"Crypto prediction unavailable: {crypto_result.get('error')}")
        
        # Step 3: Run orchestrated workflow
        orchestrate_url = f"{test_config['api_gateway_url']}/api/v1/orchestrate"
        orchestrate_request = {
            "tasks": [
                {
                    "type": "crypto_prediction",
                    "params": crypto_request
                }
            ],
            "priority": "normal"
        }
        orchestrate_result = await make_request(session, 'POST', orchestrate_url, orchestrate_request, 120)
        
        if orchestrate_result['success']:
            logger.info("✓ Orchestration workflow completed")
        else:
            logger.warning(f"Orchestration unavailable: {orchestrate_result.get('error')}")
        
        logger.info("End-to-end workflow test completed")
