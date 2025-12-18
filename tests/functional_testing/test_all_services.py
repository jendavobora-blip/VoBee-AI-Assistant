"""
Functional Testing for VOBee AI Assistant

Tests basic functionality of all services:
- Health check endpoints
- Basic API functionality
- Error handling
- Response format validation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
from typing import Dict, Any, List, Tuple
from datetime import datetime
import json

from config import SERVICES, TIMEOUT_SETTINGS, SUCCESS_CRITERIA


class ServiceTester:
    """Test individual service functionality"""
    
    def __init__(self, service_name: str, base_url: str):
        self.service_name = service_name
        self.base_url = base_url
        self.test_results = []
    
    def test_health_check(self) -> Tuple[bool, str, float]:
        """Test health check endpoint"""
        try:
            start = time.time()
            response = requests.get(
                f"{self.base_url}/health",
                timeout=TIMEOUT_SETTINGS['health_check']
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                if 'status' in data and data['status'] == 'healthy':
                    return True, f"Health check passed ({duration:.3f}s)", duration
                else:
                    return False, f"Invalid health response: {data}", duration
            else:
                return False, f"Status code: {response.status_code}", duration
        
        except requests.exceptions.ConnectionError:
            return False, "Service not reachable (connection refused)", 0.0
        except requests.exceptions.Timeout:
            return False, "Health check timed out", TIMEOUT_SETTINGS['health_check']
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def test_root_endpoint(self) -> Tuple[bool, str, float]:
        """Test root endpoint"""
        try:
            start = time.time()
            response = requests.get(
                f"{self.base_url}/",
                timeout=TIMEOUT_SETTINGS['functional_test']
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                if 'service' in data or 'endpoints' in data:
                    return True, f"Root endpoint valid ({duration:.3f}s)", duration
                else:
                    return False, f"Missing expected fields in response", duration
            else:
                return False, f"Status code: {response.status_code}", duration
        
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def test_basic_functionality(self) -> Tuple[bool, str, float]:
        """Test basic service-specific functionality"""
        
        # Service-specific tests
        tests = {
            'supreme_brain': self._test_supreme_brain,
            'agent_ecosystem': self._test_agent_ecosystem,
            'media_factory': self._test_media_factory,
            'marketing_brain': self._test_marketing_brain,
            'tech_scouting': self._test_tech_scouting,
            'hyper_learning': self._test_hyper_learning,
            'simulation': self._test_simulation,
            'cost_guard': self._test_cost_guard
        }
        
        test_func = tests.get(self.service_name)
        if test_func:
            return test_func()
        else:
            return True, "No specific test defined", 0.0
    
    def _test_supreme_brain(self) -> Tuple[bool, str, float]:
        """Test Supreme Brain chat endpoint"""
        try:
            start = time.time()
            response = requests.post(
                f"{self.base_url}/chat",
                json={"message": "Hello, status check"},
                timeout=TIMEOUT_SETTINGS['functional_test']
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data:
                    return True, f"Chat endpoint working ({duration:.3f}s)", duration
            
            return False, f"Status: {response.status_code}", duration
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def _test_agent_ecosystem(self) -> Tuple[bool, str, float]:
        """Test Agent Ecosystem stats endpoint"""
        try:
            start = time.time()
            response = requests.get(
                f"{self.base_url}/stats",
                timeout=TIMEOUT_SETTINGS['functional_test']
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                if 'stats' in data or 'success' in data:
                    return True, f"Stats endpoint working ({duration:.3f}s)", duration
            
            return False, f"Status: {response.status_code}", duration
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def _test_media_factory(self) -> Tuple[bool, str, float]:
        """Test Media Factory health"""
        # Media Factory uses health check as main test
        return self.test_health_check()
    
    def _test_marketing_brain(self) -> Tuple[bool, str, float]:
        """Test Marketing Brain health"""
        return self.test_health_check()
    
    def _test_tech_scouting(self) -> Tuple[bool, str, float]:
        """Test Tech Scouting health"""
        return self.test_health_check()
    
    def _test_hyper_learning(self) -> Tuple[bool, str, float]:
        """Test Hyper-Learning health"""
        return self.test_health_check()
    
    def _test_simulation(self) -> Tuple[bool, str, float]:
        """Test Simulation health"""
        return self.test_health_check()
    
    def _test_cost_guard(self) -> Tuple[bool, str, float]:
        """Test Cost Guard health"""
        return self.test_health_check()
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests for this service"""
        results = {
            'service': self.service_name,
            'url': self.base_url,
            'timestamp': datetime.utcnow().isoformat(),
            'tests': []
        }
        
        # Test 1: Health check
        passed, message, duration = self.test_health_check()
        results['tests'].append({
            'name': 'health_check',
            'passed': passed,
            'message': message,
            'duration': duration
        })
        
        # Only run other tests if health check passes
        if passed:
            # Test 2: Root endpoint
            passed, message, duration = self.test_root_endpoint()
            results['tests'].append({
                'name': 'root_endpoint',
                'passed': passed,
                'message': message,
                'duration': duration
            })
            
            # Test 3: Basic functionality
            passed, message, duration = self.test_basic_functionality()
            results['tests'].append({
                'name': 'basic_functionality',
                'passed': passed,
                'message': message,
                'duration': duration
            })
        
        # Calculate overall result
        results['total_tests'] = len(results['tests'])
        results['passed_tests'] = sum(1 for t in results['tests'] if t['passed'])
        results['failed_tests'] = results['total_tests'] - results['passed_tests']
        results['all_passed'] = results['passed_tests'] == results['total_tests']
        
        return results


def run_functional_tests() -> Dict[str, Any]:
    """Run functional tests on all services"""
    
    print("\n" + "="*70)
    print("VOBee Functional Testing Suite")
    print("="*70 + "\n")
    
    all_results = {
        'test_type': 'functional',
        'timestamp': datetime.utcnow().isoformat(),
        'services': {}
    }
    
    total_passed = 0
    total_failed = 0
    
    for service_name, base_url in SERVICES.items():
        print(f"\nTesting {service_name}...")
        print("-" * 70)
        
        tester = ServiceTester(service_name, base_url)
        results = tester.run_all_tests()
        all_results['services'][service_name] = results
        
        for test in results['tests']:
            status = "✓ PASS" if test['passed'] else "✗ FAIL"
            print(f"  {status} - {test['name']}: {test['message']}")
        
        total_passed += results['passed_tests']
        total_failed += results['failed_tests']
        
        if results['all_passed']:
            print(f"  → All tests passed for {service_name}")
        else:
            print(f"  → {results['failed_tests']} test(s) failed for {service_name}")
    
    # Summary
    all_results['summary'] = {
        'total_services': len(SERVICES),
        'total_tests': total_passed + total_failed,
        'passed_tests': total_passed,
        'failed_tests': total_failed,
        'success_rate': total_passed / (total_passed + total_failed) if (total_passed + total_failed) > 0 else 0,
        'meets_criteria': (total_passed / (total_passed + total_failed)) >= SUCCESS_CRITERIA['min_success_rate'] if (total_passed + total_failed) > 0 else False
    }
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total Services Tested: {all_results['summary']['total_services']}")
    print(f"Total Tests: {all_results['summary']['total_tests']}")
    print(f"Passed: {all_results['summary']['passed_tests']}")
    print(f"Failed: {all_results['summary']['failed_tests']}")
    print(f"Success Rate: {all_results['summary']['success_rate']*100:.1f}%")
    
    if all_results['summary']['meets_criteria']:
        print("\n✓ SUCCESS: All functional tests meet criteria")
    else:
        print("\n✗ FAILURE: Tests do not meet success criteria")
    
    print("="*70 + "\n")
    
    return all_results


def generate_html_report(results: Dict[str, Any], output_file: str):
    """Generate HTML report for functional tests"""
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>VOBee Functional Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .summary-item {{ text-align: center; }}
        .summary-value {{ font-size: 2em; font-weight: bold; color: #4CAF50; }}
        .summary-label {{ color: #666; font-size: 0.9em; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .pass {{ color: #4CAF50; font-weight: bold; }}
        .fail {{ color: #f44336; font-weight: bold; }}
        .service-header {{ background: #2196F3; color: white; }}
        .timestamp {{ color: #999; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>VOBee Functional Test Report</h1>
        <p class="timestamp">Generated: {results['timestamp']}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-value">{results['summary']['total_services']}</div>
                    <div class="summary-label">Services Tested</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{results['summary']['total_tests']}</div>
                    <div class="summary-label">Total Tests</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value" style="color: #4CAF50;">{results['summary']['passed_tests']}</div>
                    <div class="summary-label">Passed</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value" style="color: #f44336;">{results['summary']['failed_tests']}</div>
                    <div class="summary-label">Failed</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{results['summary']['success_rate']*100:.1f}%</div>
                    <div class="summary-label">Success Rate</div>
                </div>
            </div>
        </div>
        
        <h2>Service Details</h2>
"""
    
    for service_name, service_data in results['services'].items():
        status = "✓ PASS" if service_data['all_passed'] else "✗ FAIL"
        status_class = "pass" if service_data['all_passed'] else "fail"
        
        html += f"""
        <h3>{service_name.replace('_', ' ').title()} <span class="{status_class}">{status}</span></h3>
        <table>
            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Message</th>
                <th>Duration (s)</th>
            </tr>
"""
        
        for test in service_data['tests']:
            status = "✓ PASS" if test['passed'] else "✗ FAIL"
            status_class = "pass" if test['passed'] else "fail"
            
            html += f"""
            <tr>
                <td>{test['name']}</td>
                <td class="{status_class}">{status}</td>
                <td>{test['message']}</td>
                <td>{test['duration']:.3f}</td>
            </tr>
"""
        
        html += """
        </table>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"HTML report generated: {output_file}")


if __name__ == "__main__":
    # Run tests
    results = run_functional_tests()
    
    # Save results
    os.makedirs('test_results', exist_ok=True)
    
    # JSON output
    with open('test_results/functional_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # HTML report
    generate_html_report(results, 'test_results/functional_test_report.html')
    
    # Exit with appropriate code
    sys.exit(0 if results['summary']['meets_criteria'] else 1)
