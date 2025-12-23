# Core - VoBee AI Assistant Core Modules

Core modules for the Personal AI Operating System extension.

## Overview

This directory contains the foundational modules that extend VoBee AI Assistant from v0 into a comprehensive Personal AI Operating System. These modules provide project management, agent orchestration, and decision control capabilities.

## Modules

### 1. Project Cortex (`project_cortex/`)

Multi-project management brain capable of handling 1-50 parallel projects with complete isolation.

**Key Features:**
- Manage up to 50 active projects simultaneously
- Isolated memory per project (short-term, long-term, context)
- Budget tracking and financial management
- Agent assignment and tracking
- Sleep/wake capabilities for resource optimization
- Goal tracking and progress monitoring

**Quick Start:**
```python
from core.project_cortex import ProjectManager

pm = ProjectManager()
project = pm.create_project(
    name="AI Research Initiative",
    budget={'total': 100000, 'currency': 'USD'},
    goals=['Deploy ML model', 'Optimize performance']
)
```

See [project_cortex/README.md](project_cortex/README.md) for detailed documentation.

### 2. Decision Gates Structure (`decision_gates_structure/`)

Confirmation and approval mechanisms with output-lock requirements.

**Key Features:**
- Multiple gate types (confirmation, approval, review, merge-lock, output-lock)
- Multi-approver support
- Yes/No confirmation module
- Auto-expiry capabilities
- Non-merge prohibited interaction layer
- Output locking until approval

**Quick Start:**
```python
from core.decision_gates_structure import GateManager, GateType

gm = GateManager()
gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title="Deploy to Production",
    required_approvers=['tech-lead', 'ops-lead']
)
```

See [decision_gates_structure/README.md](decision_gates_structure/README.md) for detailed documentation.

## Integration Example

Complete example using all core modules together:

```python
from core.project_cortex import ProjectManager, MemoryManager, BudgetManager
from core.decision_gates_structure import GateManager, GateType

# Initialize all managers
pm = ProjectManager()
mm = MemoryManager()
bm = BudgetManager()
gm = GateManager()

# 1. Create a new project
project = pm.create_project(
    name="Mobile App Development",
    budget={'total': 75000, 'currency': 'USD'},
    goals=['Complete UI/UX', 'Launch beta']
)

# 2. Setup budget tracking
bm.create_budget_profile(project.project_id, total_budget=75000)

# 3. Initialize project memory
mm.create_project_memory(project.project_id)
mm.store(project.project_id, "tech_stack", ["React Native", "Node.js"])

# 4. Create approval gate for major expense
expense_gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title=f"Budget Expense - {project.name}",
    description="Approve $5000 expense for infrastructure",
    context={'project_id': project.project_id, 'amount': 5000},
    required_approvers=['finance-lead', 'project-manager']
)

# 5. After approvals...
if expense_gate.is_approved():
    bm.record_expense(project.project_id, 5000, "Cloud infrastructure")
    mm.store(project.project_id, "infrastructure_cost", 5000)

# 6. Monitor project health
print(f"Project: {project.name}")
print(f"Budget: ${bm.get_budget(project.project_id)['remaining']} remaining")
print(f"Active: {project.is_active()}")
```

## Architecture

```
core/
├── project_cortex/
│   ├── ProjectManager      # Multi-project orchestration
│   ├── Project             # Individual project entity
│   ├── MemoryManager       # Isolated memory management
│   ├── BudgetManager       # Financial tracking
│   └── AgentTracker        # Agent assignment tracking
│
└── decision_gates_structure/
    ├── GateManager         # Central gate management
    ├── DecisionGate        # Individual approval gates
    └── ConfirmationHandler # Yes/no confirmations
```

## Module Communication

The core modules are designed to work together:

1. **Projects & Decision Gates**: Gates can approve project actions (budget increases, agent assignments)
2. **Projects & Memory**: Each project has isolated memory managed by MemoryManager
3. **Projects & Budget**: Budget tracking is linked to project lifecycle
4. **Gates & Agents**: Agent assignments can require gate approval

## Best Practices

1. **Use Sleep/Wake**: Optimize resources by sleeping idle projects
2. **Gate Critical Actions**: Require approval for sensitive operations
3. **Track Everything**: Use memory and budget managers for auditability
4. **Isolate Projects**: Leverage project isolation for security and organization
5. **Monitor Health**: Regularly check project and gate statistics

## Configuration

All modules support configuration through environment variables or config files:

```python
# Example configuration
PROJECT_CORTEX_CONFIG = {
    'max_active_projects': 50,
    'max_total_projects': 100,
    'auto_sleep_threshold_minutes': 30
}

DECISION_GATES_CONFIG = {
    'default_expiry_minutes': 60,
    'require_approval_notes': True
}
```

## Monitoring

Get system-wide statistics:

```python
# Project Cortex stats
pm_stats = pm.get_project_summary()
print(f"Active projects: {pm_stats['active_projects']}/{pm_stats['max_active']}")

# Decision Gates stats
gm_stats = gm.get_manager_stats()
print(f"Pending gates: {gm_stats['pending_gates']}")
print(f"Locked outputs: {gm_stats['locked_outputs']}")
```

## Testing

Each module includes comprehensive testing capabilities:

```python
# Test project lifecycle
project = pm.create_project("Test Project")
assert project.is_active()
project.sleep()
assert project.is_sleeping()
project.wake()
assert project.is_active()

# Test gate approval
gate = gm.create_gate(GateType.APPROVAL, "Test Gate", required_approvers=['user1'])
gm.approve_gate(gate.gate_id, 'user1')
assert gate.is_approved()
```

## Extending

All modules are designed to be extensible:

- Add custom project types by extending `Project`
- Create custom gate types by extending `GateType`
- Implement custom memory backends by extending `MemoryManager`
- Add custom budget categories and tracking

## Support

For detailed documentation on each module:
- [Project Cortex Documentation](project_cortex/README.md)
- [Decision Gates Documentation](decision_gates_structure/README.md)

For system architecture:
- See `/ARCHITECTURE.md` in repository root
- See `/AUTONOMOUS_SYSTEM.md` for autonomous features
