"""
Database models for waitlist service
"""

from datetime import datetime
from typing import Optional
import uuid


class WaitlistEntry:
    """Model for waitlist entries"""
    
    def __init__(
        self,
        email: str,
        use_case: str,
        persona: str,
        priority_score: int = 0,
        position: Optional[int] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        invited_at: Optional[datetime] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.email = email
        self.use_case = use_case
        self.persona = persona
        self.priority_score = priority_score
        self.position = position
        self.created_at = created_at or datetime.utcnow()
        self.invited_at = invited_at
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'use_case': self.use_case,
            'persona': self.persona,
            'priority_score': self.priority_score,
            'position': self.position,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'invited_at': self.invited_at.isoformat() if self.invited_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(
            id=data.get('id'),
            email=data['email'],
            use_case=data['use_case'],
            persona=data['persona'],
            priority_score=data.get('priority_score', 0),
            position=data.get('position'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            invited_at=datetime.fromisoformat(data['invited_at']) if data.get('invited_at') else None
        )
