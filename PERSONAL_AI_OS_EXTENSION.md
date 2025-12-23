# Personal AI Operating System - Extension Modules

This extension transforms VoBee AI Assistant from v0 core into a comprehensive Personal AI Operating System.

## Overview

Three major module additions:

### 1. **Project Cortex** (`core/project_cortex/`)
Multi-project management brain capable of handling 1-50 parallel projects with complete isolation.

- Isolated memory, goals, and budget profiles per project
- Active agent tracking and assignment
- Sleep/wake capabilities for resource optimization
- Support for up to 50 active projects, 100 total

### 2. **Agents System** (`agents/`)
Role-based agent registry supporting 30-100+ logical roles with no vendor dependencies.

- 30+ predefined roles across 10 categories
- Operations, Frontend, Backend, Data, DevOps, Security, Testing, Design, Product, Research
- Capability-based agent matching
- Extensible placeholder structure

### 3. **Decision Gates Structure** (`core/decision_gates_structure/`)
Strict confirmation and approval mechanisms with output-lock requirements.

- Multiple gate types (confirmation, approval, review, merge-lock, output-lock)
- Yes/No module with non-merge prohibited interaction
- Multi-approver support
- Auto-expiry capabilities

## Quick Start

### Install and Import

```python
# Project Cortex
from core.project_cortex import ProjectManager, MemoryManager, BudgetManager

# Agents System
from agents import AgentRegistry, AgentRole, RoleCategory

# Decision Gates
from core.decision_gates_structure import GateManager, ConfirmationHandler, GateType
```

### Example Usage

```python
# 1. Create and manage projects
pm = ProjectManager()
project = pm.create_project(
    name="AI Platform Development",
    budget={'total': 100000, 'currency': 'USD'},
    goals=['Build backend', 'Deploy frontend', 'Launch v1.0']
)

# 2. Register and assign agents
registry = AgentRegistry()
registry.register_agent("be-001", "Backend Developer")
registry.register_agent("fe-001", "Frontend Developer")

# 3. Create approval gates
gm = GateManager()
gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title="Production Deployment",
    required_approvers=['tech-lead', 'ops-lead']
)
```

## Module Structure

```
VoBee-AI-Assistant/
├── core/
│   ├── project_cortex/           # Multi-project management
│   │   ├── __init__.py
│   │   ├── project_manager.py    # 1-50 project orchestration
│   │   ├── project.py            # Project entity with isolation
│   │   ├── memory_manager.py     # Isolated memory (short/long/context)
│   │   ├── budget_manager.py     # Financial tracking
│   │   ├── agent_tracker.py      # Agent assignment tracking
│   │   └── README.md
│   │
│   └── decision_gates_structure/ # Approval & confirmation system
│       ├── __init__.py
│       ├── gate_manager.py       # Central gate management
│       ├── decision_gate.py      # Individual gates
│       ├── confirmation_handler.py # Yes/no confirmations
│       └── README.md
│
├── agents/                        # Role-based agent registry
│   ├── __init__.py
│   ├── agent_registry.py         # Central agent management
│   ├── agent_roles.py            # 30+ role definitions
│   ├── base_agent.py             # Agent base class
│   └── README.md
│
└── [existing VoBee AI Assistant files...]
```

## Features by Module

### Project Cortex
✅ 1-50 parallel projects  
✅ Isolated memory per project  
✅ Budget profiles and tracking  
✅ Agent assignment tracking  
✅ Sleep/wake capabilities  
✅ Goal management  
✅ Auto-sleep for idle projects  

### Agents System
✅ 30+ predefined roles  
✅ 10 role categories  
✅ No vendor lock-in  
✅ Capability-based matching  
✅ Task execution framework  
✅ Agent performance tracking  
✅ Extensible architecture  

### Decision Gates
✅ Multiple gate types  
✅ Multi-approver support  
✅ Output locking  
✅ Merge protection  
✅ Auto-expiry  
✅ Yes/No confirmations  
✅ Non-merge prohibited interaction  

## Documentation

Each module includes comprehensive documentation:

- [`core/README.md`](core/README.md) - Core modules overview
- [`core/project_cortex/README.md`](core/project_cortex/README.md) - Project Cortex details
- [`core/decision_gates_structure/README.md`](core/decision_gates_structure/README.md) - Decision Gates details
- [`agents/README.md`](agents/README.md) - Agents System details

## Integration Examples

### Example 1: Project with Agents and Gates

```python
from core.project_cortex import ProjectManager
from agents import AgentRegistry
from core.decision_gates_structure import GateManager, GateType

# Initialize
pm = ProjectManager()
ar = AgentRegistry()
gm = GateManager()

# Create project
project = pm.create_project("API Development")

# Register agents
ar.register_agent("be-001", "Backend Developer")
ar.register_agent("api-001", "API Specialist")

# Create gate for deployment
deploy_gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title=f"Deploy {project.name}",
    required_approvers=['tech-lead']
)

# After approval
if deploy_gate.is_approved():
    print(f"Deploying {project.name}...")
```

### Example 2: Budget Approval Workflow

```python
from core.project_cortex import ProjectManager, BudgetManager
from core.decision_gates_structure import GateManager, GateType

pm = ProjectManager()
bm = BudgetManager()
gm = GateManager()

project = pm.create_project("Infrastructure Upgrade")
bm.create_budget_profile(project.project_id, total_budget=50000)

# Request budget increase
increase_gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title="Budget Increase Request",
    description="Increase budget by $25,000",
    required_approvers=['cfo', 'sponsor']
)

# After approvals
if increase_gate.is_approved():
    bm.add_budget(project.project_id, 25000, "Approved increase")
```

### Example 3: Agent Task with Confirmation

```python
from agents import AgentRegistry
from core.decision_gates_structure import ConfirmationHandler

ar = AgentRegistry()
ch = ConfirmationHandler()

# Register agent
ar.register_agent("ops-001", "Operations Architect")
agent = ar.get_agent("ops-001")

# Request confirmation for critical task
conf_id = ch.request_confirmation(
    confirmation_id="critical-task-001",
    message="Execute database migration? This cannot be undone.",
    timeout_seconds=300
)

# After user confirms
if ch.confirm(conf_id):
    # Execute task
    task = {'task_id': 'migration-001', 'type': 'db_migration'}
    result = agent.execute_task(task)
```

## Design Principles

1. **Modularity**: Each module is independent and can be used separately
2. **Extensibility**: Easy to add new roles, gate types, or project features
3. **No Vendor Lock-in**: Placeholder structures allow any implementation
4. **Resource Optimization**: Sleep/wake and auto-expiry prevent resource waste
5. **Auditability**: Complete tracking of all actions and decisions
6. **Isolation**: Projects have completely isolated contexts
7. **Safety**: Multi-gate approvals and confirmations prevent accidents

## Use Cases

### Research Organization
- Manage 20+ concurrent research projects
- Each project has isolated data and budget
- Researchers assigned as agents
- Publications require approval gates

### Software Development Team
- Multiple product lines as projects
- Developers as role-based agents
- Merge locks prevent unauthorized commits
- Budget tracking for each product

### AI Model Development
- Parallel model training projects
- Resource allocation per project
- Deployment gates for production
- Cost tracking and optimization

## Limits and Capacity

| Module | Limit | Configurable |
|--------|-------|-------------|
| Active Projects | 50 | Yes |
| Total Projects | 100 | Yes |
| Agents | 100 | Yes |
| Agent Roles | 100+ | Yes (extensible) |
| Decision Gates | Unlimited | - |

## Performance Considerations

- **Project Sleep/Wake**: Reduces memory usage for idle projects
- **Auto-Expiry**: Prevents accumulation of stale gates
- **Lazy Loading**: Memories loaded only when accessed
- **Efficient Indexing**: Fast lookups by ID, type, category

## Future Extensions

Potential additions to the system:

- [ ] Persistent storage backends (PostgreSQL, Redis)
- [ ] Real-time collaboration features
- [ ] Advanced analytics and reporting
- [ ] Machine learning-based agent selection
- [ ] Distributed project management
- [ ] Role-based access control (RBAC)
- [ ] Webhook integrations
- [ ] API endpoints for each module

## Migration from v0

This extension is fully backward compatible with VoBee AI Assistant v0:

- All existing services continue to work
- New modules are opt-in
- No breaking changes to existing APIs
- Can be gradually adopted

## License

Same as VoBee AI Assistant - MIT License
