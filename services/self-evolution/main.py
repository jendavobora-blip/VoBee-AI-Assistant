"""
Self-Evolution Service
Analyzes usage patterns, identifies inefficiencies, and optimizes system performance
"""

from flask import Flask, jsonify, request
import logging
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict, Counter
from elasticsearch import Elasticsearch
import numpy as np
from dataclasses import dataclass, asdict
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@dataclass
class UsagePattern:
    """Data class for usage patterns"""
    service: str
    endpoint: str
    frequency: int
    avg_response_time: float
    error_rate: float
    timestamp: str


@dataclass
class OptimizationRecommendation:
    """Data class for optimization recommendations"""
    id: str
    type: str
    target_service: str
    description: str
    priority: str
    estimated_improvement: float
    status: str
    created_at: str
    applied_at: str = None


class SelfEvolutionEngine:
    """Main self-evolution and optimization engine"""
    
    def __init__(self):
        # Configuration
        self.analysis_window_hours = int(os.getenv('ANALYSIS_WINDOW_HOURS', 24))
        self.optimization_threshold = float(os.getenv('OPTIMIZATION_THRESHOLD', 0.15))
        self.auto_apply_enabled = os.getenv('AUTO_APPLY_OPTIMIZATIONS', 'false').lower() == 'true'
        
        # Tracking data
        self.usage_patterns = defaultdict(list)
        self.recommendations = {}
        self.applied_optimizations = []
        self.rollback_history = []
        self.performance_baselines = {}
        
        # ElasticSearch for data collection
        self.es_enabled = os.getenv('ELASTICSEARCH_ENABLED', 'true').lower() == 'true'
        if self.es_enabled:
            try:
                self.es_client = Elasticsearch([os.getenv('ELASTICSEARCH_URL', 'http://elasticsearch:9200')])
                logger.info("Connected to ElasticSearch for usage analysis")
            except Exception as e:
                logger.warning(f"Failed to connect to ElasticSearch: {e}")
                self.es_enabled = False
        
        logger.info(f"Self-Evolution Engine initialized")
        logger.info(f"Analysis window: {self.analysis_window_hours}h, Auto-apply: {self.auto_apply_enabled}")
    
    def collect_usage_data(self, service: str, endpoint: str, response_time: float, 
                          status_code: int) -> None:
        """Collect usage data for analysis"""
        pattern = {
            'service': service,
            'endpoint': endpoint,
            'response_time': response_time,
            'status_code': status_code,
            'timestamp': datetime.utcnow().isoformat(),
            'is_error': status_code >= 400
        }
        
        self.usage_patterns[service].append(pattern)
        
        # Log to ElasticSearch
        self.log_usage_to_elasticsearch(pattern)
    
    def analyze_patterns(self) -> List[UsagePattern]:
        """Analyze collected usage patterns"""
        analyzed_patterns = []
        
        for service, patterns in self.usage_patterns.items():
            # Group by endpoint
            endpoint_data = defaultdict(list)
            for pattern in patterns:
                endpoint_data[pattern['endpoint']].append(pattern)
            
            # Analyze each endpoint
            for endpoint, data in endpoint_data.items():
                if len(data) < 10:  # Need minimum data points
                    continue
                
                frequency = len(data)
                response_times = [d['response_time'] for d in data]
                errors = [d for d in data if d['is_error']]
                
                usage_pattern = UsagePattern(
                    service=service,
                    endpoint=endpoint,
                    frequency=frequency,
                    avg_response_time=np.mean(response_times),
                    error_rate=len(errors) / len(data) if data else 0,
                    timestamp=datetime.utcnow().isoformat()
                )
                
                analyzed_patterns.append(usage_pattern)
        
        return analyzed_patterns
    
    def identify_inefficiencies(self, patterns: List[UsagePattern]) -> List[OptimizationRecommendation]:
        """Identify inefficiencies and generate recommendations"""
        recommendations = []
        
        for pattern in patterns:
            # Check for slow response times
            if pattern.avg_response_time > 2.0:  # More than 2 seconds
                rec_id = self.generate_recommendation_id(pattern.service, "slow_response")
                recommendation = OptimizationRecommendation(
                    id=rec_id,
                    type="performance",
                    target_service=pattern.service,
                    description=f"High response time detected ({pattern.avg_response_time:.2f}s). "
                               f"Consider adding caching or optimizing queries.",
                    priority="high" if pattern.avg_response_time > 5.0 else "medium",
                    estimated_improvement=0.3,  # 30% improvement estimate
                    status="pending",
                    created_at=datetime.utcnow().isoformat()
                )
                recommendations.append(recommendation)
            
            # Check for high error rates
            if pattern.error_rate > 0.1:  # More than 10% errors
                rec_id = self.generate_recommendation_id(pattern.service, "high_errors")
                recommendation = OptimizationRecommendation(
                    id=rec_id,
                    type="reliability",
                    target_service=pattern.service,
                    description=f"High error rate detected ({pattern.error_rate*100:.1f}%). "
                               f"Implement retry logic and improve error handling.",
                    priority="critical" if pattern.error_rate > 0.25 else "high",
                    estimated_improvement=0.5,  # 50% error reduction estimate
                    status="pending",
                    created_at=datetime.utcnow().isoformat()
                )
                recommendations.append(recommendation)
            
            # Check for high frequency endpoints - consider scaling
            if pattern.frequency > 1000:  # High traffic endpoint
                rec_id = self.generate_recommendation_id(pattern.service, "high_traffic")
                recommendation = OptimizationRecommendation(
                    id=rec_id,
                    type="scaling",
                    target_service=pattern.service,
                    description=f"High traffic detected ({pattern.frequency} requests). "
                               f"Consider horizontal scaling or load balancing.",
                    priority="medium",
                    estimated_improvement=0.2,  # 20% performance improvement
                    status="pending",
                    created_at=datetime.utcnow().isoformat()
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def generate_recommendation_id(self, service: str, issue_type: str) -> str:
        """Generate unique recommendation ID"""
        data = f"{service}:{issue_type}:{datetime.utcnow().date()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def apply_optimization(self, recommendation_id: str) -> Dict[str, Any]:
        """Apply an optimization recommendation"""
        if recommendation_id not in self.recommendations:
            return {"error": "Recommendation not found"}
        
        recommendation = self.recommendations[recommendation_id]
        
        if recommendation.status != "pending":
            return {"error": "Recommendation already processed"}
        
        # Store baseline for rollback
        baseline = self.capture_performance_baseline(recommendation.target_service)
        
        # Apply optimization based on type
        result = self.execute_optimization(recommendation)
        
        if result.get('success'):
            recommendation.status = "applied"
            recommendation.applied_at = datetime.utcnow().isoformat()
            
            self.applied_optimizations.append({
                'recommendation_id': recommendation_id,
                'recommendation': asdict(recommendation),
                'baseline': baseline,
                'applied_at': recommendation.applied_at,
                'result': result
            })
            
            # Log to ElasticSearch
            self.log_optimization_to_elasticsearch({
                'action': 'apply',
                'recommendation': asdict(recommendation),
                'result': result
            })
            
            logger.info(f"Applied optimization {recommendation_id} to {recommendation.target_service}")
        else:
            recommendation.status = "failed"
            logger.error(f"Failed to apply optimization {recommendation_id}: {result.get('error')}")
        
        return result
    
    def execute_optimization(self, recommendation: OptimizationRecommendation) -> Dict[str, Any]:
        """Execute the actual optimization"""
        # In a real implementation, this would:
        # 1. Update configuration files
        # 2. Adjust resource allocations
        # 3. Enable/disable features
        # 4. Modify deployment parameters
        
        logger.info(f"Executing optimization for {recommendation.target_service}")
        
        if recommendation.type == "performance":
            # Enable caching, optimize queries, etc.
            return {
                'success': True,
                'action': 'enabled_caching',
                'details': 'Response caching enabled for frequently accessed endpoints'
            }
        
        elif recommendation.type == "reliability":
            # Add retry logic, improve error handling
            return {
                'success': True,
                'action': 'improved_error_handling',
                'details': 'Enhanced retry logic and circuit breaker patterns implemented'
            }
        
        elif recommendation.type == "scaling":
            # Trigger auto-scaler
            return {
                'success': True,
                'action': 'triggered_scaling',
                'details': 'Horizontal scaling initiated based on traffic patterns'
            }
        
        return {'success': False, 'error': 'Unknown optimization type'}
    
    def capture_performance_baseline(self, service: str) -> Dict[str, Any]:
        """Capture current performance metrics as baseline"""
        baseline = {
            'service': service,
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': {
                'avg_response_time': 0,
                'error_rate': 0,
                'throughput': 0
            }
        }
        
        # Calculate current metrics from recent patterns
        recent_patterns = [p for p in self.usage_patterns.get(service, []) 
                          if datetime.fromisoformat(p['timestamp']) > 
                          datetime.utcnow() - timedelta(hours=1)]
        
        if recent_patterns:
            response_times = [p['response_time'] for p in recent_patterns]
            errors = [p for p in recent_patterns if p['is_error']]
            
            baseline['metrics']['avg_response_time'] = np.mean(response_times)
            baseline['metrics']['error_rate'] = len(errors) / len(recent_patterns)
            baseline['metrics']['throughput'] = len(recent_patterns)
        
        self.performance_baselines[service] = baseline
        return baseline
    
    def rollback_optimization(self, recommendation_id: str) -> Dict[str, Any]:
        """Rollback a previously applied optimization"""
        # Find the applied optimization
        optimization = None
        for opt in self.applied_optimizations:
            if opt['recommendation_id'] == recommendation_id:
                optimization = opt
                break
        
        if not optimization:
            return {"error": "Optimization not found or not applied"}
        
        # Restore baseline configuration
        logger.warning(f"Rolling back optimization {recommendation_id}")
        
        rollback_result = {
            'recommendation_id': recommendation_id,
            'service': optimization['recommendation']['target_service'],
            'rollback_time': datetime.utcnow().isoformat(),
            'baseline_restored': optimization['baseline'],
            'reason': 'Manual rollback requested'
        }
        
        self.rollback_history.append(rollback_result)
        
        # Update recommendation status
        if recommendation_id in self.recommendations:
            self.recommendations[recommendation_id].status = "rolled_back"
        
        # Log to ElasticSearch
        self.log_optimization_to_elasticsearch({
            'action': 'rollback',
            'result': rollback_result
        })
        
        return rollback_result
    
    def log_usage_to_elasticsearch(self, usage_data: Dict[str, Any]):
        """Log usage data to ElasticSearch"""
        if not self.es_enabled:
            return
        
        try:
            doc = {
                'type': 'usage_data',
                **usage_data,
                '@timestamp': datetime.utcnow().isoformat()
            }
            self.es_client.index(index='self-evolution-usage', document=doc)
        except Exception as e:
            logger.error(f"Failed to log usage to ElasticSearch: {e}")
    
    def log_optimization_to_elasticsearch(self, optimization_data: Dict[str, Any]):
        """Log optimization action to ElasticSearch"""
        if not self.es_enabled:
            return
        
        try:
            doc = {
                'type': 'optimization',
                **optimization_data,
                '@timestamp': datetime.utcnow().isoformat()
            }
            self.es_client.index(index='self-evolution-optimizations', document=doc)
        except Exception as e:
            logger.error(f"Failed to log optimization to ElasticSearch: {e}")


# Initialize self-evolution engine
evolution_engine = SelfEvolutionEngine()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "self-evolution",
        "timestamp": datetime.utcnow().isoformat(),
        "elasticsearch_enabled": evolution_engine.es_enabled,
        "auto_apply_enabled": evolution_engine.auto_apply_enabled
    })


@app.route('/collect-usage', methods=['POST'])
def collect_usage():
    """Collect usage data for analysis"""
    data = request.get_json()
    
    required_fields = ['service', 'endpoint', 'response_time', 'status_code']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    evolution_engine.collect_usage_data(
        service=data['service'],
        endpoint=data['endpoint'],
        response_time=data['response_time'],
        status_code=data['status_code']
    )
    
    return jsonify({
        "message": "Usage data collected",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze usage patterns and generate recommendations"""
    patterns = evolution_engine.analyze_patterns()
    recommendations = evolution_engine.identify_inefficiencies(patterns)
    
    # Store recommendations
    for rec in recommendations:
        evolution_engine.recommendations[rec.id] = rec
    
    return jsonify({
        "patterns_analyzed": len(patterns),
        "recommendations_generated": len(recommendations),
        "recommendations": [asdict(r) for r in recommendations],
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get all recommendations"""
    status_filter = request.args.get('status')
    
    recommendations = list(evolution_engine.recommendations.values())
    
    if status_filter:
        recommendations = [r for r in recommendations if r.status == status_filter]
    
    return jsonify({
        "count": len(recommendations),
        "recommendations": [asdict(r) for r in recommendations]
    })


@app.route('/apply-optimization/<recommendation_id>', methods=['POST'])
def apply_optimization(recommendation_id: str):
    """Apply a specific optimization"""
    result = evolution_engine.apply_optimization(recommendation_id)
    return jsonify(result)


@app.route('/rollback/<recommendation_id>', methods=['POST'])
def rollback(recommendation_id: str):
    """Rollback an applied optimization"""
    result = evolution_engine.rollback_optimization(recommendation_id)
    return jsonify(result)


@app.route('/applied-optimizations', methods=['GET'])
def get_applied_optimizations():
    """Get history of applied optimizations"""
    return jsonify({
        "count": len(evolution_engine.applied_optimizations),
        "optimizations": evolution_engine.applied_optimizations
    })


@app.route('/rollback-history', methods=['GET'])
def get_rollback_history():
    """Get rollback history"""
    return jsonify({
        "count": len(evolution_engine.rollback_history),
        "rollbacks": evolution_engine.rollback_history
    })


@app.route('/performance-baselines', methods=['GET'])
def get_baselines():
    """Get performance baselines"""
    return jsonify(evolution_engine.performance_baselines)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)
