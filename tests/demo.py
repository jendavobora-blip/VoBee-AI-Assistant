#!/usr/bin/env python3
"""
Quick QA Test Demo
Demonstrates the QA testing framework with a simple example
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.test_utils import (
    TestMetrics,
    ResourceMonitor,
    run_concurrent_requests,
    print_test_summary
)


async def demo_stress_test():
    """Demo: Simple stress test with 1000 requests"""
    print("\n" + "="*80)
    print("DEMO: Stress Test - 1000 Health Check Requests")
    print("="*80 + "\n")
    
    url = "http://localhost:8000/health"
    
    # Start resource monitoring
    monitor = ResourceMonitor()
    await monitor.start_monitoring()
    
    # Run stress test
    print("Sending 1000 concurrent requests...")
    metrics = await run_concurrent_requests(
        url=url,
        method='GET',
        data=None,
        count=1000,
        max_concurrent=100,
        timeout=10
    )
    
    # Stop monitoring
    await monitor.stop_monitoring()
    
    # Print results
    print_test_summary("Demo Stress Test", metrics, monitor)


async def demo_load_test():
    """Demo: Load test with gradual ramp-up"""
    print("\n" + "="*80)
    print("DEMO: Load Test - Ramp-up Pattern")
    print("="*80 + "\n")
    
    url = "http://localhost:8000/health"
    
    stages = [50, 100, 200]
    all_metrics = TestMetrics()
    all_metrics.start()
    
    for stage in stages:
        print(f"\nStage: {stage} concurrent requests")
        
        metrics = await run_concurrent_requests(
            url=url,
            method='GET',
            data=None,
            count=stage,
            max_concurrent=stage,
            timeout=10
        )
        
        # Aggregate metrics
        all_metrics.success_count += metrics.success_count
        all_metrics.failure_count += metrics.failure_count
        all_metrics.response_times.extend(metrics.response_times)
        
        await asyncio.sleep(1.0)
    
    all_metrics.end()
    print_test_summary("Demo Load Test (Ramp-up)", all_metrics)


async def demo_functional_test():
    """Demo: Basic functional testing"""
    print("\n" + "="*80)
    print("DEMO: Functional Test - API Endpoints")
    print("="*80 + "\n")
    
    import aiohttp
    from utils.test_utils import make_request
    
    endpoints = [
        ("Health", "http://localhost:8000/health", "GET", None),
        ("Status", "http://localhost:8000/status", "GET", None),
        ("Metrics", "http://localhost:8000/metrics", "GET", None),
    ]
    
    async with aiohttp.ClientSession() as session:
        for name, url, method, data in endpoints:
            print(f"Testing {name} endpoint...")
            result = await make_request(session, method, url, data, 10)
            
            if result['success']:
                print(f"  ✓ {name}: SUCCESS (status={result['status_code']}, time={result['response_time']:.3f}s)")
            else:
                print(f"  ✗ {name}: FAILED ({result.get('error', 'Unknown error')})")
        
        print("\nFunctional test completed!")


async def main():
    """Run demo tests"""
    print("\n" + "="*80)
    print("VoBee AI Assistant - QA Testing Framework Demo")
    print("="*80)
    print("\nThis demo showcases the QA testing capabilities:")
    print("  1. Stress Testing - High volume requests")
    print("  2. Load Testing - Gradual load increase")
    print("  3. Functional Testing - Endpoint validation")
    print("\nNote: Ensure services are running (docker-compose up -d)")
    print("="*80)
    
    try:
        # Run demos
        await demo_functional_test()
        await demo_stress_test()
        await demo_load_test()
        
        print("\n" + "="*80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nNext steps:")
        print("  - Run full tests: python run_tests.py all")
        print("  - Run stress tests: python run_tests.py stress --iterations 50000")
        print("  - Run load tests: python run_tests.py load --users 1000")
        print("  - See README.md for more options")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure services are running: docker-compose up -d")
        print("  2. Check service health: curl http://localhost:8000/health")
        print("  3. Review logs: docker-compose logs")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
