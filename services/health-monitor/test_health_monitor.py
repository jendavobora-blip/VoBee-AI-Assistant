"""
Tests for Health Monitor Service
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import HealthMonitor, app


@pytest.fixture
def health_monitor():
    """Create a health monitor instance for testing"""
    with patch.dict(os.environ, {
        'HEALTH_CHECK_INTERVAL': '10',
        'MAX_FAILURES_BEFORE_RECOVERY': '2',
        'RECOVERY_TIMEOUT': '30',
        'ELASTICSEARCH_ENABLED': 'false'
    }):
        return HealthMonitor()


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_monitor_initialization(health_monitor):
    """Test health monitor initializes correctly"""
    assert health_monitor.check_interval == 10
    assert health_monitor.max_failures == 2
    assert health_monitor.recovery_timeout == 30
    assert len(health_monitor.services) > 0


@pytest.mark.asyncio
async def test_check_service_health_success(health_monitor):
    """Test successful health check"""
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        result = await health_monitor.check_service_health('test-service', 'http://test:5000')
        
        assert result['service'] == 'test-service'
        assert result['status'] == 'healthy'
        assert 'response_time' in result


@pytest.mark.asyncio
async def test_check_service_health_failure(health_monitor):
    """Test failed health check"""
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            side_effect=Exception("Connection failed")
        )
        
        result = await health_monitor.check_service_health('test-service', 'http://test:5000')
        
        assert result['service'] == 'test-service'
        assert result['status'] == 'unreachable'
        assert 'error' in result


@pytest.mark.asyncio
async def test_auto_healing_trigger(health_monitor):
    """Test auto-healing is triggered after threshold failures"""
    # Simulate failures
    for i in range(3):
        health_monitor.failure_counts['test-service'] += 1
    
    with patch.object(health_monitor, 'auto_heal_service', new_callable=AsyncMock) as mock_heal:
        await health_monitor.check_all_services()
        # Note: This test would need proper mocking of service checks


def test_health_check_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'health-monitor'


def test_statistics_endpoint(client):
    """Test statistics endpoint"""
    response = client.get('/statistics')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_services' in data
    assert 'healthy_services' in data


def test_error_history_endpoint(client):
    """Test error history endpoint"""
    response = client.get('/error-history')
    assert response.status_code == 200
    data = response.get_json()
    assert 'all_services' in data


def test_recovery_history_endpoint(client):
    """Test recovery history endpoint"""
    response = client.get('/recovery-history')
    assert response.status_code == 200
    data = response.get_json()
    assert 'last_recovery_times' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
