"""
Database models for invite codes
"""

from datetime import datetime, timedelta
from typing import Optional


class InviteCode:
    """Model for invite codes"""
    
    def __init__(
        self,
        code: str,
        batch_id: Optional[str] = None,
        issued_to: Optional[str] = None,
        created_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
        used_by: Optional[str] = None,
        used_at: Optional[datetime] = None,
        status: str = 'active'
    ):
        self.code = code
        self.batch_id = batch_id
        self.issued_to = issued_to
        self.created_at = created_at or datetime.utcnow()
        self.expires_at = expires_at or (self.created_at + timedelta(days=7))
        self.used_by = used_by
        self.used_at = used_at
        self.status = status  # active, used, expired
    
    def is_valid(self) -> bool:
        """Check if code is valid"""
        if self.status != 'active':
            return False
        if self.used_at is not None:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return True
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'code': self.code,
            'batch_id': self.batch_id,
            'issued_to': self.issued_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'used_by': self.used_by,
            'used_at': self.used_at.isoformat() if self.used_at else None,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(
            code=data['code'],
            batch_id=data.get('batch_id'),
            issued_to=data.get('issued_to'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None,
            used_by=data.get('used_by'),
            used_at=datetime.fromisoformat(data['used_at']) if data.get('used_at') else None,
            status=data.get('status', 'active')
        )
