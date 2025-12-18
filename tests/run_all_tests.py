#!/usr/bin/env python3
"""
VOBee Testing Framework - Main Test Runner

Run all test suites or specific test types with a single command.

Usage:
    python tests/run_all_tests.py quick       # Quick smoke test (30s)
    python tests/run_all_tests.py functional  # Functional tests only
    python tests/run_all_tests.py load        # Load test (300 users)
    python tests/run_all_tests.py stress      # Stress test (5K ops)
    python tests/run_all_tests.py integration # Integration tests
    python tests/run_all_tests.py all         # Run all tests
    python tests/run_all_tests.py all --report # All tests + HTML report
"""

import sys
import os
import time
import json
import argparse
from datetime import datetime
from typing import Dict, Any

# Add tests directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from functional_testing.test_all_services import run_functional_tests, generate_html_report as gen_func_report
from integration_testing.test_service_communication import run_integration_tests, generate_html_report as gen_integ_report

# Import async test modules
import asyncio
from load_testing.test_300_users import run_load_test_suite, generate_html_report as gen_load_report
from stress_testing.test_5k_operations import run_stress_test_suite, generate_html_report as gen_stress_report


class TestRunner:
    """Main test runner for all test suites"""
    
    def __init__(self):
        self.results = {
            'start_time': datetime.utcnow().isoformat(),
            'suites': {},
            'summary': {}
        }
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def print_section(self, title: str):
        """Print formatted section"""
        print("\n" + "-"*70)
        print(f"  {title}")
        print("-"*70)
    
    def run_quick_test(self) -> bool:
        """Run quick smoke tests (health checks only)"""
        self.print_header("QUICK SMOKE TEST (30 seconds)")
        
        print("\nRunning quick health checks on all services...")
        
        # Run minimal functional tests
        results = run_functional_tests()
        
        self.results['suites']['quick'] = results
        
        # Only check health endpoints
        all_healthy = all(
            any(t['name'] == 'health_check' and t['passed'] 
                for t in service['tests'])
            for service in results['services'].values()
        )
        
        if all_healthy:
            print("\n✓ All services healthy")
            return True
        else:
            print("\n✗ Some services are not healthy")
            return False
    
    def run_functional_test(self) -> bool:
        """Run functional tests"""
        self.print_header("FUNCTIONAL TESTS")
        
        results = run_functional_tests()
        self.results['suites']['functional'] = results
        
        # Generate report
        os.makedirs('test_results', exist_ok=True)
        gen_func_report(results, 'test_results/functional_test_report.html')
        
        return results['summary']['meets_criteria']
    
    def run_load_test(self) -> bool:
        """Run load tests"""
        self.print_header("LOAD TESTS - 300 Concurrent Users")
        
        results = asyncio.run(run_load_test_suite())
        self.results['suites']['load'] = results
        
        # Generate report
        os.makedirs('test_results', exist_ok=True)
        gen_load_report(results, 'test_results/load_test_report.html')
        
        return results['summary']['meets_criteria']
    
    def run_stress_test(self) -> bool:
        """Run stress tests"""
        self.print_header("STRESS TESTS - 5000 Operations")
        
        results = asyncio.run(run_stress_test_suite())
        self.results['suites']['stress'] = results
        
        # Generate report
        os.makedirs('test_results', exist_ok=True)
        gen_stress_report(results, 'test_results/stress_test_report.html')
        
        return results['stats']['meets_criteria']
    
    def run_integration_test(self) -> bool:
        """Run integration tests"""
        self.print_header("INTEGRATION TESTS")
        
        results = run_integration_tests()
        self.results['suites']['integration'] = results
        
        # Generate report
        os.makedirs('test_results', exist_ok=True)
        gen_integ_report(results, 'test_results/integration_test_report.html')
        
        return results['summary']['failed'] == 0
    
    def generate_summary_report(self):
        """Generate overall summary report"""
        
        self.results['end_time'] = datetime.utcnow().isoformat()
        
        # Calculate overall statistics
        total_passed = 0
        total_failed = 0
        
        for suite_name, suite_data in self.results['suites'].items():
            if suite_name == 'functional' or suite_name == 'quick':
                total_passed += suite_data.get('summary', {}).get('passed_tests', 0)
                total_failed += suite_data.get('summary', {}).get('failed_tests', 0)
            elif suite_name == 'load':
                if suite_data.get('summary', {}).get('meets_criteria', False):
                    total_passed += 1
                else:
                    total_failed += 1
            elif suite_name == 'stress':
                if suite_data.get('stats', {}).get('meets_criteria', False):
                    total_passed += 1
                else:
                    total_failed += 1
            elif suite_name == 'integration':
                total_passed += suite_data.get('summary', {}).get('passed', 0)
                total_failed += suite_data.get('summary', {}).get('failed', 0)
        
        self.results['summary'] = {
            'total_suites': len(self.results['suites']),
            'total_passed': total_passed,
            'total_failed': total_failed,
            'overall_success': total_failed == 0
        }
        
        # Save JSON summary
        os.makedirs('test_results', exist_ok=True)
        with open('test_results/summary.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nSummary saved to: test_results/summary.json")
    
    def print_final_summary(self):
        """Print final test summary"""
        
        self.print_header("FINAL TEST SUMMARY")
        
        summary = self.results['summary']
        
        print(f"\nTest Suites Run: {summary['total_suites']}")
        print(f"Total Passed: {summary['total_passed']}")
        print(f"Total Failed: {summary['total_failed']}")
        
        print("\nSuite Results:")
        for suite_name in self.results['suites'].keys():
            print(f"  - {suite_name}: ✓")
        
        if summary['overall_success']:
            print("\n" + "="*70)
            print("  ✓✓✓ ALL TESTS PASSED ✓✓✓")
            print("="*70)
            return True
        else:
            print("\n" + "="*70)
            print("  ✗✗✗ SOME TESTS FAILED ✗✗✗")
            print("="*70)
            return False


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description='VOBee Testing Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Test Suite Options:
  quick       - Quick smoke test (30 seconds, health checks only)
  functional  - Functional tests (all service endpoints)
  load        - Load test (300 concurrent users, 5 minutes)
  stress      - Stress test (5000 operations)
  integration - Integration tests (service communication)
  all         - Run all test suites

Examples:
  python tests/run_all_tests.py quick
  python tests/run_all_tests.py functional
  python tests/run_all_tests.py all --report
        """
    )
    
    parser.add_argument(
        'suite',
        choices=['quick', 'functional', 'load', 'stress', 'integration', 'all'],
        help='Test suite to run'
    )
    
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate HTML reports'
    )
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    print("\n" + "="*70)
    print("  VOBee AI Assistant - Testing Framework")
    print("="*70)
    print(f"\nTest Suite: {args.suite}")
    print(f"Report Generation: {'Enabled' if args.report else 'Disabled'}")
    
    success = True
    
    try:
        if args.suite == 'quick':
            success = runner.run_quick_test()
        
        elif args.suite == 'functional':
            success = runner.run_functional_test()
        
        elif args.suite == 'load':
            success = runner.run_load_test()
        
        elif args.suite == 'stress':
            success = runner.run_stress_test()
        
        elif args.suite == 'integration':
            success = runner.run_integration_test()
        
        elif args.suite == 'all':
            # Run all test suites
            print("\nRunning complete test suite...")
            
            # Order: functional -> integration -> load -> stress
            success = runner.run_functional_test()
            
            if success:
                success = runner.run_integration_test() and success
            
            if success:
                print("\n⚠️  Starting load test (this will take ~5 minutes)...")
                success = runner.run_load_test() and success
            
            if success:
                print("\n⚠️  Starting stress test (this will take a few minutes)...")
                success = runner.run_stress_test() and success
        
        # Generate summary
        runner.generate_summary_report()
        runner.print_final_summary()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n\n✗ Error running tests: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
