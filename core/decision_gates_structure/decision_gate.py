"""
Decision Gate - Individual gate with confirmation requirements
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GateStatus(Enum):
    """Status of a decision gate"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class GateType(Enum):
    """Type of decision gate"""
    CONFIRMATION = "confirmation"  # Simple yes/no
    APPROVAL = "approval"  # Requires explicit approval
    REVIEW = "review"  # Requires review before proceeding
    MERGE_LOCK = "merge_lock"  # Blocks merge until approved
    OUTPUT_LOCK = "output_lock"  # Locks output until confirmed


class DecisionGate:
    """
    Individual decision gate requiring confirmation before proceeding
    Implements confirmation pending/output-lock requirements
    """
    
    def __init__(
        self,
        gate_id: str,
        gate_type: GateType,
        title: str,
        description: str = "",
        context: Optional[Dict[str, Any]] = None,
        required_approvers: Optional[List[str]] = None,
        auto_expire_minutes: Optional[int] = None
    ):
        """
        Initialize decision gate
        
        Args:
            gate_id: Unique gate identifier
            gate_type: Type of gate
            title: Gate title/summary
            description: Detailed description
            context: Additional context data
            required_approvers: List of approver IDs (if applicable)
            auto_expire_minutes: Minutes until auto-expiry (None = no expiry)
        """
        self.gate_id = gate_id
        self.gate_type = gate_type
        self.title = title
        self.description = description
        self.context = context or {}
        self.status = GateStatus.PENDING
        self.required_approvers = required_approvers or []
        self.approvals: List[Dict[str, Any]] = []
        self.rejections: List[Dict[str, Any]] = []
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
        self.expires_at = None
        self.resolved_at = None
        self.resolution_note = None
        
        # Set expiry if specified
        if auto_expire_minutes:
            from datetime import timedelta
            expires = datetime.utcnow() + timedelta(minutes=auto_expire_minutes)
            self.expires_at = expires.isoformat()
        
        # Output lock flag
        self.output_locked = gate_type == GateType.OUTPUT_LOCK
        
        logger.info(
            f"Created decision gate {gate_id} ({gate_type.value}): {title}"
        )
    
    def approve(
        self,
        approver_id: str,
        note: Optional[str] = None
    ) -> bool:
        """
        Approve the decision gate
        
        Args:
            approver_id: ID of the approver
            note: Optional approval note
            
        Returns:
            True if approval recorded successfully
        """
        if self.status != GateStatus.PENDING:
            logger.warning(
                f"Cannot approve gate {self.gate_id}: "
                f"Status is {self.status.value}"
            )
            return False
        
        # Check if already approved by this approver
        if any(a['approver_id'] == approver_id for a in self.approvals):
            logger.warning(
                f"Gate {self.gate_id} already approved by {approver_id}"
            )
            return False
        
        # Record approval
        approval = {
            'approver_id': approver_id,
            'note': note,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.approvals.append(approval)
        self.updated_at = datetime.utcnow().isoformat()
        
        # Check if all required approvals received
        if self._check_approval_threshold():
            self.status = GateStatus.APPROVED
            self.resolved_at = datetime.utcnow().isoformat()
            self.output_locked = False
            logger.info(f"Gate {self.gate_id} fully approved")
        
        return True
    
    def reject(
        self,
        rejector_id: str,
        reason: Optional[str] = None
    ) -> bool:
        """
        Reject the decision gate
        
        Args:
            rejector_id: ID of the rejector
            reason: Optional rejection reason
            
        Returns:
            True if rejection recorded successfully
        """
        if self.status != GateStatus.PENDING:
            logger.warning(
                f"Cannot reject gate {self.gate_id}: "
                f"Status is {self.status.value}"
            )
            return False
        
        # Record rejection
        rejection = {
            'rejector_id': rejector_id,
            'reason': reason,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.rejections.append(rejection)
        
        # Single rejection is enough to reject the gate
        self.status = GateStatus.REJECTED
        self.resolved_at = datetime.utcnow().isoformat()
        self.resolution_note = reason
        self.updated_at = datetime.utcnow().isoformat()
        
        logger.info(f"Gate {self.gate_id} rejected by {rejector_id}")
        return True
    
    def cancel(self, reason: Optional[str] = None) -> bool:
        """Cancel the decision gate"""
        if self.status != GateStatus.PENDING:
            return False
        
        self.status = GateStatus.CANCELLED
        self.resolved_at = datetime.utcnow().isoformat()
        self.resolution_note = reason
        self.updated_at = datetime.utcnow().isoformat()
        
        logger.info(f"Gate {self.gate_id} cancelled")
        return True
    
    def check_expiry(self) -> bool:
        """
        Check if gate has expired
        
        Returns:
            True if gate was expired (and status updated)
        """
        if self.status != GateStatus.PENDING:
            return False
        
        if not self.expires_at:
            return False
        
        if datetime.utcnow() > datetime.fromisoformat(self.expires_at):
            self.status = GateStatus.EXPIRED
            self.resolved_at = datetime.utcnow().isoformat()
            self.updated_at = datetime.utcnow().isoformat()
            logger.info(f"Gate {self.gate_id} expired")
            return True
        
        return False
    
    def is_approved(self) -> bool:
        """Check if gate is approved"""
        return self.status == GateStatus.APPROVED
    
    def is_rejected(self) -> bool:
        """Check if gate is rejected"""
        return self.status == GateStatus.REJECTED
    
    def is_pending(self) -> bool:
        """Check if gate is still pending"""
        self.check_expiry()  # Update status if expired
        return self.status == GateStatus.PENDING
    
    def is_output_locked(self) -> bool:
        """Check if output is locked"""
        return self.output_locked and self.status == GateStatus.PENDING
    
    def _check_approval_threshold(self) -> bool:
        """Check if approval threshold is met"""
        if not self.required_approvers:
            # No specific approvers required, any approval is sufficient
            return len(self.approvals) > 0
        
        # Check if all required approvers have approved
        approved_ids = {a['approver_id'] for a in self.approvals}
        required_ids = set(self.required_approvers)
        
        return required_ids.issubset(approved_ids)
    
    def get_approval_progress(self) -> Dict[str, Any]:
        """Get approval progress information"""
        total_required = len(self.required_approvers) if self.required_approvers else 1
        received = len(self.approvals)
        
        return {
            'total_required': total_required,
            'received': received,
            'pending': max(0, total_required - received),
            'percentage': (received / total_required * 100) if total_required > 0 else 0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert gate to dictionary"""
        return {
            'gate_id': self.gate_id,
            'gate_type': self.gate_type.value,
            'title': self.title,
            'description': self.description,
            'context': self.context,
            'status': self.status.value,
            'required_approvers': self.required_approvers,
            'approvals': self.approvals,
            'rejections': self.rejections,
            'output_locked': self.output_locked,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'expires_at': self.expires_at,
            'resolved_at': self.resolved_at,
            'resolution_note': self.resolution_note,
            'approval_progress': self.get_approval_progress()
        }
