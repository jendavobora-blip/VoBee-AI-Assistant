"""
Tests for quality gate thresholds
"""

import unittest
import sys
import os

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../services/quality-gates'))

from monitor import calculate_trust_score, should_pause_invites, get_health_status
from alerts import check_thresholds


class TestTrustScore(unittest.TestCase):
    """Test trust score calculation"""
    
    def test_perfect_metrics(self):
        """Test perfect metrics give perfect score"""
        metrics = {
            'churn_rate': 0.0,
            'fraud_rate': 0.0,
            'engagement_rate': 1.0
        }
        
        score = calculate_trust_score(metrics)
        self.assertEqual(score, 1.0)
    
    def test_high_churn_penalty(self):
        """Test high churn rate reduces score"""
        good_metrics = {
            'churn_rate': 0.10,
            'fraud_rate': 0.0,
            'engagement_rate': 1.0
        }
        
        bad_metrics = {
            'churn_rate': 0.25,
            'fraud_rate': 0.0,
            'engagement_rate': 1.0
        }
        
        good_score = calculate_trust_score(good_metrics)
        bad_score = calculate_trust_score(bad_metrics)
        
        self.assertGreater(good_score, bad_score)
    
    def test_fraud_rate_penalty(self):
        """Test fraud rate reduces score significantly"""
        good_metrics = {
            'churn_rate': 0.0,
            'fraud_rate': 0.02,
            'engagement_rate': 1.0
        }
        
        bad_metrics = {
            'churn_rate': 0.0,
            'fraud_rate': 0.10,
            'engagement_rate': 1.0
        }
        
        good_score = calculate_trust_score(good_metrics)
        bad_score = calculate_trust_score(bad_metrics)
        
        self.assertGreater(good_score, bad_score)
    
    def test_low_engagement_penalty(self):
        """Test low engagement reduces score"""
        good_metrics = {
            'churn_rate': 0.0,
            'fraud_rate': 0.0,
            'engagement_rate': 0.8
        }
        
        bad_metrics = {
            'churn_rate': 0.0,
            'fraud_rate': 0.0,
            'engagement_rate': 0.3
        }
        
        good_score = calculate_trust_score(good_metrics)
        bad_score = calculate_trust_score(bad_metrics)
        
        self.assertGreater(good_score, bad_score)
    
    def test_score_bounds(self):
        """Test score is always between 0 and 1"""
        # Worst possible metrics
        metrics = {
            'churn_rate': 1.0,
            'fraud_rate': 1.0,
            'engagement_rate': 0.0
        }
        
        score = calculate_trust_score(metrics)
        
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


class TestInvitePause(unittest.TestCase):
    """Test invite pause logic"""
    
    def test_good_metrics_allow_invites(self):
        """Test good metrics allow invites"""
        trust_score = 0.85
        churn_rate = 0.10
        
        paused = should_pause_invites(trust_score, churn_rate)
        self.assertFalse(paused)
    
    def test_low_trust_pauses_invites(self):
        """Test low trust score pauses invites"""
        trust_score = 0.65
        churn_rate = 0.10
        
        paused = should_pause_invites(trust_score, churn_rate)
        self.assertTrue(paused)
    
    def test_high_churn_pauses_invites(self):
        """Test high churn rate pauses invites"""
        trust_score = 0.85
        churn_rate = 0.25
        
        paused = should_pause_invites(trust_score, churn_rate)
        self.assertTrue(paused)
    
    def test_custom_thresholds(self):
        """Test custom thresholds work"""
        trust_score = 0.75
        churn_rate = 0.15
        
        # Default thresholds - should not pause
        paused_default = should_pause_invites(trust_score, churn_rate)
        self.assertFalse(paused_default)
        
        # Stricter thresholds - should pause
        strict_thresholds = {
            'trust_score': 0.8,
            'churn_rate': 0.1
        }
        paused_strict = should_pause_invites(trust_score, churn_rate, strict_thresholds)
        self.assertTrue(paused_strict)


class TestHealthStatus(unittest.TestCase):
    """Test health status determination"""
    
    def test_healthy_status(self):
        """Test healthy status for good metrics"""
        metrics = {
            'churn_rate': 0.08,
            'fraud_rate': 0.01,
            'engagement_rate': 0.85
        }
        
        status = get_health_status(metrics)
        self.assertEqual(status, 'healthy')
    
    def test_warning_status(self):
        """Test warning status for moderate metrics"""
        metrics = {
            'churn_rate': 0.12,
            'fraud_rate': 0.03,
            'engagement_rate': 0.65
        }
        
        status = get_health_status(metrics)
        self.assertEqual(status, 'warning')
    
    def test_critical_status(self):
        """Test critical status for bad metrics"""
        metrics = {
            'churn_rate': 0.25,
            'fraud_rate': 0.08,
            'engagement_rate': 0.40
        }
        
        status = get_health_status(metrics)
        self.assertEqual(status, 'critical')


class TestAlertGeneration(unittest.TestCase):
    """Test alert generation"""
    
    def test_no_alerts_good_metrics(self):
        """Test no alerts for good metrics"""
        metrics = {
            'churn_rate': 0.08,
            'fraud_rate': 0.01,
            'engagement_rate': 0.85,
            'trust_score': 0.90
        }
        
        alerts = check_thresholds(metrics)
        self.assertEqual(len(alerts), 0)
    
    def test_churn_warning_alert(self):
        """Test warning alert for elevated churn"""
        metrics = {
            'churn_rate': 0.17,
            'fraud_rate': 0.01,
            'engagement_rate': 0.85,
            'trust_score': 0.90
        }
        
        alerts = check_thresholds(metrics)
        
        self.assertGreater(len(alerts), 0)
        
        # Check for churn rate alert
        churn_alert = next((a for a in alerts if a.metric == 'churn_rate'), None)
        self.assertIsNotNone(churn_alert)
        self.assertEqual(churn_alert.severity, 'warning')
    
    def test_churn_critical_alert(self):
        """Test critical alert for high churn"""
        metrics = {
            'churn_rate': 0.25,
            'fraud_rate': 0.01,
            'engagement_rate': 0.85,
            'trust_score': 0.90
        }
        
        alerts = check_thresholds(metrics)
        
        # Check for critical churn alert
        churn_alert = next((a for a in alerts if a.metric == 'churn_rate'), None)
        self.assertIsNotNone(churn_alert)
        self.assertEqual(churn_alert.severity, 'critical')
    
    def test_trust_score_alert(self):
        """Test alert for low trust score"""
        metrics = {
            'churn_rate': 0.08,
            'fraud_rate': 0.01,
            'engagement_rate': 0.85,
            'trust_score': 0.65
        }
        
        alerts = check_thresholds(metrics)
        
        # Check for trust score alert
        trust_alert = next((a for a in alerts if a.metric == 'trust_score'), None)
        self.assertIsNotNone(trust_alert)
        self.assertEqual(trust_alert.severity, 'critical')
    
    def test_fraud_alert(self):
        """Test alert for high fraud rate"""
        metrics = {
            'churn_rate': 0.08,
            'fraud_rate': 0.08,
            'engagement_rate': 0.85,
            'trust_score': 0.90
        }
        
        alerts = check_thresholds(metrics)
        
        # Check for fraud alert
        fraud_alert = next((a for a in alerts if a.metric == 'fraud_rate'), None)
        self.assertIsNotNone(fraud_alert)
        self.assertEqual(fraud_alert.severity, 'critical')
    
    def test_multiple_alerts(self):
        """Test multiple alerts can be generated"""
        metrics = {
            'churn_rate': 0.25,
            'fraud_rate': 0.08,
            'engagement_rate': 0.85,
            'trust_score': 0.65
        }
        
        alerts = check_thresholds(metrics)
        
        # Should have multiple alerts
        self.assertGreater(len(alerts), 2)


if __name__ == '__main__':
    unittest.main()
