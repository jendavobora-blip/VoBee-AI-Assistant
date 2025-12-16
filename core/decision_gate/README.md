# Decision Gate

## Overview

Decision Gate is a confirmation and control system for managing critical actions in the VoBee AI Assistant. It provides a modular YES/NO gate system with extensible rules for controlling operations that require approval.

## Features

### Confirmation System
- YES/NO gate for critical action approval
- Manual approval/rejection capabilities
- Auto-approve mode for testing/development
- Bypass mechanism for non-critical actions

### Modular Rule Engine
- Define custom rules with priority levels
- Chain multiple rules for complex logic
- Enable/disable rules dynamically
- Priority-based evaluation (Critical, High, Medium, Low)

### Decision Tracking
- Track all approval requests
- Audit trail with timestamps
- Decision reasons and context
- Rule evaluation history

## Usage

### Basic Example

```python
from core.decision_gate import DecisionGate, GateRule, GateRulePriority

# Initialize the gate
gate = DecisionGate()

# Create a simple rule
budget_rule = GateRule(
    name="Budget Check",
    description="Ensure operation is within budget",
    priority=GateRulePriority.HIGH
)

# Define rule evaluation logic
def check_budget(context: dict) -> bool:
    cost = context.get('cost', 0)
    budget = context.get('budget', 0)
    return cost <= budget

budget_rule.set_evaluation_function(check_budget)
gate.add_rule(budget_rule)

# Request approval for an action
request = gate.request_approval(
    action="deploy_model",
    description="Deploy new AI model to production",
    context={
        'cost': 500,
        'budget': 1000,
        'model_name': 'gpt-custom'
    }
)

# Evaluate the request
decision = gate.evaluate_request(request.id)
print(f"Decision: {decision.value}")  # approved or rejected
```

### Creating Custom Rules

```python
# Critical security rule
security_rule = GateRule(
    name="Security Check",
    description="Verify security requirements",
    priority=GateRulePriority.CRITICAL
)

def check_security(context: dict) -> bool:
    # Check if security scan passed
    return context.get('security_scan_passed', False)

security_rule.set_evaluation_function(check_security)
gate.add_rule(security_rule)
```

### Manual Approval Workflow

```python
# Request approval
request = gate.request_approval(
    action="delete_database",
    description="Delete production database",
    context={'database': 'prod-db'}
)

# List pending requests
pending = gate.list_pending_requests()
for req in pending:
    print(f"Pending: {req.action} - {req.description}")

# Manual approval
gate.approve_request(request.id, reason="Approved by admin")

# Or manual rejection
gate.reject_request(request.id, reason="Too risky")
```

### Auto-Approve Mode

```python
# Useful for testing or non-production environments
gate = DecisionGate(auto_approve_mode=True)

request = gate.request_approval(
    action="test_action",
    description="Test operation"
)
# Automatically bypassed
print(request.decision)  # BYPASSED
```

## Architecture

### DecisionGate
The main control system that manages rules and requests.

**Key Methods:**
- `add_rule()` / `remove_rule()`: Manage rules
- `request_approval()`: Create approval request
- `evaluate_request()`: Evaluate against all rules
- `approve_request()` / `reject_request()`: Manual decisions
- `list_pending_requests()`: Get pending requests

### GateRule
Represents a modular evaluation rule.

**Key Methods:**
- `set_evaluation_function()`: Define rule logic
- `evaluate()`: Evaluate against context
- `enable()` / `disable()`: Toggle rule

### DecisionRequest
Represents an approval request.

**Properties:**
- `action`: Action requiring approval
- `context`: Additional data for evaluation
- `decision`: Current decision status
- `evaluated_rules`: History of rule evaluations

## Rule Priority Levels

1. **CRITICAL**: Must pass; immediate rejection if fails
2. **HIGH**: Important rules evaluated early
3. **MEDIUM**: Standard rules
4. **LOW**: Optional checks

Rules are evaluated in priority order, with critical rules causing immediate rejection if they fail.

## Decision States

- **PENDING**: Awaiting evaluation or manual decision
- **APPROVED**: Request approved
- **REJECTED**: Request rejected
- **BYPASSED**: Auto-approved without evaluation

## Design Principles

1. **Modularity**: Rules are independent and composable
2. **Extensibility**: Easy to add new rules without changing core logic
3. **Safety**: Fail-safe to rejection on errors
4. **Transparency**: Full audit trail of all decisions
5. **Flexibility**: Support both automated and manual workflows

## Future Extensions

This is a foundational skeleton designed for expansion:

- Conditional rules with complex logic operators (AND, OR, NOT)
- Rule templates for common patterns
- Integration with external approval systems
- Notification system for pending requests
- Time-based auto-approval/rejection
- Multi-stage approval workflows
- Role-based access control for manual approvals
- Rule versioning and rollback
- Machine learning-based rule recommendations

## Integration Points

Decision Gate can be integrated with:

- **Project Cortex**: Approve project creation/deletion
- **Agent Registry**: Control agent deployment
- **Budget Systems**: Enforce spending limits
- **Security Systems**: Validate security requirements
- **Deployment Pipelines**: Gate production deployments

## Status

**Current Version**: 0.1.0 (Skeleton)

This is a MAX_SPEED implementation focusing on structural foundations. Full functionality will be added in future iterations.
