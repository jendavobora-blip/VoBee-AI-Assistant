"""
Pytest configuration and shared fixtures for QA testing
"""

import pytest
import asyncio
import os
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Test configuration
TEST_CONFIG = {
    'api_gateway_url': os.getenv('API_GATEWAY_URL', 'http://localhost:8000'),
    'image_service_url': os.getenv('IMAGE_SERVICE_URL', 'http://localhost:5000'),
    'video_service_url': os.getenv('VIDEO_SERVICE_URL', 'http://localhost:5001'),
    'crypto_service_url': os.getenv('CRYPTO_SERVICE_URL', 'http://localhost:5002'),
    'orchestrator_url': os.getenv('ORCHESTRATOR_URL', 'http://localhost:5003'),
    'fraud_service_url': os.getenv('FRAUD_SERVICE_URL', 'http://localhost:5004'),
    'timeout': 300,
    'stress_test_iterations': int(os.getenv('STRESS_TEST_ITERATIONS', '50000')),
    'load_test_users': int(os.getenv('LOAD_TEST_USERS', '1000')),
}

@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """Provide test configuration"""
    return TEST_CONFIG

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def sample_image_request():
    """Sample image generation request"""
    return {
        "prompt": "A futuristic cityscape at sunset",
        "style": "realistic",
        "resolution": "512x512",
        "hdr": True,
        "pbr": False,
        "model": "stable-diffusion"
    }

@pytest.fixture
def sample_video_request():
    """Sample video generation request"""
    return {
        "prompt": "Flying through clouds",
        "duration": 3,
        "resolution": "720p",
        "fps": 30,
        "use_nerf": False,
        "style": "realistic"
    }

@pytest.fixture
def sample_crypto_request():
    """Sample crypto prediction request"""
    return {
        "symbol": "BTC",
        "timeframe": "1h",
        "prediction_horizon": 24
    }

@pytest.fixture
def sample_orchestration_request():
    """Sample orchestration request"""
    return {
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
        "priority": "normal"
    }

@pytest.fixture
def sample_fraud_request():
    """Sample fraud detection request"""
    return {
        "transaction_id": "test-tx-12345",
        "amount": 1000.0,
        "currency": "USD",
        "user_id": "user-123",
        "ip_address": "192.168.1.1"
    }
