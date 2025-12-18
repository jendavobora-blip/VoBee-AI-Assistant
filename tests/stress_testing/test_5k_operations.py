"""
Stress Testing for VOBee AI Assistant - 5000 Operations

Executes 5000 operations across all services with specific distribution.
Tracks failures, timeouts, and resource usage.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import aiohttp
import time
import psutil
from typing import Dict, Any, List
from datetime import datetime
import json
from collections import defaultdict

from config import SERVICES, STRESS_TEST_CONFIG, SUCCESS_CRITERIA


class StressTester:
    """Manages stress testing with high operation count"""
    
    def __init__(self):
        self.results = {
            'operations': defaultdict(lambda: {
                'total': 0,
                'completed': 0,
                'failed': 0,
                'timeouts': 0,
                'errors': [],
                'durations': []
            }),
            'resource_usage': {
                'cpu_percent': [],
                'memory_percent': [],
                'network_sent': [],
                'network_recv': []
            }
        }
        self.start_time = None
        self.end_time = None
        self.process = psutil.Process()
    
    def record_resource_usage(self):
        """Record current resource usage"""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory().percent
            
            net_io = psutil.net_io_counters()
            
            self.results['resource_usage']['cpu_percent'].append(cpu)
            self.results['resource_usage']['memory_percent'].append(memory)
            self.results['resource_usage']['network_sent'].append(net_io.bytes_sent)
            self.results['resource_usage']['network_recv'].append(net_io.bytes_recv)
        except Exception as e:
            pass  # Skip if unable to get metrics
    
    async def execute_operation(self, session: aiohttp.ClientSession, service_name: str, operation_id: int):
        """Execute a single operation against a service"""
        
        url = SERVICES[service_name]
        self.results['operations'][service_name]['total'] += 1
        
        start = time.time()
        
        try:
            async with session.get(
                f"{url}/health",
                timeout=aiohttp.ClientTimeout(total=STRESS_TEST_CONFIG['timeout_seconds'])
            ) as response:
                duration = time.time() - start
                
                if response.status == 200:
                    self.results['operations'][service_name]['completed'] += 1
                    self.results['operations'][service_name]['durations'].append(duration)
                else:
                    self.results['operations'][service_name]['failed'] += 1
                    self.results['operations'][service_name]['errors'].append(
                        f"Status {response.status}"
                    )
        
        except asyncio.TimeoutError:
            self.results['operations'][service_name]['timeouts'] += 1
            self.results['operations'][service_name]['failed'] += 1
            self.results['operations'][service_name]['errors'].append("Timeout")
        
        except Exception as e:
            self.results['operations'][service_name]['failed'] += 1
            self.results['operations'][service_name]['errors'].append(str(e))
    
    async def run_batch(self, operations: List[tuple]):
        """Run a batch of operations"""
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.execute_operation(session, service_name, op_id)
                for op_id, service_name in operations
            ]
            
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def run_stress_test(self):
        """Run the complete stress test"""
        
        print("\n  Distributing operations across services...")
        
        # Build operation list according to distribution
        operations = []
        op_id = 0
        
        for service_name, count in STRESS_TEST_CONFIG['distribution'].items():
            for _ in range(count):
                operations.append((op_id, service_name))
                op_id += 1
        
        print(f"  Total operations to execute: {len(operations)}")
        
        # Split into batches to avoid overwhelming the system
        batch_size = STRESS_TEST_CONFIG['concurrent_workers']
        batches = [
            operations[i:i + batch_size]
            for i in range(0, len(operations), batch_size)
        ]
        
        print(f"  Running {len(batches)} batches of {batch_size} concurrent operations...")
        
        # Run batches
        for i, batch in enumerate(batches):
            if i % 10 == 0:
                print(f"    Progress: {i}/{len(batches)} batches ({i*batch_size}/{len(operations)} operations)")
                self.record_resource_usage()
            
            await self.run_batch(batch)
        
        # Final resource check
        self.record_resource_usage()
        
        print(f"  ✓ Completed all batches")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics from stress test results"""
        
        total_operations = 0
        total_completed = 0
        total_failed = 0
        total_timeouts = 0
        
        service_stats = {}
        
        for service_name, data in self.results['operations'].items():
            total_operations += data['total']
            total_completed += data['completed']
            total_failed += data['failed']
            total_timeouts += data['timeouts']
            
            service_stats[service_name] = {
                'total': data['total'],
                'completed': data['completed'],
                'failed': data['failed'],
                'timeouts': data['timeouts'],
                'success_rate': data['completed'] / data['total'] if data['total'] > 0 else 0,
                'error_rate': data['failed'] / data['total'] if data['total'] > 0 else 0,
                'avg_duration': sum(data['durations']) / len(data['durations']) if data['durations'] else 0,
                'error_count': len(data['errors'])
            }
        
        # Resource usage stats
        resource_stats = {}
        for metric, values in self.results['resource_usage'].items():
            if values:
                resource_stats[metric] = {
                    'min': min(values),
                    'max': max(values),
                    'avg': sum(values) / len(values)
                }
        
        total_duration = self.end_time - self.start_time if self.end_time and self.start_time else 1
        
        stats = {
            'total_operations': total_operations,
            'completed_operations': total_completed,
            'failed_operations': total_failed,
            'timeout_operations': total_timeouts,
            'success_rate': total_completed / total_operations if total_operations > 0 else 0,
            'error_rate': total_failed / total_operations if total_operations > 0 else 0,
            'throughput': total_completed / total_duration,
            'total_duration': total_duration,
            'per_service': service_stats,
            'resource_usage': resource_stats
        }
        
        # Check against success criteria
        stats['meets_criteria'] = (
            stats['error_rate'] <= SUCCESS_CRITERIA['max_error_rate'] and
            stats['success_rate'] >= SUCCESS_CRITERIA['min_success_rate']
        )
        
        return stats


async def run_stress_test_suite():
    """Run complete stress test suite"""
    
    print("\n" + "="*70)
    print("VOBee Stress Testing Suite - 5000 Operations")
    print("="*70 + "\n")
    
    print("Configuration:")
    print(f"  Total operations: {STRESS_TEST_CONFIG['total_operations']}")
    print(f"  Concurrent workers: {STRESS_TEST_CONFIG['concurrent_workers']}")
    print(f"  Timeout: {STRESS_TEST_CONFIG['timeout_seconds']}s")
    
    print("\nDistribution:")
    for service, count in STRESS_TEST_CONFIG['distribution'].items():
        print(f"  {service}: {count} operations")
    
    print("\n" + "-"*70)
    
    tester = StressTester()
    tester.start_time = time.time()
    
    await tester.run_stress_test()
    
    tester.end_time = time.time()
    stats = tester.get_statistics()
    
    results = {
        'test_type': 'stress',
        'timestamp': datetime.utcnow().isoformat(),
        'config': STRESS_TEST_CONFIG,
        'stats': stats
    }
    
    # Print summary
    print("\n" + "="*70)
    print("STRESS TEST SUMMARY")
    print("="*70)
    print(f"Duration: {stats['total_duration']:.2f}s")
    print(f"Total Operations: {stats['total_operations']}")
    print(f"Completed: {stats['completed_operations']}")
    print(f"Failed: {stats['failed_operations']}")
    print(f"Timeouts: {stats['timeout_operations']}")
    print(f"Success Rate: {stats['success_rate']*100:.2f}%")
    print(f"Error Rate: {stats['error_rate']*100:.2f}%")
    print(f"Throughput: {stats['throughput']:.2f} ops/s")
    
    print("\nPer-Service Results:")
    for service_name, service_stats in stats['per_service'].items():
        print(f"  {service_name}:")
        print(f"    Completed: {service_stats['completed']}/{service_stats['total']}")
        print(f"    Success Rate: {service_stats['success_rate']*100:.2f}%")
        print(f"    Avg Duration: {service_stats['avg_duration']:.3f}s")
    
    if stats['resource_usage']:
        print("\nResource Usage:")
        for metric, values in stats['resource_usage'].items():
            print(f"  {metric}: min={values['min']:.2f}, max={values['max']:.2f}, avg={values['avg']:.2f}")
    
    print("\nSuccess Criteria:")
    print(f"  Error rate: {stats['error_rate']*100:.2f}% (max {SUCCESS_CRITERIA['max_error_rate']*100}%)")
    print(f"  Success rate: {stats['success_rate']*100:.2f}% (min {SUCCESS_CRITERIA['min_success_rate']*100}%)")
    
    if stats['meets_criteria']:
        print("\n✓ SUCCESS: Stress test meets all criteria")
    else:
        print("\n✗ FAILURE: Stress test does not meet criteria")
    
    print("="*70 + "\n")
    
    return results


def generate_html_report(results: Dict[str, Any], output_file: str):
    """Generate HTML report for stress tests"""
    
    stats = results['stats']
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>VOBee Stress Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #333; border-bottom: 3px solid #FF9800; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ background: #fff3e0; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .summary-item {{ text-align: center; }}
        .summary-value {{ font-size: 2em; font-weight: bold; color: #FF9800; }}
        .summary-label {{ color: #666; font-size: 0.9em; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #FF9800; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .pass {{ color: #4CAF50; }}
        .fail {{ color: #f44336; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>VOBee Stress Test Report - 5000 Operations</h1>
        <p>Generated: {results['timestamp']}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-value">{stats['total_operations']}</div>
                    <div class="summary-label">Total Operations</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{stats['completed_operations']}</div>
                    <div class="summary-label">Completed</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{stats['failed_operations']}</div>
                    <div class="summary-label">Failed</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{stats['throughput']:.1f}</div>
                    <div class="summary-label">Ops/sec</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{stats['success_rate']*100:.1f}%</div>
                    <div class="summary-label">Success Rate</div>
                </div>
            </div>
        </div>
        
        <h2>Per-Service Results</h2>
        <table>
            <tr>
                <th>Service</th>
                <th>Total</th>
                <th>Completed</th>
                <th>Failed</th>
                <th>Timeouts</th>
                <th>Success Rate</th>
                <th>Avg Duration (s)</th>
            </tr>
"""
    
    for service_name, service_stats in stats['per_service'].items():
        html += f"""
            <tr>
                <td>{service_name}</td>
                <td>{service_stats['total']}</td>
                <td>{service_stats['completed']}</td>
                <td>{service_stats['failed']}</td>
                <td>{service_stats['timeouts']}</td>
                <td>{service_stats['success_rate']*100:.2f}%</td>
                <td>{service_stats['avg_duration']:.3f}</td>
            </tr>
"""
    
    criteria_status = "PASS" if stats['meets_criteria'] else "FAIL"
    criteria_class = "pass" if stats['meets_criteria'] else "fail"
    
    html += f"""
        </table>
        
        <h2>Success Criteria: <span class="{criteria_class}">{criteria_status}</span></h2>
        <p>Error Rate: {stats['error_rate']*100:.2f}% (max {SUCCESS_CRITERIA['max_error_rate']*100}%)</p>
        <p>Success Rate: {stats['success_rate']*100:.2f}% (min {SUCCESS_CRITERIA['min_success_rate']*100}%)</p>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"HTML report generated: {output_file}")


if __name__ == "__main__":
    # Run tests
    results = asyncio.run(run_stress_test_suite())
    
    # Save results
    os.makedirs('test_results', exist_ok=True)
    
    # JSON output
    with open('test_results/stress_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # HTML report
    generate_html_report(results, 'test_results/stress_test_report.html')
    
    # Exit with appropriate code
    sys.exit(0 if results['stats']['meets_criteria'] else 1)
