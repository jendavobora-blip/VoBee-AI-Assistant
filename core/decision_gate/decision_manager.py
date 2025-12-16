"""
Decision Manager - Manages critical decisions requiring human confirmation.

Implements explicit confirmation workflow for:
- Code deployments
- Database migrations
- Budget changes
- System configuration updates
- Main branch merges
"""

import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from enum import Enum
from pathlib import Path


class DecisionType(Enum):
    """Types of decisions requiring confirmation."""
    DEPLOYMENT = "deployment"
    DATABASE_MIGRATION = "database_migration"
    BUDGET_CHANGE = "budget_change"
    CONFIG_UPDATE = "config_update"
    BRANCH_MERGE = "branch_merge"
    RESOURCE_ALLOCATION = "resource_allocation"
    API_INTEGRATION = "api_integration"
    DATA_DELETION = "data_deletion"


class DecisionStatus(Enum):
    """Status of a decision."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    EXECUTED = "executed"


class DecisionManager:
    """
    Manages decision workflow with explicit human confirmation.
    
    Features:
    - Pending decision queue
    - Approval/rejection tracking
    - Automatic expiration
    - Execution logging
    - Audit trail
    """
    
    def __init__(
        self,
        storage_path: str = "data/decisions",
        default_expiry_hours: int = 24
    ):
        """
        Initialize Decision Manager.
        
        Args:
            storage_path: Directory for decision storage
            default_expiry_hours: Default expiration time for pending decisions
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.decisions: Dict[str, dict] = {}
        self.default_expiry_hours = default_expiry_hours
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Load existing decisions
        self._load_decisions()
        
        # Clean up expired decisions
        self._expire_old_decisions()
        
        self.logger.info(
            f"DecisionManager initialized with {len(self.decisions)} decisions"
        )
    
    def request_decision(
        self,
        decision_type: DecisionType,
        title: str,
        description: str,
        proposed_action: Dict,
        risk_level: str = "medium",
        expiry_hours: Optional[int] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Request a decision that requires human confirmation.
        
        Args:
            decision_type: Type of decision
            title: Short title for the decision
            description: Detailed description of what will happen
            proposed_action: Action details (to be executed if approved)
            risk_level: 'low', 'medium', 'high', 'critical'
            expiry_hours: Hours until decision expires (uses default if None)
            metadata: Additional metadata
            
        Returns:
            Decision ID
        """
        decision_id = str(uuid.uuid4())
        
        expiry_time = datetime.utcnow() + timedelta(
            hours=expiry_hours or self.default_expiry_hours
        )
        
        decision = {
            "id": decision_id,
            "type": decision_type.value,
            "status": DecisionStatus.PENDING.value,
            "title": title,
            "description": description,
            "proposed_action": proposed_action,
            "risk_level": risk_level,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expiry_time.isoformat(),
            "approved_at": None,
            "approved_by": None,
            "executed_at": None,
            "execution_result": None,
            "metadata": metadata or {}
        }
        
        self.decisions[decision_id] = decision
        self._save_decision(decision_id)
        
        self.logger.info(
            f"Decision requested: {decision_id} - {title} "
            f"(type: {decision_type.value}, risk: {risk_level})"
        )
        
        # TODO: Integrate with notification system for high/critical risk decisions
        
        return decision_id
    
    def approve_decision(
        self,
        decision_id: str,
        approved_by: str,
        notes: Optional[str] = None
    ) -> dict:
        """
        Approve a pending decision.
        
        Args:
            decision_id: Decision to approve
            approved_by: Identifier of approver
            notes: Optional approval notes
            
        Returns:
            Updated decision
        """
        if decision_id not in self.decisions:
            raise ValueError(f"Decision '{decision_id}' not found")
        
        decision = self.decisions[decision_id]
        
        if decision["status"] != DecisionStatus.PENDING.value:
            raise ValueError(
                f"Cannot approve decision in status: {decision['status']}"
            )
        
        # Check if expired
        if self._is_expired(decision):
            decision["status"] = DecisionStatus.EXPIRED.value
            self._save_decision(decision_id)
            raise ValueError("Decision has expired")
        
        decision["status"] = DecisionStatus.APPROVED.value
        decision["approved_at"] = datetime.utcnow().isoformat()
        decision["approved_by"] = approved_by
        
        if notes:
            decision["metadata"]["approval_notes"] = notes
        
        self._save_decision(decision_id)
        
        self.logger.info(
            f"Decision approved: {decision_id} by {approved_by}"
        )
        
        return decision
    
    def reject_decision(
        self,
        decision_id: str,
        rejected_by: str,
        reason: Optional[str] = None
    ) -> dict:
        """
        Reject a pending decision.
        
        Args:
            decision_id: Decision to reject
            rejected_by: Identifier of rejecter
            reason: Optional rejection reason
            
        Returns:
            Updated decision
        """
        if decision_id not in self.decisions:
            raise ValueError(f"Decision '{decision_id}' not found")
        
        decision = self.decisions[decision_id]
        
        if decision["status"] != DecisionStatus.PENDING.value:
            raise ValueError(
                f"Cannot reject decision in status: {decision['status']}"
            )
        
        decision["status"] = DecisionStatus.REJECTED.value
        decision["rejected_at"] = datetime.utcnow().isoformat()
        decision["rejected_by"] = rejected_by
        
        if reason:
            decision["metadata"]["rejection_reason"] = reason
        
        self._save_decision(decision_id)
        
        self.logger.info(
            f"Decision rejected: {decision_id} by {rejected_by}"
        )
        
        return decision
    
    def execute_decision(
        self,
        decision_id: str,
        executor_func: Callable,
        executor_id: str
    ) -> dict:
        """
        Execute an approved decision.
        
        Args:
            decision_id: Decision to execute
            executor_func: Function to execute the action
            executor_id: Identifier of executor
            
        Returns:
            Updated decision with execution result
        """
        if decision_id not in self.decisions:
            raise ValueError(f"Decision '{decision_id}' not found")
        
        decision = self.decisions[decision_id]
        
        if decision["status"] != DecisionStatus.APPROVED.value:
            raise ValueError(
                f"Can only execute approved decisions. "
                f"Current status: {decision['status']}"
            )
        
        self.logger.info(f"Executing decision: {decision_id}")
        
        try:
            # Execute the action
            result = executor_func(decision["proposed_action"])
            
            decision["status"] = DecisionStatus.EXECUTED.value
            decision["executed_at"] = datetime.utcnow().isoformat()
            decision["executed_by"] = executor_id
            decision["execution_result"] = {
                "success": True,
                "result": result
            }
            
            self.logger.info(f"Decision executed successfully: {decision_id}")
            
        except Exception as e:
            decision["execution_result"] = {
                "success": False,
                "error": str(e)
            }
            
            self.logger.error(
                f"Decision execution failed: {decision_id} - {str(e)}"
            )
        
        self._save_decision(decision_id)
        
        return decision
    
    def get_decision(self, decision_id: str) -> Optional[dict]:
        """Get decision by ID."""
        return self.decisions.get(decision_id)
    
    def list_pending_decisions(self, risk_level: Optional[str] = None) -> List[dict]:
        """
        List all pending decisions.
        
        Args:
            risk_level: Optional filter by risk level
            
        Returns:
            List of pending decisions
        """
        pending = [
            d for d in self.decisions.values()
            if d["status"] == DecisionStatus.PENDING.value
            and not self._is_expired(d)
        ]
        
        if risk_level:
            pending = [d for d in pending if d["risk_level"] == risk_level]
        
        return sorted(pending, key=lambda d: d["created_at"])
    
    def get_decision_history(
        self,
        decision_type: Optional[DecisionType] = None,
        status: Optional[DecisionStatus] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        """
        Get decision history with optional filters.
        
        Args:
            decision_type: Filter by decision type
            status: Filter by status
            limit: Maximum number to return
            
        Returns:
            List of decisions
        """
        history = list(self.decisions.values())
        
        if decision_type:
            history = [d for d in history if d["type"] == decision_type.value]
        
        if status:
            history = [d for d in history if d["status"] == status.value]
        
        history = sorted(history, key=lambda d: d["created_at"], reverse=True)
        
        if limit:
            history = history[:limit]
        
        return history
    
    def _is_expired(self, decision: dict) -> bool:
        """Check if a decision has expired."""
        if decision["status"] != DecisionStatus.PENDING.value:
            return False
        
        expires_at = datetime.fromisoformat(decision["expires_at"])
        return datetime.utcnow() > expires_at
    
    def _expire_old_decisions(self):
        """Mark expired pending decisions as expired."""
        for decision_id, decision in self.decisions.items():
            if self._is_expired(decision):
                decision["status"] = DecisionStatus.EXPIRED.value
                self._save_decision(decision_id)
                
                self.logger.info(f"Decision expired: {decision_id}")
    
    def _save_decision(self, decision_id: str):
        """Save decision to disk."""
        decision = self.decisions[decision_id]
        decision_file = self.storage_path / f"{decision_id}.json"
        
        with open(decision_file, 'w') as f:
            json.dump(decision, f, indent=2)
    
    def _load_decisions(self):
        """Load all decisions from disk."""
        if not self.storage_path.exists():
            return
        
        for decision_file in self.storage_path.glob("*.json"):
            try:
                with open(decision_file, 'r') as f:
                    decision = json.load(f)
                    self.decisions[decision["id"]] = decision
            except Exception as e:
                self.logger.error(
                    f"Failed to load decision from {decision_file}: {e}"
                )
