"""
Decision Engine - Final decision arbiter with human approval gate.

This module makes final decisions on actions and enforces human-in-the-loop
approval for critical operations.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import logging
import hashlib
import json

logger = logging.getLogger(__name__)


class ActionCriticality(Enum):
    """Action criticality levels."""
    LOW = "low"  # Auto-approve
    MEDIUM = "medium"  # Recommend but auto-approve
    HIGH = "high"  # Require approval
    CRITICAL = "critical"  # Require approval + confirmation


class Decision:
    """Represents a decision made by the engine."""
    
    def __init__(
        self,
        action_id: str,
        action_type: str,
        description: str,
        criticality: ActionCriticality,
        proposed_actions: List[Dict[str, Any]],
        estimated_cost: float = 0.0,
        estimated_duration: int = 0
    ):
        self.action_id = action_id
        self.action_type = action_type
        self.description = description
        self.criticality = criticality
        self.proposed_actions = proposed_actions
        self.estimated_cost = estimated_cost
        self.estimated_duration = estimated_duration
        self.status = "pending_approval"
        self.created_at = datetime.utcnow()
        self.approved_at: Optional[datetime] = None
        self.executed_at: Optional[datetime] = None
        self.result: Optional[Dict[str, Any]] = None


class DecisionEngine:
    """
    Makes final decisions on actions and enforces human approval gates.
    
    Features:
    - Criticality assessment
    - Human-in-the-loop for critical actions
    - Decision logging and audit trail
    - Cost/benefit analysis
    """
    
    def __init__(self, db_connection=None):
        self.pending_decisions: Dict[str, Decision] = {}
        self.decision_history: List[Decision] = []
        self.db = db_connection
        
        # Criticality rules
        self.criticality_rules = {
            "data_deletion": ActionCriticality.CRITICAL,
            "external_api_call": ActionCriticality.HIGH,
            "code_execution": ActionCriticality.HIGH,
            "file_modification": ActionCriticality.MEDIUM,
            "data_query": ActionCriticality.LOW,
            "cache_operation": ActionCriticality.LOW,
        }
    
    def analyze_request(
        self,
        user_input: str,
        intent: Dict[str, Any],
        proposed_actions: List[Dict[str, Any]]
    ) -> Decision:
        """
        Analyze a request and create a decision.
        
        Args:
            user_input: Original user request
            intent: Parsed intent from user input
            proposed_actions: Actions proposed by agent swarm
            
        Returns:
            Decision object with approval requirements
        """
        # Generate unique action ID
        action_id = self._generate_action_id(user_input, proposed_actions)
        
        # Determine criticality
        criticality = self._assess_criticality(proposed_actions)
        
        # Estimate cost and duration
        cost = self._estimate_cost(proposed_actions)
        duration = self._estimate_duration(proposed_actions)
        
        # Create decision
        decision = Decision(
            action_id=action_id,
            action_type=intent.get("type", "unknown"),
            description=self._generate_description(intent, proposed_actions),
            criticality=criticality,
            proposed_actions=proposed_actions,
            estimated_cost=cost,
            estimated_duration=duration
        )
        
        # Store pending decision
        self.pending_decisions[action_id] = decision
        
        # Auto-approve low criticality
        if criticality == ActionCriticality.LOW:
            decision.status = "auto_approved"
            decision.approved_at = datetime.utcnow()
            logger.info(f"Auto-approved low criticality action: {action_id}")
        
        return decision
    
    def approve_decision(self, action_id: str, user_confirmation: bool = True) -> bool:
        """
        Approve a pending decision.
        
        Args:
            action_id: ID of the decision to approve
            user_confirmation: User's approval
            
        Returns:
            True if approved, False otherwise
        """
        if action_id not in self.pending_decisions:
            logger.error(f"Decision not found: {action_id}")
            return False
        
        decision = self.pending_decisions[action_id]
        
        if not user_confirmation:
            decision.status = "rejected"
            logger.info(f"Decision rejected by user: {action_id}")
            return False
        
        decision.status = "approved"
        decision.approved_at = datetime.utcnow()
        logger.info(f"Decision approved: {action_id}")
        
        return True
    
    def execute_decision(self, action_id: str) -> Dict[str, Any]:
        """
        Execute an approved decision.
        
        Args:
            action_id: ID of the decision to execute
            
        Returns:
            Execution result
        """
        if action_id not in self.pending_decisions:
            return {"success": False, "error": "Decision not found"}
        
        decision = self.pending_decisions[action_id]
        
        if decision.status not in ["approved", "auto_approved"]:
            return {"success": False, "error": "Decision not approved"}
        
        # Mark as executing
        decision.status = "executing"
        decision.executed_at = datetime.utcnow()
        
        # This would trigger actual execution via agent ecosystem
        result = {
            "success": True,
            "action_id": action_id,
            "started_at": decision.executed_at.isoformat(),
            "message": "Execution delegated to agent ecosystem"
        }
        
        decision.result = result
        decision.status = "completed"
        
        # Move to history
        self.decision_history.append(decision)
        del self.pending_decisions[action_id]
        
        return result
    
    def _generate_action_id(self, user_input: str, actions: List[Dict[str, Any]]) -> str:
        """Generate unique action ID."""
        content = f"{user_input}{json.dumps(actions)}{datetime.utcnow().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _assess_criticality(self, actions: List[Dict[str, Any]]) -> ActionCriticality:
        """Assess overall criticality of proposed actions."""
        max_criticality = ActionCriticality.LOW
        
        for action in actions:
            action_type = action.get("type", "unknown")
            criticality = self.criticality_rules.get(action_type, ActionCriticality.MEDIUM)
            
            # Take highest criticality
            if criticality.value == "critical":
                return ActionCriticality.CRITICAL
            elif criticality.value == "high" and max_criticality.value != "critical":
                max_criticality = ActionCriticality.HIGH
            elif criticality.value == "medium" and max_criticality.value == "low":
                max_criticality = ActionCriticality.MEDIUM
        
        return max_criticality
    
    def _estimate_cost(self, actions: List[Dict[str, Any]]) -> float:
        """Estimate cost of actions in USD."""
        total_cost = 0.0
        
        # Cost estimates per action type
        cost_map = {
            "api_call": 0.01,
            "image_generation": 0.04,
            "video_generation": 0.30,
            "llm_inference": 0.002,
            "data_processing": 0.001,
        }
        
        for action in actions:
            action_type = action.get("type", "unknown")
            total_cost += cost_map.get(action_type, 0.0)
        
        return round(total_cost, 4)
    
    def _estimate_duration(self, actions: List[Dict[str, Any]]) -> int:
        """Estimate duration in seconds."""
        total_duration = 0
        
        # Duration estimates per action type
        duration_map = {
            "api_call": 2,
            "image_generation": 5,
            "video_generation": 30,
            "llm_inference": 1,
            "data_processing": 3,
        }
        
        for action in actions:
            action_type = action.get("type", "unknown")
            total_duration += duration_map.get(action_type, 1)
        
        return total_duration
    
    def _generate_description(
        self,
        intent: Dict[str, Any],
        actions: List[Dict[str, Any]]
    ) -> str:
        """Generate human-readable description of proposed actions."""
        action_descriptions = []
        
        for action in actions:
            action_type = action.get("type", "unknown")
            params = action.get("parameters", {})
            
            if action_type == "image_generation":
                action_descriptions.append(f"Generate image: {params.get('prompt', 'N/A')}")
            elif action_type == "api_call":
                action_descriptions.append(f"Call API: {params.get('endpoint', 'N/A')}")
            elif action_type == "data_query":
                action_descriptions.append(f"Query data: {params.get('query', 'N/A')}")
            else:
                action_descriptions.append(f"{action_type}")
        
        return "\n".join([f"{i+1}. {desc}" for i, desc in enumerate(action_descriptions)])
    
    def get_pending_decisions(self) -> List[Dict[str, Any]]:
        """Get all pending decisions requiring approval."""
        return [
            {
                "action_id": d.action_id,
                "description": d.description,
                "criticality": d.criticality.value,
                "estimated_cost": d.estimated_cost,
                "estimated_duration": d.estimated_duration,
                "created_at": d.created_at.isoformat()
            }
            for d in self.pending_decisions.values()
            if d.status == "pending_approval"
        ]
    
    def get_decision_stats(self) -> Dict[str, Any]:
        """Get decision engine statistics."""
        return {
            "pending_decisions": len(self.pending_decisions),
            "total_decisions": len(self.decision_history),
            "auto_approved": sum(1 for d in self.decision_history if d.status == "auto_approved"),
            "user_approved": sum(1 for d in self.decision_history if d.status == "approved"),
            "rejected": sum(1 for d in self.decision_history if d.status == "rejected"),
        }
