# Personal AI Operating System - Architecture Overview

## Vision

VoBee AI Assistant is evolving into a **Personal AI Operating System** capable of orchestrating 30-100 logical AI roles to manage complex multi-project workflows with deterministic behavior, comprehensive auditing, and human-in-the-loop decision making.

## Core Principles

### 1. **Deterministic Behavior**
- All operations are logged and traceable
- No "magic" - everything is explicit and documented
- Reproducible results through consistent state management

### 2. **Modular Architecture**
- Isolated subsystems with clear interfaces
- No hard vendor lock-ins
- Pluggable components for flexibility

### 3. **Human-in-the-Loop**
- Critical decisions require explicit human approval
- Agents produce artifacts and recommendations only
- No autonomous actions on production systems

### 4. **Comprehensive Auditing**
- All actions logged with timestamps
- Decision trail maintained
- Budget and cost tracking at every level

### 5. **Incremental Evolution**
- Changes made in small, verifiable steps
- Continuous validation and testing
- Progressive enhancement without breaking existing functionality

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Personal AI Operating System                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼──────┐ ┌───▼────────┐ ┌──▼──────────┐
        │    Core      │ │   Agents   │ │   Legacy    │
        │  Framework   │ │  Registry  │ │  Services   │
        └───────┬──────┘ └────┬───────┘ └──┬──────────┘
                │             │             │
    ┌───────────┼─────────────┼─────────────┼───────────┐
    │           │             │             │           │
┌───▼────┐ ┌───▼────┐ ┌──────▼──────┐ ┌───▼────┐ ┌───▼────┐
│Project │ │Decision│ │   Cost      │ │30-100  │ │Existing│
│Cortex  │ │ Gate   │ │   Guard     │ │Agents  │ │ AI Svc │
└────────┘ └────────┘ └─────────────┘ └────────┘ └────────┘
```

## Core Framework Components

### 1. Project Cortex - Multi-Project Management

**Purpose**: Manage multiple projects with isolated contexts, budgets, and execution profiles.

**Key Features**:
- **Project Manager**: Lifecycle management (create, activate, pause, archive)
- **Project Memory**: Isolated memory per project with context, history, and patterns
- **Budget Profile**: Per-project budget tracking with alerts and enforcement
- **Quality Profile**: Speed vs. quality tradeoffs (speed/balanced/quality modes)

**State Management**:
- Active: Currently executing
- Paused: Suspended but state preserved
- Archived: Historical reference
- Initializing: Setup phase

**Example Use Case**:
```python
from core.project_cortex import ProjectManager

# Create and configure project
pm = ProjectManager()
project = pm.create_project(
    project_id="ai-chatbot-v2",
    name="AI Chatbot V2",
    budget_limit=500.00,
    quality_preference="balanced"
)

# Activate for work
pm.activate_project("ai-chatbot-v2")

# Track spending
pm.update_budget_usage("ai-chatbot-v2", cost=1.50)
```

### 2. Decision Gate - Explicit Confirmation System

**Purpose**: Ensure critical operations require human approval before execution.

**Key Features**:
- **Decision Manager**: Queue and track decisions requiring approval
- **Confirmation Workflow**: Pre-built patterns for common scenarios
- **Decision Types**: Deployment, branch merge, budget change, data deletion, etc.
- **Risk Levels**: Low, medium, high, critical
- **Auto-Expiration**: Decisions expire if not approved within timeframe

**Workflow**:
1. System requests decision
2. Human reviews proposed action
3. Human approves or rejects
4. If approved, system executes
5. Result logged for audit

**Example Use Case**:
```python
from core.decision_gate import DecisionManager, ConfirmationWorkflow

dm = DecisionManager()
workflow = ConfirmationWorkflow(dm)

# Request deployment approval
decision_id = workflow.confirm_deployment(
    environment="production",
    services=["api-gateway", "orchestrator"],
    version="v2.1.0",
    rollback_plan="Revert to v2.0.5 if errors > 5%"
)

# Later, human approves
dm.approve_decision(decision_id, approved_by="admin", notes="LGTM")

# Execute with executor function
dm.execute_decision(decision_id, execute_deployment, executor_id="deploy-bot")
```

### 3. Cost Guard - Cost Optimization & Routing

**Purpose**: Optimize costs through intelligent routing and enforce budget ceilings.

**Key Features**:
- **Cost Router**: Route requests to cost-effective providers
- **Cost Monitor**: Real-time tracking with alerts
- **Cost Optimizer**: Recommendations for cost reduction
- **Routing Strategies**: Cheapest, best value, quality-first, load-balanced

**Routing Example**:
```python
from core.cost_guard import CostRouter, RoutingStrategy

router = CostRouter(strategy=RoutingStrategy.BEST_VALUE)

# Route a text generation request
provider, metadata = router.route_request(
    request_type="text_generation",
    quality_requirement=0.8,
    budget_limit=0.05,
    estimated_tokens=1000
)
# Returns: ("gpt-3.5-turbo", {cost: 0.002, quality: 0.80})
```

**Cost Monitoring**:
```python
from core.cost_guard import CostMonitor

monitor = CostMonitor(global_cost_ceiling=1000.00)

# Record costs
monitor.record_cost(
    amount=0.02,
    service="image_generation",
    project_id="marketing-assets"
)

# Get spending report
report = monitor.get_cost_report()
# Shows: total, by service, by project, remaining budget
```

## Multi-Agent System

### Agent Architecture

**Base Agent**: All agents inherit from `BaseAgent` which provides:
- Guardrail enforcement
- Artifact generation
- Activity logging
- Permission validation

**Guardrails** (strictly enforced):
- ❌ No direct code commits
- ❌ No automatic deployments
- ❌ No main branch modifications
- ✅ Generate artifacts only
- ✅ Provide recommendations
- ✅ Require human approval for execution

### Agent Categories

#### 1. Architecture & Design
- **Architect Agent**: System design, architecture review, pattern recommendations
- Future: Cloud Architect, Data Architect, Security Architect

#### 2. Research & Analysis
- **Market Research Agent**: Market analysis, competitor research, trend identification
- Future: Technical Research, User Research, Competitive Intelligence

#### 3. Compliance & Security
- **Compliance Agent**: Security audits, compliance reviews, risk assessment
- Future: Legal Review, Privacy Officer, Audit Specialist

#### 4. Media & Content
- **Media Generation Agent**: Image/video specifications, content planning
- Future: Video Editor, Graphic Designer, Content Strategist

### Agent Workflow

```
┌──────────────┐
│ Task Request │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌─────────────┐
│    Agent     │─────▶│  Validate   │
│  Execution   │      │  Guardrails │
└──────┬───────┘      └─────────────┘
       │
       ▼
┌──────────────┐
│  Generate    │
│  Artifact    │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌─────────────┐
│   Request    │─────▶│   Human     │
│  Approval    │      │  Reviews    │
└──────────────┘      └─────┬───────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
              ┌─────────┐      ┌─────────┐
              │ Approve │      │ Reject  │
              └────┬────┘      └─────────┘
                   │
                   ▼
              ┌─────────┐
              │ Execute │
              └────┬────┘
                   │
                   ▼
              ┌─────────┐
              │  Audit  │
              │   Log   │
              └─────────┘
```

### Scaling to 30-100 Agents

The system is designed to support 30-100 specialized logical agents:

**Current**: 4 core agents (Architect, Market Research, Compliance, Media Generation)

**Planned Categories**:
- Development (Backend, Frontend, Mobile, DevOps, QA)
- Operations (SRE, Monitoring, Incident Response)
- Product (Product Manager, UX Designer, Business Analyst)
- Data (Data Scientist, ML Engineer, Data Engineer)
- Support (Technical Support, Documentation, Training)

Each agent operates independently with enforced guardrails ensuring no autonomous actions.

## Integration with Existing Services

The new framework integrates with existing VoBee services:

```
New Framework          Existing Services
┌──────────────┐      ┌──────────────────┐
│Project Cortex│─────▶│ API Gateway      │
└──────────────┘      └──────────────────┘
                             │
┌──────────────┐      ┌──────┴──────────┐
│Decision Gate │      │ Image Gen       │
└──────────────┘      │ Video Gen       │
                      │ Crypto Predict  │
┌──────────────┐      │ Orchestrator    │
│ Cost Guard   │─────▶│ Worker Pool     │
└──────────────┘      └─────────────────┘

┌──────────────┐
│   Agents     │───┐
└──────────────┘   │
                   ▼
            ┌──────────────┐
            │ Artifact     │
            │ Generation   │
            └──────────────┘
```

## Data Flow

### Project Execution Flow
1. Create/activate project in Project Cortex
2. Agent analyzes requirements and generates artifacts
3. Decision Gate requests approval for actions
4. Cost Guard routes requests efficiently
5. Budget Profile tracks spending
6. Quality Profile controls execution parameters
7. All actions logged to Project Memory
8. Audit trail maintained in Decision Gate

## Security & Compliance

### Multi-Layer Security
- **Agent Guardrails**: Prevent unauthorized actions
- **Decision Gate**: Human approval for critical operations
- **Compliance Agent**: Regular security audits
- **Audit Logging**: Complete action history
- **Budget Controls**: Financial risk mitigation

### Compliance Features
- GDPR compliance tracking
- SOC 2 readiness
- Security audit reports
- Data handling policies
- Privacy-by-design principles

## Monitoring & Observability

### What Gets Logged
- All agent actions and outputs
- Decision requests and approvals
- Cost transactions
- Budget utilization
- Quality profile changes
- Project state transitions

### Audit Trail
Every action includes:
- Timestamp (UTC)
- Actor (human or agent ID)
- Action type
- Parameters
- Result
- Associated artifacts

## Future Enhancements

### Planned Features
- [ ] Agent orchestration engine for multi-agent collaboration
- [ ] Advanced cost prediction using ML models
- [ ] Automated performance optimization suggestions
- [ ] Integration with external project management tools
- [ ] Voice interface for decision approvals
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] Custom agent creation framework

### Scalability Targets
- Support 100+ concurrent projects
- Handle 1000+ decisions per day
- Track 10,000+ agent actions per day
- Maintain <100ms decision lookup latency
- Process 100+ agent requests simultaneously

## Getting Started

See individual component documentation:
- [Decision Gate Workflows](decision_gate_workflows.md)
- [Core Adjustment Procedures](core_adjustment_procedures.md)
- [Agent Output Artifacts](agent_artifacts_examples.md)

---

**Note**: This is an evolving architecture. All changes are made incrementally with human oversight. See TODO markers throughout the codebase for areas requiring human decisions.
