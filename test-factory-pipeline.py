#!/usr/bin/env python3
"""
Integration test for Application Factory and Media Factory E2E pipeline
Tests the complete workflow from user input to media output
"""

import requests
import json
import sys
import time
from typing import Dict, Any

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_test(message: str):
    print(f"{Colors.BLUE}[TEST]{Colors.END} {message}")

def print_pass(message: str):
    print(f"{Colors.GREEN}[PASS]{Colors.END} {message}")

def print_fail(message: str):
    print(f"{Colors.RED}[FAIL]{Colors.END} {message}")

def print_info(message: str):
    print(f"{Colors.YELLOW}[INFO]{Colors.END} {message}")

# Test configuration
BASE_URL = "http://localhost"
APP_FACTORY_PORT = 5011
MEDIA_FACTORY_PORT = 5012
ORCHESTRATOR_PORT = 5003

tests_passed = 0
tests_failed = 0

def test_application_factory_health():
    """Test 1: Application Factory health check"""
    global tests_passed, tests_failed
    print_test("Testing Application Factory health...")
    
    try:
        response = requests.get(f"{BASE_URL}:{APP_FACTORY_PORT}/health", timeout=5)
        if response.status_code == 200:
            print_pass("Application Factory is healthy")
            tests_passed += 1
            return True
        else:
            print_fail(f"Application Factory returned status {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(f"Application Factory health check failed: {e}")
        tests_failed += 1
        return False

def test_media_factory_health():
    """Test 2: Media Factory health check"""
    global tests_passed, tests_failed
    print_test("Testing Media Factory health...")
    
    try:
        response = requests.get(f"{BASE_URL}:{MEDIA_FACTORY_PORT}/health", timeout=5)
        if response.status_code == 200:
            print_pass("Media Factory is healthy")
            tests_passed += 1
            return True
        else:
            print_fail(f"Media Factory returned status {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(f"Media Factory health check failed: {e}")
        tests_failed += 1
        return False

def test_intent_extraction():
    """Test 3: Application Factory intent extraction"""
    global tests_passed, tests_failed
    print_test("Testing intent extraction...")
    
    test_input = "create an image of a beautiful sunset over mountains"
    
    try:
        response = requests.post(
            f"{BASE_URL}:{APP_FACTORY_PORT}/extract-intent",
            json={"input": test_input},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            intent_type = result.get('type')
            confidence = result.get('confidence', 0)
            
            if intent_type == 'generate_image' and confidence > 0.3:
                print_pass(f"Intent extracted: {intent_type} (confidence: {confidence:.2f})")
                tests_passed += 1
                return True
            else:
                print_fail(f"Unexpected intent: {intent_type} (confidence: {confidence:.2f})")
                tests_failed += 1
                return False
        else:
            print_fail(f"Intent extraction failed with status {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(f"Intent extraction failed: {e}")
        tests_failed += 1
        return False

def test_specification_generation():
    """Test 4: Application Factory specification generation"""
    global tests_passed, tests_failed
    print_test("Testing specification generation...")
    
    test_input = "generate a video showing a flying bird in realistic style"
    
    try:
        response = requests.post(
            f"{BASE_URL}:{APP_FACTORY_PORT}/generate-spec",
            json={"input": test_input, "validate": True},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            action = result.get('action')
            target_factory = result.get('target_factory')
            validation = result.get('validation', {})
            
            if action == 'generate_video' and target_factory == 'media_factory' and validation.get('valid'):
                print_pass(f"Specification generated: {action} -> {target_factory}")
                print_info(f"  Validation: valid={validation.get('valid')}, warnings={len(validation.get('warnings', []))}")
                tests_passed += 1
                return result
            else:
                print_fail(f"Invalid specification: action={action}, target={target_factory}, valid={validation.get('valid')}")
                tests_failed += 1
                return None
        else:
            print_fail(f"Specification generation failed with status {response.status_code}")
            tests_failed += 1
            return None
    except Exception as e:
        print_fail(f"Specification generation failed: {e}")
        tests_failed += 1
        return None

def test_media_factory_image_generation():
    """Test 5: Media Factory image generation"""
    global tests_passed, tests_failed
    print_test("Testing Media Factory image generation...")
    
    task_spec = {
        "action": "generate_image",
        "parameters": {
            "prompt": "a serene lake at dawn",
            "style": "realistic",
            "resolution": "1024x1024",
            "format": "png"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}:{MEDIA_FACTORY_PORT}/process",
            json=task_spec,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status')
            output = result.get('output', {})
            
            if status == 'completed' and 'image_id' in output:
                print_pass(f"Image generated: {output.get('image_id')}")
                print_info(f"  URL: {output.get('url')}")
                print_info(f"  Processing time: {result.get('processing_time_ms')}ms")
                tests_passed += 1
                return True
            else:
                print_fail(f"Image generation failed: status={status}")
                tests_failed += 1
                return False
        else:
            print_fail(f"Media Factory returned status {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(f"Image generation failed: {e}")
        tests_failed += 1
        return False

def test_media_factory_voice_processing():
    """Test 6: Media Factory voice processing"""
    global tests_passed, tests_failed
    print_test("Testing Media Factory voice processing...")
    
    task_spec = {
        "action": "process_voice",
        "parameters": {
            "task": "transcribe_voice",
            "format": "wav"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}:{MEDIA_FACTORY_PORT}/process",
            json=task_spec,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status')
            output = result.get('output', {})
            
            if status == 'completed' and 'transcription_id' in output:
                print_pass(f"Voice transcribed: {output.get('transcription_id')}")
                print_info(f"  Text: {output.get('text')}")
                print_info(f"  Confidence: {output.get('confidence')}")
                tests_passed += 1
                return True
            else:
                print_fail(f"Voice processing failed: status={status}")
                tests_failed += 1
                return False
        else:
            print_fail(f"Media Factory returned status {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(f"Voice processing failed: {e}")
        tests_failed += 1
        return False

def test_end_to_end_pipeline():
    """Test 7: Complete E2E pipeline through orchestrator"""
    global tests_passed, tests_failed
    print_test("Testing complete E2E pipeline...")
    
    test_input = "create an image of a futuristic cityscape in realistic style"
    
    try:
        response = requests.post(
            f"{BASE_URL}:{ORCHESTRATOR_PORT}/factory-pipeline",
            json={"input": test_input},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            pipeline_id = result.get('pipeline_id')
            status = result.get('status')
            stages = result.get('stages', {})
            
            if status == 'completed':
                print_pass(f"E2E pipeline completed: {pipeline_id}")
                
                # Check Application Factory stage
                app_stage = stages.get('application_factory', {})
                if app_stage.get('status') == 'completed':
                    print_info(f"  Application Factory: ✓")
                    spec = app_stage.get('specification', {})
                    print_info(f"    Intent: {spec.get('intent', {}).get('type')}")
                    print_info(f"    Action: {spec.get('action')}")
                
                # Check Media Factory stage
                media_stage = stages.get('media_factory', {})
                if media_stage.get('status') == 'completed':
                    print_info(f"  Media Factory: ✓")
                    media_result = media_stage.get('result', {})
                    output = media_result.get('output', {})
                    print_info(f"    Output: {output.get('image_id', output.get('video_id', 'N/A'))}")
                
                # Check overall output
                output = result.get('output', {})
                if output:
                    print_info(f"  Final Output: {output}")
                
                tests_passed += 1
                return True
            else:
                print_fail(f"E2E pipeline failed: status={status}")
                print_info(f"  Error: {result.get('error', 'Unknown error')}")
                tests_failed += 1
                return False
        else:
            print_fail(f"E2E pipeline returned status {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(f"E2E pipeline failed: {e}")
        tests_failed += 1
        return False

def test_media_factory_statistics():
    """Test 8: Media Factory statistics"""
    global tests_passed, tests_failed
    print_test("Testing Media Factory statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}:{MEDIA_FACTORY_PORT}/stats", timeout=5)
        
        if response.status_code == 200:
            stats = response.json()
            total_tasks = stats.get('total_tasks', 0)
            print_pass(f"Statistics retrieved: {total_tasks} tasks processed")
            print_info(f"  Task types: {stats.get('task_types', {})}")
            tests_passed += 1
            return True
        else:
            print_fail(f"Statistics retrieval failed with status {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(f"Statistics retrieval failed: {e}")
        tests_failed += 1
        return False

def test_media_factory_capabilities():
    """Test 9: Media Factory capabilities"""
    global tests_passed, tests_failed
    print_test("Testing Media Factory capabilities...")
    
    try:
        response = requests.get(f"{BASE_URL}:{MEDIA_FACTORY_PORT}/capabilities", timeout=5)
        
        if response.status_code == 200:
            capabilities = response.json()
            supported_tasks = capabilities.get('supported_tasks', [])
            print_pass(f"Capabilities retrieved: {len(supported_tasks)} supported tasks")
            for task in supported_tasks:
                print_info(f"  - {task.get('name')}: {task.get('description')}")
            tests_passed += 1
            return True
        else:
            print_fail(f"Capabilities retrieval failed with status {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print_fail(f"Capabilities retrieval failed: {e}")
        tests_failed += 1
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  Application & Media Factory E2E Pipeline Integration Tests")
    print("="*70 + "\n")
    
    # Run all tests
    test_application_factory_health()
    test_media_factory_health()
    test_intent_extraction()
    test_specification_generation()
    test_media_factory_image_generation()
    test_media_factory_voice_processing()
    test_end_to_end_pipeline()
    test_media_factory_statistics()
    test_media_factory_capabilities()
    
    # Summary
    print("\n" + "="*70)
    print("  Test Summary")
    print("="*70)
    total_tests = tests_passed + tests_failed
    print(f"Total Tests: {total_tests}")
    print(f"{Colors.GREEN}Passed: {tests_passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {tests_failed}{Colors.END}")
    print()
    
    if tests_failed == 0:
        print(f"{Colors.GREEN}All tests passed! ✓{Colors.END}")
        return 0
    else:
        print(f"{Colors.YELLOW}Some tests failed. Please check the services.{Colors.END}")
        print("Run 'docker compose logs -f application-factory media-factory orchestrator' for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
