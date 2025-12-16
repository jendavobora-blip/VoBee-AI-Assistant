# VoBee AI Operating System - Core Architecture

## Overview

Welcome to the **Personal AI Operating System** core architecture for VoBee AI Assistant. This system provides a robust foundation for managing complex AI workflows with three foundational pillars:

1. **Project Cortex** - Multi-project management with isolated contexts
2. **Decision Gate** - Strict YES/NO confirmation for critical actions
3. **Agent Registry** - Flexible role-based multi-agent system supporting 30-100+ roles

## Quick Start

### Installation

The core architecture requires only Python 3.7+. No additional dependencies are needed for the core components.

```bash
# Clone the repository
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant
```

### Running Examples

Test each component independently:

```bash
# Test Project Cortex
python core/project_cortex/example.py

# Test Decision Gate
python core/decision_gate/example.py

# Test Agent Registry
python agents/example.py
```

## Core Components

### 1. Project Cortex

Manage multiple projects with complete isolation:

```python
from core.project_cortex import ProjectManager

# Initialize
manager = ProjectManager()

# Create a project
project = manager.create_project(
    name="AI Research",
    description="Research new ML techniques",
    budget=50000,
    currency="USD"
)

# Add goals
project.add_goal("Literature review", priority=1)
project.add_goal("Implement prototype", priority=2)

# Track budget
project.budget.spend(5000, "compute")

# Store project-specific data
project.store_memory("model_config", {"lr": 0.001})
```

**Key Features:**
- Isolated memory per project
- Goal tracking with priorities
- Budget profiles with spend tracking
- Agent assignment and tracking
- State persistence

📖 [Read full documentation](docs/project_cortex.md)

### 2. Decision Gate

Control critical actions with explicit confirmation:

```python
from core.decision_gate import DecisionGate, DecisionType

# Initialize
gate = DecisionGate()

# Request a critical decision
decision = gate.request_decision(
    action_type="deploy",
    description="Deploy to production",
    decision_type=DecisionType.CRITICAL,
    context={"service": "api", "version": "2.0"}
)

# Approve
gate.approve_decision(decision.decision_id, approved_by="admin")

# Execute
result = gate.execute_decision(decision.decision_id, deploy_function)
```

**Key Features:**
- Four decision types (CRITICAL, HIGH, NORMAL, INFO)
- Approval workflow with audit trail
- Auto-approval rules (configurable)
- Decision expiration
- Complete audit logging

📖 [Read full documentation](docs/decision_gate.md)

### 3. Agent Registry

Manage a flexible, role-based multi-agent system:

```python
from agents import AgentRegistry
from agents.roles import initialize_default_roles

# Initialize with predefined roles
registry = AgentRegistry()
initialize_default_roles(registry)

# Create an agent
dev_role = registry.get_role_by_name("SoftwareEngineer")
agent = registry.create_agent(
    name="Agent Alpha",
    role_id=dev_role.role_id,
    skills={"python", "testing", "programming"}
)

# Assign a task
assigned_agent = registry.assign_task(
    task_id="task-001",
    capability="code_development"
)

# Complete task
registry.complete_task(agent.agent_id, "task-001")
```

**Key Features:**
- 15+ predefined roles (expandable to 100+)
- API-agnostic architecture
- Capability-based task routing
- Skill matching
- Dynamic agent assignment
- Statistics and monitoring

📖 [Read full documentation](docs/agent_registry.md)

## Integration Examples

### Example 1: Project with Decision Control

Combine Project Cortex with Decision Gate:

```python
from core.project_cortex import ProjectManager
from core.decision_gate import DecisionGate, DecisionType

manager = ProjectManager()
gate = DecisionGate()

# Create project
project = manager.create_project("New Feature", budget=25000)

# Request approval for budget allocation
decision = gate.request_decision(
    action_type="allocate_budget",
    description=f"Allocate $10k to development",
    decision_type=DecisionType.HIGH,
    context={"project_id": project.project_id, "amount": 10000}
)

# After approval, allocate
if gate.get_decision(decision.decision_id).status == DecisionStatus.APPROVED:
    project.budget.allocate("development", 10000)
```

### Example 2: Agent-Driven Project

Assign agents from registry to projects:

```python
from core.project_cortex import ProjectManager
from agents import AgentRegistry
from agents.roles import initialize_default_roles

manager = ProjectManager()
registry = AgentRegistry()
initialize_default_roles(registry)

# Create project
project = manager.create_project("Mobile App")

# Assign agents from registry
dev_agent = registry.find_available_agent(capability="code_development")
qa_agent = registry.find_available_agent(capability="testing")

if dev_agent:
    project.assign_agent(dev_agent.agent_id, "Developer")
if qa_agent:
    project.assign_agent(qa_agent.agent_id, "QA Engineer")

# Track work
project.increment_agent_tasks(dev_agent.agent_id)
```

### Example 3: Complete Workflow

All three components working together:

```python
from core.project_cortex import ProjectManager
from core.decision_gate import DecisionGate, DecisionType
from agents import AgentRegistry
from agents.roles import initialize_default_roles

# Initialize all components
manager = ProjectManager()
gate = DecisionGate()
registry = AgentRegistry()
initialize_default_roles(registry)

# 1. Create project
project = manager.create_project(
    name="Critical System Upgrade",
    budget=100000
)

# 2. Assign specialized agents
security_agent = registry.find_available_agent(
    role_id=registry.get_role_by_name("SecurityAnalyst").role_id
)
dev_agent = registry.find_available_agent(
    capability="code_development"
)

project.assign_agent(security_agent.agent_id, "Security Lead")
project.assign_agent(dev_agent.agent_id, "Lead Developer")

# 3. Request decision for critical action
decision = gate.request_decision(
    action_type="deploy_upgrade",
    description="Deploy system upgrade to production",
    decision_type=DecisionType.CRITICAL,
    context={
        "project_id": project.project_id,
        "agents_assigned": len(project.get_active_agents()),
        "budget_remaining": project.budget.remaining()
    }
)

# 4. After approval, execute with tracking
if gate.get_decision(decision.decision_id).status == DecisionStatus.APPROVED:
    # Execute deployment
    result = perform_deployment()
    
    # Update project state
    project.budget.spend(25000, "deployment")
    project.increment_agent_tasks(dev_agent.agent_id)
    
    # Mark decision as executed
    gate.execute_decision(decision.decision_id, lambda d: result)
```

## Architecture Principles

### Modularity
Each component is self-contained and can be used independently. You can use:
- Just Project Cortex for project management
- Just Decision Gate for approval workflows
- Just Agent Registry for agent coordination
- Any combination of the above

### Scalability
- Support for unlimited projects
- Agent Registry scales to 100+ roles
- Efficient capability indexing
- State persistence for all components

### Flexibility
- API-agnostic agent configuration
- Custom decision types
- Extensible role system
- Pluggable execution models

### Safety
- All critical actions require confirmation
- Complete audit trails
- Project isolation prevents cross-contamination
- Budget controls prevent overspending

## Directory Structure

```
VoBee-AI-Assistant/
├── core/                          # Core OS components
│   ├── __init__.py
│   ├── project_cortex/            # Multi-project management
│   │   ├── __init__.py
│   │   ├── project_manager.py     # Main implementation
│   │   └── example.py             # Usage example
│   └── decision_gate/             # Confirmation system
│       ├── __init__.py
│       ├── confirmation_system.py # Main implementation
│       └── example.py             # Usage example
├── agents/                        # Agent system
│   ├── __init__.py
│   ├── registry.py                # Registry implementation
│   ├── roles.py                   # Predefined roles (15+)
│   └── example.py                 # Usage example
└── docs/                          # Documentation
    ├── architecture.md            # Overall architecture
    ├── project_cortex.md          # Project Cortex guide
    ├── decision_gate.md           # Decision Gate guide
    └── agent_registry.md          # Agent Registry guide
```

## Predefined Agent Roles

The system includes 15 predefined roles across multiple categories:

**Research & Analysis**
- ResearchAnalyst
- DataScientist

**Development**
- SoftwareEngineer
- DevOpsEngineer

**Creative**
- ContentCreator
- VisualDesigner

**Coordination**
- ProjectManager
- QualityAssurance

**Support**
- CustomerSupport

**Specialized**
- SecurityAnalyst
- FinancialAnalyst

**AI-Specific**
- ModelTrainer
- DataCurator

**Automation & Monitoring**
- AutomationSpecialist
- SystemMonitor

Each role can have multiple agent instances, and new roles can be added dynamically without code changes.

## State Persistence

All components support state persistence:

```python
# Save state
manager.save_state("state/projects.json")
gate.save_state("state/decisions.json")
registry.save_state("state/agents.json")

# Load state
manager.load_state("state/projects.json")
gate.load_state("state/decisions.json")
registry.load_state("state/agents.json")
```

## API Design

All components use:
- **Clear, descriptive method names**
- **Consistent return types**
- **Comprehensive error handling**
- **Type hints** (Python 3.7+)
- **Detailed docstrings**

## Future Enhancements

### Planned Features
1. **REST API** - HTTP endpoints for all components
2. **WebSocket Support** - Real-time updates
3. **Inter-Project Communication** - Agents coordinate across projects
4. **Advanced Analytics** - Decision patterns, budget forecasting
5. **Role Marketplace** - Community-contributed agent roles
6. **Multi-tenancy** - Support for multiple organizations

### Extension Points
- Custom decision types
- Project templates
- Agent execution backends
- Budget calculators
- Goal hierarchies
- Custom capabilities

## Best Practices

1. **Use descriptive names** for projects, roles, and decisions
2. **Set budgets early** and track spending
3. **Break work into goals** for better tracking
4. **Assign appropriate decision types** - CRITICAL for irreversible actions
5. **Match agents by skills** for better task routing
6. **Save state regularly** to avoid data loss
7. **Review audit logs** for compliance and debugging
8. **Use auto-approval rules carefully** to maintain safety

## Documentation

- 📘 [Architecture Overview](docs/architecture.md) - System design and principles
- 📗 [Project Cortex Guide](docs/project_cortex.md) - Complete API reference
- 📙 [Decision Gate Guide](docs/decision_gate.md) - Confirmation system details
- 📕 [Agent Registry Guide](docs/agent_registry.md) - Role-based agent management

## Contributing

This is a modular system designed for extension. To add new features:

1. **New Agent Roles**: Add to `agents/roles.py` or create dynamically
2. **New Decision Types**: Extend `DecisionType` enum
3. **New Project Features**: Add methods to `Project` class
4. **New Capabilities**: Define in role creation

## License

MIT License - See LICENSE file for details

## Support

For questions and issues:
- 📖 Read the documentation in `/docs`
- 🔍 Check the example files
- 💬 Open an issue on GitHub

---

**Note**: This core architecture is designed to be the foundation for a Personal AI Operating System. Each component can operate independently or be combined for complex workflows. The system is production-ready and can be extended to support hundreds of agent roles and thousands of concurrent projects.
