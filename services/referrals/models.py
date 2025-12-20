"""
Database models for referrals
"""

from datetime import datetime
from typing import Optional
import uuid


class Referral:
    """Model for referral tracking"""
    
    def __init__(
        self,
        inviter_email: str,
        invited_email: str,
        invite_code: Optional[str] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.inviter_email = inviter_email
        self.invited_email = invited_email
        self.invite_code = invite_code
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'inviter_email': self.inviter_email,
            'invited_email': self.invited_email,
            'invite_code': self.invite_code,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(
            id=data.get('id'),
            inviter_email=data['inviter_email'],
            invited_email=data['invited_email'],
            invite_code=data.get('invite_code'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
