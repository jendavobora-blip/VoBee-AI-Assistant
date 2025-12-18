"""
Load Testing for VOBee AI Assistant - 300 Concurrent Users

Simulates realistic load with gradual ramp-up and sustained testing.
Measures response times, throughput, and error rates.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import aiohttp
import time
from typing import Dict, Any, List
from datetime import datetime
import json
import statistics
from collections import defaultdict

from config import SERVICES, LOAD_TEST_CONFIG, SUCCESS_CRITERIA


class LoadTester:
    """Manages load testing with concurrent users"""
    
    def __init__(self):
        self.results = {
            'response_times': defaultdict(list),
            'status_codes': defaultdict(int),
            'errors': defaultdict(list),
            'requests_sent': 0,
            'requests_completed': 0,
            'requests_failed': 0
        }
        self.start_time = None
        self.end_time = None
    
    async def make_request(self, session: aiohttp.ClientSession, service_name: str, url: str) -> Dict[str, Any]:
        """Make a single HTTP request"""
        start = time.time()
        
        try:
            async with session.get(
                f"{url}/health",
                timeout=aiohttp.ClientTimeout(total=LOAD_TEST_CONFIG['timeout_seconds'])
            ) as response:
                duration = time.time() - start
                
                self.results['response_times'][service_name].append(duration)
                self.results['status_codes'][response.status] += 1
                self.results['requests_completed'] += 1
                
                return {
                    'success': response.status == 200,
                    'status': response.status,
                    'duration': duration,
                    'service': service_name
                }
        
        except asyncio.TimeoutError:
            duration = time.time() - start
            self.results['errors'][service_name].append('timeout')
            self.results['requests_failed'] += 1
            return {
                'success': False,
                'error': 'timeout',
                'duration': duration,
                'service': service_name
            }
        
        except Exception as e:
            duration = time.time() - start
            self.results['errors'][service_name].append(str(e))
            self.results['requests_failed'] += 1
            return {
                'success': False,
                'error': str(e),
                'duration': duration,
                'service': service_name
            }
    
    async def simulate_user(self, user_id: int, duration_seconds: int):
        """Simulate a single user making requests"""
        
        async with aiohttp.ClientSession() as session:
            end_time = time.time() + duration_seconds
            
            while time.time() < end_time:
                # Randomly select a service to test
                service_name = list(SERVICES.keys())[user_id % len(SERVICES)]
                service_url = SERVICES[service_name]
                
                self.results['requests_sent'] += 1
                await self.make_request(session, service_name, service_url)
                
                # Small delay to simulate realistic user behavior
                await asyncio.sleep(0.5)
    
    async def run_load_test(self, num_users: int, duration_seconds: int):
        """Run load test with specified number of concurrent users"""
        
        print(f"  Starting {num_users} concurrent users for {duration_seconds}s...")
        
        tasks = [
            self.simulate_user(i, duration_seconds)
            for i in range(num_users)
        ]
        
        await asyncio.gather(*tasks)
    
    def calculate_percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile from data"""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics from test results"""
        
        all_response_times = []
        for times in self.results['response_times'].values():
            all_response_times.extend(times)
        
        if not all_response_times:
            return {
                'error': 'No successful requests',
                'total_requests': self.results['requests_sent'],
                'failed_requests': self.results['requests_failed']
            }
        
        total_duration = self.end_time - self.start_time if self.end_time and self.start_time else 1
        
        stats = {
            'total_requests': self.results['requests_sent'],
            'completed_requests': self.results['requests_completed'],
            'failed_requests': self.results['requests_failed'],
            'error_rate': self.results['requests_failed'] / self.results['requests_sent'] if self.results['requests_sent'] > 0 else 0,
            'success_rate': self.results['requests_completed'] / self.results['requests_sent'] if self.results['requests_sent'] > 0 else 0,
            'throughput': self.results['requests_completed'] / total_duration,
            'response_times': {
                'min': min(all_response_times),
                'max': max(all_response_times),
                'mean': statistics.mean(all_response_times),
                'median': statistics.median(all_response_times),
                'p50': self.calculate_percentile(all_response_times, 0.50),
                'p95': self.calculate_percentile(all_response_times, 0.95),
                'p99': self.calculate_percentile(all_response_times, 0.99)
            },
            'per_service': {}
        }
        
        # Per-service statistics
        for service_name, times in self.results['response_times'].items():
            if times:
                stats['per_service'][service_name] = {
                    'count': len(times),
                    'mean': statistics.mean(times),
                    'p95': self.calculate_percentile(times, 0.95),
                    'p99': self.calculate_percentile(times, 0.99),
                    'errors': len(self.results['errors'][service_name])
                }
        
        # Validate against success criteria
        stats['meets_criteria'] = (
            stats['error_rate'] <= SUCCESS_CRITERIA['max_error_rate'] and
            stats['success_rate'] >= SUCCESS_CRITERIA['min_success_rate'] and
            stats['response_times']['p95'] <= SUCCESS_CRITERIA['max_p95_response_time'] and
            stats['response_times']['p99'] <= SUCCESS_CRITERIA['max_p99_response_time']
        )
        
        return stats


async def run_load_test_suite():
    """Run complete load test suite with ramp-up"""
    
    print("\n" + "="*70)
    print("VOBee Load Testing Suite - 300 Concurrent Users")
    print("="*70 + "\n")
    
    results = {
        'test_type': 'load',
        'timestamp': datetime.utcnow().isoformat(),
        'config': LOAD_TEST_CONFIG,
        'phases': []
    }
    
    # Phase 1: Ramp-up
    print("Phase 1: Gradual Ramp-up")
    print("-" * 70)
    
    for num_users in LOAD_TEST_CONFIG['ramp_up_steps']:
        print(f"\nRamp-up to {num_users} users...")
        
        tester = LoadTester()
        tester.start_time = time.time()
        
        # Run for 30 seconds at each step
        await tester.run_load_test(num_users, 30)
        
        tester.end_time = time.time()
        stats = tester.get_statistics()
        
        results['phases'].append({
            'phase': f'ramp_up_{num_users}',
            'users': num_users,
            'duration': 30,
            'stats': stats
        })
        
        print(f"  ✓ Completed {stats['completed_requests']} requests")
        print(f"  → Error rate: {stats['error_rate']*100:.2f}%")
        print(f"  → P95 response time: {stats['response_times']['p95']:.3f}s")
    
    # Phase 2: Sustained load
    print(f"\nPhase 2: Sustained Load - {LOAD_TEST_CONFIG['max_users']} users for {LOAD_TEST_CONFIG['sustained_duration_seconds']}s")
    print("-" * 70)
    
    tester = LoadTester()
    tester.start_time = time.time()
    
    await tester.run_load_test(
        LOAD_TEST_CONFIG['max_users'],
        LOAD_TEST_CONFIG['sustained_duration_seconds']
    )
    
    tester.end_time = time.time()
    stats = tester.get_statistics()
    
    results['phases'].append({
        'phase': 'sustained',
        'users': LOAD_TEST_CONFIG['max_users'],
        'duration': LOAD_TEST_CONFIG['sustained_duration_seconds'],
        'stats': stats
    })
    
    print(f"\n  ✓ Completed {stats['completed_requests']} requests")
    print(f"  → Throughput: {stats['throughput']:.2f} req/s")
    print(f"  → Error rate: {stats['error_rate']*100:.2f}%")
    print(f"  → Success rate: {stats['success_rate']*100:.2f}%")
    
    # Overall summary
    results['summary'] = stats
    
    print("\n" + "="*70)
    print("LOAD TEST SUMMARY")
    print("="*70)
    print(f"Total Requests: {stats['total_requests']}")
    print(f"Completed: {stats['completed_requests']}")
    print(f"Failed: {stats['failed_requests']}")
    print(f"Throughput: {stats['throughput']:.2f} req/s")
    print(f"\nResponse Times:")
    print(f"  P50: {stats['response_times']['p50']:.3f}s")
    print(f"  P95: {stats['response_times']['p95']:.3f}s")
    print(f"  P99: {stats['response_times']['p99']:.3f}s")
    print(f"\nSuccess Criteria:")
    print(f"  Error rate: {stats['error_rate']*100:.2f}% (max {SUCCESS_CRITERIA['max_error_rate']*100}%)")
    print(f"  Success rate: {stats['success_rate']*100:.2f}% (min {SUCCESS_CRITERIA['min_success_rate']*100}%)")
    print(f"  P95 time: {stats['response_times']['p95']:.3f}s (max {SUCCESS_CRITERIA['max_p95_response_time']}s)")
    print(f"  P99 time: {stats['response_times']['p99']:.3f}s (max {SUCCESS_CRITERIA['max_p99_response_time']}s)")
    
    if stats['meets_criteria']:
        print("\n✓ SUCCESS: Load test meets all criteria")
    else:
        print("\n✗ FAILURE: Load test does not meet criteria")
    
    print("="*70 + "\n")
    
    return results


def generate_html_report(results: Dict[str, Any], output_file: str):
    """Generate HTML report for load tests"""
    
    summary = results['summary']
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>VOBee Load Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #333; border-bottom: 3px solid #2196F3; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .summary-item {{ text-align: center; }}
        .summary-value {{ font-size: 2em; font-weight: bold; color: #2196F3; }}
        .summary-label {{ color: #666; font-size: 0.9em; }}
        .metrics {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .metric-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #ddd; }}
        .metric-label {{ font-weight: bold; }}
        .pass {{ color: #4CAF50; }}
        .fail {{ color: #f44336; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #2196F3; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>VOBee Load Test Report - 300 Concurrent Users</h1>
        <p>Generated: {results['timestamp']}</p>
        
        <div class="summary">
            <h2>Summary Statistics</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-value">{summary['total_requests']}</div>
                    <div class="summary-label">Total Requests</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{summary['throughput']:.1f}</div>
                    <div class="summary-label">Requests/sec</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{summary['error_rate']*100:.2f}%</div>
                    <div class="summary-label">Error Rate</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{summary['success_rate']*100:.1f}%</div>
                    <div class="summary-label">Success Rate</div>
                </div>
            </div>
        </div>
        
        <h2>Response Time Metrics</h2>
        <div class="metrics">
            <div class="metric-row">
                <span class="metric-label">P50 (Median):</span>
                <span>{summary['response_times']['p50']:.3f}s</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">P95:</span>
                <span>{summary['response_times']['p95']:.3f}s</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">P99:</span>
                <span>{summary['response_times']['p99']:.3f}s</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Mean:</span>
                <span>{summary['response_times']['mean']:.3f}s</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Min:</span>
                <span>{summary['response_times']['min']:.3f}s</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Max:</span>
                <span>{summary['response_times']['max']:.3f}s</span>
            </div>
        </div>
        
        <h2>Per-Service Performance</h2>
        <table>
            <tr>
                <th>Service</th>
                <th>Requests</th>
                <th>Mean (s)</th>
                <th>P95 (s)</th>
                <th>P99 (s)</th>
                <th>Errors</th>
            </tr>
"""
    
    for service_name, service_stats in summary.get('per_service', {}).items():
        html += f"""
            <tr>
                <td>{service_name}</td>
                <td>{service_stats['count']}</td>
                <td>{service_stats['mean']:.3f}</td>
                <td>{service_stats['p95']:.3f}</td>
                <td>{service_stats['p99']:.3f}</td>
                <td>{service_stats['errors']}</td>
            </tr>
"""
    
    criteria_status = "PASS" if summary['meets_criteria'] else "FAIL"
    criteria_class = "pass" if summary['meets_criteria'] else "fail"
    
    html += f"""
        </table>
        
        <h2>Success Criteria: <span class="{criteria_class}">{criteria_status}</span></h2>
        <div class="metrics">
            <div class="metric-row">
                <span class="metric-label">Error Rate:</span>
                <span>{summary['error_rate']*100:.2f}% (max {SUCCESS_CRITERIA['max_error_rate']*100}%)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Success Rate:</span>
                <span>{summary['success_rate']*100:.2f}% (min {SUCCESS_CRITERIA['min_success_rate']*100}%)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">P95 Response Time:</span>
                <span>{summary['response_times']['p95']:.3f}s (max {SUCCESS_CRITERIA['max_p95_response_time']}s)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">P99 Response Time:</span>
                <span>{summary['response_times']['p99']:.3f}s (max {SUCCESS_CRITERIA['max_p99_response_time']}s)</span>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"HTML report generated: {output_file}")


if __name__ == "__main__":
    # Run tests
    results = asyncio.run(run_load_test_suite())
    
    # Save results
    os.makedirs('test_results', exist_ok=True)
    
    # JSON output
    with open('test_results/load_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # HTML report
    generate_html_report(results, 'test_results/load_test_report.html')
    
    # Exit with appropriate code
    sys.exit(0 if results['summary']['meets_criteria'] else 1)
