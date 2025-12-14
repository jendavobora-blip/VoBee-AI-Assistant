"""
Fraud Detection Service
ML-based fraud detection for network and crypto transactions
"""

from flask import Flask, request, jsonify
import numpy as np
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class FraudDetector:
    """Fraud detection engine"""
    
    def __init__(self):
        self.threshold = float(os.getenv('ALERT_THRESHOLD', 0.75))
        logger.info(f"Fraud detector initialized with threshold={self.threshold}")
    
    def analyze_transaction(self, transaction_data):
        """Analyze a transaction for fraud indicators"""
        # Placeholder ML model
        # In production, use XGBoost/Random Forest trained on fraud data
        
        # Calculate risk score (0-1)
        risk_score = np.random.rand()
        
        # Check for common fraud patterns
        flags = []
        if transaction_data.get('amount', 0) > 10000:
            flags.append('large_amount')
            risk_score += 0.2
        
        if transaction_data.get('new_account', False):
            flags.append('new_account')
            risk_score += 0.15
        
        risk_score = min(risk_score, 1.0)
        
        return {
            'transaction_id': transaction_data.get('id', 'unknown'),
            'risk_score': risk_score,
            'is_fraud': risk_score > self.threshold,
            'flags': flags,
            'timestamp': datetime.utcnow().isoformat()
        }

detector = FraudDetector()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "fraud-detection"})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        result = detector.analyze_transaction(data)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)
