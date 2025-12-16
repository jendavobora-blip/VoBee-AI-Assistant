#!/usr/bin/env python3
"""
Test script for deadline enforcement in Swarm/Bot/Runners
Tests the orchestrator and worker pool deadline functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
ORCHESTRATOR_URL = "http://localhost:5003"
WORKER_POOL_URL = "http://localhost:5008"

def test_orchestrator_deadline():
    """Test orchestrator workflow deadline enforcement"""
    print("\n=== Testing Orchestrator Deadline Enforcement ===\n")
    
    # Test 1: Workflow with sufficient deadline
    print("Test 1: Workflow with sufficient deadline (60 seconds)")
    workflow_data = {
        "tasks": [
            {
                "type": "crypto_prediction",
                "params": {
                    "symbol": "BTC",
                    "timeframe": "1h"
                }
            }
        ],
        "priority": "high",
        "deadline": 60  # 60 seconds
    }
    
    try:
        response = requests.post(
            f"{ORCHESTRATOR_URL}/orchestrate",
            json=workflow_data,
            timeout=70
        )
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Workflow ID: {result.get('workflow_id')}")
        print(f"Status: {result.get('status')}")
        print(f"Duration: {result.get('duration'):.2f}s")
        print(f"Deadline Exceeded: {result.get('deadline_exceeded')}")
        print(f"Tasks Executed: {result.get('tasks_executed')}/{result.get('tasks_total')}")
        
        if result.get('deadline_exceeded'):
            print("❌ FAILED: Deadline should not be exceeded")
        else:
            print("✅ PASSED: Workflow completed within deadline")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    
    # Test 2: Workflow with very short deadline (should fail)
    print("Test 2: Workflow with very short deadline (1 second)")
    workflow_data = {
        "tasks": [
            {
                "type": "crypto_prediction",
                "params": {
                    "symbol": "BTC",
                    "timeframe": "1h"
                }
            },
            {
                "type": "fraud_detection",
                "params": {
                    "transaction_data": {}
                }
            }
        ],
        "priority": "normal",
        "deadline": 1  # 1 second - very short
    }
    
    try:
        response = requests.post(
            f"{ORCHESTRATOR_URL}/orchestrate",
            json=workflow_data,
            timeout=10
        )
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Workflow ID: {result.get('workflow_id')}")
        print(f"Status: {result.get('status')}")
        print(f"Duration: {result.get('duration'):.2f}s")
        print(f"Deadline Exceeded: {result.get('deadline_exceeded')}")
        print(f"Tasks Executed: {result.get('tasks_executed')}/{result.get('tasks_total')}")
        
        if result.get('deadline_exceeded'):
            print("✅ PASSED: Deadline correctly enforced")
        else:
            print("⚠️  WARNING: Expected deadline to be exceeded")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()

def test_worker_deadline():
    """Test worker pool task deadline enforcement"""
    print("\n=== Testing Worker Pool Deadline Enforcement ===\n")
    
    # Test 1: Task with sufficient deadline
    print("Test 1: Crawler task with sufficient deadline (30 seconds)")
    task_data = {
        "worker_type": "crawler",
        "task": {
            "url": "https://github.com",
            "depth": 1,
            "deadline": 30  # 30 seconds
        }
    }
    
    try:
        response = requests.post(
            f"{WORKER_POOL_URL}/task/execute",
            json=task_data,
            timeout=35
        )
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Task Status: {result.get('status')}")
        print(f"Worker ID: {result.get('worker_id')}")
        
        if result.get('status') == 'success':
            print("✅ PASSED: Task completed within deadline")
        elif result.get('status') == 'timeout':
            print("⚠️  WARNING: Task timed out (might be expected for slow network)")
        else:
            print(f"❌ FAILED: Unexpected status: {result.get('status')}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    
    # Test 2: Task with very short deadline (should timeout)
    print("Test 2: Crawler task with very short deadline (0.1 seconds)")
    task_data = {
        "worker_type": "crawler",
        "task": {
            "url": "https://github.com",
            "depth": 1,
            "deadline": 0.1  # 0.1 second - very short
        }
    }
    
    try:
        response = requests.post(
            f"{WORKER_POOL_URL}/task/execute",
            json=task_data,
            timeout=5
        )
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Task Status: {result.get('status')}")
        print(f"Worker ID: {result.get('worker_id')}")
        
        if result.get('status') in ['timeout', 'failed']:
            print("✅ PASSED: Task correctly timed out or failed due to deadline")
        else:
            print(f"⚠️  WARNING: Expected timeout, got: {result.get('status')}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    
    # Test 3: Analysis worker with deadline
    print("Test 3: Analysis task with deadline (10 seconds)")
    task_data = {
        "worker_type": "analysis",
        "task": {
            "analysis_type": "sentiment",
            "data": {"text": "This is a test"},
            "deadline": 10  # 10 seconds
        }
    }
    
    try:
        response = requests.post(
            f"{WORKER_POOL_URL}/task/execute",
            json=task_data,
            timeout=15
        )
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Task Status: {result.get('status')}")
        print(f"Worker ID: {result.get('worker_id')}")
        
        if result.get('status') == 'success':
            print("✅ PASSED: Analysis task completed within deadline")
        else:
            print(f"❌ FAILED: Unexpected status: {result.get('status')}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()

def check_services():
    """Check if services are running"""
    print("\n=== Checking Services ===\n")
    
    services = [
        ("Orchestrator", f"{ORCHESTRATOR_URL}/health"),
        ("Worker Pool", f"{WORKER_POOL_URL}/health")
    ]
    
    all_healthy = True
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: Healthy")
            else:
                print(f"❌ {name}: Unhealthy (Status: {response.status_code})")
                all_healthy = False
        except Exception as e:
            print(f"❌ {name}: Not reachable - {e}")
            all_healthy = False
    
    print()
    return all_healthy

def main():
    """Run all tests"""
    print("=" * 60)
    print("Deadline Enforcement Test Suite")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Check if services are running
    if not check_services():
        print("\n⚠️  WARNING: Some services are not available.")
        print("Please start the services with: docker compose up -d")
        print("Or run: ./deploy.sh")
        return
    
    # Run tests
    test_orchestrator_deadline()
    test_worker_deadline()
    
    print("=" * 60)
    print("Test Suite Completed")
    print(f"Finished at: {datetime.now().isoformat()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
