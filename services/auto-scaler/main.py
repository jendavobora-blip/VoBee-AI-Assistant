"""
Auto-Scaler Service
Monitors resource usage and scales services automatically
"""

from flask import Flask, jsonify
import psutil
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class AutoScaler:
    """Auto-scaling engine based on metrics"""
    
    def __init__(self):
        self.scale_up_threshold = int(os.getenv('SCALE_UP_THRESHOLD', 80))
        self.scale_down_threshold = int(os.getenv('SCALE_DOWN_THRESHOLD', 20))
        logger.info(f"Auto-scaler initialized: up={self.scale_up_threshold}%, down={self.scale_down_threshold}%")
    
    def get_metrics(self):
        """Get current system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def should_scale_up(self, metrics):
        """Determine if scaling up is needed"""
        return metrics['cpu_percent'] > self.scale_up_threshold or \
               metrics['memory_percent'] > self.scale_up_threshold
    
    def should_scale_down(self, metrics):
        """Determine if scaling down is needed"""
        return metrics['cpu_percent'] < self.scale_down_threshold and \
               metrics['memory_percent'] < self.scale_down_threshold

scaler = AutoScaler()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "auto-scaler"})

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(scaler.get_metrics())

@app.route('/scaling-decision', methods=['GET'])
def scaling_decision():
    metrics = scaler.get_metrics()
    decision = {
        'metrics': metrics,
        'recommendation': 'maintain'
    }
    
    if scaler.should_scale_up(metrics):
        decision['recommendation'] = 'scale_up'
    elif scaler.should_scale_down(metrics):
        decision['recommendation'] = 'scale_down'
    
    return jsonify(decision)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=False)
