# Vobio AI Studio - Architecture

## System Overview

Vobio AI Studio is a production-ready AI orchestration platform with complete runtime contracts, safety systems, and observability.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│                  Login | Chat | Image | Video | LifeSync        │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vobio API (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ API Server (api_server_integrated.py)                    │  │
│  │  - Authentication & Authorization                         │  │
│  │  - Request Routing                                        │  │
│  │  - Global Error Handling                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌────────────┬────────────┼────────────┬───────────┐          │
│  ▼            ▼            ▼            ▼           ▼          │
│ ┌────┐  ┌─────────┐  ┌────────┐  ┌──────────┐ ┌───────┐      │
│ │Feat│  │Identity │  │Safety  │  │Cost      │ │Approva│      │
│ │Gate│  │Manager  │  │System  │  │Tracker   │ │l Queue│      │
│ │    │  │         │  │        │  │          │ │       │      │
│ └────┘  └─────────┘  └────────┘  └──────────┘ └───────┘      │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ AI Orchestrator (LangGraph)                              │  │
│  │  - State Management                                      │  │
│  │  - Workflow Execution                                    │  │
│  │  - Operation Routing                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌────────────┬────────────┼────────────┬───────────┐          │
│  ▼            ▼            ▼            ▼           ▼          │
│ ┌────┐  ┌─────────┐  ┌────────┐  ┌──────────┐ ┌───────┐      │
│ │Chat│  │Image    │  │Video   │  │LifeSync  │ │Memory │      │
│ │Mock│  │Gen Mock │  │Gen Mock│  │Module    │ │Service│      │
│ └────┘  └─────────┘  └────────┘  └──────────┘ └───────┘      │
└────────────────────────┬─────────────┬──────────────────────────┘
                         │             │
          ┌──────────────┼─────────────┼──────────────┐
          ▼              ▼             ▼              ▼
    ┌──────────┐   ┌─────────┐  ┌──────────┐  ┌──────────┐
    │ Qdrant   │   │Langfuse │  │   OTEL   │  │PostgreSQL│
    │ (Vector) │   │ (Obs)   │  │Collector │  │(Langfuse)│
    └──────────┘   └─────────┘  └──────────┘  └──────────┘
```

## Component Responsibilities

### 1. API Server (`api_server_integrated.py`)
- **Purpose**: Main entry point for all client requests
- **Responsibilities**:
  - Route HTTP requests to appropriate handlers
  - Enforce authentication (X-User-ID header)
  - Apply CORS policies
  - Handle errors globally
  - Initialize all services on startup
- **Dependencies**: All other modules

### 2. Telemetry (`telemetry.py`)
- **Purpose**: Distributed tracing and metrics
- **Technology**: OpenTelemetry
- **Responsibilities**:
  - Setup OTLP exporters
  - Instrument FastAPI application
  - Provide tracer and meter instances
- **Exports to**: OTEL Collector → Langfuse

### 3. Feature Gates (`feature_gates.py`)
- **Purpose**: Runtime feature toggles
- **Technology**: OpenFeature SDK
- **Responsibilities**:
  - Manage feature flags (code execution, image gen, etc.)
  - Allow environment-based overrides
  - Provide feature status API
- **Configuration**: In-memory provider (can be extended to remote)

### 4. Identity Manager (`identity.py`)
- **Purpose**: User authentication
- **Technology**: WebAuthn (mock), JWT
- **Responsibilities**:
  - Authenticate users via passkey (mock mode)
  - Create and verify JWT session tokens
  - Manage user sessions
- **Storage**: In-memory (production would use Redis/DB)

### 5. Memory Service (`memory_service.py`)
- **Purpose**: User context and memory storage
- **Technology**: Qdrant vector database
- **Responsibilities**:
  - Store user memories as vectors
  - Search relevant memories by query
  - Provide context for AI interactions
- **Fallback**: Mock embeddings if Qdrant unavailable

### 6. Cost Tracker (`cost_tracker.py`)
- **Purpose**: Usage tracking and limit enforcement
- **Technology**: Langfuse
- **Responsibilities**:
  - Track hourly/daily costs per user
  - Enforce configurable limits
  - Log traces to Langfuse for observability
- **Limits**: Hourly ($2), Daily ($10) - configurable via env

### 7. Safety System (`safety_system.py`)
- **Purpose**: Code and API safety validation
- **Technology**: RestrictedPython
- **Responsibilities**:
  - Validate Python code for dangerous operations
  - Check file operations against protected files
  - Sanitize outputs to prevent XSS
  - Quarantine dangerous files
- **Protected**: Core system files, config, .env

### 8. Human Approval Queue (`human_approval.py`)
- **Purpose**: Operations requiring human review
- **Responsibilities**:
  - Create approval requests for risky operations
  - Track request status (pending/approved/rejected/expired)
  - Expire requests after timeout (24h default)
  - Provide approval API for reviewers

### 9. AI Orchestrator (`ai_orchestrator.py`)
- **Purpose**: Coordinate AI operations
- **Technology**: LangGraph
- **Responsibilities**:
  - Build and execute state graphs
  - Route operations to appropriate handlers
  - Validate inputs
  - Format outputs
- **Operations**: chat, generate_image, generate_video, lifesync_decision

### 10. LifeSync Module (`lifesync_module.py`)
- **Purpose**: Decision assistance system
- **Responsibilities**:
  - Analyze decision scenarios
  - Score options based on multiple factors
  - Provide recommendations with reasoning
  - Track decision outcomes (future learning)

## Data Flow

### Example: Image Generation Request

1. **Client** → POST `/api/generate/image` with prompt
2. **API Server** → Verify X-User-ID header
3. **Feature Gates** → Check if `enable_image_generation` is on
4. **Cost Tracker** → Verify user hasn't exceeded limits
5. **Safety System** → Validate prompt for dangerous content
6. **AI Orchestrator** → Execute through LangGraph
   - Validate input
   - Check safety
   - Execute mock generation
   - Format output
7. **Cost Tracker** → Log cost to Langfuse
8. **Memory Service** → Store interaction
9. **API Server** → Return result to client

## Runtime Contract

### OpenFeature (Feature Flags)
- **Provider**: In-Memory
- **Purpose**: Enable/disable features without deployment
- **Flags**: code_execution, image_generation, video_generation, lifesync, human_approval, cost_tracking, safety_checks

### LangGraph (Orchestration)
- **Purpose**: Stateful AI workflows
- **Nodes**: validate_input → check_safety → execute_operation → format_output
- **State**: Carries user_id, operation, input_data, result, error

### Langfuse (Observability)
- **Purpose**: Cost tracking, tracing, analytics
- **Data**: Traces, generations, costs, metadata
- **Access**: http://localhost:3000

### OpenTelemetry (Tracing)
- **Purpose**: Distributed tracing and metrics
- **Exporter**: OTLP to collector
- **Instrumentation**: FastAPI automatic

### Qdrant (Vector Memory)
- **Purpose**: User context storage
- **Collection**: user_memories
- **Vector Size**: 384 (mock embeddings)

### Passkey (Identity)
- **Purpose**: Passwordless authentication
- **Implementation**: Mock mode (JWT sessions)
- **Real Mode**: Would use WebAuthn API

## Security Architecture

### Defense in Depth

1. **Input Validation**: All requests validated by Pydantic models
2. **Authentication**: X-User-ID header required for protected endpoints
3. **Authorization**: Feature gates control access
4. **Rate Limiting**: Cost tracker enforces usage limits
5. **Code Safety**: RestrictedPython validates code execution
6. **File Protection**: Protected files cannot be modified
7. **Output Sanitization**: HTML escaping prevents XSS
8. **Quarantine**: Dangerous files isolated

### Protected Resources

- Core Python modules
- Configuration files
- Environment variables
- Docker Compose files

### Allowed Operations

- Write to: skills/, knowledge/, temp/, logs/
- Read: All files (with safety checks)
- Execute: Validated code only (when enabled)

## Scalability

### Horizontal Scaling

- **API Server**: Stateless, can run multiple instances
- **Load Balancer**: Add nginx/traefik in front
- **Session Storage**: Move from in-memory to Redis
- **Database**: Qdrant, Langfuse-DB already persistent

### Vertical Scaling

- **AI Operations**: Currently mocked, add GPU workers
- **Vector Search**: Qdrant supports large collections
- **Observability**: Langfuse handles high trace volumes

## Monitoring

### Health Checks

- `/health` - API status and feature flags
- Qdrant: `/health`
- Langfuse: `/api/health`
- OTEL Collector: port 13133

### Logs

- **Level**: Configurable via LOG_LEVEL env
- **Format**: Structured JSON
- **Location**: Docker logs (stdout)

### Metrics (via OTEL)

- Request count
- Request duration
- Error rate
- Cost per user

## Future Enhancements

1. **Real AI Integration**: Replace mocks with actual models
2. **Persistent Sessions**: Redis for session storage
3. **Advanced RBAC**: Role-based access control
4. **Webhook Support**: Async notifications
5. **API Versioning**: /v1/, /v2/ endpoints
6. **GraphQL API**: Alternative to REST
7. **WebSocket**: Real-time updates
8. **Multi-tenancy**: Organization support
