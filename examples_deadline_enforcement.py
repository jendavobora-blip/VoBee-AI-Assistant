#!/usr/bin/env python3
"""
Example usage of deadline enforcement for Swarm/Bot/Runners

This script demonstrates how to use deadline enforcement with the
orchestrator and worker pool services.
"""

import requests
import json

# Service URLs
ORCHESTRATOR_URL = "http://localhost:5003"
WORKER_POOL_URL = "http://localhost:5008"
API_GATEWAY_URL = "http://localhost:8000"

def example_1_orchestrator_with_deadline():
    """
    Example 1: Execute a workflow with a deadline through the orchestrator
    """
    print("\n" + "=" * 60)
    print("Example 1: Orchestrator Workflow with Deadline")
    print("=" * 60 + "\n")
    
    workflow_data = {
        "tasks": [
            {
                "type": "crypto_prediction",
                "params": {
                    "symbol": "BTC",
                    "timeframe": "1h",
                    "prediction_horizon": 24
                }
            }
        ],
        "priority": "high",
        "deadline": 120  # 2 minutes deadline
    }
    
    print("Sending workflow request with 120-second deadline...")
    print(f"Request: {json.dumps(workflow_data, indent=2)}\n")
    
    try:
        response = requests.post(
            f"{ORCHESTRATOR_URL}/orchestrate",
            json=workflow_data,
            timeout=130
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Response received:")
            print(f"  Workflow ID: {result.get('workflow_id')}")
            print(f"  Status: {result.get('status')}")
            print(f"  Duration: {result.get('duration', 0):.2f} seconds")
            print(f"  Deadline: {result.get('deadline')} seconds")
            print(f"  Deadline Exceeded: {result.get('deadline_exceeded')}")
            print(f"  Tasks Executed: {result.get('tasks_executed')}/{result.get('tasks_total')}")
            
            if result.get('deadline_exceeded'):
                print("\n⚠️  Workflow deadline was exceeded!")
            else:
                print("\n✅ Workflow completed within deadline")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_2_worker_task_with_deadline():
    """
    Example 2: Execute a worker task with a deadline
    """
    print("\n" + "=" * 60)
    print("Example 2: Worker Pool Task with Deadline")
    print("=" * 60 + "\n")
    
    task_data = {
        "worker_type": "crawler",
        "task": {
            "url": "https://api.github.com",
            "depth": 1,
            "deadline": 15  # 15 seconds deadline
        }
    }
    
    print("Sending crawler task with 15-second deadline...")
    print(f"Request: {json.dumps(task_data, indent=2)}\n")
    
    try:
        response = requests.post(
            f"{WORKER_POOL_URL}/task/execute",
            json=task_data,
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Response received:")
            print(f"  Task Status: {result.get('status')}")
            print(f"  Worker ID: {result.get('worker_id')}")
            
            if result.get('status') == 'success':
                print(f"  Data: {json.dumps(result.get('data'), indent=4)}")
                print("\n✅ Task completed within deadline")
            elif result.get('status') == 'timeout':
                print(f"  Error: {result.get('error')}")
                print("\n⚠️  Task exceeded deadline")
            else:
                print(f"  Error: {result.get('error')}")
                print("\n❌ Task failed")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_3_api_gateway_with_deadline():
    """
    Example 3: Use API Gateway with deadline enforcement
    """
    print("\n" + "=" * 60)
    print("Example 3: API Gateway Orchestration with Deadline")
    print("=" * 60 + "\n")
    
    workflow_data = {
        "tasks": [
            {
                "type": "crypto_prediction",
                "params": {
                    "symbol": "ETH",
                    "timeframe": "1h"
                }
            }
        ],
        "priority": "critical",
        "deadline": 60  # 1 minute deadline
    }
    
    print("Sending request through API Gateway with 60-second deadline...")
    print(f"Request: {json.dumps(workflow_data, indent=2)}\n")
    
    try:
        response = requests.post(
            f"{API_GATEWAY_URL}/api/v1/orchestrate",
            json=workflow_data,
            timeout=70
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Response received:")
            print(f"  Workflow ID: {result.get('workflow_id')}")
            print(f"  Status: {result.get('status')}")
            print(f"  Duration: {result.get('duration', 0):.2f} seconds")
            print(f"  Deadline Exceeded: {result.get('deadline_exceeded')}")
            
            if result.get('deadline_exceeded'):
                print("\n⚠️  Workflow deadline was exceeded!")
            else:
                print("\n✅ Workflow completed within deadline")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_4_analysis_worker_deadline():
    """
    Example 4: Analysis worker with deadline
    """
    print("\n" + "=" * 60)
    print("Example 4: Analysis Worker with Deadline")
    print("=" * 60 + "\n")
    
    task_data = {
        "worker_type": "analysis",
        "task": {
            "analysis_type": "sentiment",
            "data": {
                "text": "Bitcoin price is rising rapidly, showing strong bullish signals!"
            },
            "deadline": 10  # 10 seconds deadline
        }
    }
    
    print("Sending analysis task with 10-second deadline...")
    print(f"Request: {json.dumps(task_data, indent=2)}\n")
    
    try:
        response = requests.post(
            f"{WORKER_POOL_URL}/task/execute",
            json=task_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Response received:")
            print(f"  Task Status: {result.get('status')}")
            print(f"  Worker ID: {result.get('worker_id')}")
            
            if result.get('status') == 'success':
                print(f"  Analysis: {json.dumps(result.get('analysis'), indent=4)}")
                print("\n✅ Analysis completed within deadline")
            elif result.get('status') == 'timeout':
                print(f"  Error: {result.get('error')}")
                print("\n⚠️  Task exceeded deadline")
            else:
                print(f"  Error: {result.get('error')}")
                print("\n❌ Task failed")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("DEADLINE ENFORCEMENT EXAMPLES")
    print("VoBee AI Assistant - Swarm/Bot/Runners")
    print("=" * 60)
    
    print("\nNOTE: These examples require the services to be running.")
    print("Start services with: docker compose up -d")
    print("Or run: ./deploy.sh\n")
    
    input("Press Enter to run Example 1 (Orchestrator with Deadline)...")
    example_1_orchestrator_with_deadline()
    
    input("\nPress Enter to run Example 2 (Worker Task with Deadline)...")
    example_2_worker_task_with_deadline()
    
    input("\nPress Enter to run Example 3 (API Gateway with Deadline)...")
    example_3_api_gateway_with_deadline()
    
    input("\nPress Enter to run Example 4 (Analysis Worker with Deadline)...")
    example_4_analysis_worker_deadline()
    
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETED")
    print("=" * 60 + "\n")
    
    print("For more information, see DEADLINE_ENFORCEMENT.md")

if __name__ == "__main__":
    main()
