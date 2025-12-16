"""
Gate Manager - Manages all decision gates in the system
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from uuid import uuid4

from .decision_gate import DecisionGate, GateStatus, GateType

logger = logging.getLogger(__name__)


class GateManager:
    """
    Central manager for all decision gates
    Enforces confirmation pending and output lock requirements
    """
    
    def __init__(self):
        self.gates: Dict[str, DecisionGate] = {}
        self.created_at = datetime.utcnow().isoformat()
        logger.info("GateManager initialized")
    
    def create_gate(
        self,
        gate_type: GateType,
        title: str,
        description: str = "",
        context: Optional[Dict[str, Any]] = None,
        required_approvers: Optional[List[str]] = None,
        auto_expire_minutes: Optional[int] = None
    ) -> DecisionGate:
        """
        Create a new decision gate
        
        Args:
            gate_type: Type of gate to create
            title: Gate title
            description: Gate description
            context: Additional context
            required_approvers: List of required approver IDs
            auto_expire_minutes: Auto-expiry time in minutes
            
        Returns:
            Created DecisionGate instance
        """
        gate_id = str(uuid4())
        
        gate = DecisionGate(
            gate_id=gate_id,
            gate_type=gate_type,
            title=title,
            description=description,
            context=context,
            required_approvers=required_approvers,
            auto_expire_minutes=auto_expire_minutes
        )
        
        self.gates[gate_id] = gate
        logger.info(f"Created gate {gate_id}: {title}")
        
        return gate
    
    def get_gate(self, gate_id: str) -> Optional[DecisionGate]:
        """Get gate by ID"""
        gate = self.gates.get(gate_id)
        if gate:
            gate.check_expiry()  # Update expiry status
        return gate
    
    def approve_gate(
        self,
        gate_id: str,
        approver_id: str,
        note: Optional[str] = None
    ) -> bool:
        """
        Approve a decision gate
        
        Args:
            gate_id: Gate identifier
            approver_id: Approver identifier
            note: Optional approval note
            
        Returns:
            True if approval successful
        """
        gate = self.get_gate(gate_id)
        if not gate:
            logger.error(f"Gate {gate_id} not found")
            return False
        
        return gate.approve(approver_id, note)
    
    def reject_gate(
        self,
        gate_id: str,
        rejector_id: str,
        reason: Optional[str] = None
    ) -> bool:
        """
        Reject a decision gate
        
        Args:
            gate_id: Gate identifier
            rejector_id: Rejector identifier
            reason: Rejection reason
            
        Returns:
            True if rejection successful
        """
        gate = self.get_gate(gate_id)
        if not gate:
            logger.error(f"Gate {gate_id} not found")
            return False
        
        return gate.reject(rejector_id, reason)
    
    def cancel_gate(
        self,
        gate_id: str,
        reason: Optional[str] = None
    ) -> bool:
        """Cancel a gate"""
        gate = self.get_gate(gate_id)
        if not gate:
            return False
        
        return gate.cancel(reason)
    
    def get_all_gates(self) -> List[DecisionGate]:
        """Get all gates"""
        return list(self.gates.values())
    
    def get_pending_gates(self) -> List[DecisionGate]:
        """Get all pending gates"""
        return [
            gate for gate in self.gates.values()
            if gate.is_pending()
        ]
    
    def get_approved_gates(self) -> List[DecisionGate]:
        """Get all approved gates"""
        return [
            gate for gate in self.gates.values()
            if gate.is_approved()
        ]
    
    def get_rejected_gates(self) -> List[DecisionGate]:
        """Get all rejected gates"""
        return [
            gate for gate in self.gates.values()
            if gate.is_rejected()
        ]
    
    def get_locked_outputs(self) -> List[DecisionGate]:
        """Get all gates with locked outputs"""
        return [
            gate for gate in self.gates.values()
            if gate.is_output_locked()
        ]
    
    def get_gates_by_type(self, gate_type: GateType) -> List[DecisionGate]:
        """Get all gates of a specific type"""
        return [
            gate for gate in self.gates.values()
            if gate.gate_type == gate_type
        ]
    
    def cleanup_expired_gates(self) -> int:
        """
        Check all gates for expiry and update status
        
        Returns:
            Number of gates that were marked as expired
        """
        expired_count = 0
        for gate in self.gates.values():
            if gate.check_expiry():
                expired_count += 1
        
        if expired_count > 0:
            logger.info(f"Marked {expired_count} gates as expired")
        
        return expired_count
    
    def get_manager_stats(self) -> Dict[str, Any]:
        """Get manager statistics"""
        self.cleanup_expired_gates()  # Update expiry status first
        
        status_counts = {}
        for status in GateStatus:
            count = len([
                g for g in self.gates.values()
                if g.status == status
            ])
            status_counts[status.value] = count
        
        type_counts = {}
        for gate_type in GateType:
            count = len(self.get_gates_by_type(gate_type))
            type_counts[gate_type.value] = count
        
        return {
            'total_gates': len(self.gates),
            'pending_gates': len(self.get_pending_gates()),
            'approved_gates': len(self.get_approved_gates()),
            'rejected_gates': len(self.get_rejected_gates()),
            'locked_outputs': len(self.get_locked_outputs()),
            'status_breakdown': status_counts,
            'type_breakdown': type_counts,
            'created_at': self.created_at,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def check_gate_approval(self, gate_id: str) -> bool:
        """
        Check if a gate is approved (for use in flow control)
        
        Args:
            gate_id: Gate identifier
            
        Returns:
            True if gate is approved, False otherwise
        """
        gate = self.get_gate(gate_id)
        if not gate:
            return False
        
        return gate.is_approved()
    
    def wait_for_approval(
        self,
        gate_id: str,
        raise_on_reject: bool = True
    ) -> bool:
        """
        Wait for gate approval (blocking operation in real implementation)
        This is a placeholder - in production would implement actual waiting
        
        Args:
            gate_id: Gate to wait for
            raise_on_reject: Raise exception if rejected
            
        Returns:
            True if approved
            
        Raises:
            RuntimeError: If gate rejected and raise_on_reject is True
        """
        gate = self.get_gate(gate_id)
        if not gate:
            raise ValueError(f"Gate {gate_id} not found")
        
        # In real implementation, this would poll or use event-based waiting
        # For now, just check current status
        
        if gate.is_approved():
            return True
        
        if gate.is_rejected() and raise_on_reject:
            raise RuntimeError(
                f"Gate {gate_id} was rejected: {gate.resolution_note}"
            )
        
        return False
    
    def delete_gate(self, gate_id: str) -> bool:
        """Delete a gate from the system"""
        if gate_id in self.gates:
            del self.gates[gate_id]
            logger.info(f"Deleted gate {gate_id}")
            return True
        return False
