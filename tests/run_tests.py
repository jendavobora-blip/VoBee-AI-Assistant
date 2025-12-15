#!/usr/bin/env python3
"""
QA Test Runner - Main entry point for running QA tests
Supports different test categories and configurations
"""

import argparse
import sys
import os
import subprocess
import logging
from datetime import datetime
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QATestRunner:
    """Main test runner for QA testing framework"""
    
    def __init__(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.results_dir = os.path.join(self.test_dir, 'results')
        os.makedirs(self.results_dir, exist_ok=True)
    
    def run_tests(self, test_category: str, iterations: int = None, users: int = None, 
                  workers: int = 4, verbose: bool = False) -> int:
        """
        Run QA tests for specified category
        
        Args:
            test_category: Category of tests to run (stress, functional, load, edge_cases, all)
            iterations: Number of iterations for stress tests
            users: Number of concurrent users for load tests
            workers: Number of parallel workers
            verbose: Verbose output
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Set environment variables
        env = os.environ.copy()
        if iterations:
            env['STRESS_TEST_ITERATIONS'] = str(iterations)
        if users:
            env['LOAD_TEST_USERS'] = str(users)
        
        # Build pytest command
        cmd = ['pytest']
        
        # Test selection
        if test_category == 'all':
            cmd.append(self.test_dir)
        elif test_category == 'quick':
            # Quick validation tests only
            cmd.extend([
                '-k', 'quick',
                self.test_dir
            ])
        else:
            test_path = os.path.join(self.test_dir, test_category)
            if os.path.exists(test_path):
                cmd.append(test_path)
            else:
                logger.error(f"Test category '{test_category}' not found")
                return 1
        
        # Pytest options
        cmd.extend([
            f'-n', str(workers),  # Parallel execution
            '-v' if verbose else '-q',
            '--tb=short',
            '--strict-markers',
            f'--html={self.results_dir}/report_{test_category}_{timestamp}.html',
            '--self-contained-html',
        ])
        
        # Add coverage if requested
        if verbose:
            cmd.extend([
                '--cov=.',
                f'--cov-report=html:{self.results_dir}/coverage_{timestamp}',
            ])
        
        logger.info(f"Running {test_category} tests...")
        logger.info(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, env=env, cwd=self.test_dir)
            
            if result.returncode == 0:
                logger.info(f"✓ {test_category} tests completed successfully")
                logger.info(f"Report saved to: {self.results_dir}/report_{test_category}_{timestamp}.html")
            else:
                logger.error(f"✗ {test_category} tests failed with exit code {result.returncode}")
            
            return result.returncode
            
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return 1
    
    def list_tests(self):
        """List all available test categories"""
        categories = []
        
        for item in os.listdir(self.test_dir):
            item_path = os.path.join(self.test_dir, item)
            if os.path.isdir(item_path) and not item.startswith('__') and item != 'utils' and item != 'results':
                # Count tests in category
                test_files = [f for f in os.listdir(item_path) if f.startswith('test_') and f.endswith('.py')]
                categories.append((item, len(test_files)))
        
        print("\nAvailable Test Categories:")
        print("-" * 60)
        for category, count in categories:
            print(f"  {category:<20} ({count} test file(s))")
        print("-" * 60)
        print(f"  {'all':<20} (Run all test categories)")
        print(f"  {'quick':<20} (Quick validation tests)")
        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='VoBee AI Assistant QA Test Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python run_tests.py all
  
  # Run stress tests with 50,000 iterations
  python run_tests.py stress --iterations 50000
  
  # Run load tests with 1000 concurrent users
  python run_tests.py load --users 1000
  
  # Run functional tests with verbose output
  python run_tests.py functional --verbose
  
  # Quick validation (fast smoke tests)
  python run_tests.py quick
  
  # List all available test categories
  python run_tests.py --list
        """
    )
    
    parser.add_argument(
        'category',
        nargs='?',
        choices=['stress', 'functional', 'load', 'edge_cases', 'all', 'quick'],
        help='Test category to run'
    )
    
    parser.add_argument(
        '--iterations',
        type=int,
        help='Number of iterations for stress tests (default: 50000)'
    )
    
    parser.add_argument(
        '--users',
        type=int,
        help='Number of concurrent users for load tests (default: 1000)'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output with coverage'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available test categories'
    )
    
    args = parser.parse_args()
    
    runner = QATestRunner()
    
    if args.list:
        runner.list_tests()
        return 0
    
    if not args.category:
        parser.print_help()
        print("\nError: Test category is required (or use --list to see available categories)")
        return 1
    
    return runner.run_tests(
        test_category=args.category,
        iterations=args.iterations,
        users=args.users,
        workers=args.workers,
        verbose=args.verbose
    )


if __name__ == '__main__':
    sys.exit(main())
