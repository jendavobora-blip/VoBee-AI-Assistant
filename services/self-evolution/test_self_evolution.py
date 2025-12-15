"""
Tests for Self-Evolution Service
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SelfEvolutionEngine, UsagePattern, OptimizationRecommendation, app


@pytest.fixture
def evolution_engine():
    """Create a self-evolution engine instance for testing"""
    with patch.dict(os.environ, {
        'ANALYSIS_WINDOW_HOURS': '24',
        'OPTIMIZATION_THRESHOLD': '0.15',
        'AUTO_APPLY_OPTIMIZATIONS': 'false',
        'ELASTICSEARCH_ENABLED': 'false'
    }):
        return SelfEvolutionEngine()


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_evolution_engine_initialization(evolution_engine):
    """Test evolution engine initializes correctly"""
    assert evolution_engine.analysis_window_hours == 24
    assert evolution_engine.optimization_threshold == 0.15
    assert evolution_engine.auto_apply_enabled == False


def test_collect_usage_data(evolution_engine):
    """Test usage data collection"""
    evolution_engine.collect_usage_data(
        service='test-service',
        endpoint='/test',
        response_time=2.5,
        status_code=200
    )
    
    assert 'test-service' in evolution_engine.usage_patterns
    assert len(evolution_engine.usage_patterns['test-service']) == 1


def test_analyze_patterns_with_sufficient_data(evolution_engine):
    """Test pattern analysis with sufficient data"""
    # Generate sample data
    for i in range(20):
        evolution_engine.collect_usage_data(
            service='test-service',
            endpoint='/test',
            response_time=2.5 + (i % 3),
            status_code=200
        )
    
    patterns = evolution_engine.analyze_patterns()
    assert len(patterns) > 0
    assert isinstance(patterns[0], UsagePattern)


def test_identify_inefficiencies_slow_response(evolution_engine):
    """Test identification of slow response times"""
    # Create pattern with slow response time
    pattern = UsagePattern(
        service='test-service',
        endpoint='/test',
        frequency=100,
        avg_response_time=3.5,  # Slow
        error_rate=0.05,
        timestamp='2024-01-01T00:00:00'
    )
    
    recommendations = evolution_engine.identify_inefficiencies([pattern])
    
    assert len(recommendations) > 0
    assert any(r.type == 'performance' for r in recommendations)


def test_identify_inefficiencies_high_errors(evolution_engine):
    """Test identification of high error rates"""
    # Create pattern with high error rate
    pattern = UsagePattern(
        service='test-service',
        endpoint='/test',
        frequency=100,
        avg_response_time=1.0,
        error_rate=0.15,  # High error rate
        timestamp='2024-01-01T00:00:00'
    )
    
    recommendations = evolution_engine.identify_inefficiencies([pattern])
    
    assert len(recommendations) > 0
    assert any(r.type == 'reliability' for r in recommendations)


def test_identify_inefficiencies_high_traffic(evolution_engine):
    """Test identification of high traffic patterns"""
    # Create pattern with high traffic
    pattern = UsagePattern(
        service='test-service',
        endpoint='/test',
        frequency=1500,  # High traffic
        avg_response_time=1.0,
        error_rate=0.02,
        timestamp='2024-01-01T00:00:00'
    )
    
    recommendations = evolution_engine.identify_inefficiencies([pattern])
    
    assert len(recommendations) > 0
    assert any(r.type == 'scaling' for r in recommendations)


def test_apply_optimization(evolution_engine):
    """Test applying an optimization"""
    # Create a recommendation
    rec = OptimizationRecommendation(
        id='test123',
        type='performance',
        target_service='test-service',
        description='Test optimization',
        priority='high',
        estimated_improvement=0.3,
        status='pending',
        created_at='2024-01-01T00:00:00'
    )
    
    evolution_engine.recommendations['test123'] = rec
    
    result = evolution_engine.apply_optimization('test123')
    
    assert result['success'] == True
    assert rec.status == 'applied'


def test_rollback_optimization(evolution_engine):
    """Test rolling back an optimization"""
    # Create and apply an optimization
    rec = OptimizationRecommendation(
        id='test123',
        type='performance',
        target_service='test-service',
        description='Test optimization',
        priority='high',
        estimated_improvement=0.3,
        status='pending',
        created_at='2024-01-01T00:00:00'
    )
    
    evolution_engine.recommendations['test123'] = rec
    evolution_engine.apply_optimization('test123')
    
    # Rollback
    result = evolution_engine.rollback_optimization('test123')
    
    assert 'recommendation_id' in result
    assert result['recommendation_id'] == 'test123'


def test_health_check_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'self-evolution'


def test_collect_usage_endpoint(client):
    """Test collect usage endpoint"""
    response = client.post('/collect-usage', json={
        'service': 'test-service',
        'endpoint': '/test',
        'response_time': 2.5,
        'status_code': 200
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data


def test_collect_usage_endpoint_missing_fields(client):
    """Test collect usage endpoint with missing fields"""
    response = client.post('/collect-usage', json={
        'service': 'test-service'
    })
    assert response.status_code == 400


def test_recommendations_endpoint(client):
    """Test recommendations endpoint"""
    response = client.get('/recommendations')
    assert response.status_code == 200
    data = response.get_json()
    assert 'count' in data
    assert 'recommendations' in data


def test_recommendations_endpoint_with_filter(client):
    """Test recommendations endpoint with status filter"""
    response = client.get('/recommendations?status=pending')
    assert response.status_code == 200
    data = response.get_json()
    assert 'recommendations' in data


def test_applied_optimizations_endpoint(client):
    """Test applied optimizations endpoint"""
    response = client.get('/applied-optimizations')
    assert response.status_code == 200
    data = response.get_json()
    assert 'count' in data
    assert 'optimizations' in data


def test_rollback_history_endpoint(client):
    """Test rollback history endpoint"""
    response = client.get('/rollback-history')
    assert response.status_code == 200
    data = response.get_json()
    assert 'count' in data
    assert 'rollbacks' in data


def test_performance_baselines_endpoint(client):
    """Test performance baselines endpoint"""
    response = client.get('/performance-baselines')
    assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
