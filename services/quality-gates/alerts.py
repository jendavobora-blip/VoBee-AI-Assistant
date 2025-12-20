"""
Alert system for quality gate violations
"""

from datetime import datetime
from typing import Dict, List


class Alert:
    """Alert model"""
    
    def __init__(self, severity: str, message: str, metric: str, value: float, threshold: float):
        self.id = datetime.utcnow().isoformat()
        self.severity = severity  # info, warning, critical
        self.message = message
        self.metric = metric
        self.value = value
        self.threshold = threshold
        self.timestamp = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'severity': self.severity,
            'message': self.message,
            'metric': self.metric,
            'value': self.value,
            'threshold': self.threshold,
            'timestamp': self.timestamp.isoformat()
        }


def check_thresholds(metrics: Dict) -> List[Alert]:
    """
    Check metrics against thresholds and generate alerts
    
    Args:
        metrics: Dictionary of system metrics
    
    Returns:
        List of alerts
    """
    alerts = []
    
    # Churn rate alerts
    churn_rate = metrics.get('churn_rate', 0)
    if churn_rate > 0.2:
        alerts.append(Alert(
            severity='critical',
            message='Churn rate exceeds critical threshold',
            metric='churn_rate',
            value=churn_rate,
            threshold=0.2
        ))
    elif churn_rate > 0.15:
        alerts.append(Alert(
            severity='warning',
            message='Churn rate exceeds warning threshold',
            metric='churn_rate',
            value=churn_rate,
            threshold=0.15
        ))
    
    # Trust score alerts
    trust_score = metrics.get('trust_score', 1.0)
    if trust_score < 0.7:
        alerts.append(Alert(
            severity='critical',
            message='Trust score below critical threshold',
            metric='trust_score',
            value=trust_score,
            threshold=0.7
        ))
    elif trust_score < 0.8:
        alerts.append(Alert(
            severity='warning',
            message='Trust score below warning threshold',
            metric='trust_score',
            value=trust_score,
            threshold=0.8
        ))
    
    # Fraud rate alerts
    fraud_rate = metrics.get('fraud_rate', 0)
    if fraud_rate > 0.05:
        alerts.append(Alert(
            severity='critical',
            message='Fraud rate exceeds threshold',
            metric='fraud_rate',
            value=fraud_rate,
            threshold=0.05
        ))
    
    return alerts
