"""
Decision Gate - Strict YES/NO Confirmation System

This module provides a robust confirmation system for all critical actions,
ensuring explicit user approval before execution.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from uuid import uuid4
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class DecisionType(Enum):
    """Types of decisions requiring confirmation"""
    CRITICAL = "critical"      # Requires confirmation, cannot be auto-approved
    HIGH = "high"             # Requires confirmation, can be auto-approved with rules
    NORMAL = "normal"         # Can be auto-approved
    INFO = "info"             # Informational, no confirmation needed


class DecisionStatus(Enum):
    """Status of a decision"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    EXECUTED = "executed"


@dataclass
class Decision:
    """
    Represents a single decision requiring confirmation.
    
    Each decision tracks:
    - Unique ID and metadata
    - Action description and context
    - Confirmation status
    - Execution results
    """
    decision_id: str = field(default_factory=lambda: str(uuid4()))
    action_type: str = ""
    description: str = ""
    decision_type: DecisionType = DecisionType.NORMAL
    context: Dict[str, Any] = field(default_factory=dict)
    status: DecisionStatus = DecisionStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    responded_at: Optional[str] = None
    executed_at: Optional[str] = None
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None
    execution_result: Optional[Dict[str, Any]] = None
    
    def approve(self, approved_by: str = "user"):
        """Approve the decision"""
        if self.status != DecisionStatus.PENDING:
            raise ValueError(f"Cannot approve decision in status: {self.status.value}")
        
        self.status = DecisionStatus.APPROVED
        self.approved_by = approved_by
        self.responded_at = datetime.utcnow().isoformat()
        logger.info(f"Decision {self.decision_id} approved by {approved_by}")
    
    def reject(self, reason: str = "User rejected", rejected_by: str = "user"):
        """Reject the decision"""
        if self.status != DecisionStatus.PENDING:
            raise ValueError(f"Cannot reject decision in status: {self.status.value}")
        
        self.status = DecisionStatus.REJECTED
        self.rejection_reason = reason
        self.responded_at = datetime.utcnow().isoformat()
        logger.info(f"Decision {self.decision_id} rejected: {reason}")
    
    def mark_executed(self, result: Dict[str, Any]):
        """Mark decision as executed with result"""
        if self.status != DecisionStatus.APPROVED:
            raise ValueError(f"Cannot execute decision in status: {self.status.value}")
        
        self.status = DecisionStatus.EXECUTED
        self.execution_result = result
        self.executed_at = datetime.utcnow().isoformat()
        logger.info(f"Decision {self.decision_id} executed")
    
    def expire(self):
        """Mark decision as expired"""
        if self.status == DecisionStatus.PENDING:
            self.status = DecisionStatus.EXPIRED
            self.responded_at = datetime.utcnow().isoformat()
            logger.info(f"Decision {self.decision_id} expired")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "decision_id": self.decision_id,
            "action_type": self.action_type,
            "description": self.description,
            "decision_type": self.decision_type.value,
            "context": self.context,
            "status": self.status.value,
            "created_at": self.created_at,
            "responded_at": self.responded_at,
            "executed_at": self.executed_at,
            "approved_by": self.approved_by,
            "rejection_reason": self.rejection_reason,
            "execution_result": self.execution_result
        }


class DecisionGate:
    """
    Central gate for all critical decisions.
    
    Provides:
    - Strict YES/NO confirmation for critical actions
    - Audit trail of all decisions
    - Auto-approval rules (configurable)
    - Decision expiration and cleanup
    """
    
    def __init__(self, enable_auto_approval: bool = False):
        self.decisions: Dict[str, Decision] = {}
        self.enable_auto_approval = enable_auto_approval
        self.auto_approval_rules: Dict[str, Callable[[Decision], bool]] = {}
        self.audit_log: List[Dict[str, Any]] = []
        logger.info(f"DecisionGate initialized (auto-approval: {enable_auto_approval})")
    
    def request_decision(
        self,
        action_type: str,
        description: str,
        decision_type: DecisionType = DecisionType.NORMAL,
        context: Optional[Dict[str, Any]] = None
    ) -> Decision:
        """
        Request a decision for an action.
        
        Args:
            action_type: Type of action (e.g., "deploy", "delete", "spend")
            description: Human-readable description of the action
            decision_type: Criticality level of the decision
            context: Additional context for the decision
        
        Returns:
            Decision object with unique ID
        """
        decision = Decision(
            action_type=action_type,
            description=description,
            decision_type=decision_type,
            context=context or {}
        )
        
        self.decisions[decision.decision_id] = decision
        self._log_audit("decision_requested", decision)
        
        # Check if auto-approval is possible
        if self._can_auto_approve(decision):
            decision.approve(approved_by="auto-approval")
            self._log_audit("decision_auto_approved", decision)
        
        logger.info(
            f"Decision requested: {action_type} - {description} "
            f"(ID: {decision.decision_id}, Type: {decision_type.value})"
        )
        
        return decision
    
    def get_decision(self, decision_id: str) -> Optional[Decision]:
        """Get a decision by ID"""
        return self.decisions.get(decision_id)
    
    def approve_decision(
        self,
        decision_id: str,
        approved_by: str = "user"
    ) -> bool:
        """
        Approve a pending decision.
        
        Args:
            decision_id: ID of the decision to approve
            approved_by: Identifier of who approved it
        
        Returns:
            True if approved successfully, False otherwise
        """
        decision = self.get_decision(decision_id)
        if not decision:
            logger.warning(f"Decision not found: {decision_id}")
            return False
        
        try:
            decision.approve(approved_by)
            self._log_audit("decision_approved", decision)
            return True
        except ValueError as e:
            logger.error(f"Failed to approve decision {decision_id}: {e}")
            return False
    
    def reject_decision(
        self,
        decision_id: str,
        reason: str = "User rejected",
        rejected_by: str = "user"
    ) -> bool:
        """
        Reject a pending decision.
        
        Args:
            decision_id: ID of the decision to reject
            reason: Reason for rejection
            rejected_by: Identifier of who rejected it
        
        Returns:
            True if rejected successfully, False otherwise
        """
        decision = self.get_decision(decision_id)
        if not decision:
            logger.warning(f"Decision not found: {decision_id}")
            return False
        
        try:
            decision.reject(reason, rejected_by)
            self._log_audit("decision_rejected", decision)
            return True
        except ValueError as e:
            logger.error(f"Failed to reject decision {decision_id}: {e}")
            return False
    
    def execute_decision(
        self,
        decision_id: str,
        executor_func: Callable[[Decision], Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Execute an approved decision.
        
        Args:
            decision_id: ID of the decision to execute
            executor_func: Function that executes the action
        
        Returns:
            Execution result or None if execution failed
        """
        decision = self.get_decision(decision_id)
        if not decision:
            logger.warning(f"Decision not found: {decision_id}")
            return None
        
        if decision.status != DecisionStatus.APPROVED:
            logger.warning(
                f"Cannot execute decision {decision_id} - "
                f"status is {decision.status.value}"
            )
            return None
        
        try:
            # Execute the action
            result = executor_func(decision)
            decision.mark_executed(result)
            self._log_audit("decision_executed", decision)
            return result
        except Exception as e:
            logger.error(f"Error executing decision {decision_id}: {e}")
            result = {"success": False, "error": str(e)}
            decision.mark_executed(result)
            self._log_audit("decision_execution_failed", decision)
            return result
    
    def list_pending_decisions(self) -> List[Decision]:
        """Get all pending decisions"""
        return [
            d for d in self.decisions.values()
            if d.status == DecisionStatus.PENDING
        ]
    
    def list_decisions_by_status(self, status: DecisionStatus) -> List[Decision]:
        """Get all decisions with a specific status"""
        return [
            d for d in self.decisions.values()
            if d.status == status
        ]
    
    def add_auto_approval_rule(
        self,
        rule_name: str,
        rule_func: Callable[[Decision], bool]
    ):
        """
        Add an auto-approval rule.
        
        Args:
            rule_name: Name of the rule
            rule_func: Function that returns True if decision can be auto-approved
        """
        self.auto_approval_rules[rule_name] = rule_func
        logger.info(f"Added auto-approval rule: {rule_name}")
    
    def remove_auto_approval_rule(self, rule_name: str) -> bool:
        """Remove an auto-approval rule"""
        if rule_name in self.auto_approval_rules:
            del self.auto_approval_rules[rule_name]
            logger.info(f"Removed auto-approval rule: {rule_name}")
            return True
        return False
    
    def _can_auto_approve(self, decision: Decision) -> bool:
        """Check if a decision can be auto-approved"""
        # CRITICAL decisions cannot be auto-approved
        if decision.decision_type == DecisionType.CRITICAL:
            return False
        
        # INFO decisions are always auto-approved
        if decision.decision_type == DecisionType.INFO:
            return True
        
        # Check if auto-approval is enabled
        if not self.enable_auto_approval:
            return False
        
        # HIGH and NORMAL decisions check rules
        for rule_name, rule_func in self.auto_approval_rules.items():
            try:
                if rule_func(decision):
                    logger.info(
                        f"Decision {decision.decision_id} auto-approved by rule: {rule_name}"
                    )
                    return True
            except Exception as e:
                logger.error(f"Error in auto-approval rule {rule_name}: {e}")
        
        return False
    
    def expire_old_decisions(self, max_age_hours: int = 24):
        """Expire pending decisions older than specified hours"""
        cutoff_time = datetime.utcnow().timestamp() - (max_age_hours * 3600)
        expired_count = 0
        
        for decision in self.decisions.values():
            if decision.status == DecisionStatus.PENDING:
                created_timestamp = datetime.fromisoformat(
                    decision.created_at
                ).timestamp()
                
                if created_timestamp < cutoff_time:
                    decision.expire()
                    self._log_audit("decision_expired", decision)
                    expired_count += 1
        
        if expired_count > 0:
            logger.info(f"Expired {expired_count} old decisions")
    
    def _log_audit(self, event_type: str, decision: Decision):
        """Log an audit event"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "decision_id": decision.decision_id,
            "action_type": decision.action_type,
            "status": decision.status.value
        }
        self.audit_log.append(audit_entry)
    
    def get_audit_log(
        self,
        decision_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get audit log entries.
        
        Args:
            decision_id: Filter by decision ID (optional)
            limit: Maximum number of entries to return (optional)
        
        Returns:
            List of audit log entries
        """
        logs = self.audit_log
        
        if decision_id:
            logs = [log for log in logs if log["decision_id"] == decision_id]
        
        if limit:
            logs = logs[-limit:]
        
        return logs
    
    def save_state(self, filepath: str):
        """Save all decisions and audit log to a JSON file"""
        state = {
            "decisions": {
                decision_id: decision.to_dict()
                for decision_id, decision in self.decisions.items()
            },
            "audit_log": self.audit_log,
            "enable_auto_approval": self.enable_auto_approval
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Saved DecisionGate state to {filepath}")
    
    def load_state(self, filepath: str):
        """Load decisions and audit log from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
            
            self.enable_auto_approval = state.get("enable_auto_approval", False)
            self.audit_log = state.get("audit_log", [])
            self.decisions.clear()
            
            for decision_id, decision_data in state.get("decisions", {}).items():
                decision = Decision(
                    decision_id=decision_id,
                    action_type=decision_data["action_type"],
                    description=decision_data["description"],
                    decision_type=DecisionType(decision_data["decision_type"]),
                    context=decision_data.get("context", {}),
                    status=DecisionStatus(decision_data["status"])
                )
                decision.created_at = decision_data["created_at"]
                decision.responded_at = decision_data.get("responded_at")
                decision.executed_at = decision_data.get("executed_at")
                decision.approved_by = decision_data.get("approved_by")
                decision.rejection_reason = decision_data.get("rejection_reason")
                decision.execution_result = decision_data.get("execution_result")
                
                self.decisions[decision_id] = decision
            
            logger.info(f"Loaded DecisionGate state from {filepath}")
            logger.info(f"Loaded {len(self.decisions)} decisions")
        
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            raise
