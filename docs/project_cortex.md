# Project Cortex - Multi-Project Management System

## Overview

Project Cortex is the multi-project management core of the VoBee AI Operating System. It enables the system to handle multiple projects simultaneously, each with:

- Isolated memory and context
- Defined goals and objectives
- Budget profiles and tracking
- Active agent assignments

## Core Concepts

### Projects

A **Project** represents a distinct unit of work with:
- Unique identifier
- Name and description
- Status (active, paused, completed, archived)
- Creation and update timestamps

### Project Memory

Each project maintains **isolated memory** - a key-value store for project-specific data:

```python
# Store data
project.store_memory("api_key", "sk-...")
project.store_memory("config", {"env": "production"})

# Retrieve data
api_key = project.retrieve_memory("api_key")
config = project.retrieve_memory("config", default={})

# Clear all memory
project.clear_memory()
```

**Use Cases**:
- API credentials per project
- Configuration settings
- Cached results
- Intermediate computations
- Project-specific preferences

### Goals

Projects track **goals** - specific objectives to accomplish:

```python
# Add goals
goal1 = project.add_goal("Deploy to production", priority=1)
goal2 = project.add_goal("Write documentation", priority=2)

# Complete a goal
project.complete_goal(goal1.goal_id)

# Get pending goals
pending = project.get_pending_goals()
```

Each goal includes:
- Unique ID
- Description
- Priority (lower number = higher priority)
- Completion status
- Timestamps (created, completed)

### Budget Profiles

Each project has a **budget profile** for financial tracking:

```python
# Set budget
project.set_budget(total=50000, currency="USD")

# Allocate budget
project.budget.allocate("development", 30000)
project.budget.allocate("marketing", 15000)

# Spend budget
project.budget.spend(5000, category="development")

# Check remaining
remaining = project.budget.remaining()  # 45000
```

Budget features:
- Total budget and currency
- Category-based allocation
- Spend tracking
- Remaining calculation

### Agent Assignments

Projects track **which agents are working on them**:

```python
# Assign agents
project.assign_agent("agent-001", role="Developer")
project.assign_agent("agent-002", role="Designer")

# Update agent status
project.update_agent_status("agent-001", "busy")

# Track completed tasks
project.increment_agent_tasks("agent-001")

# Get active agents
active = project.get_active_agents()

# Remove agent
project.remove_agent("agent-002")
```

## Project Manager

The **ProjectManager** coordinates all projects in the system.

### Creating Projects

```python
from core.project_cortex import ProjectManager

manager = ProjectManager()

# Create a project
project = manager.create_project(
    name="Website Redesign",
    description="Modernize company website",
    budget=25000,
    currency="USD"
)
```

### Managing Projects

```python
# Get project by ID
project = manager.get_project(project_id)

# Get project by name
project = manager.get_project_by_name("Website Redesign")

# List all projects
all_projects = manager.list_projects()

# List by status
from core.project_cortex import ProjectStatus
active_projects = manager.list_projects(status=ProjectStatus.ACTIVE)

# Delete a project
manager.delete_project(project_id)
```

### Active Project

The manager maintains an **active project** - the current focus:

```python
# Get active project
current = manager.get_active_project()

# Switch active project
manager.set_active_project(another_project_id)
```

### Cross-Project Queries

```python
# Get all active agents across all projects
all_agents = manager.get_all_active_agents()
# Returns: {project_id: [AgentAssignment, ...], ...}
```

### State Persistence

```python
# Save all projects to file
manager.save_state("projects.json")

# Load projects from file
manager.load_state("projects.json")
```

State includes:
- All projects with full data
- Active project ID
- Complete memory, goals, budgets, agents

## Usage Patterns

### Pattern 1: Client Projects

```python
# Separate client projects
client_a = manager.create_project("Client A - Mobile App")
client_b = manager.create_project("Client B - Website")

# Each has isolated memory
client_a.store_memory("brand_colors", {"primary": "#FF0000"})
client_b.store_memory("brand_colors", {"primary": "#0000FF"})

# Each has separate budget
client_a.set_budget(100000, "USD")
client_b.set_budget(50000, "USD")
```

### Pattern 2: R&D Initiatives

```python
# Research projects with experiments
ml_research = manager.create_project("ML Model Research")
ml_research.add_goal("Literature review", priority=1)
ml_research.add_goal("Dataset collection", priority=2)
ml_research.add_goal("Model training", priority=3)

# Store experimental results
ml_research.store_memory("experiment_1", {
    "accuracy": 0.87,
    "parameters": {"lr": 0.001}
})
```

### Pattern 3: Product Development

```python
# Product with milestones as goals
product = manager.create_project("SaaS Product v2.0")
product.set_budget(200000, "USD")

# Milestones
product.add_goal("Alpha release", priority=1)
product.add_goal("Beta testing", priority=2)
product.add_goal("Production launch", priority=3)

# Team assignments
product.assign_agent("dev-team-lead", "Project Manager")
product.assign_agent("frontend-dev-1", "Frontend Developer")
product.assign_agent("backend-dev-1", "Backend Developer")
```

## API Reference

### Project Class

**Methods**:
- `add_goal(description, priority=1)` - Add a goal
- `complete_goal(goal_id)` - Mark goal complete
- `assign_agent(agent_id, role)` - Assign agent
- `remove_agent(agent_id)` - Remove agent
- `update_agent_status(agent_id, status)` - Update agent status
- `increment_agent_tasks(agent_id)` - Increment task count
- `set_budget(total, currency)` - Set budget
- `store_memory(key, value)` - Store in memory
- `retrieve_memory(key, default)` - Retrieve from memory
- `clear_memory()` - Clear all memory
- `change_status(status)` - Change project status
- `get_active_agents()` - Get active agents
- `get_pending_goals()` - Get pending goals
- `to_dict()` - Export to dictionary

**Properties**:
- `project_id` - Unique ID
- `name` - Project name
- `description` - Description
- `status` - Current status
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `memory` - Memory dict
- `goals` - List of goals
- `budget` - BudgetProfile instance
- `agents` - Dict of agent assignments

### ProjectManager Class

**Methods**:
- `create_project(name, description, budget, currency)` - Create project
- `get_project(project_id)` - Get by ID
- `get_project_by_name(name)` - Get by name
- `list_projects(status)` - List projects
- `delete_project(project_id)` - Delete project
- `set_active_project(project_id)` - Set active
- `get_active_project()` - Get active
- `get_all_active_agents()` - Get all agents
- `save_state(filepath)` - Save to JSON
- `load_state(filepath)` - Load from JSON

## Best Practices

1. **Use descriptive names**: Make project names clear and unique
2. **Set budgets early**: Establish budget before spending
3. **Track goals**: Break work into measurable goals
4. **Clean memory**: Clear unused memory to save space
5. **Archive completed**: Set status to ARCHIVED when done
6. **Save state regularly**: Persist state to avoid data loss

## Integration with Other Components

### With Decision Gate

```python
# Require approval for budget changes
decision = gate.request_decision(
    action_type="set_budget",
    description=f"Set budget for {project.name}",
    decision_type=DecisionType.CRITICAL,
    context={"project_id": project.project_id, "amount": 100000}
)
```

### With Agent Registry

```python
# Assign agents from registry to project
agent = registry.find_available_agent(capability="development")
if agent:
    project.assign_agent(agent.agent_id, agent.role_id)
```

## Example: Complete Workflow

See `core/project_cortex/example.py` for a complete working example.

```bash
python core/project_cortex/example.py
```
