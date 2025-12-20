"""
Trust score calculation and monitoring
"""

from datetime import datetime, timedelta
from typing import Dict


def calculate_trust_score(metrics: Dict) -> float:
    """
    Calculate overall trust score for the system
    
    Args:
        metrics: Dictionary of system metrics
    
    Returns:
        Trust score between 0 and 1
    """
    score = 1.0
    
    # Churn rate impact
    churn_rate = metrics.get('churn_rate', 0)
    if churn_rate > 0.15:  # 15% threshold
        score -= (churn_rate - 0.15) * 2
    
    # Fraud rate impact
    fraud_rate = metrics.get('fraud_rate', 0)
    if fraud_rate > 0.05:  # 5% threshold
        score -= (fraud_rate - 0.05) * 3
    
    # Engagement rate impact
    engagement_rate = metrics.get('engagement_rate', 1.0)
    if engagement_rate < 0.5:  # 50% threshold
        score -= (0.5 - engagement_rate)
    
    # Ensure score is between 0 and 1
    return max(0.0, min(1.0, score))


def should_pause_invites(trust_score: float, churn_rate: float, thresholds: Dict = None) -> bool:
    """
    Determine if invites should be paused
    
    Args:
        trust_score: Current trust score
        churn_rate: Current churn rate
        thresholds: Optional custom thresholds
    
    Returns:
        True if invites should be paused
    """
    if thresholds is None:
        thresholds = {
            'trust_score': 0.7,
            'churn_rate': 0.2
        }
    
    if trust_score < thresholds['trust_score']:
        return True
    
    if churn_rate > thresholds['churn_rate']:
        return True
    
    return False


def get_health_status(metrics: Dict) -> str:
    """
    Get overall health status
    
    Args:
        metrics: Dictionary of system metrics
    
    Returns:
        Health status: 'healthy', 'warning', or 'critical'
    """
    trust_score = calculate_trust_score(metrics)
    churn_rate = metrics.get('churn_rate', 0)
    
    if trust_score >= 0.8 and churn_rate < 0.1:
        return 'healthy'
    elif trust_score >= 0.7 and churn_rate < 0.15:
        return 'warning'
    else:
        return 'critical'
