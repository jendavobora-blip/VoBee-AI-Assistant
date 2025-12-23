# Personal AI Operating System - Core Architecture

## Overview

This documentation describes the core architecture for VoBee AI Assistant as it evolves into a **Personal AI Operating System**. The system is designed around three foundational pillars:

1. **Project Cortex** - Multi-project management
2. **Decision Gate** - Strict confirmation system
3. **Agent Registry** - Role-based multi-agent system

## Architecture Principles

### Design Goals

- **Modularity**: Each component is self-contained and independently useful
- **Scalability**: Support for 30-100+ agent roles without hard-coding
- **Flexibility**: API-agnostic design that doesn't lock into specific providers
- **Safety**: All critical actions require explicit confirmation
- **Isolation**: Projects maintain separate memory and context

### Directory Structure

```
VoBee-AI-Assistant/
├── core/                          # Core operating system components
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
│   ├── registry.py                # Agent registry implementation
│   ├── roles.py                   # Predefined role definitions
│   └── example.py                 # Usage example
└── docs/                          # Documentation
    ├── architecture.md            # This file
    ├── project_cortex.md          # Project Cortex details
    ├── decision_gate.md           # Decision Gate details
    └── agent_registry.md          # Agent Registry details
```

## Core Components

### 1. Project Cortex

**Purpose**: Manage multiple projects with complete isolation

**Key Features**:
- Unique project IDs with metadata
- Isolated memory/context per project
- Goal tracking and completion
- Budget profiles with spend tracking
- Active agent assignments

**Use Cases**:
- Managing multiple client projects
- Separate R&D initiatives
- Distinct product development efforts
- Isolated testing environments

### 2. Decision Gate

**Purpose**: Control all critical actions with YES/NO confirmations

**Key Features**:
- Four decision types (CRITICAL, HIGH, NORMAL, INFO)
- Strict approval workflow
- Complete audit trail
- Auto-approval rules (configurable)
- Decision expiration

**Use Cases**:
- Production deployments
- Budget approvals
- Data deletions
- System configuration changes
- Critical AI actions

### 3. Agent Registry

**Purpose**: Manage a flexible, role-based multi-agent system

**Key Features**:
- 15+ predefined roles (expandable to 100+)
- Capability-based task routing
- API-agnostic architecture
- Dynamic agent assignment
- Status tracking and statistics

**Use Cases**:
- Distributed task execution
- Specialized agent teams
- Resource allocation
- Workload balancing

## Integration Patterns

### Pattern 1: Project-Scoped Agents

Combine Project Cortex with Agent Registry to assign agents to specific projects:

```python
# Create a project
project = manager.create_project("AI Research", budget=50000)

# Assign agents to the project
project.assign_agent("agent-001", "ResearchAnalyst")
project.assign_agent("agent-002", "DataScientist")

# Track agent work within project context
project.increment_agent_tasks("agent-001")
```

### Pattern 2: Confirmed Actions

Use Decision Gate to control project actions:

```python
# Request decision for budget spend
decision = gate.request_decision(
    action_type="budget_spend",
    description=f"Spend $10,000 on GPU compute",
    decision_type=DecisionType.CRITICAL,
    context={"project_id": project.project_id, "amount": 10000}
)

# Wait for approval
if decision.status == DecisionStatus.APPROVED:
    project.budget.spend(10000, "compute")
```

### Pattern 3: Capability-Based Routing

Route tasks to agents based on capabilities:

```python
# Find agent with specific capability
agent = registry.assign_task(
    task_id="task-123",
    capability="ml_modeling",
    required_skills={"python", "pytorch"}
)

# Complete and track
registry.complete_task(agent.agent_id, "task-123")
```

## Implementation Decisions

### Why Three Pillars?

1. **Project Cortex**: Organizations need to manage multiple initiatives simultaneously with clear boundaries
2. **Decision Gate**: Autonomous systems need human oversight for critical actions
3. **Agent Registry**: Different tasks require different specialized capabilities

### Why API-Agnostic?

- Flexibility to switch providers (OpenAI, Anthropic, local models)
- Cost optimization across different tasks
- Avoid vendor lock-in
- Support for custom implementations

### Why Role-Based?

- Scales to 100+ specialized roles
- Clear separation of concerns
- Easy to extend without modifying core code
- Natural mapping to real-world workflows

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

## Future Enhancements

### Planned Features

1. **Inter-Project Communication**: Allow agents to coordinate across projects
2. **Advanced Budgeting**: Multi-currency support, forecasting, alerts
3. **Agent Learning**: Agents improve based on task completion success
4. **Decision Analytics**: Patterns in decision-making
5. **Role Marketplace**: Community-contributed agent roles

### Extension Points

- Custom decision types
- Project templates
- Agent execution backends
- Budget calculators
- Goal hierarchies

## Getting Started

See the individual component documentation:
- [Project Cortex Documentation](project_cortex.md)
- [Decision Gate Documentation](decision_gate.md)
- [Agent Registry Documentation](agent_registry.md)

Or run the examples:
```bash
python core/project_cortex/example.py
python core/decision_gate/example.py
python agents/example.py
```
