"""
Tests for referral quality calculation
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../services/referrals'))

from quality import calculate_quality_score, calculate_rewards


class TestReferralQuality(unittest.TestCase):
    """Test referral quality scoring"""
    
    def test_no_referrals(self):
        """Test quality score with no referrals"""
        score = calculate_quality_score([])
        self.assertEqual(score, 0.0)
    
    def test_recent_referrals(self):
        """Test recent referrals score higher"""
        recent_referrals = [
            {'created_at': datetime.utcnow() - timedelta(days=5)},
            {'created_at': datetime.utcnow() - timedelta(days=10)},
        ]
        
        old_referrals = [
            {'created_at': datetime.utcnow() - timedelta(days=50)},
            {'created_at': datetime.utcnow() - timedelta(days=60)},
        ]
        
        recent_score = calculate_quality_score(recent_referrals, days_active=30)
        old_score = calculate_quality_score(old_referrals, days_active=30)
        
        self.assertGreater(recent_score, old_score)
    
    def test_score_range(self):
        """Test score is always between 0 and 1"""
        # Very recent referrals
        referrals = [
            {'created_at': datetime.utcnow()},
            {'created_at': datetime.utcnow() - timedelta(days=1)},
            {'created_at': datetime.utcnow() - timedelta(days=2)},
        ]
        
        score = calculate_quality_score(referrals)
        
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_quality_with_iso_strings(self):
        """Test quality calculation with ISO string dates"""
        referrals = [
            {'created_at': (datetime.utcnow() - timedelta(days=5)).isoformat()},
            {'created_at': (datetime.utcnow() - timedelta(days=10)).isoformat()},
        ]
        
        score = calculate_quality_score(referrals)
        
        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 1.0)


class TestReferralRewards(unittest.TestCase):
    """Test referral reward calculation"""
    
    def test_no_referrals_no_rewards(self):
        """Test no rewards for no referrals"""
        rewards = calculate_rewards(0, 0.0)
        self.assertEqual(len(rewards), 0)
    
    def test_first_milestone(self):
        """Test rewards for 3 referrals"""
        rewards = calculate_rewards(3, 0.5)
        
        # Should have at least one reward
        self.assertGreater(len(rewards), 0)
        
        # Check for invite codes reward
        invite_reward = next((r for r in rewards if r['type'] == 'invite_codes'), None)
        self.assertIsNotNone(invite_reward)
        self.assertEqual(invite_reward['amount'], 3)
    
    def test_second_milestone(self):
        """Test rewards for 10 referrals"""
        rewards = calculate_rewards(10, 0.5)
        
        # Should have multiple rewards
        self.assertGreater(len(rewards), 1)
        
        # Check both milestones present
        reward_amounts = [r['amount'] for r in rewards if r['type'] == 'invite_codes']
        self.assertIn(3, reward_amounts)
        self.assertIn(5, reward_amounts)
    
    def test_premium_milestone(self):
        """Test premium reward for 25 referrals"""
        rewards = calculate_rewards(25, 0.5)
        
        # Check for premium reward
        premium_reward = next((r for r in rewards if r['type'] == 'premium'), None)
        self.assertIsNotNone(premium_reward)
        self.assertEqual(premium_reward['duration'], '1 month')
    
    def test_quality_bonus(self):
        """Test quality bonus for high-quality referrals"""
        # High quality + enough referrals
        rewards = calculate_rewards(5, 0.85)
        
        # Should have quality bonus
        quality_bonus = next((r for r in rewards if r['type'] == 'quality_bonus'), None)
        self.assertIsNotNone(quality_bonus)
        self.assertEqual(quality_bonus['amount'], 2)
    
    def test_no_quality_bonus_low_quality(self):
        """Test no quality bonus for low quality"""
        # Low quality score
        rewards = calculate_rewards(5, 0.5)
        
        # Should not have quality bonus
        quality_bonus = next((r for r in rewards if r['type'] == 'quality_bonus'), None)
        self.assertIsNone(quality_bonus)
    
    def test_no_quality_bonus_insufficient_referrals(self):
        """Test no quality bonus with too few referrals"""
        # High quality but not enough referrals
        rewards = calculate_rewards(3, 0.85)
        
        # Should not have quality bonus
        quality_bonus = next((r for r in rewards if r['type'] == 'quality_bonus'), None)
        self.assertIsNone(quality_bonus)


if __name__ == '__main__':
    unittest.main()
