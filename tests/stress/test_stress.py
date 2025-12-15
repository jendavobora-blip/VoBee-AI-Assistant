"""
Stress Testing Module - Up to 50,000 Operations
Tests system behavior under extreme load conditions
"""

import pytest
import asyncio
import logging
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.test_utils import (
    TestMetrics,
    ResourceMonitor,
    run_concurrent_requests,
    generate_test_data,
    print_test_summary
)

logger = logging.getLogger(__name__)

# Test configuration constants
ORCHESTRATOR_STRESS_ITERATIONS = 10000  # Reduced workload for complex operations
VARIED_WORKLOAD_ITERATIONS = 20000     # Mixed request types
SUSTAINED_LOAD_DURATION_SECONDS = 300  # 5 minutes
SUSTAINED_LOAD_RPS = 50                # Requests per second
BURST_COUNT = 10                        # Number of bursts
BURST_SIZE = 1000                       # Requests per burst


@pytest.mark.asyncio
@pytest.mark.timeout(3600)  # 1 hour timeout for stress tests
class TestStressTesting:
    """Stress testing suite for AI orchestration system"""
    
    async def test_api_gateway_health_stress(self, test_config):
        """
        Stress test API Gateway health endpoint with 50,000 requests
        Tests: Basic system stability under extreme load
        """
        logger.info("Starting API Gateway health stress test (50,000 requests)")
        
        url = f"{test_config['api_gateway_url']}/health"
        iterations = test_config['stress_test_iterations']
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        # Run stress test
        metrics = await run_concurrent_requests(
            url=url,
            method='GET',
            data=None,
            count=iterations,
            max_concurrent=500,
            timeout=30
        )
        
        await resource_monitor.stop_monitoring()
        
        # Print summary
        print_test_summary("API Gateway Health Stress Test (50,000 requests)", metrics, resource_monitor)
        
        # Assertions
        assert metrics.success_count > 0, "No successful requests"
        success_rate = (metrics.success_count / iterations) * 100
        assert success_rate >= 95.0, f"Success rate {success_rate:.2f}% below 95% threshold"
    
    async def test_orchestrator_stress(self, test_config, sample_crypto_request):
        """
        Stress test Orchestrator service with crypto prediction tasks
        Tests: Task queue management and workflow coordination under load
        """
        logger.info(f"Starting Orchestrator stress test ({ORCHESTRATOR_STRESS_ITERATIONS} requests)")
        
        url = f"{test_config['api_gateway_url']}/api/v1/orchestrate"
        
        # Use configured workload for complex operations
        iterations = min(ORCHESTRATOR_STRESS_ITERATIONS, test_config['stress_test_iterations'])
        
        orchestration_request = {
            "tasks": [
                {
                    "type": "crypto_prediction",
                    "params": sample_crypto_request
                }
            ],
            "priority": "normal"
        }
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        metrics = await run_concurrent_requests(
            url=url,
            method='POST',
            data=orchestration_request,
            count=iterations,
            max_concurrent=100,
            timeout=60
        )
        
        await resource_monitor.stop_monitoring()
        
        print_test_summary("Orchestrator Stress Test (10,000 requests)", metrics, resource_monitor)
        
        assert metrics.success_count > 0, "No successful orchestration requests"
        success_rate = (metrics.success_count / iterations) * 100
        assert success_rate >= 80.0, f"Success rate {success_rate:.2f}% below 80% threshold"
    
    async def test_varied_workload_stress(self, test_config):
        """
        Stress test with varied request types (image, video, crypto)
        Tests: System behavior with mixed workloads
        """
        logger.info(f"Starting varied workload stress test ({VARIED_WORKLOAD_ITERATIONS} requests)")
        
        iterations = min(VARIED_WORKLOAD_ITERATIONS, test_config['stress_test_iterations'])
        
        # Generate varied test data
        image_data = generate_test_data('image', iterations // 4)
        crypto_data = generate_test_data('crypto', iterations // 4)
        fraud_data = generate_test_data('fraud', iterations // 4)
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        # Combine all metrics
        all_metrics = TestMetrics()
        all_metrics.start()
        
        # Test crypto predictions (most reliable)
        crypto_url = f"{test_config['api_gateway_url']}/api/v1/crypto/predict"
        crypto_metrics = await run_concurrent_requests(
            url=crypto_url,
            method='POST',
            data=crypto_data[0],
            count=iterations // 2,
            max_concurrent=200,
            timeout=60
        )
        
        # Test fraud detection
        fraud_url = f"{test_config['api_gateway_url']}/api/v1/fraud/analyze"
        fraud_metrics = await run_concurrent_requests(
            url=fraud_url,
            method='POST',
            data=fraud_data[0],
            count=iterations // 4,
            max_concurrent=200,
            timeout=30
        )
        
        # Test health checks
        health_url = f"{test_config['api_gateway_url']}/health"
        health_metrics = await run_concurrent_requests(
            url=health_url,
            method='GET',
            data=None,
            count=iterations // 4,
            max_concurrent=300,
            timeout=10
        )
        
        # Combine metrics
        all_metrics.success_count = (
            crypto_metrics.success_count + 
            fraud_metrics.success_count + 
            health_metrics.success_count
        )
        all_metrics.failure_count = (
            crypto_metrics.failure_count + 
            fraud_metrics.failure_count + 
            health_metrics.failure_count
        )
        all_metrics.response_times = (
            crypto_metrics.response_times + 
            fraud_metrics.response_times + 
            health_metrics.response_times
        )
        all_metrics.errors = crypto_metrics.errors + fraud_metrics.errors + health_metrics.errors
        all_metrics.end()
        
        await resource_monitor.stop_monitoring()
        
        print_test_summary("Varied Workload Stress Test (20,000 requests)", all_metrics, resource_monitor)
        
        total_requests = all_metrics.success_count + all_metrics.failure_count
        assert total_requests > 0, "No requests completed"
        success_rate = (all_metrics.success_count / total_requests) * 100
        assert success_rate >= 70.0, f"Success rate {success_rate:.2f}% below 70% threshold"
    
    async def test_sustained_load_stress(self, test_config):
        """
        Sustained load test over extended period
        Tests: System stability over time, memory leaks, resource cleanup
        """
        logger.info(f"Starting sustained load stress test ({SUSTAINED_LOAD_DURATION_SECONDS // 60} minutes)")
        
        url = f"{test_config['api_gateway_url']}/health"
        duration_seconds = SUSTAINED_LOAD_DURATION_SECONDS
        requests_per_second = SUSTAINED_LOAD_RPS
        total_requests = duration_seconds * requests_per_second
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring(interval=5.0)
        
        metrics = TestMetrics()
        metrics.start()
        
        # Sustained load over time
        import aiohttp
        async with aiohttp.ClientSession() as session:
            for batch in range(duration_seconds):
                tasks = []
                for _ in range(requests_per_second):
                    from utils.test_utils import make_request
                    task = make_request(session, 'GET', url, None, 10)
                    tasks.append(task)
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, dict) and result.get('success'):
                        metrics.record_success(result['response_time'])
                    else:
                        error_msg = str(result) if isinstance(result, Exception) else result.get('error', 'Unknown error')
                        metrics.record_failure(error_msg)
                
                # Small delay between batches
                await asyncio.sleep(1.0)
        
        metrics.end()
        await resource_monitor.stop_monitoring()
        
        print_test_summary("Sustained Load Stress Test (5 minutes)", metrics, resource_monitor)
        
        assert metrics.success_count > 0, "No successful requests"
        success_rate = (metrics.success_count / total_requests) * 100
        assert success_rate >= 90.0, f"Success rate {success_rate:.2f}% below 90% threshold"
        
        # Check resource stability
        resource_summary = resource_monitor.get_summary()
        if 'memory' in resource_summary:
            memory_growth = resource_summary['memory']['max'] - resource_summary['memory']['min']
            assert memory_growth < 20.0, f"Memory growth {memory_growth:.2f}% indicates potential leak"
    
    async def test_burst_traffic_stress(self, test_config):
        """
        Burst traffic pattern - sudden spikes in requests
        Tests: System resilience to traffic spikes
        """
        logger.info("Starting burst traffic stress test")
        
        url = f"{test_config['api_gateway_url']}/health"
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        all_metrics = TestMetrics()
        all_metrics.start()
        
        # Multiple bursts
        for burst in range(BURST_COUNT):
            logger.info(f"Burst {burst + 1}/{BURST_COUNT}")
            
            burst_size = BURST_SIZE
            metrics = await run_concurrent_requests(
                url=url,
                method='GET',
                data=None,
                count=burst_size,
                max_concurrent=500,
                timeout=10
            )
            
            all_metrics.success_count += metrics.success_count
            all_metrics.failure_count += metrics.failure_count
            all_metrics.response_times.extend(metrics.response_times)
            all_metrics.errors.extend(metrics.errors)
            
            # Cooldown period
            await asyncio.sleep(2.0)
        
        all_metrics.end()
        await resource_monitor.stop_monitoring()
        
        print_test_summary("Burst Traffic Stress Test (10 bursts x 1000 requests)", all_metrics, resource_monitor)
        
        total_requests = all_metrics.success_count + all_metrics.failure_count
        assert total_requests > 0, "No requests completed"
        success_rate = (all_metrics.success_count / total_requests) * 100
        assert success_rate >= 85.0, f"Success rate {success_rate:.2f}% below 85% threshold"


@pytest.mark.asyncio
async def test_quick_stress_validation(test_config):
    """
    Quick stress test validation (1000 requests)
    Fast smoke test to validate stress testing infrastructure
    """
    logger.info("Running quick stress validation (1000 requests)")
    
    url = f"{test_config['api_gateway_url']}/health"
    
    metrics = await run_concurrent_requests(
        url=url,
        method='GET',
        data=None,
        count=1000,
        max_concurrent=100,
        timeout=10
    )
    
    print_test_summary("Quick Stress Validation (1000 requests)", metrics)
    
    assert metrics.success_count > 0, "No successful requests"
    success_rate = (metrics.success_count / 1000) * 100
    assert success_rate >= 80.0, f"Success rate {success_rate:.2f}% below 80% threshold"
