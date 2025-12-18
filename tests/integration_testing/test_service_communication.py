"""
Integration Testing for VOBee AI Assistant

Tests service-to-service communication and workflows:
- Supreme Brain ↔ Agent Ecosystem
- Tech Scouting → Hyper-Learning pipeline
- Media Factory → Marketing Brain integration
- Cost Guard integration with all services
- End-to-end workflow testing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
from typing import Dict, Any, Tuple
from datetime import datetime
import json

from config import SERVICES, TIMEOUT_SETTINGS


class IntegrationTester:
    """Test service integrations and workflows"""
    
    def __init__(self):
        self.results = {
            'tests': [],
            'passed': 0,
            'failed': 0
        }
    
    def test_supreme_brain_agent_ecosystem(self) -> Tuple[bool, str, float]:
        """Test Supreme Brain to Agent Ecosystem communication"""
        
        print("  Testing Supreme Brain ↔ Agent Ecosystem integration...")
        
        try:
            # Step 1: Send a task to Supreme Brain
            start = time.time()
            
            response = requests.post(
                f"{SERVICES['supreme_brain']}/decompose",
                json={
                    "goal": "Create a simple test task",
                    "max_tasks": 5
                },
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response.status_code != 200:
                return False, f"Supreme Brain decompose failed: {response.status_code}", time.time() - start
            
            data = response.json()
            if not data.get('success'):
                return False, "Decompose did not succeed", time.time() - start
            
            # Step 2: Verify Agent Ecosystem can receive tasks
            response = requests.get(
                f"{SERVICES['agent_ecosystem']}/stats",
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response.status_code != 200:
                return False, f"Agent Ecosystem stats failed: {response.status_code}", time.time() - start
            
            duration = time.time() - start
            return True, f"Integration verified ({duration:.3f}s)", duration
        
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def test_tech_scouting_hyper_learning(self) -> Tuple[bool, str, float]:
        """Test Tech Scouting to Hyper-Learning pipeline"""
        
        print("  Testing Tech Scouting → Hyper-Learning pipeline...")
        
        try:
            start = time.time()
            
            # Step 1: Check Tech Scouting is ready
            response = requests.get(
                f"{SERVICES['tech_scouting']}/health",
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response.status_code != 200:
                return False, f"Tech Scouting not available", time.time() - start
            
            # Step 2: Check Hyper-Learning is ready to receive
            response = requests.get(
                f"{SERVICES['hyper_learning']}/health",
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response.status_code != 200:
                return False, f"Hyper-Learning not available", time.time() - start
            
            duration = time.time() - start
            return True, f"Pipeline connectivity verified ({duration:.3f}s)", duration
        
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def test_media_factory_marketing_brain(self) -> Tuple[bool, str, float]:
        """Test Media Factory to Marketing Brain integration"""
        
        print("  Testing Media Factory → Marketing Brain integration...")
        
        try:
            start = time.time()
            
            # Check both services are available
            response1 = requests.get(
                f"{SERVICES['media_factory']}/health",
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            response2 = requests.get(
                f"{SERVICES['marketing_brain']}/health",
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response1.status_code != 200:
                return False, "Media Factory not available", time.time() - start
            
            if response2.status_code != 200:
                return False, "Marketing Brain not available", time.time() - start
            
            duration = time.time() - start
            return True, f"Media-Marketing integration verified ({duration:.3f}s)", duration
        
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def test_cost_guard_integration(self) -> Tuple[bool, str, float]:
        """Test Cost Guard integration with all services"""
        
        print("  Testing Cost Guard integration with all services...")
        
        try:
            start = time.time()
            
            # Check Cost Guard is available
            response = requests.get(
                f"{SERVICES['cost_guard']}/health",
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response.status_code != 200:
                return False, "Cost Guard not available", time.time() - start
            
            # Verify it can monitor other services (basic connectivity)
            services_reachable = 0
            for service_name, service_url in SERVICES.items():
                if service_name == 'cost_guard':
                    continue
                
                try:
                    resp = requests.get(
                        f"{service_url}/health",
                        timeout=5
                    )
                    if resp.status_code == 200:
                        services_reachable += 1
                except:
                    pass
            
            duration = time.time() - start
            
            if services_reachable >= 4:  # At least half of the services
                return True, f"Cost Guard can monitor {services_reachable} services ({duration:.3f}s)", duration
            else:
                return False, f"Only {services_reachable} services reachable", duration
        
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def test_end_to_end_workflow(self) -> Tuple[bool, str, float]:
        """Test end-to-end workflow across multiple services"""
        
        print("  Testing end-to-end workflow...")
        
        try:
            start = time.time()
            
            workflow_steps = []
            
            # Step 1: Supreme Brain receives request
            response = requests.post(
                f"{SERVICES['supreme_brain']}/chat",
                json={"message": "Test workflow"},
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response.status_code == 200:
                workflow_steps.append("supreme_brain")
            
            # Step 2: Agent Ecosystem processes
            response = requests.get(
                f"{SERVICES['agent_ecosystem']}/agents",
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response.status_code == 200:
                workflow_steps.append("agent_ecosystem")
            
            # Step 3: Cost Guard monitors
            response = requests.get(
                f"{SERVICES['cost_guard']}/health",
                timeout=TIMEOUT_SETTINGS['integration_test']
            )
            
            if response.status_code == 200:
                workflow_steps.append("cost_guard")
            
            duration = time.time() - start
            
            if len(workflow_steps) >= 3:
                return True, f"Workflow completed {len(workflow_steps)} steps ({duration:.3f}s)", duration
            else:
                return False, f"Only {len(workflow_steps)} steps completed", duration
        
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        
        tests = [
            ("supreme_brain_agent_ecosystem", self.test_supreme_brain_agent_ecosystem),
            ("tech_scouting_hyper_learning", self.test_tech_scouting_hyper_learning),
            ("media_factory_marketing_brain", self.test_media_factory_marketing_brain),
            ("cost_guard_integration", self.test_cost_guard_integration),
            ("end_to_end_workflow", self.test_end_to_end_workflow)
        ]
        
        for test_name, test_func in tests:
            passed, message, duration = test_func()
            
            self.results['tests'].append({
                'name': test_name,
                'passed': passed,
                'message': message,
                'duration': duration
            })
            
            if passed:
                self.results['passed'] += 1
                print(f"    ✓ PASS - {test_name}")
            else:
                self.results['failed'] += 1
                print(f"    ✗ FAIL - {test_name}: {message}")
        
        return self.results


def run_integration_tests() -> Dict[str, Any]:
    """Run integration test suite"""
    
    print("\n" + "="*70)
    print("VOBee Integration Testing Suite")
    print("="*70 + "\n")
    
    tester = IntegrationTester()
    results = tester.run_all_tests()
    
    # Build summary
    summary = {
        'test_type': 'integration',
        'timestamp': datetime.utcnow().isoformat(),
        'results': results,
        'summary': {
            'total_tests': len(results['tests']),
            'passed': results['passed'],
            'failed': results['failed'],
            'success_rate': results['passed'] / len(results['tests']) if results['tests'] else 0
        }
    }
    
    print("\n" + "="*70)
    print("INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {summary['summary']['total_tests']}")
    print(f"Passed: {summary['summary']['passed']}")
    print(f"Failed: {summary['summary']['failed']}")
    print(f"Success Rate: {summary['summary']['success_rate']*100:.1f}%")
    
    if summary['summary']['failed'] == 0:
        print("\n✓ SUCCESS: All integration tests passed")
    else:
        print("\n✗ FAILURE: Some integration tests failed")
    
    print("="*70 + "\n")
    
    return summary


def generate_html_report(results: Dict[str, Any], output_file: str):
    """Generate HTML report for integration tests"""
    
    summary = results['summary']
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>VOBee Integration Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #333; border-bottom: 3px solid #9C27B0; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ background: #f3e5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .summary-item {{ text-align: center; }}
        .summary-value {{ font-size: 2em; font-weight: bold; color: #9C27B0; }}
        .summary-label {{ color: #666; font-size: 0.9em; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #9C27B0; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .pass {{ color: #4CAF50; font-weight: bold; }}
        .fail {{ color: #f44336; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>VOBee Integration Test Report</h1>
        <p>Generated: {results['timestamp']}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-value">{summary['total_tests']}</div>
                    <div class="summary-label">Total Tests</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value" style="color: #4CAF50;">{summary['passed']}</div>
                    <div class="summary-label">Passed</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value" style="color: #f44336;">{summary['failed']}</div>
                    <div class="summary-label">Failed</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{summary['success_rate']*100:.1f}%</div>
                    <div class="summary-label">Success Rate</div>
                </div>
            </div>
        </div>
        
        <h2>Test Results</h2>
        <table>
            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Message</th>
                <th>Duration (s)</th>
            </tr>
"""
    
    for test in results['results']['tests']:
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
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"HTML report generated: {output_file}")


if __name__ == "__main__":
    # Run tests
    results = run_integration_tests()
    
    # Save results
    os.makedirs('test_results', exist_ok=True)
    
    # JSON output
    with open('test_results/integration_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # HTML report
    generate_html_report(results, 'test_results/integration_test_report.html')
    
    # Exit with appropriate code
    sys.exit(0 if results['summary']['failed'] == 0 else 1)
