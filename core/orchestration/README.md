# Core Orchestration

The Core Orchestration module provides project-level coordination for multi-factory workflows, intelligent task routing, and factory connectivity.

## Overview

The Core Orchestration layer is designed to:
- Coordinate complex workflows spanning multiple factories
- Intelligently route tasks to appropriate factories
- Manage factory connections and communication
- Enable modular, extensible architecture
- Balance modularity with connectivity

## Architecture

```
core/orchestration/
├── __init__.py              # Orchestration engine and exports
├── workflow.py              # Workflow coordination and templates
├── factory_connector.py     # Factory integration layer
└── router.py                # Intelligent task routing
```

## Components

### OrchestrationEngine

Main entry point for orchestration operations. Provides unified interface for:
- Workflow execution
- Task routing
- Factory status monitoring

### WorkflowCoordinator

Manages multi-step workflows across factories:
- Step dependency management
- Parallel execution support
- Error recovery and retries
- Result aggregation
- Template-based workflows

### FactoryConnector

Central connector for all factory types:
- Standardized factory interfaces
- Connection management
- Status monitoring
- Capability discovery

### TaskRouter

Intelligent routing of tasks to factories:
- Multiple routing strategies
- Rule-based routing
- Load balancing
- Priority handling

## Usage Examples

### Simple Workflow Execution

```python
from core.orchestration import OrchestrationEngine, WorkflowTemplate, WorkflowStep

# Initialize orchestration engine
engine = OrchestrationEngine()

# Create a workflow template
template = WorkflowTemplate(
    workflow_id="generate-and-analyze",
    name="Generate Image and Analyze Market",
    description="Generate product image and analyze market opportunity",
    steps=[
        WorkflowStep(
            step_id="step1",
            name="Generate Product Image",
            factory_type="media",
            action="generate_image",
            parameters={"prompt": "Product mockup", "style": "realistic"}
        ),
        WorkflowStep(
            step_id="step2",
            name="Analyze Market",
            factory_type="research",
            action="market_analysis",
            parameters={"market_sector": "technology"},
            dependencies=["step1"]  # Waits for step1 to complete
        )
    ]
)

# Execute workflow
execution = engine.execute_workflow(template)
print(f"Execution ID: {execution.execution_id}")
print(f"Status: {execution.status}")
```

### Task Routing

```python
from core.orchestration import TaskRouter, RoutingStrategy

# Initialize router with strategy
router = TaskRouter({
    "strategy": "CONTENT_BASED",
    "default_factory": "media"
})

# Route an image generation task
task = {
    "type": "image_generation",
    "keywords": ["image", "generate"],
    "parameters": {"prompt": "Sunset landscape"}
}
factory = router.route(task)
print(f"Routed to: {factory}")  # Output: "media"

# Route a research task
task = {
    "type": "market_research",
    "keywords": ["market", "analysis"],
    "parameters": {"sector": "healthcare"}
}
factory = router.route(task)
print(f"Routed to: {factory}")  # Output: "research"
```

### Factory Connection Management

```python
from core.orchestration import FactoryConnector, FactoryType

# Initialize connector
connector = FactoryConnector()

# Get all factory statuses
status = connector.get_all_status()
print(status)

# Execute action on specific factory
result = connector.execute_on_factory(
    factory_type=FactoryType.MEDIA,
    action="generate_image",
    parameters={"prompt": "Abstract art", "style": "modern"}
)

# Get factory capabilities
capabilities = connector.get_all_capabilities()
print(capabilities)
```

### Complex Multi-Factory Workflow

```python
from core.orchestration import WorkflowCoordinator

coordinator = WorkflowCoordinator({
    "max_retries": 3,
    "parallel_execution": True
})

# Create complex workflow
template = coordinator.create_template(
    name="Product Launch Campaign",
    description="Generate media and conduct research for product launch",
    steps=[
        {
            "step_id": "research_market",
            "name": "Market Research",
            "factory_type": "research",
            "action": "market_analysis",
            "parameters": {"market_sector": "technology", "depth": "comprehensive"}
        },
        {
            "step_id": "discover_trends",
            "name": "Trend Discovery",
            "factory_type": "research",
            "action": "discover_technology",
            "parameters": {"query": "emerging tech trends"},
            "dependencies": []  # Can run in parallel with research_market
        },
        {
            "step_id": "generate_images",
            "name": "Product Images",
            "factory_type": "media",
            "action": "generate_images",
            "parameters": {"prompts": ["Product hero", "Product detail"]},
            "dependencies": ["research_market"]
        },
        {
            "step_id": "generate_video",
            "name": "Product Video",
            "factory_type": "media",
            "action": "generate_video",
            "parameters": {"prompt": "Product showcase", "duration": 30},
            "dependencies": ["generate_images"]
        }
    ]
)

# Execute workflow
execution = coordinator.execute(template)

# Monitor execution
while execution.status in ["PENDING", "RUNNING"]:
    print(f"Current step: {execution.current_step}")
    print(f"Status: {execution.status}")
    # Wait and check again...

print(f"Final status: {execution.status}")
print(f"Results: {execution.results}")
```

## Routing Strategies

### CONTENT_BASED (Default)
Routes tasks based on content analysis and predefined rules. Best for heterogeneous task types.

### PRIORITY_BASED
Routes high-priority tasks differently than normal tasks. Useful for time-sensitive operations.

### LOAD_BALANCED
Distributes tasks based on factory load. Optimal for high-throughput scenarios.

### ROUND_ROBIN
Simple round-robin distribution. Good for homogeneous task types.

### CAPABILITY_BASED
Routes based on factory capabilities. Ensures tasks go to capable factories.

## Factory Types

Currently supported:
- **MEDIA**: Image, video, voice generation and processing
- **RESEARCH**: Market analysis, research agents, discovery

Future factories:
- **APPLICATION**: Application generation and deployment
- **DATA**: Data processing and transformation
- **ANALYTICS**: Analytics and reporting

## Workflow Features

### Step Dependencies
Define which steps must complete before others can start:
```python
WorkflowStep(
    step_id="step2",
    dependencies=["step1", "step3"]  # Waits for both step1 and step3
)
```

### Parallel Execution
Steps without dependencies can execute in parallel:
```python
coordinator = WorkflowCoordinator({
    "parallel_execution": True  # Enable parallel execution
})
```

### Error Recovery
Automatic retry on failure:
```python
coordinator = WorkflowCoordinator({
    "max_retries": 3  # Retry failed steps up to 3 times
})
```

### Workflow Control
- **Pause**: Pause running workflows
- **Resume**: Resume paused workflows
- **Cancel**: Cancel pending/running workflows

## Extension Guidelines

### Adding New Factory Type

1. Define in `FactoryType` enum:
```python
class FactoryType(Enum):
    NEW_FACTORY = "new_factory"
```

2. Create factory interface:
```python
class NewFactoryInterface(FactoryInterface):
    def execute(self, action, parameters):
        # Implementation
        pass
    
    def get_status(self):
        # Implementation
        pass
    
    def get_capabilities(self):
        # Implementation
        pass
```

3. Register in `FactoryConnector`:
```python
def _initialize_factories(self):
    self._factories[FactoryType.NEW_FACTORY] = NewFactoryInterface(...)
```

### Adding Custom Routing Rules

```python
router.add_rule(RoutingRule(
    rule_id="custom_rule",
    name="Custom Routing Rule",
    condition=lambda task: task.get("custom_field") == "special",
    target_factory="research",
    priority=20  # Higher priority than default rules
))
```

## Integration Points

### Media Factory Integration
- Actions: `generate_image`, `generate_video`, `text_to_speech`
- Status: Workflow availability, processing capacity
- Results: Generated media files, metadata

### Research Factory Integration
- Actions: `market_analysis`, `discover_technology`, `analyze_papers`
- Status: Agent availability, data source connectivity
- Results: Research findings, insights, recommendations

### Service Integration
- Can integrate with existing services (image-generation, video-generation)
- Provides abstraction layer over direct service calls
- Enables service composition and orchestration

## Configuration

```python
config = {
    "workflow": {
        "max_retries": 3,
        "parallel_execution": True,
        "timeout": 3600  # seconds
    },
    "factories": {
        "media": {"service_endpoint": "http://media-factory:5100"},
        "research": {"service_endpoint": "http://research-factory:5200"}
    },
    "routing": {
        "strategy": "LOAD_BALANCED",
        "default_factory": "media"
    }
}

engine = OrchestrationEngine(config)
```

## Future Enhancements

- [ ] Advanced dependency resolution (AND/OR logic)
- [ ] Dynamic workflow modification
- [ ] Workflow versioning and rollback
- [ ] Real-time monitoring dashboard
- [ ] Distributed workflow execution
- [ ] Workflow templates marketplace
- [ ] Machine learning-based routing
- [ ] Cost optimization routing
