"""
Load Testing Module
Evaluates response times and system behavior under maximum limits
"""

import pytest
import asyncio
import logging
from typing import Dict, Any, List
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.test_utils import (
    TestMetrics,
    ResourceMonitor,
    run_concurrent_requests,
    generate_test_data,
    print_test_summary
)

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.timeout(1800)  # 30 minute timeout
class TestLoadTesting:
    """Load testing suite for evaluating system performance"""
    
    async def test_concurrent_users_load(self, test_config):
        """
        Test system with concurrent users (1000 users)
        Simulates realistic user load
        """
        logger.info("Starting concurrent users load test (1000 users)")
        
        url = f"{test_config['api_gateway_url']}/health"
        concurrent_users = min(1000, test_config['load_test_users'])
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        metrics = await run_concurrent_requests(
            url=url,
            method='GET',
            data=None,
            count=concurrent_users,
            max_concurrent=concurrent_users,
            timeout=30
        )
        
        await resource_monitor.stop_monitoring()
        
        print_test_summary(f"Concurrent Users Load Test ({concurrent_users} users)", metrics, resource_monitor)
        
        # Performance assertions
        assert metrics.success_count > 0, "No successful requests"
        
        summary = metrics.get_summary()
        if 'avg_response_time' in summary:
            assert summary['avg_response_time'] < 5.0, f"Average response time {summary['avg_response_time']:.2f}s exceeds 5s threshold"
            assert summary['p95_response_time'] < 10.0, f"95th percentile {summary['p95_response_time']:.2f}s exceeds 10s threshold"
    
    async def test_ramp_up_load(self, test_config):
        """
        Ramp-up load test - gradually increase load
        Tests: System behavior as load increases
        """
        logger.info("Starting ramp-up load test")
        
        url = f"{test_config['api_gateway_url']}/health"
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        all_metrics = TestMetrics()
        all_metrics.start()
        
        # Ramp up stages
        stages = [
            (100, 50, "100 users"),
            (250, 125, "250 users"),
            (500, 250, "500 users"),
            (1000, 500, "1000 users"),
        ]
        
        for users, max_concurrent, stage_name in stages:
            logger.info(f"Ramp-up stage: {stage_name}")
            
            metrics = await run_concurrent_requests(
                url=url,
                method='GET',
                data=None,
                count=users,
                max_concurrent=max_concurrent,
                timeout=30
            )
            
            all_metrics.success_count += metrics.success_count
            all_metrics.failure_count += metrics.failure_count
            all_metrics.response_times.extend(metrics.response_times)
            all_metrics.errors.extend(metrics.errors)
            
            # Brief pause between stages
            await asyncio.sleep(2.0)
        
        all_metrics.end()
        await resource_monitor.stop_monitoring()
        
        print_test_summary("Ramp-up Load Test (100-1000 users)", all_metrics, resource_monitor)
        
        total_requests = all_metrics.success_count + all_metrics.failure_count
        success_rate = (all_metrics.success_count / total_requests) * 100
        assert success_rate >= 85.0, f"Success rate {success_rate:.2f}% below 85% threshold"
    
    async def test_sustained_high_load(self, test_config):
        """
        Sustained high load test (2000 requests over 2 minutes)
        Tests: System stability under continuous high load
        """
        logger.info("Starting sustained high load test")
        
        url = f"{test_config['api_gateway_url']}/health"
        duration_seconds = 120  # 2 minutes
        requests_per_second = 20
        total_requests = duration_seconds * requests_per_second
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        metrics = TestMetrics()
        metrics.start()
        
        import aiohttp
        from utils.test_utils import make_request
        
        async with aiohttp.ClientSession() as session:
            for second in range(duration_seconds):
                if second % 10 == 0:
                    logger.info(f"Progress: {second}/{duration_seconds} seconds")
                
                tasks = []
                for _ in range(requests_per_second):
                    task = make_request(session, 'GET', url, None, 10)
                    tasks.append(task)
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, dict) and result.get('success'):
                        metrics.record_success(result['response_time'])
                    else:
                        error_msg = str(result) if isinstance(result, Exception) else result.get('error', 'Unknown')
                        metrics.record_failure(error_msg)
                
                await asyncio.sleep(1.0)
        
        metrics.end()
        await resource_monitor.stop_monitoring()
        
        print_test_summary("Sustained High Load Test (2 minutes)", metrics, resource_monitor)
        
        success_rate = (metrics.success_count / total_requests) * 100
        assert success_rate >= 90.0, f"Success rate {success_rate:.2f}% below 90% threshold"
        
        summary = metrics.get_summary()
        if 'avg_response_time' in summary:
            assert summary['avg_response_time'] < 3.0, f"Average response time {summary['avg_response_time']:.2f}s exceeds 3s"
    
    async def test_peak_load_capacity(self, test_config):
        """
        Peak load capacity test
        Tests: Maximum request handling capacity
        """
        logger.info("Starting peak load capacity test")
        
        url = f"{test_config['api_gateway_url']}/health"
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        # Test increasing concurrent load
        results_by_load = []
        
        for concurrent_load in [100, 500, 1000, 2000]:
            logger.info(f"Testing with {concurrent_load} concurrent requests")
            
            metrics = await run_concurrent_requests(
                url=url,
                method='GET',
                data=None,
                count=concurrent_load,
                max_concurrent=concurrent_load,
                timeout=30
            )
            
            summary = metrics.get_summary()
            results_by_load.append({
                'load': concurrent_load,
                'success_rate': summary['success_rate'],
                'avg_response_time': summary.get('avg_response_time', 0),
                'requests_per_second': summary['requests_per_second']
            })
            
            # Brief pause
            await asyncio.sleep(3.0)
        
        await resource_monitor.stop_monitoring()
        
        # Print results
        print("\n" + "=" * 80)
        print("PEAK LOAD CAPACITY TEST RESULTS")
        print("=" * 80)
        print(f"{'Load':<15} {'Success Rate':<15} {'Avg Response (s)':<20} {'Req/s':<15}")
        print("-" * 80)
        
        for result in results_by_load:
            print(f"{result['load']:<15} {result['success_rate']:>13.2f}% {result['avg_response_time']:>18.3f} {result['requests_per_second']:>13.2f}")
        
        print("=" * 80 + "\n")
        
        # At least lower loads should have good success rate
        assert results_by_load[0]['success_rate'] >= 90.0, "Low load test failed"
    
    async def test_mixed_endpoint_load(self, test_config):
        """
        Mixed endpoint load test
        Tests: Load distribution across multiple endpoints
        """
        logger.info("Starting mixed endpoint load test")
        
        resource_monitor = ResourceMonitor()
        await resource_monitor.start_monitoring()
        
        all_metrics = TestMetrics()
        all_metrics.start()
        
        # Test different endpoints
        endpoints = [
            (f"{test_config['api_gateway_url']}/health", 'GET', None, 500),
            (f"{test_config['api_gateway_url']}/status", 'GET', None, 300),
            (f"{test_config['api_gateway_url']}/metrics", 'GET', None, 200),
        ]
        
        for url, method, data, count in endpoints:
            logger.info(f"Testing {url.split('/')[-1]} endpoint with {count} requests")
            
            metrics = await run_concurrent_requests(
                url=url,
                method=method,
                data=data,
                count=count,
                max_concurrent=200,
                timeout=30
            )
            
            all_metrics.success_count += metrics.success_count
            all_metrics.failure_count += metrics.failure_count
            all_metrics.response_times.extend(metrics.response_times)
            all_metrics.errors.extend(metrics.errors)
        
        all_metrics.end()
        await resource_monitor.stop_monitoring()
        
        print_test_summary("Mixed Endpoint Load Test (1000 requests)", all_metrics, resource_monitor)
        
        total_requests = all_metrics.success_count + all_metrics.failure_count
        success_rate = (all_metrics.success_count / total_requests) * 100
        assert success_rate >= 85.0, f"Success rate {success_rate:.2f}% below 85% threshold"
    
    async def test_response_time_distribution(self, test_config):
        """
        Response time distribution analysis
        Tests: Consistency of response times under load
        """
        logger.info("Starting response time distribution test")
        
        url = f"{test_config['api_gateway_url']}/health"
        
        metrics = await run_concurrent_requests(
            url=url,
            method='GET',
            data=None,
            count=5000,
            max_concurrent=500,
            timeout=30
        )
        
        summary = metrics.get_summary()
        
        print("\n" + "=" * 80)
        print("RESPONSE TIME DISTRIBUTION ANALYSIS")
        print("=" * 80)
        
        if 'avg_response_time' in summary:
            print(f"\nResponse Time Statistics (5000 requests):")
            print(f"  Minimum:              {summary['min_response_time']:.3f}s")
            print(f"  Average:              {summary['avg_response_time']:.3f}s")
            print(f"  Median:               {summary['median_response_time']:.3f}s")
            print(f"  95th Percentile:      {summary['p95_response_time']:.3f}s")
            print(f"  99th Percentile:      {summary['p99_response_time']:.3f}s")
            print(f"  Maximum:              {summary['max_response_time']:.3f}s")
            
            # Response time consistency check
            p95_p50_ratio = summary['p95_response_time'] / summary['median_response_time']
            print(f"\nConsistency Ratio (P95/Median): {p95_p50_ratio:.2f}x")
            
            assert p95_p50_ratio < 5.0, f"Response time inconsistency: {p95_p50_ratio:.2f}x variation"
        
        print("=" * 80 + "\n")


@pytest.mark.asyncio
async def test_quick_load_validation(test_config):
    """
    Quick load test validation (500 requests)
    Fast smoke test for load testing infrastructure
    """
    logger.info("Running quick load validation (500 requests)")
    
    url = f"{test_config['api_gateway_url']}/health"
    
    metrics = await run_concurrent_requests(
        url=url,
        method='GET',
        data=None,
        count=500,
        max_concurrent=250,
        timeout=10
    )
    
    print_test_summary("Quick Load Validation (500 requests)", metrics)
    
    assert metrics.success_count > 0, "No successful requests"
    success_rate = (metrics.success_count / 500) * 100
    assert success_rate >= 80.0, f"Success rate {success_rate:.2f}% below 80%"
