# Agents System - Role-Based Agent Registry

A flexible, extensible agent management system supporting 30-100 logical roles with no hard-wired vendor dependencies.

## Overview

The Agents System provides a comprehensive framework for managing diverse agent roles across various domains including operations, frontend, backend, data, DevOps, security, testing, design, product management, and research.

**Key Features:**
- Support for 30-100+ logical agent roles
- Role-based organization by category
- Capability-based agent matching
- No vendor lock-in (placeholder structure)
- Extensible architecture for adding custom roles
- Agent lifecycle management

## Architecture

```
Agents System
├── AgentRegistry (Central Management)
│   ├── Agent Registration
│   ├── Role Assignment
│   └── Capability Matching
├── AgentRole (Role Definitions)
│   ├── 30+ Predefined Roles
│   ├── 10 Role Categories
│   └── Capability Mappings
└── BaseAgent (Agent Interface)
    ├── Task Execution
    ├── Status Management
    └── History Tracking
```

## Components

### 1. AgentRole - Role Definitions

Defines 30+ logical roles organized into categories:

**Role Categories:**
- **OPERATIONS**: Operations Architect, Operations Manager
- **FRONTEND**: Frontend Architect, Frontend Developer, UI/UX Specialist
- **BACKEND**: Backend Architect, Backend Developer, API Specialist
- **DATA**: Data Architect, Data Engineer, Data Scientist, ML Engineer
- **DEVOPS**: DevOps Architect, DevOps Engineer, SRE
- **SECURITY**: Security Architect, Security Engineer
- **TESTING**: QA Architect, QA Engineer
- **DESIGN**: Design Lead, Visual Designer
- **PRODUCT**: Product Manager, Product Owner
- **RESEARCH**: Research Scientist, AI Researcher

**Example Usage:**
```python
from agents import AgentRole, RoleCategory

# Get all available roles
all_roles = AgentRole.get_all_roles()
print(f"Total roles defined: {len(all_roles)}")

# Get roles by category
backend_roles = AgentRole.get_roles_by_category(RoleCategory.BACKEND)
for role in backend_roles:
    print(f"{role['name']}: {role['description']}")

# Access specific role definition
ops_architect = AgentRole.OPERATIONS_ARCHITECT
print(f"Capabilities: {ops_architect['capabilities']}")
print(f"Required Skills: {ops_architect['required_skills']}")
```

### 2. BaseAgent - Agent Base Class

Abstract base class for all agents providing common interface:

**Key Methods:**
- `execute_task()`: Execute assigned tasks
- `validate_capability()`: Check capability availability
- `get_info()`: Get agent information
- `update_status()`: Update agent status
- `record_task()`: Track task history

**Example Usage:**
```python
from agents import BaseAgent, PlaceholderAgent, AgentRole

# Create a placeholder agent
role = AgentRole.BACKEND_DEVELOPER
agent = PlaceholderAgent(
    agent_id="agent-001",
    role=role,
    config={'environment': 'production'}
)

# Execute a task
task = {
    'task_id': 'task-123',
    'description': 'Implement user authentication',
    'parameters': {'framework': 'FastAPI'}
}
result = agent.execute_task(task)

# Check capabilities
has_api = agent.validate_capability('api_implementation')
print(f"Can implement APIs: {has_api}")

# Get agent info
info = agent.get_info()
print(f"Agent: {info['role']}, Status: {info['status']}")
```

### 3. AgentRegistry - Central Management

Manages all agents in the system with registration, lookup, and matching.

**Key Features:**
- Agent registration with role assignment
- Capability-based agent search
- Category-based filtering
- Best agent matching for tasks
- Registry statistics

**Example Usage:**
```python
from agents import AgentRegistry, AgentRole

# Initialize registry
registry = AgentRegistry()

# Register agents
registry.register_agent(
    agent_id="backend-001",
    role_name="Backend Developer"
)

registry.register_agent(
    agent_id="frontend-001",
    role_name="Frontend Developer"
)

# Get agents by category
from agents import RoleCategory
backend_agents = registry.get_agents_by_category(RoleCategory.BACKEND)

# Find agents with specific capability
api_agents = registry.get_agents_with_capability('api_implementation')

# Find best agent for a task
best_agent = registry.find_best_agent(
    required_capabilities=['api_implementation', 'database_operations'],
    preferred_category=RoleCategory.BACKEND
)

# Get registry statistics
stats = registry.get_registry_stats()
print(f"Total agents: {stats['total_agents']}")
print(f"Capacity: {stats['capacity_utilization']}")
```

## Complete Integration Example

```python
from agents import AgentRegistry, AgentRole, RoleCategory, PlaceholderAgent

# 1. Initialize registry
registry = AgentRegistry()

# 2. Register multiple agents across different roles
agents_to_register = [
    ("ops-001", "Operations Architect"),
    ("fe-001", "Frontend Developer"),
    ("be-001", "Backend Developer"),
    ("be-002", "API Specialist"),
    ("data-001", "Data Engineer"),
    ("ml-001", "ML Engineer"),
    ("devops-001", "DevOps Engineer"),
    ("sec-001", "Security Engineer"),
    ("qa-001", "QA Engineer")
]

for agent_id, role_name in agents_to_register:
    registry.register_agent(agent_id, role_name)

# 3. Get registry overview
stats = registry.get_registry_stats()
print(f"\nRegistry Status:")
print(f"  Total Agents: {stats['total_agents']}/{stats['max_agents']}")
print(f"  Utilization: {stats['capacity_utilization']}")
print(f"\nAgents by Category:")
for category, count in stats['agents_by_category'].items():
    if count > 0:
        print(f"  {category}: {count}")

# 4. Find specialist for API development
api_specialists = registry.get_agents_with_capability('api_implementation')
print(f"\nAPI Specialists: {len(api_specialists)}")

# 5. Assign task to best agent
task = {
    'task_id': 'task-api-001',
    'description': 'Build REST API for user management',
    'required_capabilities': ['api_implementation', 'database_operations']
}

best_agent = registry.find_best_agent(
    required_capabilities=task['required_capabilities'],
    preferred_category=RoleCategory.BACKEND
)

if best_agent:
    print(f"\nBest agent for task: {best_agent.role['name']}")
    result = best_agent.execute_task(task)
    print(f"Task result: {result['status']}")

# 6. Get detailed agent summary
summary = registry.get_agent_summary("be-001")
if summary:
    print(f"\nAgent Summary:")
    print(f"  ID: {summary['agent_id']}")
    print(f"  Role: {summary['role']}")
    print(f"  Status: {summary['status']}")
    print(f"  Total Tasks: {summary['total_tasks']}")
```

## Adding Custom Roles

The system is designed to be easily extended with new roles:

```python
# In agent_roles.py, add new role definition:

CUSTOM_ROLE = {
    'name': 'Custom Specialist',
    'category': RoleCategory.OPERATIONS,  # or any appropriate category
    'description': 'Specialized role for custom tasks',
    'capabilities': [
        'custom_capability_1',
        'custom_capability_2',
        'custom_capability_3'
    ],
    'required_skills': ['skill1', 'skill2', 'skill3']
}
```

## Implementing Custom Agents

To replace placeholder agents with real implementations:

```python
from agents import BaseAgent
from typing import Dict, Any

class CustomAgent(BaseAgent):
    """Custom agent with vendor-specific implementation"""
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Your custom implementation here
        # Could integrate with OpenAI, Anthropic, or any other service
        
        self.update_status("executing")
        
        # ... custom task execution logic ...
        
        result = {
            'status': 'completed',
            'output': 'task output',
            'metadata': {}
        }
        
        self.record_task(task, result)
        self.update_status("ready")
        
        return result
    
    def validate_capability(self, capability: str) -> bool:
        return capability in self.get_capabilities()

# Register custom agent
registry.register_agent(
    agent_id="custom-001",
    role_name="Backend Developer",
    agent_class=CustomAgent,
    config={'api_key': 'your-key', 'model': 'gpt-4'}
)
```

## Role Capabilities Reference

### Operations Roles
- **Operations Architect**: system_architecture, infrastructure_planning, resource_optimization, workflow_design
- **Operations Manager**: task_coordination, team_management, process_optimization, monitoring

### Frontend Roles
- **Frontend Architect**: ui_architecture, component_design, performance_optimization, framework_selection
- **Frontend Developer**: ui_development, component_implementation, state_management, responsive_design
- **UI/UX Specialist**: interface_design, user_flow_design, prototyping, usability_testing

### Backend Roles
- **Backend Architect**: api_design, database_architecture, microservices_design, scalability_planning
- **Backend Developer**: api_implementation, database_operations, business_logic, integration
- **API Specialist**: rest_api_design, graphql_design, api_documentation, api_security

### Data Roles
- **Data Architect**: data_modeling, pipeline_design, data_warehouse_design, etl_design
- **Data Engineer**: pipeline_implementation, data_processing, data_integration, data_quality
- **Data Scientist**: data_analysis, ml_modeling, statistical_analysis, prediction
- **ML Engineer**: model_training, model_deployment, model_optimization, mlops

### DevOps Roles
- **DevOps Architect**: cicd_design, infrastructure_as_code, automation_strategy, cloud_architecture
- **DevOps Engineer**: cicd_implementation, container_orchestration, monitoring_setup, automation
- **SRE**: reliability_engineering, incident_response, performance_tuning, monitoring

### Security Roles
- **Security Architect**: security_design, threat_modeling, security_architecture, compliance_design
- **Security Engineer**: security_implementation, vulnerability_scanning, penetration_testing, security_monitoring

### Testing Roles
- **QA Architect**: test_strategy, framework_design, quality_metrics, automation_strategy
- **QA Engineer**: test_implementation, automated_testing, manual_testing, bug_tracking

### Design Roles
- **Design Lead**: design_strategy, design_systems, team_leadership, brand_development
- **Visual Designer**: visual_design, graphics_creation, icon_design, illustration

### Product Roles
- **Product Manager**: product_strategy, roadmap_planning, stakeholder_management, requirements_gathering
- **Product Owner**: backlog_management, user_story_creation, prioritization, sprint_planning

### Research Roles
- **Research Scientist**: research_design, experimentation, paper_writing, innovation
- **AI Researcher**: ai_research, model_development, algorithm_design, benchmarking

## Best Practices

1. **Use Role-Based Assignment**: Match agents to tasks based on role capabilities
2. **Leverage Categories**: Organize agents by category for easier management
3. **Track Agent Performance**: Monitor task history and success rates
4. **Implement Custom Agents**: Replace placeholders with real implementations as needed
5. **Extend Roles**: Add domain-specific roles as your system grows
6. **Capability Matching**: Use capability-based search for optimal agent selection

## Limits and Configuration

- **Max Agents**: 100 (configurable via `AgentRegistry.MAX_AGENTS`)
- **Role Categories**: 10 predefined categories
- **Predefined Roles**: 30+ roles (easily extensible)
- **Custom Roles**: Unlimited (add to `AgentRole` class)

## No Vendor Lock-In

The system is designed with **no hard-wired vendor dependencies**:
- `PlaceholderAgent` provides a template implementation
- `BaseAgent` defines the interface contract
- Easy to integrate any AI service (OpenAI, Anthropic, local models, etc.)
- Swap implementations without changing the registry or role definitions
