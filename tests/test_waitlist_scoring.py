"""
Tests for waitlist scoring algorithm
"""

import unittest
import sys
import os

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../services/waitlist'))

from scoring import calculate_priority_score, estimate_wait_time


class TestWaitlistScoring(unittest.TestCase):
    """Test waitlist priority scoring"""
    
    def test_solo_founder_score(self):
        """Test solo founder gets correct base score"""
        score = calculate_priority_score(
            "user@example.com",
            "I want to use VoBee",
            "solo_founder"
        )
        self.assertEqual(score, 10)
    
    def test_agency_higher_score(self):
        """Test agency gets higher score than solo founder"""
        agency_score = calculate_priority_score(
            "agency@example.com",
            "I want to use VoBee",
            "agency"
        )
        solo_score = calculate_priority_score(
            "solo@example.com",
            "I want to use VoBee",
            "solo_founder"
        )
        self.assertGreater(agency_score, solo_score)
    
    def test_detailed_use_case_bonus(self):
        """Test detailed use case gets bonus points"""
        detailed = "I want to use VoBee for marketing automation content creation " \
                  "and time-saving workflows to help my team be more productive " \
                  "with AI-powered tools for our daily operations"
        
        brief = "I want to use VoBee"
        
        detailed_score = calculate_priority_score(
            "user@example.com",
            detailed,
            "solo_founder"
        )
        brief_score = calculate_priority_score(
            "user@example.com",
            brief,
            "solo_founder"
        )
        
        self.assertGreater(detailed_score, brief_score)
    
    def test_keyword_bonus(self):
        """Test keywords increase score"""
        with_keywords = "I need marketing automation for content"
        without_keywords = "I need this tool for my work"
        
        with_score = calculate_priority_score(
            "user@example.com",
            with_keywords,
            "solo_founder"
        )
        without_score = calculate_priority_score(
            "user@example.com",
            without_keywords,
            "solo_founder"
        )
        
        self.assertGreater(with_score, without_score)
    
    def test_combined_bonuses(self):
        """Test all bonuses stack correctly"""
        max_score = calculate_priority_score(
            "agency@example.com",
            "I need marketing automation for content creation with AI time-saving workflows " \
            "to help our agency deliver better results for clients through automated processes " \
            "and intelligent content generation that saves time and improves quality",
            "agency"
        )
        
        # Agency (20) + detailed (10) + keywords (5) = 35
        self.assertEqual(max_score, 35)
    
    def test_estimate_wait_time(self):
        """Test wait time estimation"""
        # Test different positions
        self.assertEqual(estimate_wait_time(30, 1000), "1-2 days")
        self.assertEqual(estimate_wait_time(100, 1000), "1 week")
        self.assertEqual(estimate_wait_time(300, 1000), "2-3 weeks")
        self.assertEqual(estimate_wait_time(700, 1000), "1 month")
        self.assertEqual(estimate_wait_time(1500, 2000), "4-6 weeks")


if __name__ == '__main__':
    unittest.main()
