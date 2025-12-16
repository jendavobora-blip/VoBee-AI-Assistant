# Agent Registry - Role-Based Multi-Agent System

## Overview

The Agent Registry is a flexible, extensible system for managing 30-100+ logical agent roles without hard-coding API dependencies. It provides a role-based architecture that separates logical capabilities from implementation details.

## Core Concepts

### Roles vs Agents

- **Role**: A logical function in the system (e.g., "Software Engineer", "Data Analyst")
- **Agent**: A specific instance fulfilling a role

This separation allows:
- Multiple agents per role
- API-agnostic implementations
- Dynamic role creation
- Flexible execution models

### Capabilities

**Capabilities** define what a role can do:

```python
from agents import AgentCapability

capability = AgentCapability(
    name="code_review",
    description="Review code for quality and bugs",
    required_skills=["programming", "code-analysis"]
)
```

Each capability specifies:
- Name (identifier)
- Description (what it does)
- Required skills
- Optional parameters

### Skills

**Skills** are attributes that agents possess:

```python
agent_skills = {"python", "testing", "code-review", "git"}
```

Agents are matched to tasks based on skill requirements.

## Basic Usage

### Initialize Registry

```python
from agents import AgentRegistry
from agents.roles import initialize_default_roles

# Create registry
registry = AgentRegistry()

# Load 15+ predefined roles
initialize_default_roles(registry)

# Check what was loaded
print(f"Loaded {len(registry.list_roles())} roles")
```

### Create Custom Role

```python
from agents import AgentCapability

# Define capabilities
capabilities = [
    AgentCapability(
        name="database_optimization",
        description="Optimize database queries",
        required_skills=["sql", "performance-tuning"]
    ),
    AgentCapability(
        name="schema_design",
        description="Design database schemas",
        required_skills=["sql", "data-modeling"]
    )
]

# Create role
role = registry.create_role(
    name="DatabaseSpecialist",
    description="Expert in database management and optimization",
    capabilities=capabilities,
    priority=5,
    max_concurrent_tasks=3
)
```

### Create Agents

```python
# Get a role
dev_role = registry.get_role_by_name("SoftwareEngineer")

# Create agent instance
agent = registry.create_agent(
    name="Agent Alpha",
    role_id=dev_role.role_id,
    skills={"python", "javascript", "testing", "programming", "software-design"},
    api_config={
        "provider": "openai",
        "model": "gpt-4",
        "temperature": 0.7
    }
)
```

### Assign Tasks

```python
# Assign by specific agent
agent = registry.assign_task(
    task_id="task-001",
    agent_id="specific-agent-id"
)

# Assign by role
agent = registry.assign_task(
    task_id="task-002",
    role_id=dev_role.role_id
)

# Assign by capability
agent = registry.assign_task(
    task_id="task-003",
    capability="code_development"
)

# Assign by required skills
agent = registry.assign_task(
    task_id="task-004",
    required_skills={"python", "testing"}
)
```

### Complete Tasks

```python
# Mark task complete
success = registry.complete_task(
    agent_id=agent.agent_id,
    task_id="task-001"
)

# Agent automatically becomes available again
```

## Predefined Roles

The system includes 15+ predefined roles (see `agents/roles.py`):

### Research & Analysis
- **ResearchAnalyst**: Web research and data analysis
- **DataScientist**: ML modeling and visualization

### Development
- **SoftwareEngineer**: Code development and testing
- **DevOpsEngineer**: Deployment and monitoring

### Creative
- **ContentCreator**: Writing and documentation
- **VisualDesigner**: Image generation and UI design

### Coordination
- **ProjectManager**: Task planning and resource allocation
- **QualityAssurance**: Quality review and testing

### Support
- **CustomerSupport**: User assistance and documentation

### Specialized
- **SecurityAnalyst**: Security audits and vulnerability assessment
- **FinancialAnalyst**: Budget analysis and forecasting

### AI-Specific
- **ModelTrainer**: ML model training and tuning
- **DataCurator**: Data collection and cleaning

### Automation
- **AutomationSpecialist**: Workflow automation and optimization

### Monitoring
- **SystemMonitor**: Health monitoring and alerting

## Advanced Features

### Finding Agents

```python
# Find available agent by role
agent = registry.find_available_agent(role_id=dev_role.role_id)

# Find by capability
agent = registry.find_available_agent(capability="ml_modeling")

# Find by skills
agent = registry.find_available_agent(
    required_skills={"python", "pytorch", "ml"}
)

# Combine criteria
agent = registry.find_available_agent(
    role_id=dev_role.role_id,
    required_skills={"python", "testing"}
)
```

### List and Filter

```python
# List all agents
all_agents = registry.list_agents()

# Filter by role
dev_agents = registry.list_agents(role_id=dev_role.role_id)

# Filter by status
from agents import AgentStatus
available = registry.list_agents(status=AgentStatus.AVAILABLE)
busy = registry.list_agents(status=AgentStatus.BUSY)
```

### Statistics

```python
stats = registry.get_statistics()

print(f"Total Roles: {stats['total_roles']}")
print(f"Total Agents: {stats['total_agents']}")
print(f"By Status: {stats['agents_by_status']}")
print(f"By Role: {stats['agents_by_role']}")
print(f"Tasks Completed: {stats['total_tasks_completed']}")
print(f"Active Tasks: {stats['active_tasks']}")
```

### Agent Status Management

```python
# Agents automatically transition:
# AVAILABLE -> BUSY (when task assigned)
# BUSY -> AVAILABLE (when all tasks complete)

# Manual status updates
agent.update_status(AgentStatus.OFFLINE)
agent.update_status(AgentStatus.ERROR)
agent.update_status(AgentStatus.AVAILABLE)
```

### Custom Execution

Agents can have custom execution functions:

```python
def custom_executor(task_data):
    """Custom execution logic"""
    # Your implementation here
    return {"result": "success"}

agent = registry.create_agent(
    name="Custom Agent",
    role_id=role.role_id,
    skills={"custom"},
    executor=custom_executor
)

# Later, execute tasks with custom logic
if agent.executor:
    result = agent.executor(task_data)
```

## API-Agnostic Design

The registry doesn't hard-code API providers:

```python
# OpenAI agent
openai_agent = registry.create_agent(
    name="GPT-4 Agent",
    role_id=role_id,
    skills=required_skills,
    api_config={
        "provider": "openai",
        "model": "gpt-4",
        "api_key_ref": "OPENAI_API_KEY"
    }
)

# Anthropic agent
anthropic_agent = registry.create_agent(
    name="Claude Agent",
    role_id=role_id,
    skills=required_skills,
    api_config={
        "provider": "anthropic",
        "model": "claude-3-opus",
        "api_key_ref": "ANTHROPIC_API_KEY"
    }
)

# Local model agent
local_agent = registry.create_agent(
    name="Local Agent",
    role_id=role_id,
    skills=required_skills,
    api_config={
        "provider": "local",
        "model_path": "/models/llama-7b",
        "device": "cuda"
    }
)
```

## Usage Patterns

### Pattern 1: Task Queue Processing

```python
# Get tasks from queue
tasks = get_pending_tasks()

for task in tasks:
    # Find appropriate agent
    agent = registry.assign_task(
        task_id=task["id"],
        capability=task["required_capability"],
        required_skills=set(task.get("required_skills", []))
    )
    
    if agent:
        # Execute task with agent
        execute_task(task, agent)
    else:
        # No available agent, requeue
        requeue_task(task)
```

### Pattern 2: Specialized Teams

```python
# Create a specialized team for a project
team = {
    "pm": registry.create_agent("PM-1", pm_role.role_id, {...}),
    "dev1": registry.create_agent("Dev-1", dev_role.role_id, {...}),
    "dev2": registry.create_agent("Dev-2", dev_role.role_id, {...}),
    "qa": registry.create_agent("QA-1", qa_role.role_id, {...})
}

# Assign tasks to specific team members
registry.assign_task("design-task", agent_id=team["pm"].agent_id)
registry.assign_task("code-task-1", agent_id=team["dev1"].agent_id)
registry.assign_task("code-task-2", agent_id=team["dev2"].agent_id)
registry.assign_task("test-task", agent_id=team["qa"].agent_id)
```

### Pattern 3: Load Balancing

```python
# Distribute tasks across available agents
tasks = get_pending_tasks()

for task in tasks:
    # Find least busy agent with required capability
    agents = registry.list_agents(
        status=AgentStatus.AVAILABLE,
        role_id=required_role_id
    )
    
    if agents:
        # Pick first available
        agent = agents[0]
        registry.assign_task(task["id"], agent_id=agent.agent_id)
```

### Pattern 4: Dynamic Role Creation

```python
# Create new roles at runtime based on needs
def create_custom_role(name, description, capabilities):
    return registry.create_role(
        name=name,
        description=description,
        capabilities=[
            AgentCapability(**cap) for cap in capabilities
        ]
    )

# Example: Create a specialized role
blockchain_role = create_custom_role(
    name="BlockchainDeveloper",
    description="Blockchain and smart contract development",
    capabilities=[
        {
            "name": "smart_contract_dev",
            "description": "Develop smart contracts",
            "required_skills": ["solidity", "web3", "blockchain"]
        }
    ]
)
```

## Integration Examples

### With Project Cortex

```python
# Assign agents from registry to project
def assign_team_to_project(project, role_names):
    for role_name in role_names:
        # Find agent with role
        role = registry.get_role_by_name(role_name)
        agent = registry.find_available_agent(role_id=role.role_id)
        
        if agent:
            # Assign to project
            project.assign_agent(agent.agent_id, role.name)
            
            # Mark agent as busy
            agent.update_status(AgentStatus.BUSY)
```

### With Decision Gate

```python
# Require approval for agent role changes
def reassign_agent_role(agent_id, new_role_id):
    decision = gate.request_decision(
        action_type="reassign_agent",
        description=f"Change agent role",
        decision_type=DecisionType.HIGH,
        context={
            "agent_id": agent_id,
            "new_role_id": new_role_id
        }
    )
    
    return decision.decision_id
```

## API Reference

### AgentRegistry Class

**Methods**:
- `register_role(role)` - Register a role
- `create_role(name, description, capabilities, priority, max_concurrent_tasks)` - Create and register role
- `get_role(role_id)` - Get role by ID
- `get_role_by_name(name)` - Get role by name
- `list_roles()` - List all roles
- `find_roles_by_capability(capability_name)` - Find roles with capability
- `register_agent(agent)` - Register an agent
- `create_agent(name, role_id, skills, api_config, executor)` - Create and register agent
- `get_agent(agent_id)` - Get agent by ID
- `list_agents(role_id, status)` - List agents with filters
- `find_available_agent(role_id, capability, required_skills)` - Find matching available agent
- `assign_task(task_id, agent_id, role_id, capability, required_skills)` - Assign task to agent
- `complete_task(agent_id, task_id)` - Mark task complete
- `remove_agent(agent_id)` - Remove agent
- `get_statistics()` - Get registry statistics
- `save_state(filepath)` - Save to JSON
- `load_state(filepath)` - Load from JSON

### Agent Class

**Methods**:
- `update_status(status)` - Update status
- `assign_task(task_id)` - Assign task
- `complete_task(task_id)` - Complete task
- `has_skill(skill)` - Check for skill
- `has_skills(skills)` - Check for multiple skills
- `to_dict()` - Export to dictionary

**Properties**:
- `agent_id` - Unique ID
- `name` - Agent name
- `role_id` - Role ID
- `status` - Current status
- `skills` - Set of skills
- `current_tasks` - List of active task IDs
- `completed_tasks` - Count of completed tasks
- `api_config` - API configuration dict
- `executor` - Custom executor function

## Best Practices

1. **Define roles clearly**: Each role should have distinct purpose
2. **Use skill matching**: Assign tasks based on required skills
3. **Monitor agent load**: Don't overload agents with too many tasks
4. **Track completion**: Use task completion for analytics
5. **Save state regularly**: Persist registry state
6. **Use priorities**: Higher priority roles for critical tasks
7. **API flexibility**: Don't hard-code provider details
8. **Clean up**: Remove offline/error agents periodically

## Scaling to 100+ Roles

The system is designed to scale:

```python
# Roles are indexed by capability for fast lookup
# No performance degradation with 100+ roles

# Add as many roles as needed
for i in range(100):
    registry.create_role(
        name=f"SpecializedRole{i}",
        description=f"Specialized role for task type {i}",
        capabilities=[...]
    )
```

## Example: Complete Workflow

See `agents/example.py` for a complete working example.

```bash
python agents/example.py
```
