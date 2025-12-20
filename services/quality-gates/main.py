"""
Quality Gates Service - Flask API for system health monitoring
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import os

from monitor import calculate_trust_score, should_pause_invites, get_health_status
from alerts import check_thresholds

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# In-memory metrics storage (for demo/development purposes)
# In production, replace this with Redis, database, or metrics collection service
# TODO: Integrate with Prometheus, StatsD, or similar metrics backend
current_metrics = {
    'churn_rate': 0.12,
    'fraud_rate': 0.02,
    'engagement_rate': 0.75,
    'active_users': 1000,
    'new_signups_today': 25
}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'quality-gates',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/quality/trust-score', methods=['GET'])
def get_trust_score():
    """Get current trust score and metrics"""
    try:
        trust_score = calculate_trust_score(current_metrics)
        churn_rate = current_metrics.get('churn_rate', 0)
        invites_paused = should_pause_invites(trust_score, churn_rate)
        
        return jsonify({
            'trust_score': round(trust_score, 2),
            'churn_rate': churn_rate,
            'fraud_rate': current_metrics.get('fraud_rate', 0),
            'engagement_rate': current_metrics.get('engagement_rate', 0),
            'invites_paused': invites_paused,
            'health_status': get_health_status(current_metrics)
        })
        
    except Exception as e:
        logger.error(f"Error calculating trust score: {e}")
        return jsonify({'error': 'Failed to calculate trust score'}), 500


@app.route('/api/quality/evaluate-gate', methods=['POST'])
def evaluate_gate():
    """Evaluate if quality gates allow new invites"""
    try:
        # Get current metrics
        trust_score = calculate_trust_score(current_metrics)
        churn_rate = current_metrics.get('churn_rate', 0)
        invites_allowed = not should_pause_invites(trust_score, churn_rate)
        
        # Check for alerts
        alerts = check_thresholds({
            **current_metrics,
            'trust_score': trust_score
        })
        
        return jsonify({
            'invites_allowed': invites_allowed,
            'trust_score': round(trust_score, 2),
            'metrics': current_metrics,
            'alerts': [alert.to_dict() for alert in alerts]
        })
        
    except Exception as e:
        logger.error(f"Error evaluating gate: {e}")
        return jsonify({'error': 'Failed to evaluate gate'}), 500


@app.route('/api/quality/metrics', methods=['POST'])
def update_metrics():
    """Update system metrics"""
    try:
        data = request.get_json()
        
        # Update metrics
        if 'churn_rate' in data:
            current_metrics['churn_rate'] = data['churn_rate']
        if 'fraud_rate' in data:
            current_metrics['fraud_rate'] = data['fraud_rate']
        if 'engagement_rate' in data:
            current_metrics['engagement_rate'] = data['engagement_rate']
        if 'active_users' in data:
            current_metrics['active_users'] = data['active_users']
        if 'new_signups_today' in data:
            current_metrics['new_signups_today'] = data['new_signups_today']
        
        return jsonify({
            'status': 'success',
            'metrics': current_metrics
        })
        
    except Exception as e:
        logger.error(f"Error updating metrics: {e}")
        return jsonify({'error': 'Failed to update metrics'}), 500


@app.route('/api/quality/alerts', methods=['GET'])
def get_alerts():
    """Get current alerts"""
    try:
        trust_score = calculate_trust_score(current_metrics)
        alerts = check_thresholds({
            **current_metrics,
            'trust_score': trust_score
        })
        
        return jsonify({
            'alerts': [alert.to_dict() for alert in alerts],
            'count': len(alerts)
        })
        
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({'error': 'Failed to get alerts'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
