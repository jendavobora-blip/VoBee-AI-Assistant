"""
Utility functions for QA testing
"""

import time
import psutil
import logging
from typing import Dict, List, Any, Callable
from datetime import datetime
import asyncio
import aiohttp

logger = logging.getLogger(__name__)


class TestMetrics:
    """Track and calculate test metrics"""
    
    def __init__(self):
        self.response_times: List[float] = []
        self.errors: List[Dict[str, Any]] = []
        self.success_count: int = 0
        self.failure_count: int = 0
        self.start_time: float = None
        self.end_time: float = None
    
    def start(self):
        """Start timing"""
        self.start_time = time.time()
    
    def end(self):
        """End timing"""
        self.end_time = time.time()
    
    def record_success(self, response_time: float):
        """Record successful request"""
        self.success_count += 1
        self.response_times.append(response_time)
    
    def record_failure(self, error: str, response_time: float = None):
        """Record failed request"""
        self.failure_count += 1
        self.errors.append({
            'error': error,
            'timestamp': datetime.utcnow().isoformat(),
            'response_time': response_time
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        total_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
        total_requests = self.success_count + self.failure_count
        
        summary = {
            'total_requests': total_requests,
            'successful_requests': self.success_count,
            'failed_requests': self.failure_count,
            'success_rate': (self.success_count / total_requests * 100) if total_requests > 0 else 0,
            'total_time_seconds': total_time,
            'requests_per_second': total_requests / total_time if total_time > 0 else 0,
        }
        
        if self.response_times:
            sorted_times = sorted(self.response_times)
            summary.update({
                'avg_response_time': sum(self.response_times) / len(self.response_times),
                'min_response_time': min(self.response_times),
                'max_response_time': max(self.response_times),
                'median_response_time': sorted_times[len(sorted_times) // 2],
                'p95_response_time': sorted_times[int(len(sorted_times) * 0.95)],
                'p99_response_time': sorted_times[int(len(sorted_times) * 0.99)],
            })
        
        return summary


class ResourceMonitor:
    """Monitor system resource usage during tests"""
    
    def __init__(self):
        self.cpu_samples: List[float] = []
        self.memory_samples: List[float] = []
        self.monitoring = False
        self.monitor_task = None
    
    async def start_monitoring(self, interval: float = 1.0):
        """Start monitoring resources"""
        self.monitoring = True
        self.monitor_task = asyncio.create_task(self._monitor_loop(interval))
    
    async def stop_monitoring(self):
        """Stop monitoring resources"""
        self.monitoring = False
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
    
    async def _monitor_loop(self, interval: float):
        """Monitor loop"""
        while self.monitoring:
            try:
                cpu = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory().percent
                self.cpu_samples.append(cpu)
                self.memory_samples.append(memory)
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error monitoring resources: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get resource usage summary"""
        summary = {}
        
        if self.cpu_samples:
            summary['cpu'] = {
                'avg': sum(self.cpu_samples) / len(self.cpu_samples),
                'min': min(self.cpu_samples),
                'max': max(self.cpu_samples),
            }
        
        if self.memory_samples:
            summary['memory'] = {
                'avg': sum(self.memory_samples) / len(self.memory_samples),
                'min': min(self.memory_samples),
                'max': max(self.memory_samples),
            }
        
        return summary


async def make_request(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
    data: Dict[str, Any] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Make HTTP request with error handling
    
    Args:
        session: aiohttp session
        method: HTTP method
        url: Request URL
        data: Request data
        timeout: Request timeout
    
    Returns:
        Response data and metadata
    """
    start_time = time.time()
    
    try:
        async with session.request(
            method,
            url,
            json=data,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as response:
            response_time = time.time() - start_time
            
            try:
                response_data = await response.json()
            except Exception:
                response_data = await response.text()
            
            return {
                'success': response.status == 200,
                'status_code': response.status,
                'response_time': response_time,
                'data': response_data,
                'error': None
            }
    
    except asyncio.TimeoutError:
        return {
            'success': False,
            'status_code': None,
            'response_time': time.time() - start_time,
            'data': None,
            'error': 'Request timeout'
        }
    except Exception as e:
        return {
            'success': False,
            'status_code': None,
            'response_time': time.time() - start_time,
            'data': None,
            'error': str(e)
        }


async def run_concurrent_requests(
    url: str,
    method: str,
    data: Dict[str, Any],
    count: int,
    max_concurrent: int = 100,
    timeout: int = 30
) -> TestMetrics:
    """
    Run concurrent requests and collect metrics
    
    Args:
        url: Request URL
        method: HTTP method
        data: Request data
        count: Number of requests to make
        max_concurrent: Maximum concurrent requests
        timeout: Request timeout
    
    Returns:
        TestMetrics with results
    """
    metrics = TestMetrics()
    metrics.start()
    
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def limited_request(session):
        async with semaphore:
            result = await make_request(session, method, url, data, timeout)
            
            if result['success']:
                metrics.record_success(result['response_time'])
            else:
                metrics.record_failure(
                    result.get('error', f"Status: {result['status_code']}"),
                    result['response_time']
                )
    
    async with aiohttp.ClientSession() as session:
        tasks = [limited_request(session) for _ in range(count)]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    metrics.end()
    return metrics


def generate_test_data(data_type: str, count: int = 1) -> List[Dict[str, Any]]:
    """
    Generate test data for various scenarios
    
    Args:
        data_type: Type of test data to generate
        count: Number of data items to generate
    
    Returns:
        List of test data dictionaries
    """
    from faker import Faker
    fake = Faker()
    
    generators = {
        'image': lambda: {
            'prompt': fake.sentence(nb_words=6),
            'style': fake.random_element(['realistic', 'anime', 'oil-painting', 'abstract']),
            'resolution': fake.random_element(['512x512', '1024x1024']),
            'hdr': fake.boolean(),
            'pbr': fake.boolean(),
            'model': 'stable-diffusion'
        },
        'video': lambda: {
            'prompt': fake.sentence(nb_words=8),
            'duration': fake.random_int(min=3, max=10),
            'resolution': fake.random_element(['720p', '1080p']),
            'fps': fake.random_element([30, 60]),
            'use_nerf': fake.boolean(),
            'style': fake.random_element(['realistic', 'cinematic', 'abstract'])
        },
        'crypto': lambda: {
            'symbol': fake.random_element(['BTC', 'ETH', 'XRP', 'ADA', 'SOL']),
            'timeframe': fake.random_element(['1h', '4h', '1d']),
            'prediction_horizon': fake.random_int(min=12, max=48)
        },
        'fraud': lambda: {
            'transaction_id': fake.uuid4(),
            'amount': fake.random_number(digits=4, fix_len=False),
            'currency': fake.currency_code(),
            'user_id': fake.uuid4(),
            'ip_address': fake.ipv4()
        }
    }
    
    if data_type not in generators:
        raise ValueError(f"Unknown data type: {data_type}")
    
    return [generators[data_type]() for _ in range(count)]


def print_test_summary(test_name: str, metrics: TestMetrics, resource_monitor: ResourceMonitor = None):
    """
    Print formatted test summary
    
    Args:
        test_name: Name of the test
        metrics: Test metrics
        resource_monitor: Optional resource monitor
    """
    print("\n" + "=" * 80)
    print(f"TEST SUMMARY: {test_name}")
    print("=" * 80)
    
    summary = metrics.get_summary()
    
    print(f"\nRequest Statistics:")
    print(f"  Total Requests:       {summary['total_requests']}")
    print(f"  Successful:           {summary['successful_requests']}")
    print(f"  Failed:               {summary['failed_requests']}")
    print(f"  Success Rate:         {summary['success_rate']:.2f}%")
    print(f"  Total Time:           {summary['total_time_seconds']:.2f}s")
    print(f"  Requests/Second:      {summary['requests_per_second']:.2f}")
    
    if 'avg_response_time' in summary:
        print(f"\nResponse Times (seconds):")
        print(f"  Average:              {summary['avg_response_time']:.3f}")
        print(f"  Minimum:              {summary['min_response_time']:.3f}")
        print(f"  Maximum:              {summary['max_response_time']:.3f}")
        print(f"  Median:               {summary['median_response_time']:.3f}")
        print(f"  95th Percentile:      {summary['p95_response_time']:.3f}")
        print(f"  99th Percentile:      {summary['p99_response_time']:.3f}")
    
    if resource_monitor:
        resource_summary = resource_monitor.get_summary()
        if resource_summary:
            print(f"\nResource Usage:")
            if 'cpu' in resource_summary:
                print(f"  CPU Average:          {resource_summary['cpu']['avg']:.2f}%")
                print(f"  CPU Peak:             {resource_summary['cpu']['max']:.2f}%")
            if 'memory' in resource_summary:
                print(f"  Memory Average:       {resource_summary['memory']['avg']:.2f}%")
                print(f"  Memory Peak:          {resource_summary['memory']['max']:.2f}%")
    
    if metrics.errors and len(metrics.errors) <= 10:
        print(f"\nErrors ({len(metrics.errors)}):")
        for i, error in enumerate(metrics.errors[:10], 1):
            print(f"  {i}. {error['error']}")
    elif metrics.errors:
        print(f"\nErrors: {len(metrics.errors)} (showing first 10)")
        for i, error in enumerate(metrics.errors[:10], 1):
            print(f"  {i}. {error['error']}")
    
    print("=" * 80 + "\n")
