# Getting Started with VoBee AI Operating System

## Quick Start Guide

This guide will help you get started with the VoBee AI Operating System core architecture.

## Prerequisites

- Python 3.7 or higher
- No external dependencies required for core components

## Installation

```bash
# Clone the repository
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant
```

## Running Examples

### 1. Project Cortex Example

Manage multiple projects with isolated contexts:

```bash
python core/project_cortex/example.py
```

**What it demonstrates:**
- Creating projects with budgets
- Adding and tracking goals
- Assigning agents to projects
- Managing project memory
- Budget spending and tracking

### 2. Decision Gate Example

Control critical actions with confirmations:

```bash
python core/decision_gate/example.py
```

**What it demonstrates:**
- Requesting decisions for critical actions
- Approving and rejecting decisions
- Executing approved decisions
- Viewing audit trail
- State persistence

### 3. Agent Registry Example

Manage role-based agent system:

```bash
python agents/example.py
```

**What it demonstrates:**
- Loading predefined agent roles
- Creating agent instances
- Assigning tasks by capability
- Completing tasks
- Viewing registry statistics

### 4. Complete Integration Example

See all components working together:

```bash
python examples/complete_integration.py
```

**What it demonstrates:**
- Creating a production upgrade project
- Assigning specialized agents
- Requesting budget approval
- Simulating work progress
- Critical deployment decision
- Full audit trail and statistics

## Basic Usage

### Project Management

```python
from core.project_cortex import ProjectManager

# Create manager
manager = ProjectManager()

# Create a project
project = manager.create_project(
    name="My Project",
    description="Project description",
    budget=10000,
    currency="USD"
)

# Add goals
project.add_goal("Complete phase 1", priority=1)

# Store project data
project.store_memory("api_key", "sk-...")

# Track spending
project.budget.spend(1000, "development")
```

### Decision Control

```python
from core.decision_gate import DecisionGate, DecisionType

# Create gate
gate = DecisionGate()

# Request decision
decision = gate.request_decision(
    action_type="deploy",
    description="Deploy to production",
    decision_type=DecisionType.CRITICAL
)

# Approve
gate.approve_decision(decision.decision_id, approved_by="admin")

# Execute
result = gate.execute_decision(decision.decision_id, my_function)
```

### Agent Coordination

```python
from agents import AgentRegistry
from agents.roles import initialize_default_roles

# Create registry
registry = AgentRegistry()
initialize_default_roles(registry)

# Create agent
role = registry.get_role_by_name("SoftwareEngineer")
agent = registry.create_agent(
    name="Agent 1",
    role_id=role.role_id,
    skills={"python", "testing"}
)

# Assign task
assigned = registry.assign_task(
    task_id="task-1",
    capability="code_development"
)
```

## Documentation

Comprehensive documentation is available in the `/docs` folder:

- **[README](docs/README.md)** - Overview and getting started
- **[Architecture](docs/architecture.md)** - System design and principles
- **[Project Cortex](docs/project_cortex.md)** - Multi-project management guide
- **[Decision Gate](docs/decision_gate.md)** - Confirmation system guide
- **[Agent Registry](docs/agent_registry.md)** - Role-based agent system guide

## File Structure

```
VoBee-AI-Assistant/
├── core/                      # Core OS components
│   ├── project_cortex/        # Multi-project management
│   └── decision_gate/         # Confirmation system
├── agents/                    # Agent registry and roles
├── docs/                      # Documentation
└── examples/                  # Working examples
```

## Common Use Cases

### 1. Managing Multiple Client Projects

```python
# Create separate projects for each client
client_a = manager.create_project("Client A - Website")
client_b = manager.create_project("Client B - Mobile App")

# Each has isolated budget and memory
client_a.set_budget(50000, "USD")
client_b.set_budget(75000, "USD")
```

### 2. Requiring Approval for Critical Actions

```python
# Request approval before deployment
decision = gate.request_decision(
    action_type="production_deploy",
    description="Deploy v2.0 to production",
    decision_type=DecisionType.CRITICAL
)

# Deployment only happens after approval
```

### 3. Building Specialized Teams

```python
# Assign different agent roles to a project
security = registry.create_agent("Security-1", security_role.role_id, ...)
developer = registry.create_agent("Dev-1", dev_role.role_id, ...)
qa = registry.create_agent("QA-1", qa_role.role_id, ...)

project.assign_agent(security.agent_id, "Security Lead")
project.assign_agent(developer.agent_id, "Developer")
project.assign_agent(qa.agent_id, "QA Engineer")
```

## State Persistence

Save and restore state for all components:

```python
# Save
manager.save_state("projects.json")
gate.save_state("decisions.json")
registry.save_state("agents.json")

# Load
manager.load_state("projects.json")
gate.load_state("decisions.json")
registry.load_state("agents.json")
```

## Next Steps

1. **Run the examples** to see the components in action
2. **Read the documentation** for detailed API references
3. **Start building** your own AI workflows
4. **Extend the system** with custom roles and capabilities

## Support

- 📖 Check `/docs` for detailed documentation
- 🔍 Review example code in each component
- 💬 Open an issue on GitHub for questions

## Architecture Principles

- **Modular**: Use components independently or together
- **Scalable**: Supports unlimited projects and 100+ agent roles
- **Flexible**: API-agnostic, no vendor lock-in
- **Safe**: Critical actions require explicit confirmation
- **Persistent**: Complete state management

---

**The VoBee AI Operating System is ready to power your AI workflows!** 🚀
