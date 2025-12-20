"""
SQLAlchemy models for Waitlist and Invite system
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import hashlib

Base = declarative_base()


class WaitlistEntry(Base):
    """Waitlist entry model"""
    __tablename__ = 'waitlist_entries'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    email_hash = Column(String(64), nullable=False, index=True)  # GDPR-friendly hash
    use_case = Column(Text, nullable=False)
    persona = Column(String(50), nullable=False)
    priority_score = Column(Float, nullable=False, default=0.0)
    position = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    invited_at = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default='pending')  # pending, invited, joined
    
    def __init__(self, email, use_case, persona):
        self.email = email
        self.email_hash = hashlib.sha256(email.encode()).hexdigest()
        self.use_case = use_case
        self.persona = persona


class InviteCode(Base):
    """Invite code model"""
    __tablename__ = 'invite_codes'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    issued_to_email = Column(String(255), nullable=False)
    batch_id = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    used_by = Column(String(255), nullable=True)
    used_at = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default='active')  # active, used, expired
    
    def __init__(self, code, issued_to_email, batch_id=None):
        self.code = code
        self.issued_to_email = issued_to_email
        self.batch_id = batch_id
        self.expires_at = datetime.utcnow() + timedelta(days=7)
    
    def is_valid(self):
        """Check if code is valid (not used and not expired)"""
        return (self.status == 'active' and 
                self.expires_at > datetime.utcnow() and 
                self.used_by is None)


class Referral(Base):
    """Referral tracking model"""
    __tablename__ = 'referrals'
    
    id = Column(Integer, primary_key=True)
    referrer_email = Column(String(255), nullable=False, index=True)
    referred_email = Column(String(255), nullable=False)
    invite_code = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    redeemed_at = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default='pending')  # pending, redeemed, active


class UserAccount(Base):
    """User account model for tracking eligibility"""
    __tablename__ = 'user_accounts'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    trial_started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    active_days_count = Column(Integer, nullable=False, default=0)
    last_active_at = Column(DateTime, nullable=True)
    tier = Column(String(20), nullable=False, default='trial')
    referral_codes_earned = Column(Integer, nullable=False, default=0)
    referral_codes_available = Column(Integer, nullable=False, default=0)
    
    def is_eligible_for_referrals(self):
        """Check if user is eligible to generate referral codes"""
        days_since_trial = (datetime.utcnow() - self.trial_started_at).days
        return (days_since_trial >= 14 and 
                self.active_days_count >= 10 and
                self.referral_codes_available > 0)


class QualityMetrics(Base):
    """Quality gate metrics tracking"""
    __tablename__ = 'quality_metrics'
    
    id = Column(Integer, primary_key=True)
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    dau = Column(Integer, nullable=False, default=0)  # Daily Active Users
    mau = Column(Integer, nullable=False, default=0)  # Monthly Active Users
    feature_adoption_rate = Column(Float, nullable=False, default=0.0)
    paid_conversion_rate = Column(Float, nullable=False, default=0.0)
    referral_quality_score = Column(Float, nullable=False, default=0.0)
    trust_score = Column(Float, nullable=False, default=0.0)
    churn_rate_30d = Column(Float, nullable=False, default=0.0)
    invite_pause_status = Column(Boolean, nullable=False, default=False)


class InviteBatch(Base):
    """Batch release tracking"""
    __tablename__ = 'invite_batches'
    
    id = Column(Integer, primary_key=True)
    batch_id = Column(String(50), unique=True, nullable=False, index=True)
    batch_size = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
