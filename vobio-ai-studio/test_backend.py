#!/usr/bin/env python3
"""
Test script for Vobio AI Studio backend
Tests all API endpoints and functionality
"""

import asyncio
import json
import sys
import time
import requests
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

def print_header(text: str):
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}\n")

def print_result(success: bool, test_name: str, details: str = ""):
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"    {details}")

def test_health_check() -> bool:
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        data = response.json()
        success = response.status_code == 200 and data.get("status") == "healthy"
        print_result(success, "Health Check", f"Status: {data.get('status')}, Engine: {data.get('engine')}")
        return success
    except Exception as e:
        print_result(False, "Health Check", f"Error: {str(e)}")
        return False

def test_gpu_info() -> bool:
    """Test GPU info endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/gpu-info", timeout=5)
        data = response.json()
        success = response.status_code == 200 and "device" in data
        print_result(success, "GPU Info", f"Device: {data.get('device')}, Available: {data.get('available')}")
        return success
    except Exception as e:
        print_result(False, "GPU Info", f"Error: {str(e)}")
        return False

def test_image_generation() -> bool:
    """Test image generation endpoint"""
    try:
        payload = {
            "prompt": "A beautiful sunset over mountains",
            "style": "realistic",
            "resolution": "1024x1024",
            "hdr": True,
            "pbr": True
        }
        response = requests.post(f"{BASE_URL}/generate/image", json=payload, timeout=30)
        data = response.json()
        success = (
            response.status_code == 200 and 
            data.get("status") == "success" and
            "image_id" in data
        )
        print_result(success, "Image Generation", 
                    f"Operation ID: {data.get('operation_id')}, Status: {data.get('status')}")
        return success
    except Exception as e:
        print_result(False, "Image Generation", f"Error: {str(e)}")
        return False

def test_video_generation() -> bool:
    """Test video generation endpoint"""
    try:
        payload = {
            "prompt": "Flying through clouds",
            "duration": 3,
            "resolution": "4K",
            "fps": 30,
            "use_nerf": False
        }
        response = requests.post(f"{BASE_URL}/generate/video", json=payload, timeout=30)
        data = response.json()
        success = (
            response.status_code == 200 and 
            data.get("status") == "success" and
            "video_id" in data
        )
        print_result(success, "Video Generation", 
                    f"Operation ID: {data.get('operation_id')}, Duration: {data.get('duration')}s")
        return success
    except Exception as e:
        print_result(False, "Video Generation", f"Error: {str(e)}")
        return False

def main():
    print_header("Vobio AI Studio - Backend Tests")
    
    # Wait for server to be ready
    print("Checking if server is running...")
    max_retries = 5
    for i in range(max_retries):
        try:
            requests.get(f"{BASE_URL}/health", timeout=2)
            print("✓ Server is ready\n")
            break
        except:
            if i == max_retries - 1:
                print("✗ Server is not responding. Please start the backend first.")
                print(f"  Run: cd backend && python api_server.py")
                sys.exit(1)
            print(f"  Waiting for server... ({i+1}/{max_retries})")
            time.sleep(2)
    
    # Run tests
    results = []
    results.append(test_health_check())
    results.append(test_gpu_info())
    results.append(test_image_generation())
    results.append(test_video_generation())
    
    # Summary
    print_header("Test Summary")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
