# Quick Start Guide - Personal AI Operating System Extensions

Get started with the new Personal AI OS modules in under 5 minutes!

## Installation

No additional dependencies needed - all modules use Python standard library.

```bash
# Clone the repository
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant

# Run the complete integration example
python examples/complete_integration.py
```

## Basic Usage

### 1. Project Management

Create and manage multiple projects:

```python
from core.project_cortex import ProjectManager

# Initialize
pm = ProjectManager()

# Create a project
project = pm.create_project(
    name="My AI Project",
    budget={'total': 50000, 'currency': 'USD'},
    goals=['Build model', 'Deploy to production']
)

# Check status
print(f"Project {project.name} is {project.status.value}")
print(f"Goals: {project.goals}")

# Sleep/wake for resource management
project.sleep()  # Free up resources
project.wake()   # Resume work
```

### 2. Agent System

Register and assign agents to work on projects:

```python
from agents import AgentRegistry

# Initialize
registry = AgentRegistry()

# Register agents
registry.register_agent("dev-001", "Backend Developer")
registry.register_agent("dev-002", "Frontend Developer")

# Find agent with specific capability
api_agents = registry.get_agents_with_capability('api_implementation')

# Assign agent to task
agent = registry.get_agent("dev-001")
result = agent.execute_task({
    'task_id': 'build-api',
    'description': 'Build REST API'
})
```

### 3. Decision Gates

Require approval before critical operations:

```python
from core.decision_gates_structure import GateManager, GateType

# Initialize
gm = GateManager()

# Create approval gate
gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title="Deploy to Production",
    description="Deploy version 2.0",
    required_approvers=['tech-lead', 'ops-lead']
)

# Approvers respond
gm.approve_gate(gate.gate_id, 'tech-lead', 'Code looks good')
gm.approve_gate(gate.gate_id, 'ops-lead', 'Infrastructure ready')

# Check if approved
if gate.is_approved():
    print("Deployment approved!")
    # Proceed with deployment...
```

## Common Workflows

### Workflow 1: New Project Setup

```python
from core.project_cortex import ProjectManager, MemoryManager, BudgetManager
from agents import AgentRegistry
from core.decision_gates_structure import GateManager, GateType

# 1. Create project
pm = ProjectManager()
project = pm.create_project(name="New Feature Development")

# 2. Setup budget
bm = BudgetManager()
bm.create_budget_profile(project.project_id, total_budget=30000)

# 3. Initialize memory
mm = MemoryManager()
mm.create_project_memory(project.project_id)
mm.store(project.project_id, "phase", "planning")

# 4. Assign team
registry = AgentRegistry()
registry.register_agent("dev-001", "Backend Developer")
registry.register_agent("dev-002", "Frontend Developer")

print(f"Project '{project.name}' ready with 2 developers!")
```

### Workflow 2: Budget Approval

```python
from core.project_cortex import BudgetManager
from core.decision_gates_structure import GateManager, GateType

bm = BudgetManager()
gm = GateManager()

# Create approval gate for expense
expense_gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title="Infrastructure Expense",
    description="Cloud services for Q1",
    context={'amount': 5000, 'category': 'infrastructure'},
    required_approvers=['finance-lead']
)

# After approval
if expense_gate.is_approved():
    bm.record_expense(
        project_id,
        amount=5000,
        description="Q1 cloud services",
        category="infrastructure"
    )
```

### Workflow 3: Resource Optimization

```python
from core.project_cortex import ProjectManager

pm = ProjectManager()

# Automatically sleep idle projects
slept_projects = pm.auto_sleep_idle_projects(idle_threshold_minutes=30)
print(f"Put {len(slept_projects)} idle projects to sleep")

# Check capacity
summary = pm.get_project_summary()
print(f"Using {summary['active_projects']}/{summary['max_active']} slots")
print(f"Capacity: {summary['capacity_utilization']}")
```

## Module Combinations

### Combine All Three Modules

```python
from core.project_cortex import ProjectManager, BudgetManager
from agents import AgentRegistry
from core.decision_gates_structure import GateManager, ConfirmationHandler, GateType

# Setup
pm = ProjectManager()
bm = BudgetManager()
ar = AgentRegistry()
gm = GateManager()
ch = ConfirmationHandler()

# Create project
project = pm.create_project("Critical System Update")
bm.create_budget_profile(project.project_id, total_budget=100000)

# Assign specialists
ar.register_agent("sec-001", "Security Engineer")
ar.register_agent("ops-001", "Operations Architect")

# Require confirmation for critical action
conf_id = ch.request_confirmation(
    confirmation_id="system-update-001",
    message="Apply system-wide update? This affects all users.",
    timeout_seconds=300
)

# Create multi-level approval for deployment
deploy_gate = gm.create_gate(
    gate_type=GateType.APPROVAL,
    title="Critical System Deployment",
    required_approvers=['security-lead', 'ops-lead', 'cto']
)

# After all approvals and confirmations...
if ch.confirm(conf_id) and deploy_gate.is_approved():
    print("All approvals received, proceeding with update")
    bm.record_expense(project.project_id, 10000, "Deployment costs")
```

## Available Roles

Choose from 30+ predefined roles:

**Operations**: Operations Architect, Operations Manager  
**Frontend**: Frontend Architect, Frontend Developer, UI/UX Specialist  
**Backend**: Backend Architect, Backend Developer, API Specialist  
**Data**: Data Architect, Data Engineer, Data Scientist, ML Engineer  
**DevOps**: DevOps Architect, DevOps Engineer, SRE  
**Security**: Security Architect, Security Engineer  
**Testing**: QA Architect, QA Engineer  
**Design**: Design Lead, Visual Designer  
**Product**: Product Manager, Product Owner  
**Research**: Research Scientist, AI Researcher  

## Gate Types

Choose the right gate for your use case:

- **CONFIRMATION**: Simple yes/no decisions
- **APPROVAL**: Requires explicit approval from designated people
- **REVIEW**: Requires review before proceeding
- **MERGE_LOCK**: Blocks code merges until approved
- **OUTPUT_LOCK**: Locks output until confirmed (for sensitive data)

## Tips & Best Practices

1. **Start Small**: Begin with 1-2 projects to understand the workflow
2. **Use Sleep/Wake**: Optimize resources by sleeping idle projects
3. **Track Everything**: Use memory for important project data
4. **Gate Critical Actions**: Always require approval for production deployments
5. **Monitor Budget**: Check budget utilization regularly
6. **Assign Right Roles**: Match agent capabilities to task requirements

## Next Steps

- Read the [full documentation](PERSONAL_AI_OS_EXTENSION.md)
- Explore the [complete integration example](examples/complete_integration.py)
- Check module-specific READMEs:
  - [Project Cortex](core/project_cortex/README.md)
  - [Agents System](agents/README.md)
  - [Decision Gates](core/decision_gates_structure/README.md)

## Support

For detailed information:
- See [ARCHITECTURE.md](ARCHITECTURE.md) for system architecture
- See [AUTONOMOUS_SYSTEM.md](AUTONOMOUS_SYSTEM.md) for autonomous features
- Check the main [README.md](README.md) for VoBee AI Assistant

## Limits

- Active Projects: 50 (configurable)
- Total Projects: 100 (configurable)
- Agents: 100 (configurable)
- Decision Gates: Unlimited
- Agent Roles: 30+ predefined (extensible)

## Example Output

When you run the integration example, you'll see:

```
================================================================================
SYSTEM STATUS REPORT
================================================================================

[Project Cortex]
  Total Projects: 3
  Active Projects: 3/50
  Capacity Utilization: 6.0%

[Agents System]
  Total Agents: 7
  Capacity: 7.0%

[Decision Gates]
  Total Gates: 2
  Approved: 2
  Locked Outputs: 0
```

Happy building! 🚀
