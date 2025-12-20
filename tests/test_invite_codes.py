"""
Tests for invite code generation and validation
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../services/invites'))

from generator import generate_invite_code, generate_batch
from models import InviteCode


class TestInviteCodeGeneration(unittest.TestCase):
    """Test invite code generation"""
    
    def test_code_format(self):
        """Test code has correct format"""
        code = generate_invite_code()
        
        # Check format: VOBEE-XXXXXXXXXXXX
        self.assertTrue(code.startswith("VOBEE-"))
        parts = code.split("-")
        self.assertEqual(len(parts), 2)
        self.assertEqual(len(parts[1]), 12)
        
        # Check all hex characters
        self.assertTrue(all(c in "0123456789ABCDEF" for c in parts[1]))
    
    def test_code_uniqueness(self):
        """Test generated codes are unique"""
        codes = [generate_invite_code() for _ in range(100)]
        
        # All codes should be unique
        self.assertEqual(len(codes), len(set(codes)))
    
    def test_batch_generation(self):
        """Test batch generation"""
        batch_size = 50
        codes = generate_batch(batch_size)
        
        self.assertEqual(len(codes), batch_size)
        self.assertEqual(len(codes), len(set(codes)))  # All unique
    
    def test_batch_format(self):
        """Test all codes in batch have correct format"""
        codes = generate_batch(10)
        
        for code in codes:
            self.assertTrue(code.startswith("VOBEE-"))
            parts = code.split("-")
            self.assertEqual(len(parts[1]), 12)


class TestInviteCodeValidation(unittest.TestCase):
    """Test invite code validation"""
    
    def test_valid_active_code(self):
        """Test active code is valid"""
        code = InviteCode(
            code="VOBEE-TEST123456",
            status="active"
        )
        self.assertTrue(code.is_valid())
    
    def test_used_code_invalid(self):
        """Test used code is invalid"""
        code = InviteCode(
            code="VOBEE-TEST123456",
            status="active",
            used_at=datetime.utcnow()
        )
        self.assertFalse(code.is_valid())
    
    def test_expired_code_invalid(self):
        """Test expired code is invalid"""
        code = InviteCode(
            code="VOBEE-TEST123456",
            status="active",
            expires_at=datetime.utcnow() - timedelta(days=1)
        )
        self.assertFalse(code.is_valid())
    
    def test_inactive_status_invalid(self):
        """Test inactive status makes code invalid"""
        code = InviteCode(
            code="VOBEE-TEST123456",
            status="expired"
        )
        self.assertFalse(code.is_valid())
    
    def test_code_expiration_default(self):
        """Test code expires after 7 days by default"""
        code = InviteCode(code="VOBEE-TEST123456")
        
        expected_expiry = code.created_at + timedelta(days=7)
        
        # Allow 1 second tolerance for test execution time
        delta = abs((code.expires_at - expected_expiry).total_seconds())
        self.assertLess(delta, 1)
    
    def test_code_to_dict(self):
        """Test serialization to dict"""
        code = InviteCode(
            code="VOBEE-TEST123456",
            batch_id="BATCH-001"
        )
        
        data = code.to_dict()
        
        self.assertEqual(data['code'], "VOBEE-TEST123456")
        self.assertEqual(data['batch_id'], "BATCH-001")
        self.assertEqual(data['status'], "active")
    
    def test_code_from_dict(self):
        """Test deserialization from dict"""
        data = {
            'code': "VOBEE-TEST123456",
            'batch_id': "BATCH-001",
            'status': "active",
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(days=7)).isoformat()
        }
        
        code = InviteCode.from_dict(data)
        
        self.assertEqual(code.code, "VOBEE-TEST123456")
        self.assertEqual(code.batch_id, "BATCH-001")
        self.assertEqual(code.status, "active")


if __name__ == '__main__':
    unittest.main()
