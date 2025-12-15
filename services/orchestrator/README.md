# Orchestrator Service

Coordinates all AI services, manages task queues, and handles workflows with advanced bot swarm orchestration.

## Features

- **Task Orchestration** - Coordinate multiple AI services
- **Bot Swarm Management** - Up to 50,000 concurrent bots
- **L20 Tier Orchestration** - Advanced business products
- **Task Queue Management** - Redis-based queuing
- **Workflow Coordination** - Execute complex workflows
- **Service Discovery** - Dynamic service endpoints

## Bot Swarm Orchestration

### Capacity
- **Maximum bots**: 50,000 concurrent instances
- **Tiers**: Standard, Advanced, L20
- **Scalability**: Horizontal scaling across swarms

### Bot Tiers

#### Standard Tier
- Basic task execution
- Standard capabilities
- General purpose bots

#### Advanced Tier
- Enhanced processing power
- Specialized capabilities
- Higher priority task execution

#### L20 Tier
- Enterprise-grade orchestration
- Maximum capabilities
- Highest priority
- Advanced business products support

## API Endpoints

### Bot Management

#### Create Bot
```bash
POST /bots
Content-Type: application/json

{
  "name": "bot-worker-1",
  "tier": "L20",
  "capabilities": ["data_processing", "analytics", "reporting"]
}
```

**Response:**
```json
{
  "id": "bot-abc-123",
  "name": "bot-worker-1",
  "tier": "L20",
  "status": "active",
  "tasks_completed": 0,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Get Bot Status
```bash
GET /bots/{bot_id}
```

**Response:**
```json
{
  "id": "bot-abc-123",
  "name": "bot-worker-1",
  "tier": "L20",
  "status": "active",
  "tasks_completed": 150,
  "total_tasks": 200,
  "pending_tasks": 50,
  "completed_tasks": 150,
  "last_active": "2024-01-01T00:00:00Z"
}
```

#### Get Bot Statistics
```bash
GET /bots/stats
```

**Response:**
```json
{
  "total_created": 10000,
  "active_bots": 8500,
  "tasks_executed": 1500000,
  "tier_distribution": {
    "standard": 5000,
    "advanced": 2500,
    "L20": 1000
  },
  "swarm_count": 25,
  "capacity_remaining": 41500,
  "utilization_percent": 17.0,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Swarm Management

#### Create Bot Swarm
```bash
POST /swarms
Content-Type: application/json

{
  "name": "processing-swarm",
  "count": 5000,
  "tier": "L20",
  "capabilities": ["data_processing", "analytics", "ml_inference"]
}
```

**Response:**
```json
{
  "id": "swarm-xyz-456",
  "name": "processing-swarm",
  "bot_count": 5000,
  "tier": "L20",
  "bot_ids": ["bot-1", "bot-2", "..."],
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Get Swarm Status
```bash
GET /swarms/{swarm_id}
```

**Response:**
```json
{
  "id": "swarm-xyz-456",
  "name": "processing-swarm",
  "bot_count": 5000,
  "tier": "L20",
  "active_bots": 4850,
  "total_tasks_completed": 750000,
  "average_tasks_per_bot": 150.0,
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Task Assignment

#### Assign Task to Bot
```bash
POST /bots/{bot_id}/tasks
Content-Type: application/json

{
  "type": "data_processing",
  "data": {
    "input_file": "data.csv",
    "operations": ["clean", "transform", "analyze"]
  }
}
```

**Response:**
```json
{
  "task_id": "task-123",
  "bot_id": "bot-abc-123",
  "task_type": "data_processing",
  "status": "assigned",
  "assigned_at": "2024-01-01T00:00:00Z"
}
```

#### Assign Task to Swarm (Mass-Action)
```bash
POST /swarms/{swarm_id}/tasks
Content-Type: application/json

{
  "type": "distributed_analysis",
  "data": {
    "dataset": "large_dataset.csv",
    "analysis_type": "sentiment",
    "chunk_size": 1000
  }
}
```

**Response:**
```json
{
  "swarm_id": "swarm-xyz-456",
  "task_type": "distributed_analysis",
  "assignments": 5000,
  "status": "distributed",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Complete Bot Task
```bash
POST /bots/{bot_id}/tasks/{task_id}/complete
```

### Traditional Orchestration

#### Orchestrate Workflow
```bash
POST /orchestrate
Content-Type: application/json

{
  "tasks": [
    {
      "type": "image_generation",
      "params": {"prompt": "Sunset landscape"}
    },
    {
      "type": "crypto_prediction",
      "params": {"symbol": "BTC"}
    }
  ],
  "priority": "high"
}
```

#### Get Task Status
```bash
GET /task/{task_id}
```

## Usage Examples

### Create L20 Bot Swarm
```python
import requests

swarm_config = {
    "name": "enterprise-processing-swarm",
    "count": 10000,
    "tier": "L20",
    "capabilities": [
        "data_processing",
        "ml_inference",
        "analytics",
        "reporting"
    ]
}

response = requests.post('http://localhost:5003/swarms', json=swarm_config)
swarm = response.json()
print(f"Created swarm with {swarm['bot_count']} bots")
print(f"Swarm ID: {swarm['id']}")
```

### Distribute Task Across Swarm
```python
import requests

task = {
    "type": "mass_data_processing",
    "data": {
        "dataset": "customer_data_2024.csv",
        "operations": ["clean", "enrich", "analyze"],
        "output_format": "json"
    }
}

response = requests.post('http://localhost:5003/swarms/swarm-123/tasks', 
                        json=task)
result = response.json()
print(f"Task distributed to {result['assignments']} bots")
```

### Monitor Bot Performance
```python
import requests

# Get overall statistics
response = requests.get('http://localhost:5003/bots/stats')
stats = response.json()

print(f"Active bots: {stats['active_bots']}")
print(f"Tasks executed: {stats['tasks_executed']}")
print(f"Utilization: {stats['utilization_percent']}%")

# Get specific bot status
response = requests.get('http://localhost:5003/bots/bot-abc-123')
bot = response.json()
print(f"Bot {bot['name']}: {bot['tasks_completed']} tasks completed")
```

### Monitor Swarm Health
```python
import requests

response = requests.get('http://localhost:5003/swarms/swarm-123')
swarm = response.json()

print(f"Swarm: {swarm['name']}")
print(f"Active bots: {swarm['active_bots']} / {swarm['bot_count']}")
print(f"Total tasks: {swarm['total_tasks_completed']}")
print(f"Avg tasks/bot: {swarm['average_tasks_per_bot']}")
```

## L20 Orchestration Features

The L20 tier provides enterprise-grade capabilities:

- **50,000 bot capacity** - Maximum concurrent bots
- **Priority execution** - Highest priority task processing
- **Advanced analytics** - Detailed performance metrics
- **Custom capabilities** - Tailored bot configurations
- **High availability** - Automatic failover and recovery
- **Scalable architecture** - Horizontal scaling support

## Architecture

### Bot Lifecycle
1. **Creation** - Bot instantiated with tier and capabilities
2. **Assignment** - Tasks assigned to bot or swarm
3. **Execution** - Bot processes assigned tasks
4. **Monitoring** - Real-time health and performance tracking
5. **Completion** - Task marked complete, stats updated

### Swarm Coordination
1. **Swarm Creation** - Multiple bots created as a group
2. **Task Distribution** - Tasks distributed across all bots
3. **Load Balancing** - Even distribution of workload
4. **Health Monitoring** - Track swarm and individual bot health
5. **Scaling** - Add/remove bots dynamically

## Configuration

Environment variables:
- `REDIS_HOST` - Redis hostname (default: redis-service)
- `REDIS_PORT` - Redis port (default: 6379)
- `POSTGRES_HOST` - PostgreSQL hostname
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `IMAGE_SERVICE_URL` - Image generation service URL
- `VIDEO_SERVICE_URL` - Video generation service URL
- `CRYPTO_SERVICE_URL` - Crypto prediction service URL
- `FRAUD_SERVICE_URL` - Fraud detection service URL
- `COMPRESSION_SERVICE_URL` - Compression service URL
- `MARKETING_SERVICE_URL` - Marketing intelligence service URL

## Docker

```bash
# Build
docker build -t orchestrator-service .

# Run
docker run -p 5003:5003 \
  -e REDIS_HOST=redis \
  -e POSTGRES_HOST=postgres \
  orchestrator-service
```

## Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "orchestrator",
  "redis": "connected",
  "timestamp": "2024-01-01T00:00:00Z"
}
```
