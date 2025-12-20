# Orchestration Guide

## 🧠 Understanding the Orchestrator Brain

The VoBee AI Orchestrator is the intelligent core that coordinates all AI modules, routes tasks, manages resources, and continuously learns to improve performance.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Request                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               AI Brain (Decision Making)                 │
│  - Analyzes request                                      │
│  - Prioritizes tasks                                     │
│  - Allocates resources                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Task Router (Intelligent Routing)             │
│  - Finds capable services                                │
│  - Load balancing                                        │
│  - Fallback strategies                                   │
└────────────────────┬────────────────────────────────────┘
                     │
            ┌────────┴────────┐
            ▼                 ▼
┌──────────────────┐   ┌──────────────────┐
│   AI Service 1   │   │   AI Service 2   │
│  (email-ai)      │   │  (content-ai)    │
└────────┬─────────┘   └────────┬─────────┘
         │                      │
         └──────────┬───────────┘
                    ▼
┌─────────────────────────────────────────────────────────┐
│          Memory System (Learning & Context)              │
│  - Stores results                                        │
│  - Learns patterns                                       │
│  - Improves over time                                    │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│        Self-Improvement (Performance Analysis)           │
│  - Analyzes performance                                  │
│  - Suggests optimizations                                │
│  - Tracks improvements                                   │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Core Components

### 1. AI Brain (`ai-brain.py`)

**Purpose**: Central intelligence for decision-making

**Key Functions**:
```python
from services.orchestrator.ai_brain import ai_brain

# Make intelligent decision
decision = ai_brain.make_decision({
    'task_type': 'email_campaign',
    'priority': 'high',
    'resources': {'cpu': 4, 'memory': 8192}
})

# Prioritize tasks
tasks = [
    {'type': 'email_campaign', 'priority': 'normal'},
    {'type': 'finance', 'priority': 'high'}
]
prioritized = ai_brain.prioritize_tasks(tasks)

# Learn from results
ai_brain.learn_from_result({
    'task_type': 'email_campaign',
    'success': True,
    'execution_time': 5.2
})
```

**Decision Process**:
1. Analyzes task context
2. Selects best service based on past performance
3. Allocates resources
4. Calculates confidence score
5. Provides reasoning

### 2. Task Router (`task-router.py`)

**Purpose**: Intelligent task routing with load balancing

**Key Functions**:
```python
from services.orchestrator.task_router import task_router

# Register a service
task_router.register_service(
    service_name='email-ai',
    endpoint='http://email-ai:5100',
    capabilities=['email_campaign', 'email_automation']
)

# Route a task
routing_decision = task_router.route_task({
    'id': 'task_123',
    'type': 'email',
    'requirements': {}
})

# Handle failure with fallback
fallback_decision = task_router.handle_failure(routing_decision)

# Update service health
task_router.update_service_health('email-ai', 'healthy')
```

**Routing Strategy**:
1. Find all capable services
2. Filter healthy services
3. Apply load balancing (round-robin, random, least-loaded)
4. Select primary and fallback services
5. Return routing decision with retry strategy

### 3. Memory System (`memory-system.py`)

**Purpose**: Store results, learn patterns, manage context

**Key Functions**:
```python
from services.orchestrator.memory_system import memory_system

# Store task result
memory_system.store_task_result(
    task_id='task_123',
    task_data={'type': 'email_campaign'},
    result={'success': True, 'execution_time': 5.2}
)

# Get success patterns
patterns = memory_system.get_success_patterns('email_campaign')

# Create context for related tasks
memory_system.create_context('campaign_2024', {
    'campaign_name': 'Q1 Launch',
    'target_audience': 'tech_enthusiasts'
})

# Get context
context = memory_system.get_context('campaign_2024')

# Get relevant memories
memories = memory_system.get_relevant_memories('email_campaign', limit=10)
```

**Memory Types**:
- **Short-term**: Last 100 tasks
- **Long-term**: Patterns and statistics
- **Context**: Active execution contexts
- **Pattern Library**: Learned patterns

### 4. Self-Improvement (`self-improvement.py`)

**Purpose**: Analyze performance and suggest optimizations

⚠️ **IMPORTANT**: ONLY SUGGESTS - NEVER AUTO-APPLIES

**Key Functions**:
```python
from services.orchestrator.self_improvement import self_improvement

# Analyze performance
analysis = self_improvement.analyze_performance(time_window=24)

# Get pending suggestions
high_priority = self_improvement.get_pending_suggestions(priority='high')

# Track implementation
self_improvement.track_improvement(
    suggestion_id='sug_123',
    result={
        'success': True,
        'impact': {
            'before': {'response_time': 3.5},
            'after': {'response_time': 2.1},
            'improvement': {'response_time_reduction': '40%'}
        }
    }
)

# Get improvement report
report = self_improvement.get_improvement_report()
```

**Analysis Areas**:
- Performance bottlenecks
- Resource utilization
- Service health
- Optimization opportunities

### 5. Module Manager (`module-manager.py`)

**Purpose**: Control AI modules lifecycle

**Key Functions**:
```python
from services.orchestrator.module_manager import module_manager

# Get all modules
all_modules = module_manager.get_all_modules()

# Get modules by category
business_modules = module_manager.get_all_modules(category='business')

# Get enabled modules only
enabled = module_manager.get_all_modules(enabled_only=True)

# Enable module
module_manager.enable_module('email-ai')

# Disable module
module_manager.disable_module('email-ai')

# Get module status
status = module_manager.get_module_status('email-ai')

# Get health summary
health = module_manager.get_health_summary()

# Get modules by category
by_category = module_manager.get_modules_by_category()
```

**Module States**:
- **Enabled**: Active and available
- **Disabled**: Inactive but configured
- **Healthy**: Working correctly
- **Degraded**: Partial functionality
- **Unhealthy**: Not working

## 🔄 Task Execution Flow

### Complete Flow Example

```python
# 1. Receive task request
task = {
    'id': 'task_123',
    'type': 'email_campaign',
    'priority': 'high',
    'data': {
        'subject': 'Product Launch',
        'content': 'Check out our new product...',
        'audience': 'customers'
    }
}

# 2. AI Brain makes decision
decision = ai_brain.make_decision({
    'task_type': task['type'],
    'priority': task['priority'],
    'resources': {'cpu': 4, 'memory': 8192}
})
# Result: {
#   'selected_service': 'email-ai',
#   'priority_level': 3,
#   'confidence': 0.85
# }

# 3. Task Router finds route
routing = task_router.route_task(task)
# Result: {
#   'primary_service': 'email-ai',
#   'endpoint': 'http://email-ai:5100',
#   'fallback_services': ['marketing-ai'],
#   'retry_strategy': {'max_retries': 3, 'backoff': 'exponential'}
# }

# 4. Execute task (simplified)
import requests
try:
    response = requests.post(
        routing['endpoint'] + '/process',
        json=task['data'],
        timeout=30
    )
    result = response.json()
    success = True
except Exception as e:
    # 5. Handle failure with fallback
    routing = task_router.handle_failure(routing)
    success = False
    result = {'error': str(e)}

# 6. Store result in memory
memory_system.store_task_result(
    task_id=task['id'],
    task_data=task,
    result={'success': success, 'data': result, 'execution_time': 5.2}
)

# 7. Learn from result
ai_brain.learn_from_result({
    'task_type': task['type'],
    'success': success,
    'execution_time': 5.2
})
```

## 📊 Task Prioritization

### Priority Levels

```python
priority_scores = {
    'critical': 4,  # Security, fraud, urgent issues
    'high': 3,      # Important business operations
    'normal': 2,    # Regular operations
    'low': 1        # Background tasks, non-urgent
}
```

### Task Type Priority Modifiers

```python
type_multipliers = {
    'fraud_detection': 1.5,  # Security tasks
    'finance': 1.5,          # Financial operations
    'crypto_prediction': 1.2,# Time-sensitive
    'email_campaign': 1.0,   # Standard
    'video_generation': 0.8  # Resource-intensive
}
```

### Example Prioritization

```python
tasks = [
    {'type': 'email_campaign', 'priority': 'normal'},   # Score: 2.0
    {'type': 'fraud_detection', 'priority': 'high'},    # Score: 4.5
    {'type': 'video_generation', 'priority': 'high'},   # Score: 2.4
    {'type': 'finance', 'priority': 'critical'}         # Score: 6.0
]

# After prioritization:
# 1. finance (6.0)
# 2. fraud_detection (4.5)
# 3. video_generation (2.4)
# 4. email_campaign (2.0)
```

## 🔄 Retry Strategies

### Exponential Backoff

```python
retry_strategy = {
    'max_retries': 3,
    'backoff': 'exponential',
    'timeout': 30
}

# Retry delays: 1s, 2s, 4s, 8s...
```

### Linear Backoff

```python
retry_strategy = {
    'max_retries': 3,
    'backoff': 'linear',
    'timeout': 60
}

# Retry delays: 5s, 10s, 15s...
```

## 🎯 Load Balancing Strategies

### Round Robin

```python
# Distributes tasks evenly across services
# Task 1 → Service A
# Task 2 → Service B
# Task 3 → Service C
# Task 4 → Service A (cycles back)
```

### Random

```python
# Randomly selects a service
# Good for unpredictable loads
```

### Least Loaded

```python
# Selects service with lowest current load
# Requires load metrics from services
```

## 📈 Learning & Improvement

### What the System Learns

1. **Success Rates**: Which services succeed for which tasks
2. **Execution Times**: How long tasks take
3. **Error Patterns**: Common failure modes
4. **Resource Usage**: Optimal resource allocation
5. **Best Practices**: Patterns that lead to success

### How Learning Improves Performance

```python
# Initial: No historical data
decision_1 = ai_brain.make_decision({'task_type': 'email_campaign'})
# confidence: 0.7 (default)

# After 10 successful executions
decision_2 = ai_brain.make_decision({'task_type': 'email_campaign'})
# confidence: 0.92 (learned from history)

# After 100 executions with 95% success rate
decision_3 = ai_brain.make_decision({'task_type': 'email_campaign'})
# confidence: 0.98 (high confidence)
```

## 🔒 Safety Mechanisms

### 1. Health Monitoring

```python
# Continuous health checks
task_router.update_service_health('email-ai', 'healthy')

# Only route to healthy services
routing = task_router.route_task(task)  # Filters unhealthy
```

### 2. Fallback Strategies

```python
# Primary service fails → Use fallback
routing = {
    'primary_service': 'email-ai',
    'fallback_services': ['marketing-ai', 'content-ai']
}
```

### 3. Dependency Management

```python
# Can't disable service with active dependents
result = module_manager.disable_module('database-connector')
# Error: "Required by email-ai, finance-ai"
```

### 4. Suggestions Only (Self-Improvement)

```python
# Self-improvement NEVER auto-applies
suggestion = {
    'action': 'increase_cpu',
    'auto_apply': False,  # Always False
    'requires': 'MANUAL_APPROVAL'
}
```

## 📊 Monitoring & Observability

### Get System Stats

```python
# Routing statistics
stats = task_router.get_routing_stats()
# {
#   'total_routes': 1000,
#   'service_distribution': {'email-ai': 400, 'content-ai': 600}
# }

# Memory summary
memory_summary = memory_system.get_memory_summary()
# {
#   'short_term_count': 100,
#   'long_term_types': 15,
#   'patterns_learned': 25
# }

# Health summary
health = module_manager.get_health_summary()
# {
#   'total_modules': 30,
#   'enabled': 28,
#   'healthy': 27
# }

# Performance summary
performance = ai_brain.get_performance_summary()
# {
#   'total_decisions': 5000,
#   'task_types_learned': 20
# }
```

## 🎯 Best Practices

1. **Always Check Health**: Before routing, ensure services are healthy
2. **Use Priorities**: Set appropriate priority levels for tasks
3. **Learn Continuously**: Let the system learn from all executions
4. **Monitor Performance**: Regularly check orchestrator metrics
5. **Review Suggestions**: Act on self-improvement suggestions
6. **Enable Gradually**: Enable new modules one at a time
7. **Test Fallbacks**: Ensure fallback strategies work

---

*Last Updated: 2024-01-20*
