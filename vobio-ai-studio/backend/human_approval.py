"""
Human Approval Queue System
Manages operations that require human approval
"""

import os
import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

APPROVAL_TIMEOUT_HOURS = int(os.getenv("APPROVAL_TIMEOUT_HOURS", "24"))


class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest:
    """Represents a request for human approval"""
    
    def __init__(self, user_id: str, operation_type: str, operation_data: Dict[str, Any], 
                 risk_level: str, reason: str):
        self.request_id = str(uuid.uuid4())
        self.user_id = user_id
        self.operation_type = operation_type
        self.operation_data = operation_data
        self.risk_level = risk_level
        self.reason = reason
        self.status = ApprovalStatus.PENDING
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(hours=APPROVAL_TIMEOUT_HOURS)
        self.reviewed_at = None
        self.reviewed_by = None
        self.review_comment = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "operation_type": self.operation_type,
            "operation_data": self.operation_data,
            "risk_level": self.risk_level,
            "reason": self.reason,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "reviewed_by": self.reviewed_by,
            "review_comment": self.review_comment
        }
    
    def is_expired(self) -> bool:
        """Check if request has expired"""
        return datetime.utcnow() > self.expires_at


class HumanApprovalQueue:
    """Manages queue of operations requiring human approval"""
    
    def __init__(self):
        self.requests: Dict[str, ApprovalRequest] = {}
    
    def create_request(self, user_id: str, operation_type: str, 
                      operation_data: Dict[str, Any], risk_level: str, 
                      reason: str) -> ApprovalRequest:
        """Create a new approval request"""
        request = ApprovalRequest(user_id, operation_type, operation_data, risk_level, reason)
        self.requests[request.request_id] = request
        
        logger.info(f"Approval request created: {request.request_id} ({operation_type}, risk: {risk_level})")
        
        return request
    
    def get_request(self, request_id: str) -> Optional[ApprovalRequest]:
        """Get a specific request"""
        request = self.requests.get(request_id)
        
        # Check expiration
        if request and request.is_expired() and request.status == ApprovalStatus.PENDING:
            request.status = ApprovalStatus.EXPIRED
            logger.info(f"Request expired: {request_id}")
        
        return request
    
    def approve_request(self, request_id: str, reviewer: str, comment: Optional[str] = None) -> bool:
        """Approve a request"""
        request = self.get_request(request_id)
        
        if not request:
            logger.warning(f"Request not found: {request_id}")
            return False
        
        if request.status != ApprovalStatus.PENDING:
            logger.warning(f"Request not in pending state: {request_id} (status: {request.status})")
            return False
        
        if request.is_expired():
            request.status = ApprovalStatus.EXPIRED
            logger.warning(f"Request expired: {request_id}")
            return False
        
        request.status = ApprovalStatus.APPROVED
        request.reviewed_at = datetime.utcnow()
        request.reviewed_by = reviewer
        request.review_comment = comment
        
        logger.info(f"Request approved: {request_id} by {reviewer}")
        return True
    
    def reject_request(self, request_id: str, reviewer: str, comment: Optional[str] = None) -> bool:
        """Reject a request"""
        request = self.get_request(request_id)
        
        if not request:
            logger.warning(f"Request not found: {request_id}")
            return False
        
        if request.status != ApprovalStatus.PENDING:
            logger.warning(f"Request not in pending state: {request_id}")
            return False
        
        request.status = ApprovalStatus.REJECTED
        request.reviewed_at = datetime.utcnow()
        request.reviewed_by = reviewer
        request.review_comment = comment
        
        logger.info(f"Request rejected: {request_id} by {reviewer}")
        return True
    
    def get_pending_requests(self, user_id: Optional[str] = None) -> List[ApprovalRequest]:
        """Get all pending requests, optionally filtered by user"""
        pending = []
        
        for request in self.requests.values():
            # Update expired requests
            if request.is_expired() and request.status == ApprovalStatus.PENDING:
                request.status = ApprovalStatus.EXPIRED
            
            # Filter
            if request.status == ApprovalStatus.PENDING:
                if user_id is None or request.user_id == user_id:
                    pending.append(request)
        
        # Sort by creation time (oldest first)
        pending.sort(key=lambda r: r.created_at)
        
        return pending
    
    def get_user_requests(self, user_id: str, status: Optional[ApprovalStatus] = None) -> List[ApprovalRequest]:
        """Get all requests for a user, optionally filtered by status"""
        user_requests = []
        
        for request in self.requests.values():
            if request.user_id == user_id:
                if status is None or request.status == status:
                    user_requests.append(request)
        
        # Sort by creation time (newest first)
        user_requests.sort(key=lambda r: r.created_at, reverse=True)
        
        return user_requests
    
    def cleanup_expired(self):
        """Mark all expired pending requests as expired"""
        expired_count = 0
        
        for request in self.requests.values():
            if request.is_expired() and request.status == ApprovalStatus.PENDING:
                request.status = ApprovalStatus.EXPIRED
                expired_count += 1
        
        if expired_count > 0:
            logger.info(f"Marked {expired_count} requests as expired")


# Global instance
_approval_queue = None


def get_approval_queue() -> HumanApprovalQueue:
    """Get or create the global HumanApprovalQueue instance"""
    global _approval_queue
    if _approval_queue is None:
        _approval_queue = HumanApprovalQueue()
    return _approval_queue
