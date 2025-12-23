# Factory Architecture - Implementation Guide

This document describes the newly implemented factory architecture for the VoBee AI Assistant, including Media Factory, Research Factory, and Core Orchestration.

## 📋 Overview

The factory architecture provides a modular, extensible framework for organizing AI workflows into specialized domains:

- **Media Factory** (`factories/media/`) - Image, video, and voice generation/processing
- **Research Factory** (`factories/research/`) - Market analysis and autonomous research agents
- **Core Orchestration** (`core/orchestration/`) - Multi-factory workflow coordination

## 🏗️ Architecture

```
VoBee-AI-Assistant/
├── factories/
│   ├── __init__.py                 # Factory module root
│   ├── media/                      # Media Factory
│   │   ├── __init__.py            # Media factory registry
│   │   ├── base.py                # Abstract base classes
│   │   ├── image.py               # Image workflow
│   │   ├── video.py               # Video workflow
│   │   ├── voice.py               # Voice workflow
│   │   └── README.md              # Media factory documentation
│   └── research/                   # Research Factory
│       ├── __init__.py            # Research factory registry
│       ├── base.py                # Abstract base classes
│       ├── market_analysis.py     # Market analysis workflow
│       ├── research_agent.py      # Research agent workflow
│       └── README.md              # Research factory documentation
├── core/
│   ├── __init__.py                 # Core module root
│   └── orchestration/              # Core Orchestration
│       ├── __init__.py            # Orchestration engine
│       ├── workflow.py            # Workflow coordination
│       ├── factory_connector.py   # Factory integration
│       ├── router.py              # Task routing
│       └── README.md              # Orchestration documentation
└── examples/
    └── factory_integration_demo.py # Integration examples
```

## 🚀 Quick Start

### Import and Use Media Factory

```python
from factories.media import MediaFactoryRegistry, MediaType

# Get an image workflow
image_workflow = MediaFactoryRegistry.get_workflow(MediaType.IMAGE)

# Generate an image
task = image_workflow.process({
    "prompt": "A futuristic city with flying cars",
    "style": "realistic",
    "resolution": "1024x1024",
    "model": "stable-diffusion"
})

print(f"Task ID: {task.task_id}")
print(f"Status: {task.status.value}")
```

### Import and Use Research Factory

```python
from factories.research import ResearchFactoryRegistry, ResearchType

# Get a market analysis workflow
market_workflow = ResearchFactoryRegistry.get_workflow(ResearchType.MARKET_ANALYSIS)

# Analyze competitors
task = market_workflow.analyze_competitors(
    market_sector="technology",
    competitors=["CompanyA", "CompanyB"],
    metrics=["market_share", "innovation"]
)

print(f"Task ID: {task.task_id}")
print(f"Priority: {task.priority.value}")
```

### Use Core Orchestration

```python
from core.orchestration import OrchestrationEngine, WorkflowCoordinator

# Initialize orchestration engine
engine = OrchestrationEngine()

# Check factory status
status = engine.get_factory_status()
print(status)

# Create a multi-factory workflow
coordinator = WorkflowCoordinator()
template = coordinator.create_template(
    name="Content Creation Pipeline",
    description="Research-driven content generation",
    steps=[
        {
            "name": "Market Research",
            "factory_type": "research",
            "action": "market_analysis",
            "parameters": {"market_sector": "tech"}
        },
        {
            "name": "Generate Image",
            "factory_type": "media",
            "action": "generate_image",
            "parameters": {"prompt": "Product hero"},
            "dependencies": ["step_0"]
        }
    ]
)

execution = coordinator.execute(template)
print(f"Execution ID: {execution.execution_id}")
```

## 📚 Key Components

### Media Factory

**Purpose**: Manage media-related workflows (image, video, voice)

**Key Classes**:
- `MediaFactory` - Abstract base class for media workflows
- `MediaTask` - Represents a media processing task
- `ImageWorkflow` - Image generation and processing
- `VideoWorkflow` - Video generation and processing
- `VoiceWorkflow` - Voice/audio generation and processing

**Features**:
- Task-based workflow management
- Support for multiple models (Stable Diffusion, DALL-E, etc.)
- Batch processing capabilities
- Status tracking and error handling

### Research Factory

**Purpose**: Conduct market research and autonomous discovery

**Key Classes**:
- `ResearchFactory` - Abstract base class for research workflows
- `ResearchTask` - Represents a research task
- `MarketAnalysisWorkflow` - Market and competitive analysis
- `ResearchAgentWorkflow` - Autonomous research agents

**Features**:
- Multi-source data collection
- Competitive analysis
- Trend identification
- Autonomous discovery agents
- Priority-based task management

### Core Orchestration

**Purpose**: Coordinate multi-factory workflows

**Key Classes**:
- `OrchestrationEngine` - Main orchestration interface
- `WorkflowCoordinator` - Manage multi-step workflows
- `FactoryConnector` - Connect to different factories
- `TaskRouter` - Intelligent task routing

**Features**:
- Multi-factory workflow coordination
- Dependency management
- Parallel execution support
- Intelligent routing strategies
- Error recovery and retries

## 🔧 Integration with Existing Services

The factory architecture is designed to integrate with existing VoBee services:

### Media Factory → Existing Services
- **Image Workflow** → `image-generation` service (port 5000)
- **Video Workflow** → `video-generation` service (port 5001)
- **Voice Workflow** → Future voice service (port 5009)

### Research Factory → Existing Services
- **Research Agents** → `spy-orchestration` service (port 5006)
- **Market Analysis** → Data sources and analysis tools

### Orchestration → Existing Services
- **Workflow Execution** → `orchestrator` service (port 5003)
- **Task Routing** → `api-gateway` service (port 8000)

## 📖 Examples

Run the comprehensive integration demo:

```bash
python3 examples/factory_integration_demo.py
```

This demonstrates:
- Media factory workflows (image, video, voice)
- Research factory workflows (market analysis, research agents)
- Core orchestration (routing, multi-factory workflows)
- Task management and status tracking

## 🎯 Design Principles

1. **Modularity**: Each factory is independent and self-contained
2. **Extensibility**: Easy to add new workflows and factory types
3. **Reversibility**: All changes are non-destructive and can be reverted
4. **Auditability**: Task tracking and status management throughout
5. **Integration**: Designed to work with existing services

## 🔄 Workflow Execution Flow

```
User Request
     ↓
TaskRouter (Intelligent Routing)
     ↓
FactoryConnector (Factory Selection)
     ↓
WorkflowCoordinator (Step Orchestration)
     ↓
Factory Implementation (Task Execution)
     ↓
Result Aggregation
     ↓
Response to User
```

## 📝 Task States

### Media Tasks
- `PENDING` - Task created, awaiting processing
- `PROCESSING` - Task currently being processed
- `COMPLETED` - Task completed successfully
- `FAILED` - Task failed with error
- `CANCELLED` - Task cancelled by user

### Research Tasks
- `PENDING` - Task created, awaiting execution
- `COLLECTING_DATA` - Gathering data from sources
- `ANALYZING` - Performing analysis
- `COMPLETED` - Task completed successfully
- `FAILED` - Task failed with error
- `CANCELLED` - Task cancelled by user

## 🛣️ Routing Strategies

The task router supports multiple strategies:

1. **CONTENT_BASED** (Default) - Route based on task content and keywords
2. **PRIORITY_BASED** - Route based on task priority
3. **LOAD_BALANCED** - Distribute based on factory load
4. **ROUND_ROBIN** - Simple round-robin distribution
5. **CAPABILITY_BASED** - Route based on factory capabilities

## 🔮 Future Enhancements

- [ ] Async processing with webhooks
- [ ] Real-time progress tracking
- [ ] Result caching and retrieval
- [ ] Multi-step pipeline workflows
- [ ] Advanced error recovery
- [ ] Metrics and monitoring integration
- [ ] Additional factory types (Application, Data, Analytics)
- [ ] Machine learning-based routing
- [ ] Cost optimization

## 📄 Documentation

Each component has its own detailed README:
- [Media Factory README](factories/media/README.md)
- [Research Factory README](factories/research/README.md)
- [Core Orchestration README](core/orchestration/README.md)

## 🧪 Testing

All modules have been validated for:
- ✅ Import compatibility
- ✅ Interface consistency
- ✅ Workflow creation and execution
- ✅ Task routing and management
- ✅ Multi-factory coordination

## 🤝 Contributing

When extending the factory architecture:

1. Follow the established patterns in base classes
2. Implement all abstract methods
3. Add comprehensive docstrings
4. Update relevant README files
5. Test integration with existing components
6. Maintain backward compatibility

## 📞 Support

For questions or issues with the factory architecture:
- Review component READMEs for detailed documentation
- Run `examples/factory_integration_demo.py` for usage examples
- Check existing workflow implementations for patterns

---

**Version**: 0.1.0  
**Status**: ✅ Ready for Extension  
**Last Updated**: 2025-12-16
