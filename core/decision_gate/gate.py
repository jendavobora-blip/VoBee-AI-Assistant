"""
Decision Gate - Control system for critical actions.

Implements a confirmation system with YES/NO gates and modular rules
for controlling critical operations in the AI system.
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import uuid


class GateDecision(Enum):
    """Gate decision outcomes."""
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"
    BYPASSED = "bypassed"


class GateRulePriority(Enum):
    """Rule evaluation priority levels."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class GateRule:
    """
    Represents a modular rule for decision evaluation.
    
    Rules can be chained and combined to create complex decision logic.
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        priority: GateRulePriority = GateRulePriority.MEDIUM,
        rule_id: Optional[str] = None
    ):
        """
        Initialize a gate rule.
        
        Args:
            name: Rule name
            description: Rule description
            priority: Rule priority for evaluation order
            rule_id: Unique identifier (auto-generated if not provided)
        """
        self.id = rule_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.priority = priority
        self.enabled = True
        self.created_at = datetime.now()
        
        # Rule evaluation function (to be overridden or set)
        self._evaluation_func: Optional[Callable] = None
    
    def set_evaluation_function(self, func: Callable[[Dict[str, Any]], bool]) -> None:
        """
        Set the evaluation function for this rule.
        
        Args:
            func: Function that takes context and returns bool (True = approve, False = reject)
        """
        self._evaluation_func = func
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """
        Evaluate the rule against given context.
        
        Args:
            context: Context data for evaluation
            
        Returns:
            True if rule approves, False if rejects
        """
        if not self.enabled:
            return True  # Disabled rules don't block
        
        if self._evaluation_func is None:
            return True  # No evaluation function means auto-approve
        
        try:
            return self._evaluation_func(context)
        except Exception as e:
            # Log error and fail-safe to rejection for safety
            print(f"Rule {self.name} evaluation error: {e}")
            return False
    
    def enable(self) -> None:
        """Enable this rule."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable this rule."""
        self.enabled = False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert rule to dictionary representation.
        
        Returns:
            Dictionary with rule data
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority.value,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat()
        }


class DecisionRequest:
    """Represents a request for decision approval."""
    
    def __init__(
        self,
        action: str,
        description: str = "",
        context: Optional[Dict[str, Any]] = None,
        requires_confirmation: bool = True,
        request_id: Optional[str] = None
    ):
        """
        Initialize a decision request.
        
        Args:
            action: Action requiring approval
            description: Detailed description
            context: Additional context data
            requires_confirmation: Whether confirmation is required
            request_id: Unique identifier
        """
        self.id = request_id or str(uuid.uuid4())
        self.action = action
        self.description = description
        self.context = context or {}
        self.requires_confirmation = requires_confirmation
        self.decision = GateDecision.PENDING
        self.created_at = datetime.now()
        self.decided_at: Optional[datetime] = None
        self.decision_reason: Optional[str] = None
        self.evaluated_rules: List[Dict[str, Any]] = []
    
    def approve(self, reason: str = "") -> None:
        """
        Approve the request.
        
        Args:
            reason: Approval reason
        """
        self.decision = GateDecision.APPROVED
        self.decided_at = datetime.now()
        self.decision_reason = reason
    
    def reject(self, reason: str = "") -> None:
        """
        Reject the request.
        
        Args:
            reason: Rejection reason
        """
        self.decision = GateDecision.REJECTED
        self.decided_at = datetime.now()
        self.decision_reason = reason
    
    def bypass(self, reason: str = "") -> None:
        """
        Bypass the gate (auto-approve without evaluation).
        
        Args:
            reason: Bypass reason
        """
        self.decision = GateDecision.BYPASSED
        self.decided_at = datetime.now()
        self.decision_reason = reason
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert request to dictionary representation.
        
        Returns:
            Dictionary with request data
        """
        return {
            'id': self.id,
            'action': self.action,
            'description': self.description,
            'context': self.context,
            'decision': self.decision.value,
            'decision_reason': self.decision_reason,
            'created_at': self.created_at.isoformat(),
            'decided_at': self.decided_at.isoformat() if self.decided_at else None,
            'evaluated_rules': self.evaluated_rules
        }


class DecisionGate:
    """
    Central decision control system.
    
    Manages approval workflow for critical actions using modular rules.
    Provides YES/NO confirmation gates with extensible rule engine.
    """
    
    def __init__(self, auto_approve_mode: bool = False):
        """
        Initialize the Decision Gate.
        
        Args:
            auto_approve_mode: If True, automatically approve all requests (for testing)
        """
        self.rules: Dict[str, GateRule] = {}
        self.requests: Dict[str, DecisionRequest] = {}
        self.auto_approve_mode = auto_approve_mode
        self.created_at = datetime.now()
    
    def add_rule(self, rule: GateRule) -> None:
        """
        Add a rule to the gate.
        
        Args:
            rule: Gate rule to add
        """
        self.rules[rule.id] = rule
    
    def remove_rule(self, rule_id: str) -> bool:
        """
        Remove a rule from the gate.
        
        Args:
            rule_id: Rule identifier
            
        Returns:
            True if removed, False if not found
        """
        if rule_id in self.rules:
            del self.rules[rule_id]
            return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[GateRule]:
        """
        Get a specific rule.
        
        Args:
            rule_id: Rule identifier
            
        Returns:
            Rule or None if not found
        """
        return self.rules.get(rule_id)
    
    def list_rules(self, enabled_only: bool = False) -> List[GateRule]:
        """
        List all rules.
        
        Args:
            enabled_only: Only return enabled rules
            
        Returns:
            List of rules
        """
        rules = list(self.rules.values())
        if enabled_only:
            rules = [r for r in rules if r.enabled]
        # Sort by priority
        return sorted(rules, key=lambda r: r.priority.value)
    
    def request_approval(
        self,
        action: str,
        description: str = "",
        context: Optional[Dict[str, Any]] = None,
        requires_confirmation: bool = True
    ) -> DecisionRequest:
        """
        Request approval for an action.
        
        Args:
            action: Action requiring approval
            description: Detailed description
            context: Additional context
            requires_confirmation: Whether confirmation is required
            
        Returns:
            Decision request object
        """
        request = DecisionRequest(
            action=action,
            description=description,
            context=context,
            requires_confirmation=requires_confirmation
        )
        self.requests[request.id] = request
        
        # Auto-approve if in auto-approve mode
        if self.auto_approve_mode:
            request.bypass(reason="Auto-approve mode enabled")
            return request
        
        # If confirmation not required, auto-approve
        if not requires_confirmation:
            request.bypass(reason="Confirmation not required")
            return request
        
        return request
    
    def evaluate_request(self, request_id: str) -> GateDecision:
        """
        Evaluate a request against all rules.
        
        Args:
            request_id: Request identifier
            
        Returns:
            Gate decision
        """
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        if request.decision != GateDecision.PENDING:
            return request.decision  # Already decided
        
        # Get enabled rules sorted by priority
        rules = self.list_rules(enabled_only=True)
        
        # Evaluate each rule
        all_approved = True
        for rule in rules:
            result = rule.evaluate(request.context)
            request.evaluated_rules.append({
                'rule_id': rule.id,
                'rule_name': rule.name,
                'result': 'approved' if result else 'rejected',
                'priority': rule.priority.value
            })
            
            if not result:
                all_approved = False
                # Critical rules immediately reject
                if rule.priority == GateRulePriority.CRITICAL:
                    request.reject(reason=f"Critical rule '{rule.name}' rejected the request")
                    return request.decision
        
        # Final decision based on all rules
        if all_approved:
            request.approve(reason="All rules approved")
        else:
            request.reject(reason="One or more rules rejected the request")
        
        return request.decision
    
    def approve_request(self, request_id: str, reason: str = "") -> bool:
        """
        Manually approve a request.
        
        Args:
            request_id: Request identifier
            reason: Approval reason
            
        Returns:
            True if successful
        """
        request = self.requests.get(request_id)
        if request:
            request.approve(reason=reason or "Manual approval")
            return True
        return False
    
    def reject_request(self, request_id: str, reason: str = "") -> bool:
        """
        Manually reject a request.
        
        Args:
            request_id: Request identifier
            reason: Rejection reason
            
        Returns:
            True if successful
        """
        request = self.requests.get(request_id)
        if request:
            request.reject(reason=reason or "Manual rejection")
            return True
        return False
    
    def get_request(self, request_id: str) -> Optional[DecisionRequest]:
        """
        Get a specific request.
        
        Args:
            request_id: Request identifier
            
        Returns:
            Request or None
        """
        return self.requests.get(request_id)
    
    def list_pending_requests(self) -> List[DecisionRequest]:
        """
        List all pending requests.
        
        Returns:
            List of pending requests
        """
        return [r for r in self.requests.values() if r.decision == GateDecision.PENDING]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert gate state to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'auto_approve_mode': self.auto_approve_mode,
            'total_rules': len(self.rules),
            'enabled_rules': len([r for r in self.rules.values() if r.enabled]),
            'total_requests': len(self.requests),
            'pending_requests': len(self.list_pending_requests()),
            'rules': {rid: r.to_dict() for rid, r in self.rules.items()},
            'created_at': self.created_at.isoformat()
        }
