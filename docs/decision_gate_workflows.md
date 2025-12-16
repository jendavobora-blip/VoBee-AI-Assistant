# Decision Gate Workflows

## Overview

The Decision Gate system ensures that critical operations require explicit human approval before execution. This document describes common workflows and best practices.

## Core Concepts

### Decision Lifecycle

```
                    ┌─────────┐
                    │ Created │
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │ Pending │
                    └────┬────┘
                         │
           ┌─────────────┼─────────────┐
           │             │             │
      ┌────▼────┐   ┌───▼────┐   ┌───▼─────┐
      │Approved │   │Rejected│   │ Expired │
      └────┬────┘   └────────┘   └─────────┘
           │
      ┌────▼────┐
      │Executed │
      └─────────┘
```

States:
1. **Created**: Decision request submitted
2. **Pending**: Awaiting human review
3. **Approved**: Human approved, ready for execution
4. **Rejected**: Human rejected, will not execute (terminal state)
5. **Expired**: Time limit passed without approval (terminal state)
6. **Executed**: Action completed (only for approved decisions, terminal state)

### Decision Types

- **Deployment**: Code/service deployments
- **Branch Merge**: Git branch merges (especially to main)
- **Budget Change**: Project budget modifications
- **Config Update**: System configuration changes
- **Data Deletion**: Permanent data removal
- **Resource Allocation**: Compute/storage allocation changes
- **API Integration**: New external API integrations
- **Database Migration**: Schema changes

### Risk Levels

- **Low**: Minor changes, low impact
- **Medium**: Moderate impact, reversible
- **High**: Significant impact, complex rollback
- **Critical**: Production changes, data loss risk, regulatory impact

## Common Workflows

### Workflow 1: Production Deployment

**Scenario**: Deploying new version to production

```python
from core.decision_gate import DecisionManager, ConfirmationWorkflow

# Initialize
dm = DecisionManager()
workflow = ConfirmationWorkflow(dm)

# Step 1: Request deployment approval
decision_id = workflow.confirm_deployment(
    environment="production",
    services=["api-gateway", "orchestrator", "worker-pool"],
    version="v2.1.0",
    rollback_plan="kubectl rollout undo deployment/{service}"
)

print(f"Deployment approval requested: {decision_id}")
print("Awaiting human approval...")

# Step 2: Human reviews via UI/CLI and approves
# (This happens outside the script)
```

**Human Review Checklist**:
- [ ] Code review completed
- [ ] Tests passing
- [ ] Staging deployment successful
- [ ] Rollback plan verified
- [ ] Team notified
- [ ] Monitoring alerts configured

**Approval Process**:
```python
# After review, human approves
dm.approve_decision(
    decision_id=decision_id,
    approved_by="admin@company.com",
    notes="All checks passed. Deploying during maintenance window."
)

# Step 3: Execute deployment
def execute_deployment(action):
    """Execute the deployment."""
    env = action["environment"]
    services = action["services"]
    version = action["version"]
    
    # TODO: Actual deployment logic
    print(f"Deploying {services} to {env} version {version}")
    return {"status": "success", "services_deployed": len(services)}

result = dm.execute_decision(
    decision_id=decision_id,
    executor_func=execute_deployment,
    executor_id="deploy-automation"
)

print(f"Deployment result: {result['execution_result']}")
```

### Workflow 2: Main Branch Merge

**Scenario**: Merging feature branch to main

```python
# Step 1: Request merge approval
decision_id = workflow.confirm_branch_merge(
    source_branch="feature/new-agent-system",
    target_branch="main",
    changes_summary="""
    - Added multi-agent framework
    - Implemented decision gate system
    - Updated documentation
    - 2500 lines added, 50 lines removed
    - All tests passing
    """,
    reviewer="senior-dev@company.com"
)

# Step 2: Human reviews changes
# - Inspect diff
# - Run tests locally
# - Check for breaking changes
# - Verify documentation

# Step 3: Approve or reject
dm.approve_decision(
    decision_id=decision_id,
    approved_by="senior-dev@company.com",
    notes="Code reviewed, architecture approved, tests passing"
)

# Step 4: Execute merge
def execute_merge(action):
    """Execute git merge."""
    # TODO: Actual merge logic via git API
    return {"status": "merged", "commit_sha": "abc123"}

result = dm.execute_decision(
    decision_id=decision_id,
    executor_func=execute_merge,
    executor_id="git-automation"
)
```

### Workflow 3: Budget Increase

**Scenario**: Increasing project budget due to expanded scope

```python
# Step 1: Request budget change
decision_id = workflow.confirm_budget_change(
    project_id="ai-chatbot-v2",
    current_budget=500.00,
    new_budget=1000.00,
    justification="""
    Original scope expanded to include:
    - Additional language support
    - Enhanced image generation
    - Extended testing period
    
    Current spend: $420 (84%)
    Projected additional cost: $450
    """
)

# Step 2: Finance team reviews
# - Verify budget availability
# - Review cost projections
# - Assess ROI

# Step 3: Approve
dm.approve_decision(
    decision_id=decision_id,
    approved_by="finance-manager@company.com",
    notes="Budget increase approved. Updated in financial system."
)

# Step 4: Execute update
def update_budget(action):
    """Update project budget."""
    from core.project_cortex import ProjectManager
    
    pm = ProjectManager()
    project = pm.get_project(action["project_id"])
    project["budget_limit"] = action["new_budget"]
    pm._save_project(action["project_id"])
    
    return {"status": "updated", "new_limit": action["new_budget"]}

result = dm.execute_decision(
    decision_id=decision_id,
    executor_func=update_budget,
    executor_id="budget-automation"
)
```

### Workflow 4: Data Deletion

**Scenario**: Deleting old analytics data (high risk)

```python
# Step 1: Request deletion approval
decision_id = workflow.confirm_data_deletion(
    data_type="analytics_events",
    scope="events older than 2 years",
    estimated_records=5_000_000,
    backup_available=True
)

# Step 2: Data team reviews
# - Verify backup exists and is complete
# - Confirm retention policy allows deletion
# - Check no active analysis depends on this data
# - Ensure compliance with data retention regulations

# Step 3: Double-check and approve
dm.approve_decision(
    decision_id=decision_id,
    approved_by="data-lead@company.com",
    notes="Backup verified at s3://backups/analytics-2021-2022.tar.gz. Retention policy allows deletion."
)

# Step 4: Execute deletion
def delete_data(action):
    """Execute data deletion."""
    # TODO: Actual deletion logic
    # - Archive to cold storage first
    # - Delete from primary database
    # - Verify deletion
    return {
        "status": "deleted",
        "records_deleted": action["estimated_records"],
        "backup_location": "s3://backups/analytics-2021-2022.tar.gz"
    }

result = dm.execute_decision(
    decision_id=decision_id,
    executor_func=delete_data,
    executor_id="data-automation"
)
```

## Best Practices

### 1. Clear Decision Titles
❌ Bad: "Update config"  
✅ Good: "Update API rate limits: 100 → 1000 req/min"

### 2. Detailed Descriptions
Include:
- What will change
- Why it's needed
- Impact assessment
- Rollback plan
- Risk mitigation

### 3. Appropriate Risk Levels
- Use `critical` for production changes, data loss, security
- Use `high` for significant impacts
- Use `medium` for moderate changes
- Use `low` for minor updates

### 4. Reasonable Expiration Times
- Critical/Production: 2-6 hours (timely decision required)
- High priority: 12-24 hours
- Medium priority: 24-48 hours
- Low priority: 48-72 hours

### 5. Document Approval Rationale
Always include notes explaining:
- What was verified
- Why it was approved/rejected
- Any conditions or caveats

## Anti-Patterns to Avoid

### ❌ Auto-Approval
Never automatically approve decisions. This defeats the purpose of human oversight.

```python
# WRONG - Don't do this!
decision_id = dm.request_decision(...)
dm.approve_decision(decision_id, approved_by="automation")  # BAD!
dm.execute_decision(decision_id, ...)
```

### ❌ Bypassing Decision Gate
Don't execute critical actions without going through Decision Gate.

```python
# WRONG - No approval!
def deploy_to_production():
    os.system("kubectl apply -f production.yaml")  # BAD!
```

### ❌ Vague Descriptions
Don't be vague about what will happen.

```python
# WRONG - Too vague
decision_id = workflow.confirm_deployment(
    environment="production",
    services=["some services"],  # Which ones?
    version="latest",  # Which version exactly?
    rollback_plan="rollback"  # How?
)
```

## Integration Examples

### CLI Tool for Reviewing Decisions

```python
#!/usr/bin/env python3
"""CLI tool for reviewing pending decisions."""

from core.decision_gate import DecisionManager
import sys

def main():
    dm = DecisionManager()
    
    # List pending decisions
    pending = dm.list_pending_decisions()
    
    if not pending:
        print("No pending decisions.")
        return
    
    print(f"\n{len(pending)} Pending Decisions:\n")
    
    for i, decision in enumerate(pending, 1):
        print(f"{i}. [{decision['risk_level'].upper()}] {decision['title']}")
        print(f"   ID: {decision['id']}")
        print(f"   Created: {decision['created_at']}")
        print(f"   Expires: {decision['expires_at']}")
        print()
    
    # Interactive approval
    choice = input("Enter decision number to review (or 'q' to quit): ")
    
    if choice.lower() == 'q':
        return
    
    try:
        idx = int(choice) - 1
        decision = pending[idx]
        
        print(f"\n{'='*60}")
        print(f"Decision: {decision['title']}")
        print(f"{'='*60}")
        print(f"\nType: {decision['type']}")
        print(f"Risk Level: {decision['risk_level']}")
        print(f"\nDescription:\n{decision['description']}")
        print(f"\nProposed Action:\n{decision['proposed_action']}")
        print(f"{'='*60}\n")
        
        action = input("Approve (a), Reject (r), or Skip (s)? ").lower()
        
        if action == 'a':
            notes = input("Approval notes: ")
            dm.approve_decision(decision['id'], "cli-user", notes)
            print("✓ Approved")
        elif action == 'r':
            reason = input("Rejection reason: ")
            dm.reject_decision(decision['id'], "cli-user", reason)
            print("✗ Rejected")
        else:
            print("Skipped")
    
    except (ValueError, IndexError):
        print("Invalid choice")

if __name__ == "__main__":
    main()
```

### Web Dashboard Integration

```python
from flask import Flask, jsonify, request
from core.decision_gate import DecisionManager

app = Flask(__name__)
dm = DecisionManager()

@app.route("/api/decisions/pending")
def get_pending_decisions():
    """API endpoint for pending decisions."""
    pending = dm.list_pending_decisions()
    return jsonify({"decisions": pending})

@app.route("/api/decisions/<decision_id>/approve", methods=["POST"])
def approve_decision(decision_id):
    """Approve a decision."""
    data = request.json
    
    dm.approve_decision(
        decision_id=decision_id,
        approved_by=data["approved_by"],
        notes=data.get("notes", "")
    )
    
    return jsonify({"status": "approved"})

# Similar endpoints for reject, get details, etc.
```

## Monitoring & Alerts

### Decision Metrics to Track
- Pending decision count
- Average approval time
- Approval rate
- Expired decision count
- Decisions by risk level
- Execution success rate

### Alert Thresholds
- Alert if critical decisions pending > 2 hours
- Alert if high-risk decisions pending > 12 hours
- Alert if approval rate < 80%
- Alert if execution failure rate > 5%

## TODO Markers for Human Intervention

Throughout the decision gate code, you'll find TODO markers indicating where human decisions are required:

```python
# TODO: Integrate with notification system for high/critical risk decisions
# TODO: Add validation for budget_limit range
# TODO: Add validation for quality_preference options
```

These markers indicate areas where the system needs human input to complete functionality.

## Summary

The Decision Gate system provides:
- ✅ Explicit human approval for critical actions
- ✅ Complete audit trail
- ✅ Risk-based workflows
- ✅ Flexible integration options
- ✅ Protection against autonomous actions

Always remember: **The system suggests, humans decide, the system executes with approval.**

---

For more information, see:
- [Architecture Overview](architecture_overview.md)
- [Core Adjustment Procedures](core_adjustment_procedures.md)
