# Project Cortex - Multi-Project Management Brain

Project Cortex is the central orchestration module for managing 1-50 parallel projects with complete isolation, resource management, and lifecycle control.

## Overview

Project Cortex provides a comprehensive framework for managing multiple concurrent projects, each with:
- **Isolated Memory**: Separate memory spaces (short-term, long-term, context)
- **Goal Tracking**: Define and monitor project objectives
- **Budget Management**: Financial tracking with transaction history
- **Agent Assignment**: Track and manage agents working on projects
- **Sleep/Wake Capabilities**: Resource optimization through project hibernation

## Components

### 1. ProjectManager
Central orchestrator for all projects. Manages project lifecycle and enforces limits.

**Key Features:**
- Support for up to 50 active projects
- Support for up to 100 total projects (including sleeping/archived)
- Automatic idle project detection and sleep
- Project status management (active, sleeping, paused, completed, archived)

**Example Usage:**
```python
from core.project_cortex import ProjectManager

# Initialize manager
pm = ProjectManager()

# Create a new project
project = pm.create_project(
    name="AI Research Initiative",
    description="Research and implement new AI models",
    budget={'total': 100000, 'currency': 'USD'},
    goals=['Implement GPT-4 integration', 'Deploy to production']
)

# Get project summary
summary = pm.get_project_summary()
print(f"Active projects: {summary['active_projects']}/{summary['max_active']}")

# Sleep idle projects (auto-optimization)
slept = pm.auto_sleep_idle_projects(idle_threshold_minutes=30)
```

### 2. Project
Individual project entity with complete isolation.

**Key Features:**
- Status lifecycle management
- Goal tracking and updates
- Budget operations (spending, allocation)
- Agent assignment
- Project-specific memory storage
- Sleep/wake state tracking

**Example Usage:**
```python
# Add goals
project.add_goal("Complete testing phase")

# Update budget
project.update_budget(5000, operation="spend")

# Assign agents
project.assign_agent("agent-123", "Backend Developer")

# Store project memory
project.store_memory("api_endpoint", "https://api.example.com")

# Put project to sleep
project.sleep()

# Wake up project
project.wake()
```

### 3. MemoryManager
Manages isolated memory for each project with multiple memory types.

**Memory Types:**
- **short_term**: Temporary session-based memory
- **long_term**: Persistent memory across sessions
- **context**: Current execution context/state

**Example Usage:**
```python
from core.project_cortex import MemoryManager

mm = MemoryManager()

# Store different types of memory
mm.store(project_id, "session_token", "abc123", memory_type="short_term")
mm.store(project_id, "api_key", "secret", memory_type="long_term")
mm.store(project_id, "current_step", 3, memory_type="context")

# Retrieve memory
token = mm.retrieve(project_id, "session_token", memory_type="short_term")

# Search memory
results = mm.search_memory(project_id, "api")

# Clear short-term memory
mm.clear_short_term(project_id)
```

### 4. BudgetManager
Handles financial tracking and budget allocation for projects.

**Key Features:**
- Multi-currency support
- Transaction history
- Budget reservation system
- Expense tracking by category
- Utilization monitoring

**Example Usage:**
```python
from core.project_cortex import BudgetManager

bm = BudgetManager()

# Create budget profile
bm.create_budget_profile(project_id, total_budget=50000, currency="USD")

# Record expense
bm.record_expense(
    project_id,
    amount=1500,
    description="Cloud infrastructure costs",
    category="infrastructure"
)

# Reserve budget for planned expense
bm.reserve_budget(project_id, amount=5000, description="GPU cluster rental")

# Get budget summary
summary = bm.get_budget_summary(project_id)
print(f"Budget utilization: {summary['utilization_percent']}%")

# Get transaction history
transactions = bm.get_transaction_history(project_id, limit=10)
```

### 5. AgentTracker
Tracks agent assignments and monitors agent activity across projects.

**Key Features:**
- Agent registry with capabilities
- Project assignment tracking
- Agent status management (available/assigned)
- Performance metrics
- Activity monitoring

**Example Usage:**
```python
from core.project_cortex import AgentTracker

at = AgentTracker()

# Register an agent
at.register_agent(
    agent_id="agent-001",
    role="Backend Developer",
    capabilities=["Python", "FastAPI", "PostgreSQL"],
    metadata={"experience_level": "senior"}
)

# Assign agent to project
at.assign_agent_to_project(
    project_id,
    agent_id="agent-001",
    assignment_details={"primary_focus": "API development"}
)

# Update agent activity
at.update_agent_activity(project_id, "agent-001", task_completed=True)

# Get agent performance
performance = at.get_agent_performance("agent-001")

# Get available agents
available = at.get_available_agents()
```

## Integration Example

Complete example integrating all components:

```python
from core.project_cortex import (
    ProjectManager,
    MemoryManager,
    BudgetManager,
    AgentTracker
)

# Initialize all managers
pm = ProjectManager()
mm = MemoryManager()
bm = BudgetManager()
at = AgentTracker()

# Create a new project
project = pm.create_project(
    name="Mobile App Development",
    description="Build iOS and Android apps",
    budget={'total': 75000, 'currency': 'USD'},
    goals=['Complete UI/UX design', 'Implement core features', 'Launch beta']
)

# Setup budget tracking
bm.create_budget_profile(project.project_id, total_budget=75000, currency="USD")

# Initialize project memory
mm.create_project_memory(project.project_id)
mm.store(project.project_id, "tech_stack", ["React Native", "Node.js", "MongoDB"])

# Register and assign agents
at.register_agent("dev-001", "Frontend Developer", ["React", "React Native"])
at.register_agent("dev-002", "Backend Developer", ["Node.js", "MongoDB"])
at.assign_agent_to_project(project.project_id, "dev-001")
at.assign_agent_to_project(project.project_id, "dev-002")

# Track expenses
bm.record_expense(project.project_id, 5000, "Design tools subscription", "software")

# Monitor progress
print(f"Project: {project.name}")
print(f"Active agents: {len(at.get_project_agents(project.project_id))}")
print(f"Budget remaining: ${bm.get_budget(project.project_id)['remaining']}")

# Optimize resources - sleep idle projects
pm.auto_sleep_idle_projects(idle_threshold_minutes=30)
```

## Architecture

```
Project Cortex
├── ProjectManager (Orchestration)
│   ├── Project Lifecycle Management
│   ├── Resource Allocation
│   └── Auto-optimization
├── Project (Entity)
│   ├── Status Management
│   ├── Goal Tracking
│   └── Sleep/Wake State
├── MemoryManager (Data)
│   ├── Short-term Memory
│   ├── Long-term Memory
│   └── Context Memory
├── BudgetManager (Financial)
│   ├── Budget Tracking
│   ├── Transaction History
│   └── Reservations
└── AgentTracker (Resources)
    ├── Agent Registry
    ├── Assignments
    └── Performance Metrics
```

## Limits and Constraints

- **Max Active Projects**: 50
- **Max Total Projects**: 100 (including sleeping/archived)
- **Memory Types**: 3 per project (short_term, long_term, context)
- **Agent Status**: available, assigned
- **Project Status**: active, sleeping, paused, completed, archived

## Best Practices

1. **Use Sleep/Wake for Resource Optimization**: Put idle projects to sleep to free resources
2. **Track Budget Carefully**: Use categories for expenses to understand spending patterns
3. **Leverage Memory Types**: Use appropriate memory type for data lifecycle
4. **Monitor Agent Performance**: Track agent activity to optimize assignments
5. **Set Clear Goals**: Define measurable project goals for better tracking
6. **Regular Auto-Sleep**: Run auto-sleep periodically to optimize resource usage

## Export/Import

All managers support data export/import for persistence:

```python
# Export project data
data = pm.to_dict()

# Import project data
pm.from_dict(data)
```
