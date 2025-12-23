# Decision Gates Structure - Confirmation and Approval Mechanisms

A comprehensive decision gate system implementing confirmation pending, output-lock requirements, and yes/no module with non-merge prohibited interaction layer.

## Overview

The Decision Gates Structure provides a robust framework for managing decisions that require explicit approval or confirmation before proceeding. This is critical for:
- Preventing unintended actions
- Enforcing approval workflows
- Implementing output locks until confirmation
- Managing multi-step approval processes

**Key Features:**
- Multiple gate types (confirmation, approval, review, merge-lock, output-lock)
- Yes/No confirmation module
- Multi-approver support
- Auto-expiry capabilities
- Output locking mechanism
- Non-merge prohibited interaction layer

## Architecture

```
Decision Gates Structure
├── GateManager (Central Management)
│   ├── Gate Creation
│   ├── Approval/Rejection Processing
│   └── Expiry Management
├── DecisionGate (Gate Entity)
│   ├── Status Tracking
│   ├── Approval Collection
│   └── Output Lock Control
└── ConfirmationHandler (Yes/No Module)
    ├── Simple Confirmations
    ├── Timeout Management
    └── Callback Execution
```

## Components

### 1. DecisionGate - Individual Gate Entity

Represents a single decision gate requiring approval/confirmation.

**Gate Types:**
- **CONFIRMATION**: Simple yes/no confirmation
- **APPROVAL**: Requires explicit approval from designated approvers
- **REVIEW**: Requires review before proceeding
- **MERGE_LOCK**: Blocks merge operations until approved
- **OUTPUT_LOCK**: Locks output until confirmed

**Gate Statuses:**
- **PENDING**: Awaiting decision
- **APPROVED**: Approved and passed
- **REJECTED**: Rejected and blocked
- **EXPIRED**: Timed out without decision
- **CANCELLED**: Manually cancelled

**Example Usage:**
```python
from core.decision_gates_structure import DecisionGate, GateType, GateStatus

# Create a gate
gate = DecisionGate(
    gate_id="gate-001",
    gate_type=GateType.APPROVAL,
    title="Deploy to Production",
    description="Approve deployment of version 2.0 to production",
    context={'version': '2.0', 'environment': 'production'},
    required_approvers=['manager-001', 'devops-lead'],
    auto_expire_minutes=60  # Auto-expire after 1 hour
)

# First approver
gate.approve('manager-001', note="Looks good to me")

# Second approver (gate becomes approved)
gate.approve('devops-lead', note="Infrastructure ready")

# Check status
if gate.is_approved():
    print("Deployment approved!")

# Check output lock
if gate.is_output_locked():
    print("Output is locked, waiting for approval")
```

### 2. GateManager - Central Gate Management

Manages all decision gates in the system.

**Key Features:**
- Gate creation and lifecycle management
- Centralized approval/rejection handling
- Automatic expiry checking
- Statistics and reporting
- Gate filtering by type/status

**Example Usage:**
```python
from core.decision_gates_structure import GateManager, GateType

# Initialize manager
manager = GateManager()

# Create gates
deploy_gate = manager.create_gate(
    gate_type=GateType.APPROVAL,
    title="Production Deployment",
    description="Deploy new features to production",
    required_approvers=['lead-001', 'ops-001'],
    auto_expire_minutes=30
)

merge_gate = manager.create_gate(
    gate_type=GateType.MERGE_LOCK,
    title="Merge Feature Branch",
    description="Merge feature/new-auth into main",
    required_approvers=['tech-lead']
)

# Approve a gate
manager.approve_gate(
    gate_id=deploy_gate.gate_id,
    approver_id='lead-001',
    note='Code review passed'
)

# Reject a gate
manager.reject_gate(
    gate_id=merge_gate.gate_id,
    rejector_id='tech-lead',
    reason='Tests failing'
)

# Get pending gates
pending = manager.get_pending_gates()
print(f"Pending approvals: {len(pending)}")

# Get locked outputs
locked = manager.get_locked_outputs()

# Cleanup expired gates
expired_count = manager.cleanup_expired_gates()

# Get statistics
stats = manager.get_manager_stats()
print(f"Total gates: {stats['total_gates']}")
print(f"Pending: {stats['pending_gates']}")
print(f"Locked outputs: {stats['locked_outputs']}")
```

### 3. ConfirmationHandler - Simple Yes/No Module

Simplified handler for binary yes/no confirmations.

**Key Features:**
- Simple yes/no interface
- Timeout support
- Callback execution on confirm/reject
- Confirmation history
- Non-blocking design

**Example Usage:**
```python
from core.decision_gates_structure import ConfirmationHandler

# Initialize handler
handler = ConfirmationHandler()

# Define callbacks
def on_confirmed():
    print("Action confirmed, proceeding...")

def on_rejected():
    print("Action rejected, cancelling...")

# Request confirmation
conf_id = handler.request_confirmation(
    confirmation_id="conf-001",
    message="Delete all user data? This action cannot be undone.",
    context={'data_count': 1000, 'action': 'delete'},
    timeout_seconds=300,  # 5 minute timeout
    on_confirm=on_confirmed,
    on_reject=on_rejected
)

# User responds with YES
handler.confirm(conf_id, note="User explicitly confirmed")

# Or user responds with NO
# handler.reject(conf_id, reason="User cancelled action")

# Get pending confirmations
pending = handler.get_pending_confirmations()

# Get statistics
stats = handler.get_statistics()
print(f"Confirmed: {stats['confirmed']}")
print(f"Rejected: {stats['rejected']}")
```

## Complete Integration Example

```python
from core.decision_gates_structure import (
    GateManager,
    ConfirmationHandler,
    GateType
)

# Initialize both systems
gate_mgr = GateManager()
conf_handler = ConfirmationHandler()

# Scenario: Code deployment workflow

# 1. Simple confirmation for minor change
conf_id = conf_handler.request_confirmation(
    confirmation_id="deploy-staging",
    message="Deploy to staging environment?",
    timeout_seconds=60
)

# User confirms
if conf_handler.confirm(conf_id):
    print("Deploying to staging...")

# 2. Multi-approval gate for production deployment
prod_gate = gate_mgr.create_gate(
    gate_type=GateType.APPROVAL,
    title="Production Deployment - v2.0",
    description="Deploy version 2.0 to production servers",
    context={
        'version': '2.0',
        'changes': ['new-feature-1', 'bugfix-2'],
        'risk_level': 'medium'
    },
    required_approvers=['tech-lead', 'devops-lead', 'product-owner'],
    auto_expire_minutes=120  # 2 hour window
)

# Approvers respond
gate_mgr.approve_gate(prod_gate.gate_id, 'tech-lead', 'Code reviewed')
gate_mgr.approve_gate(prod_gate.gate_id, 'devops-lead', 'Infrastructure ready')
gate_mgr.approve_gate(prod_gate.gate_id, 'product-owner', 'Approved for release')

# Check if ready to deploy
if gate_mgr.check_gate_approval(prod_gate.gate_id):
    print("All approvals received, deploying to production...")
else:
    print("Still waiting for approvals...")

# 3. Output lock for sensitive operation
sensitive_gate = gate_mgr.create_gate(
    gate_type=GateType.OUTPUT_LOCK,
    title="Database Migration",
    description="Run database migration scripts",
    required_approvers=['dba-lead']
)

# Prevent output until approved
if sensitive_gate.is_output_locked():
    print("Output locked - waiting for DBA approval")
    # Block output operations...

# DBA approves
gate_mgr.approve_gate(sensitive_gate.gate_id, 'dba-lead', 'Schema verified')

# Output now unlocked
if not sensitive_gate.is_output_locked():
    print("Output unlocked - proceeding with migration")

# 4. Get system overview
gate_stats = gate_mgr.get_manager_stats()
conf_stats = conf_handler.get_statistics()

print(f"\nGate System Status:")
print(f"  Total gates: {gate_stats['total_gates']}")
print(f"  Pending: {gate_stats['pending_gates']}")
print(f"  Approved: {gate_stats['approved_gates']}")
print(f"  Rejected: {gate_stats['rejected_gates']}")
print(f"  Locked outputs: {gate_stats['locked_outputs']}")

print(f"\nConfirmation System Status:")
print(f"  Total: {conf_stats['total_confirmations']}")
print(f"  Pending: {conf_stats['pending']}")
print(f"  Confirmed: {conf_stats['confirmed']}")
print(f"  Rejected: {conf_stats['rejected']}")
```

## Workflow Examples

### 1. Merge Protection Workflow

```python
# Prevent merge until conditions met
merge_gate = gate_mgr.create_gate(
    gate_type=GateType.MERGE_LOCK,
    title="Merge PR #123",
    description="Merge feature branch to main",
    required_approvers=['code-reviewer', 'ci-system']
)

# Code reviewer approves
gate_mgr.approve_gate(merge_gate.gate_id, 'code-reviewer', 'LGTM')

# CI system approves after tests pass
gate_mgr.approve_gate(merge_gate.gate_id, 'ci-system', 'All tests passed')

# Now safe to merge
if merge_gate.is_approved():
    # Perform merge...
    pass
```

### 2. Output Lock for Data Export

```python
# Lock output until approval
export_gate = gate_mgr.create_gate(
    gate_type=GateType.OUTPUT_LOCK,
    title="Export Customer Data",
    description="Export 10,000 customer records",
    required_approvers=['privacy-officer', 'manager'],
    context={'record_count': 10000, 'data_type': 'PII'}
)

# Run export process
data = fetch_customer_data()

# Check if output can be released
if export_gate.is_output_locked():
    print("Waiting for privacy approval before releasing data...")
    # Store data securely, don't output yet
else:
    # Output approved
    write_export_file(data)
```

### 3. Critical Action Confirmation

```python
# Critical action requiring confirmation
conf_id = conf_handler.request_confirmation(
    confirmation_id="delete-production-db",
    message="DELETE PRODUCTION DATABASE? This is IRREVERSIBLE!",
    context={'database': 'production', 'backup_verified': True},
    timeout_seconds=30
)

# User must explicitly confirm
# handler.confirm(conf_id, note="Confirmed by authorized admin")
# OR
# handler.reject(conf_id, reason="Action cancelled")

# Check confirmation status
confirmation = conf_handler.get_confirmation(conf_id)
if confirmation and confirmation['status'] == 'confirmed':
    # Proceed with deletion
    pass
elif confirmation and confirmation['status'] == 'rejected':
    print("Database deletion cancelled")
elif confirmation and confirmation['status'] == 'timeout':
    print("Confirmation timed out - action cancelled for safety")
```

## Best Practices

1. **Use Appropriate Gate Types**: Choose the right gate type for your use case
2. **Set Reasonable Timeouts**: Prevent gates from staying open indefinitely
3. **Require Multiple Approvers for Critical Actions**: Implement separation of duties
4. **Lock Sensitive Outputs**: Use OUTPUT_LOCK for PII or sensitive data
5. **Log All Decisions**: Track who approved/rejected and when
6. **Handle Expiry Gracefully**: Clean up expired gates regularly
7. **Provide Clear Context**: Include relevant information in gate descriptions
8. **Use Callbacks**: Leverage on_confirm/on_reject for automatic actions

## Security Considerations

- All approvals are logged with timestamps and approver IDs
- Rejected gates cannot be re-approved (must create new gate)
- Expired gates are automatically marked and cannot be approved
- Output locks prevent data leakage before approval
- Non-merge prohibition prevents unauthorized code merges

## Integration with Project Cortex

Decision gates can be used with Project Cortex for project-level approvals:

```python
from core.project_cortex import ProjectManager
from core.decision_gates_structure import GateManager, GateType

pm = ProjectManager()
gm = GateManager()

# Create project
project = pm.create_project(
    name="Critical Infrastructure Update",
    budget={'total': 100000, 'currency': 'USD'}
)

# Create approval gate for budget increase
budget_gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title=f"Budget Increase for {project.name}",
    description="Increase budget by $50,000",
    context={'project_id': project.project_id, 'amount': 50000},
    required_approvers=['cfo', 'project-sponsor']
)

# After approvals...
if budget_gate.is_approved():
    project.update_budget(50000, operation='add')
```

## Monitoring and Reporting

```python
# Regular cleanup
gate_mgr.cleanup_expired_gates()

# Get pending items needing attention
pending_gates = gate_mgr.get_pending_gates()
pending_confs = conf_handler.get_pending_confirmations()

# Generate report
stats = gate_mgr.get_manager_stats()
print(f"Decision Gates Health Report:")
print(f"  Active gates: {stats['pending_gates']}")
print(f"  Locked outputs: {stats['locked_outputs']}")
print(f"  Resolution rate: {stats['approved_gates'] / max(1, stats['total_gates']) * 100:.1f}%")
```
