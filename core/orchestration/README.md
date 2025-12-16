# Core Orchestration

## Overview

The Core Orchestration module provides project-level workflow coordination and factory orchestration across Application, Media, and Research Factories. It supports modular and parallel workstreams for complex multi-factory workflows.

## Structure

```
core/orchestration/
├── __init__.py              # Module exports and version
├── orchestrator.py          # Core project orchestrator
├── workflow_manager.py      # Workflow definition and management
├── factory_coordinator.py   # Inter-factory coordination
└── README.md               # This file
```

## Components

### ProjectOrchestrator

The main orchestrator class for coordinating project-level workflows across multiple factories.

**Key Features:**
- Factory registration and management
- Cross-factory workflow creation and execution
- Workflow status tracking and history
- Support for parallel and sequential execution patterns

**Usage:**
```python
from core.orchestration import ProjectOrchestrator
from factories.media import MediaFactory
from factories.research import ResearchFactory

# Initialize orchestrator
orchestrator = ProjectOrchestrator(config={
    'workflow': {'max_parallel': 4},
    'coordinator': {'max_workers': 4}
})

# Register factories
media_factory = MediaFactory()
research_factory = ResearchFactory()

orchestrator.register_factory('media', media_factory)
orchestrator.register_factory('research', research_factory)

# Create a workflow
workflow_id = orchestrator.create_workflow('content_pipeline', {
    'steps': [
        {
            'factory': 'research',
            'action': 'analyze_market',
            'params': {'symbol': 'BTC'}
        },
        {
            'factory': 'media',
            'action': 'create_media',
            'params': {'type': 'image', 'prompt': 'BTC trend'}
        }
    ],
    'factories': ['research', 'media'],
    'parallel': False
})

# Execute workflow
result = orchestrator.execute_workflow(workflow_id)

# Check status
status = orchestrator.get_workflow_status(workflow_id)
```

### WorkflowManager

Manages workflow definitions, templates, and execution patterns.

**Key Features:**
- Workflow definition creation and management
- Template-based workflow creation
- Workflow validation
- Reusable workflow templates

**Usage:**
```python
from core.orchestration import WorkflowManager

manager = WorkflowManager()

# Register a template
manager.register_template('market_research_pipeline', {
    'steps': [
        {'factory': 'research', 'action': 'analyze_market'},
        {'factory': 'research', 'action': 'initiate_research'}
    ],
    'factories': ['research'],
    'parallel': False
})

# Create workflow from template
workflow_id = manager.create_from_template('market_research_pipeline', {
    'params': {'symbol': 'ETH'}
})
```

### FactoryCoordinator

Coordinates communication and workflow execution across multiple factories.

**Key Features:**
- Sequential execution support
- Parallel execution support with thread pooling
- Context passing between workflow steps
- Error handling and recovery
- Execution history tracking

**Usage:**
```python
from core.orchestration import FactoryCoordinator

coordinator = FactoryCoordinator(config={'max_workers': 4})

# Coordinate workflow execution
result = coordinator.coordinate(
    workflow_id='wf_123',
    workflow_config={
        'steps': [...],
        'parallel': True
    },
    factories={
        'media': media_factory,
        'research': research_factory
    }
)
```

## Design Principles

1. **Modular**: Each component is independent and composable
2. **Parallel-capable**: Support for parallel workstream execution
3. **Interface-driven**: Clear interfaces for factory integration
4. **Extensible**: Easy to add new workflow patterns
5. **Auditable**: Complete execution history tracking
6. **Reversible**: Changes can be easily rolled back

## Workflow Patterns

### Sequential Execution

Steps execute one after another, with context passing:
```python
workflow_config = {
    'steps': [
        {'factory': 'research', 'action': 'analyze_market', 'params': {}},
        {'factory': 'media', 'action': 'create_media', 'params': {}}
    ],
    'parallel': False
}
```

### Parallel Execution

Steps execute concurrently:
```python
workflow_config = {
    'steps': [
        {'factory': 'media', 'action': 'create_image', 'params': {}},
        {'factory': 'media', 'action': 'create_video', 'params': {}},
        {'factory': 'research', 'action': 'analyze_market', 'params': {}}
    ],
    'parallel': True
}
```

### Mixed Patterns

Combine sequential and parallel execution using nested workflows.

## Future Development

- Advanced workflow scheduling and retry logic
- Conditional step execution
- Workflow branching and merging
- Resource pooling and optimization
- Real-time workflow monitoring and visualization
- Webhook integration for external triggers
- Workflow versioning and rollback
- Performance metrics and analytics

## Integration Points

- Integrates with all factories (Application, Media, Research)
- Compatible with existing orchestrator service
- Can leverage worker-pool for distributed execution
- Extensible for future factory additions
