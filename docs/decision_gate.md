# Decision Gate - Strict Confirmation System

## Overview

Decision Gate is a strict YES/NO confirmation system that controls all critical actions in the VoBee AI Operating System. It ensures that important operations require explicit human approval before execution.

## Core Concepts

### Decision Types

Four levels of decision criticality:

1. **CRITICAL** - Cannot be auto-approved, always requires human confirmation
   - Production deployments
   - Data deletions
   - Large budget spends
   - System-wide changes

2. **HIGH** - Requires confirmation, but can be auto-approved with rules
   - Service restarts
   - Configuration changes
   - Medium budget spends

3. **NORMAL** - Can be auto-approved
   - Log cleanups
   - Cache clears
   - Minor updates

4. **INFO** - Informational only, no confirmation needed
   - Status updates
   - Notifications
   - Reports

### Decision Status

Each decision progresses through states:

- **PENDING** - Awaiting approval/rejection
- **APPROVED** - Approved, ready for execution
- **REJECTED** - Rejected, will not execute
- **EXPIRED** - Timed out without response
- **EXECUTED** - Successfully executed

## Basic Usage

### Creating the Gate

```python
from core.decision_gate import DecisionGate, DecisionType

# Initialize (auto-approval disabled by default)
gate = DecisionGate(enable_auto_approval=False)
```

### Requesting Decisions

```python
# Request a critical decision
decision = gate.request_decision(
    action_type="deploy",
    description="Deploy version 2.0 to production",
    decision_type=DecisionType.CRITICAL,
    context={
        "service": "api-gateway",
        "version": "2.0.0",
        "environment": "production"
    }
)

print(f"Decision ID: {decision.decision_id}")
print(f"Status: {decision.status.value}")  # "pending"
```

### Approving Decisions

```python
# Approve the decision
success = gate.approve_decision(
    decision_id=decision.decision_id,
    approved_by="admin@example.com"
)

# Check status
decision = gate.get_decision(decision.decision_id)
print(f"Status: {decision.status.value}")  # "approved"
```

### Rejecting Decisions

```python
# Reject with reason
success = gate.reject_decision(
    decision_id=decision.decision_id,
    reason="Not ready for production yet",
    rejected_by="admin@example.com"
)
```

### Executing Decisions

```python
def deploy_service(decision):
    """Function that performs the actual deployment"""
    service = decision.context["service"]
    version = decision.context["version"]
    
    # Perform deployment
    # ...
    
    return {
        "success": True,
        "deployment_id": "deploy-12345",
        "timestamp": datetime.utcnow().isoformat()
    }

# Execute approved decision
result = gate.execute_decision(
    decision_id=decision.decision_id,
    executor_func=deploy_service
)

print(f"Execution result: {result}")
```

## Advanced Features

### Auto-Approval Rules

Enable auto-approval with custom rules:

```python
# Enable auto-approval
gate = DecisionGate(enable_auto_approval=True)

# Define a rule
def small_budget_rule(decision):
    """Auto-approve budget spends under $1000"""
    if decision.action_type == "budget_spend":
        amount = decision.context.get("amount", 0)
        return amount < 1000
    return False

# Add the rule
gate.add_auto_approval_rule("small_budget", small_budget_rule)

# Now small budget spends are auto-approved
decision = gate.request_decision(
    action_type="budget_spend",
    description="Purchase API credits",
    decision_type=DecisionType.NORMAL,
    context={"amount": 500}
)
# This decision will be auto-approved immediately
```

### Listing Decisions

```python
# Get all pending decisions
pending = gate.list_pending_decisions()
for dec in pending:
    print(f"{dec.decision_id}: {dec.description}")

# Get decisions by status
from core.decision_gate import DecisionStatus
approved = gate.list_decisions_by_status(DecisionStatus.APPROVED)
rejected = gate.list_decisions_by_status(DecisionStatus.REJECTED)
```

### Decision Expiration

```python
# Expire decisions older than 24 hours
gate.expire_old_decisions(max_age_hours=24)

# Or custom age
gate.expire_old_decisions(max_age_hours=1)  # 1 hour
```

### Audit Trail

Complete audit log of all decision events:

```python
# Get full audit log
all_logs = gate.get_audit_log()

# Get logs for specific decision
decision_logs = gate.get_audit_log(decision_id=decision.decision_id)

# Get recent logs
recent_logs = gate.get_audit_log(limit=10)

# Audit log includes:
# - Timestamp
# - Event type (requested, approved, rejected, executed, etc.)
# - Decision ID
# - Action type
# - Current status
```

### State Persistence

```python
# Save all decisions and audit log
gate.save_state("decisions.json")

# Load from file
gate.load_state("decisions.json")
```

## Usage Patterns

### Pattern 1: Deployment Pipeline

```python
# Request deployment decision
decision = gate.request_decision(
    action_type="deploy",
    description=f"Deploy {service_name} v{version}",
    decision_type=DecisionType.CRITICAL,
    context={
        "service": service_name,
        "version": version,
        "environment": "production",
        "git_commit": commit_sha
    }
)

# Wait for approval (in practice, this would be async)
# User reviews and approves via UI/API

# Once approved, execute
if gate.get_decision(decision.decision_id).status == DecisionStatus.APPROVED:
    result = gate.execute_decision(decision.decision_id, deploy_function)
```

### Pattern 2: Budget Control

```python
def spend_budget(project_id, amount, category):
    # Request decision
    decision = gate.request_decision(
        action_type="budget_spend",
        description=f"Spend ${amount} on {category}",
        decision_type=DecisionType.HIGH if amount > 1000 else DecisionType.NORMAL,
        context={
            "project_id": project_id,
            "amount": amount,
            "category": category
        }
    )
    
    # Return decision ID for tracking
    return decision.decision_id
```

### Pattern 3: Data Operations

```python
# Require approval for data deletion
decision = gate.request_decision(
    action_type="delete_data",
    description="Delete old user data (90+ days)",
    decision_type=DecisionType.CRITICAL,
    context={
        "record_count": 1000,
        "age_days": 90,
        "table": "user_events"
    }
)

# Explicit approval required before deletion
```

### Pattern 4: Automated Cleanup with Approval

```python
# Enable auto-approval for routine cleanup
gate.add_auto_approval_rule("routine_cleanup", lambda d: 
    d.action_type == "cleanup" and 
    d.context.get("days_old", 0) > 30
)

# This will be auto-approved
decision = gate.request_decision(
    action_type="cleanup",
    description="Clean up old logs",
    decision_type=DecisionType.NORMAL,
    context={"days_old": 45, "size_mb": 100}
)
```

## Integration Examples

### With Project Cortex

```python
# Require approval for project budget changes
def change_project_budget(project, new_budget):
    decision = gate.request_decision(
        action_type="change_budget",
        description=f"Change budget for {project.name}",
        decision_type=DecisionType.CRITICAL,
        context={
            "project_id": project.project_id,
            "old_budget": project.budget.total_budget,
            "new_budget": new_budget
        }
    )
    
    return decision.decision_id
```

### With Agent Registry

```python
# Require approval for agent role changes
def change_agent_role(agent, new_role_id):
    decision = gate.request_decision(
        action_type="change_agent_role",
        description=f"Change role for agent {agent.name}",
        decision_type=DecisionType.HIGH,
        context={
            "agent_id": agent.agent_id,
            "old_role": agent.role_id,
            "new_role": new_role_id
        }
    )
    
    return decision.decision_id
```

## API Reference

### DecisionGate Class

**Constructor**:
- `DecisionGate(enable_auto_approval=False)` - Create gate instance

**Methods**:
- `request_decision(action_type, description, decision_type, context)` - Request new decision
- `get_decision(decision_id)` - Get decision by ID
- `approve_decision(decision_id, approved_by)` - Approve decision
- `reject_decision(decision_id, reason, rejected_by)` - Reject decision
- `execute_decision(decision_id, executor_func)` - Execute approved decision
- `list_pending_decisions()` - Get all pending decisions
- `list_decisions_by_status(status)` - Get decisions by status
- `add_auto_approval_rule(rule_name, rule_func)` - Add auto-approval rule
- `remove_auto_approval_rule(rule_name)` - Remove rule
- `expire_old_decisions(max_age_hours)` - Expire old pending decisions
- `get_audit_log(decision_id, limit)` - Get audit log entries
- `save_state(filepath)` - Save to JSON
- `load_state(filepath)` - Load from JSON

### Decision Class

**Methods**:
- `approve(approved_by)` - Approve this decision
- `reject(reason, rejected_by)` - Reject this decision
- `mark_executed(result)` - Mark as executed
- `expire()` - Mark as expired
- `to_dict()` - Export to dictionary

**Properties**:
- `decision_id` - Unique ID
- `action_type` - Type of action
- `description` - Human-readable description
- `decision_type` - DecisionType enum
- `context` - Additional context dict
- `status` - Current status
- `created_at` - Creation timestamp
- `responded_at` - Response timestamp
- `executed_at` - Execution timestamp
- `approved_by` - Who approved
- `rejection_reason` - Why rejected
- `execution_result` - Execution result

## Best Practices

1. **Use appropriate decision types**: CRITICAL for irreversible actions
2. **Provide context**: Include all relevant information in context dict
3. **Set descriptions clearly**: Make it obvious what will happen
4. **Review audit logs**: Regularly check decision patterns
5. **Expire old decisions**: Clean up stale pending decisions
6. **Test auto-approval rules**: Ensure rules work as expected
7. **Save state periodically**: Don't lose decision history

## Security Considerations

- **Authentication**: Verify `approved_by` identity in production
- **Authorization**: Ensure approver has permission for action type
- **Audit retention**: Keep audit logs for compliance
- **Rate limiting**: Prevent decision request spam
- **Context validation**: Sanitize context data

## Example: Complete Workflow

See `core/decision_gate/example.py` for a complete working example.

```bash
python core/decision_gate/example.py
```
