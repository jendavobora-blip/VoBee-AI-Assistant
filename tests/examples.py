#!/usr/bin/env python3
"""
Simple Example: Standalone QA Test
Demonstrates basic usage without pytest
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.test_utils import (
    TestMetrics,
    ResourceMonitor,
    run_concurrent_requests,
    print_test_summary
)


async def example_simple_test():
    """
    Example 1: Simple stress test
    Tests API Gateway health endpoint with 100 requests
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple Stress Test")
    print("="*80 + "\n")
    
    # Configuration
    api_url = os.getenv('API_GATEWAY_URL', 'http://localhost:8000')
    url = f"{api_url}/health"
    
    print(f"Target URL: {url}")
    print("Sending 100 concurrent requests...\n")
    
    # Run test
    metrics = await run_concurrent_requests(
        url=url,
        method='GET',
        data=None,
        count=100,
        max_concurrent=50,
        timeout=10
    )
    
    # Display results
    print_test_summary("Simple Stress Test", metrics)
    
    # Basic assertions
    total = metrics.success_count + metrics.failure_count
    success_rate = (metrics.success_count / total * 100) if total > 0 else 0
    
    if success_rate >= 80:
        print("✅ TEST PASSED: Success rate >= 80%")
    else:
        print("❌ TEST FAILED: Success rate < 80%")
    
    return success_rate >= 80


async def example_with_monitoring():
    """
    Example 2: Test with resource monitoring
    Shows how to monitor CPU and memory during tests
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Test with Resource Monitoring")
    print("="*80 + "\n")
    
    api_url = os.getenv('API_GATEWAY_URL', 'http://localhost:8000')
    url = f"{api_url}/health"
    
    # Create resource monitor
    monitor = ResourceMonitor()
    await monitor.start_monitoring(interval=0.5)
    
    print("Running test with resource monitoring...\n")
    
    # Run test
    metrics = await run_concurrent_requests(
        url=url,
        method='GET',
        data=None,
        count=200,
        max_concurrent=100,
        timeout=10
    )
    
    # Stop monitoring
    await monitor.stop_monitoring()
    
    # Display results with resource usage
    print_test_summary("Test with Monitoring", metrics, monitor)
    
    return True


async def example_custom_test():
    """
    Example 3: Custom test with manual request tracking
    Demonstrates low-level control
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Custom Test Implementation")
    print("="*80 + "\n")
    
    import aiohttp
    from utils.test_utils import make_request
    
    api_url = os.getenv('API_GATEWAY_URL', 'http://localhost:8000')
    
    # Initialize metrics
    metrics = TestMetrics()
    metrics.start()
    
    # Test different endpoints
    endpoints = [
        ('Health', f"{api_url}/health"),
        ('Status', f"{api_url}/status"),
        ('Metrics', f"{api_url}/metrics"),
    ]
    
    async with aiohttp.ClientSession() as session:
        for name, url in endpoints:
            print(f"Testing {name} endpoint: {url}")
            
            # Send 10 requests to each endpoint
            for i in range(10):
                result = await make_request(session, 'GET', url, timeout=10)
                
                if result['success']:
                    metrics.record_success(result['response_time'])
                else:
                    metrics.record_failure(result.get('error', 'Unknown error'))
            
            print(f"  ✓ Completed 10 requests to {name}")
    
    metrics.end()
    
    # Display summary
    print_test_summary("Custom Test", metrics)
    
    return True


async def example_varied_requests():
    """
    Example 4: Test with varied request types
    Shows testing different API operations
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Varied Request Types")
    print("="*80 + "\n")
    
    import aiohttp
    from utils.test_utils import make_request
    
    api_url = os.getenv('API_GATEWAY_URL', 'http://localhost:8000')
    
    metrics = TestMetrics()
    metrics.start()
    
    async with aiohttp.ClientSession() as session:
        # Test 1: GET requests
        print("Testing GET requests...")
        for _ in range(20):
            result = await make_request(
                session, 'GET', f"{api_url}/health", timeout=10
            )
            if result['success']:
                metrics.record_success(result['response_time'])
            else:
                metrics.record_failure(result.get('error', 'Unknown'))
        
        # Test 2: POST request with data
        print("Testing POST requests...")
        crypto_data = {
            "symbol": "BTC",
            "timeframe": "1h",
            "prediction_horizon": 24
        }
        
        for _ in range(10):
            result = await make_request(
                session, 'POST', 
                f"{api_url}/api/v1/crypto/predict",
                data=crypto_data,
                timeout=30
            )
            if result['success']:
                metrics.record_success(result['response_time'])
            else:
                metrics.record_failure(result.get('error', 'Service unavailable'))
    
    metrics.end()
    print_test_summary("Varied Requests Test", metrics)
    
    return True


async def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("VoBee AI Assistant - QA Testing Examples")
    print("="*80)
    print("\nThese examples demonstrate how to use the QA testing framework.")
    print("Make sure services are running: docker-compose up -d")
    print("="*80)
    
    results = []
    
    try:
        # Run examples
        results.append(("Simple Test", await example_simple_test()))
        results.append(("Monitoring Test", await example_with_monitoring()))
        results.append(("Custom Test", await example_custom_test()))
        results.append(("Varied Requests", await example_varied_requests()))
        
        # Summary
        print("\n" + "="*80)
        print("EXAMPLES SUMMARY")
        print("="*80)
        
        for name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"  {name:<20} {status}")
        
        all_passed = all(result[1] for result in results)
        
        print("="*80)
        
        if all_passed:
            print("\n🎉 All examples completed successfully!")
            print("\nNext steps:")
            print("  - Try the full demo: python demo.py")
            print("  - Run actual tests: python run_tests.py quick")
            print("  - See README.md for comprehensive guide")
        else:
            print("\n⚠️  Some examples failed - check if services are running")
            print("  Run: docker-compose up -d")
        
        print("="*80 + "\n")
        
        return 0 if all_passed else 1
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure services are running: docker-compose up -d")
        print("  2. Check API Gateway: curl http://localhost:8000/health")
        print("  3. Review logs: docker-compose logs")
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
