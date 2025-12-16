# Project Cortex

## Overview

Project Cortex is the central project management system for VoBee AI Assistant. It provides capabilities for managing multiple projects with isolated contexts, including memory, goals, budgets, and agent assignments.

## Features

### Multi-Project Management
- Create and manage multiple isolated projects
- Each project has its own memory, goals, and budget
- Project lifecycle management (active, sleeping, paused, completed, archived)

### Isolated Project Context
- **Memory**: Key-value storage for project-specific data
- **Goals**: Prioritized goal tracking with metadata
- **Budget**: Track allocated budget and expenditures

### Agent Tracking
- Track active agents assigned to each project
- Monitor agent status (active, idle, sleeping, error)
- Sleep/wake capabilities for resource management

### Sleep/Wake Capabilities
- Put projects to sleep to conserve resources
- Wake projects when needed
- Automatically manages agent states during sleep/wake cycles

## Usage

### Basic Example

```python
from core.project_cortex import ProjectCortex, ProjectStatus, AgentStatus

# Initialize the cortex
cortex = ProjectCortex()

# Create a new project
project = cortex.create_project(
    name="AI Backend System",
    description="Build scalable backend for AI services",
    budget=10000.0
)

# Add goals to the project
project.add_goal(
    goal="Design database schema",
    priority=1,
    metadata={"complexity": "high"}
)

# Update project memory
project.update_memory("database_type", "PostgreSQL")
project.update_memory("api_framework", "FastAPI")

# Track an agent working on the project
project.track_agent(
    agent_id="agent-001",
    role="backend_builder",
    status=AgentStatus.ACTIVE
)

# Track budget expenditure
project.update_budget(250.0)

# Put project to sleep when not in use
project.sleep()

# Wake project when needed
project.wake()
```

### Managing Multiple Projects

```python
# List all active projects
active_projects = cortex.list_projects(status=ProjectStatus.ACTIVE)

# Get specific project
project = cortex.get_project(project_id="...")

# Get statistics
stats = cortex.to_dict()
print(f"Total projects: {stats['total_projects']}")
print(f"Active projects: {stats['active_projects']}")
print(f"Total budget spent: ${stats['total_budget_spent']}")
```

## Architecture

### ProjectCortex
The main management class that coordinates all projects.

**Key Methods:**
- `create_project()`: Create a new isolated project
- `get_project()`: Retrieve project by ID
- `list_projects()`: List all projects with optional filtering
- `sleep_project()`: Put a project to sleep
- `wake_project()`: Wake a sleeping project

### Project
Represents an individual project with isolated context.

**Key Methods:**
- `add_goal()`: Add a prioritized goal
- `update_memory()` / `get_memory()`: Manage project memory
- `track_agent()`: Assign and track agents
- `update_budget()`: Track expenditures
- `sleep()` / `wake()`: Manage project lifecycle

## Design Principles

1. **Isolation**: Each project has completely isolated context
2. **Extensibility**: Easy to add new capabilities without breaking existing code
3. **Resource Management**: Sleep/wake enables efficient resource allocation
4. **Auditability**: All changes are timestamped and trackable
5. **Modularity**: Clear boundaries between projects and agents

## Future Extensions

This is a foundational skeleton designed for rapid expansion:

- Persistent storage backend
- Event-driven architecture for project state changes
- Advanced budget forecasting and alerts
- Agent collaboration patterns
- Project templates and blueprints
- Cross-project resource sharing
- Advanced scheduling and prioritization

## Status

**Current Version**: 0.1.0 (Skeleton)

This is a MAX_SPEED implementation focusing on structural foundations. Full functionality will be added in future iterations.
