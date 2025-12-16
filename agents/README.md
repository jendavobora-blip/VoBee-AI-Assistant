# Agent Registry

## Overview

Agent Registry is a role-based agent management system for VoBee AI Assistant. It provides vendor-agnostic agent definitions focused on logical roles and capabilities rather than specific AI provider implementations.

## Features

### Role-Based Agent Management
- Pre-defined logical roles (Architect, Backend Builder, Tester, etc.)
- Support for secondary roles
- Vendor-agnostic design
- Focus on capabilities over implementation

### Agent Capabilities
- Define specific skills and proficiencies
- Proficiency levels (1-10 scale)
- Capability-based agent discovery
- Extensible capability system

### Agent Lifecycle
- Registration and unregistration
- Status tracking (Available, Busy, Offline, Error, Maintenance)
- Task assignment and completion
- Performance metrics (placeholder for future)

### Intelligent Discovery
- Find agents by role
- Find agents by capability and proficiency
- Find available agents matching criteria
- Advanced filtering and search

## Agent Roles

### Architecture & Design
- **Architect**: System architecture and design
- **Designer**: UI/UX and visual design
- **System Planner**: System planning and strategy

### Development
- **Backend Builder**: Backend development
- **Frontend Builder**: Frontend development
- **Full Stack Builder**: Full-stack development
- **Database Engineer**: Database design and optimization

### Quality & Testing
- **Tester**: Testing and quality assurance
- **QA Engineer**: Quality engineering
- **Security Auditor**: Security reviews and audits

### Operations
- **DevOps Engineer**: DevOps and infrastructure
- **Deployment Manager**: Deployment and release management
- **Monitoring Specialist**: System monitoring and observability

### Content & Documentation
- **Technical Writer**: Technical documentation
- **Documentation Manager**: Documentation management

### Analysis & Research
- **Data Analyst**: Data analysis and insights
- **Researcher**: Research and investigation
- **Code Reviewer**: Code review and quality

### Management & Coordination
- **Project Manager**: Project management
- **Coordinator**: Team coordination

### Specialized
- **AI Trainer**: AI model training
- **Model Optimizer**: Model optimization
- **Custom**: Custom roles

## Usage

### Basic Example

```python
from agents import AgentRegistry, Agent, AgentRole, AgentStatus

# Initialize the registry
registry = AgentRegistry()

# Create and register an agent
architect = Agent(
    name="Senior Architect",
    role=AgentRole.ARCHITECT,
    description="Experienced system architect specializing in microservices"
)

# Add capabilities
architect.add_capability("system_design", "Design scalable systems", proficiency=9)
architect.add_capability("microservices", "Microservices architecture", proficiency=8)
architect.add_capability("cloud_architecture", "Cloud-native design", proficiency=9)

# Add secondary role
architect.add_secondary_role(AgentRole.SYSTEM_PLANNER)

# Register the agent
registry.register_agent(architect)
```

### Creating Multiple Agents

```python
# Backend developer
backend_dev = Agent(
    name="Backend Developer",
    role=AgentRole.BACKEND_BUILDER,
    description="Python and FastAPI specialist"
)
backend_dev.add_capability("python", "Python programming", proficiency=9)
backend_dev.add_capability("fastapi", "FastAPI framework", proficiency=8)
backend_dev.add_capability("databases", "Database design", proficiency=7)
registry.register_agent(backend_dev)

# QA Engineer
qa_engineer = Agent(
    name="QA Engineer",
    role=AgentRole.QA_ENGINEER,
    description="Automated testing specialist"
)
qa_engineer.add_capability("test_automation", "Test automation", proficiency=8)
qa_engineer.add_capability("pytest", "Pytest framework", proficiency=9)
registry.register_agent(qa_engineer)
```

### Finding Agents

```python
# Find all architects
architects = registry.find_agents_by_role(AgentRole.ARCHITECT)

# Find available architects
available_architects = registry.find_agents_by_role(
    AgentRole.ARCHITECT,
    status=AgentStatus.AVAILABLE
)

# Find agents with specific capability
python_experts = registry.find_agents_by_capability(
    capability="python",
    min_proficiency=8,
    status=AgentStatus.AVAILABLE
)

# Find best match for a task
agent = registry.find_available_agent(
    role=AgentRole.BACKEND_BUILDER,
    required_capabilities=["python", "fastapi"]
)
```

### Task Assignment

```python
# Assign a task to an agent
if agent:
    agent.assign_task(
        task_id="task-123",
        project_id="project-456"
    )
    print(f"Agent status: {agent.status.value}")  # busy

# Complete the task
agent.complete_task()
print(f"Agent status: {agent.status.value}")  # available
print(f"Tasks completed: {agent.tasks_completed}")  # 1
```

### Registry Statistics

```python
# Get overall statistics
stats = registry.get_statistics()
print(f"Total agents: {stats['total_agents']}")
print(f"Available: {stats['available_agents']}")
print(f"Busy: {stats['busy_agents']}")
print(f"Role distribution: {stats['role_distribution']}")
```

## Architecture

### AgentRegistry
Central management system for all agents.

**Key Methods:**
- `register_agent()` / `unregister_agent()`: Manage agents
- `get_agent()`: Get specific agent
- `find_agents_by_role()`: Search by role
- `find_agents_by_capability()`: Search by capability
- `find_available_agent()`: Find best match
- `get_statistics()`: Get registry statistics

### Agent
Represents an individual AI agent.

**Key Methods:**
- `add_capability()`: Add a capability
- `add_secondary_role()`: Add secondary role
- `assign_task()` / `complete_task()`: Manage tasks
- `has_capability()`: Check for capability
- `set_status()`: Update status

### AgentCapability
Represents a specific skill or capability.

**Properties:**
- `name`: Capability name
- `description`: Detailed description
- `proficiency`: Skill level (1-10)
- `metadata`: Additional information

## Design Principles

1. **Vendor Agnostic**: No dependencies on specific AI providers
2. **Role-Based**: Organized by logical responsibilities
3. **Capability-Focused**: Skills over implementations
4. **Extensible**: Easy to add new roles and capabilities
5. **Discoverable**: Powerful search and filtering
6. **Flexible**: Support for multiple roles per agent

## Future Extensions

This is a foundational skeleton designed for expansion:

- Agent collaboration patterns
- Team formation algorithms
- Load balancing across agents
- Performance tracking and analytics
- Agent learning and improvement
- Cost optimization
- Specialized agent pools
- Agent health monitoring
- Automated agent provisioning
- Cross-project agent sharing
- Agent reputation system
- Skill recommendations

## Integration Points

Agent Registry integrates with:

- **Project Cortex**: Assign agents to projects
- **Decision Gate**: Approve agent deployments
- **Task Management**: Route tasks to appropriate agents
- **Monitoring**: Track agent performance
- **Budget Management**: Cost allocation per agent

## Vendor Independence

The registry is designed to work with any AI agent implementation:

- No hardcoded vendor APIs
- Generic role definitions
- Capability-based matching
- Pluggable agent backends
- Provider-agnostic metrics

This allows you to:
- Switch AI providers without code changes
- Use multiple providers simultaneously
- Add custom agent implementations
- Integrate with various AI platforms

## Status

**Current Version**: 0.1.0 (Skeleton)

This is a MAX_SPEED implementation focusing on structural foundations. Full functionality will be added in future iterations.
