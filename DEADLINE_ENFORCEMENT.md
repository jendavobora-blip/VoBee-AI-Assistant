# Deadline Enforcement for Swarm/Bot/Runners

## Overview

The VoBee AI Assistant now includes comprehensive deadline enforcement for all task execution in the Swarm/Bot/Runners system. This ensures that tasks complete within specified time limits and prevents resource waste from long-running or stuck tasks.

## Features

### 1. Orchestrator Workflow Deadlines

The orchestrator service supports workflow-level deadlines that apply to the entire task workflow:

- **Workflow Deadline**: Set a maximum execution time for all tasks in a workflow
- **Automatic Cancellation**: Tasks are cancelled if the workflow deadline is exceeded
- **Partial Completion**: Workflows can complete partially if deadline is reached
- **Status Tracking**: Clear indication of whether deadline was exceeded

### 2. Worker Task Deadlines

Individual worker tasks support task-level deadlines:

- **Task-Level Deadlines**: Each task can have its own deadline
- **Pre-execution Check**: Deadlines are validated before task execution starts
- **Post-execution Check**: Results are validated against deadline after completion
- **Timeout Status**: Tasks report timeout status with partial results when available

### 3. Supported Worker Types

Deadline enforcement is implemented for all worker types:

- **Crawler Workers**: Web scraping and data collection tasks
- **Analysis Workers**: Data processing and analysis tasks  
- **Benchmark Workers**: Performance testing tasks

## API Usage

### Orchestrator Workflow with Deadline

Execute a workflow with a deadline:

```bash
curl -X POST http://localhost:5003/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {
        "type": "crypto_prediction",
        "params": {
          "symbol": "BTC",
          "timeframe": "1h"
        }
      },
      {
        "type": "image_generation",
        "params": {
          "prompt": "AI landscape"
        }
      }
    ],
    "priority": "high",
    "deadline": 300
  }'
```

**Parameters:**
- `tasks`: Array of tasks to execute
- `priority`: Workflow priority (low, normal, high, critical)
- `deadline`: Maximum execution time in seconds (optional)

**Response:**
```json
{
  "workflow_id": "uuid",
  "status": "completed",
  "priority": "high",
  "deadline": 300,
  "duration": 45.2,
  "deadline_exceeded": false,
  "tasks_executed": 2,
  "tasks_total": 2,
  "results": [...],
  "started_at": "2025-12-16T20:00:00.000Z",
  "completed_at": "2025-12-16T20:00:45.200Z"
}
```

**Status Values:**
- `completed`: All tasks completed within deadline
- `partially_completed_deadline_exceeded`: Some tasks cancelled due to deadline

### Worker Pool Task with Deadline

Execute a worker task with a deadline:

```bash
curl -X POST http://localhost:5008/task/execute \
  -H "Content-Type: application/json" \
  -d '{
    "worker_type": "crawler",
    "task": {
      "url": "https://github.com",
      "depth": 1,
      "deadline": 30
    }
  }'
```

**Parameters:**
- `worker_type`: Type of worker (crawler, analysis, benchmark)
- `task`: Task parameters including optional `deadline` in seconds

**Response:**
```json
{
  "status": "success",
  "worker_id": "worker-uuid",
  "data": {
    "url": "https://github.com",
    "status_code": 200,
    "content_length": 12345,
    "crawled_at": "2025-12-16T20:00:00.000Z"
  }
}
```

**Status Values:**
- `success`: Task completed within deadline
- `timeout`: Task exceeded deadline during execution
- `failed`: Task failed before deadline (includes pre-deadline failures)

## Examples

### Example 1: Time-Sensitive Crypto Prediction

Execute a crypto prediction with a 60-second deadline:

```bash
curl -X POST http://localhost:5003/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {
        "type": "crypto_prediction",
        "params": {
          "symbol": "BTC",
          "timeframe": "1h",
          "prediction_horizon": 24
        }
      }
    ],
    "priority": "critical",
    "deadline": 60
  }'
```

### Example 2: Crawler Task with Short Deadline

Execute a quick web crawl with a 10-second deadline:

```bash
curl -X POST http://localhost:5008/task/execute \
  -H "Content-Type: application/json" \
  -d '{
    "worker_type": "crawler",
    "task": {
      "url": "https://api.github.com",
      "depth": 1,
      "deadline": 10
    }
  }'
```

### Example 3: Analysis Task with Deadline

Run data analysis with a 20-second deadline:

```bash
curl -X POST http://localhost:5008/task/execute \
  -H "Content-Type: application/json" \
  -d '{
    "worker_type": "analysis",
    "task": {
      "analysis_type": "sentiment",
      "data": {
        "text": "Sample text for sentiment analysis"
      },
      "deadline": 20
    }
  }'
```

## Best Practices

### 1. Setting Appropriate Deadlines

- **Crawler Tasks**: 10-60 seconds depending on target complexity
- **Analysis Tasks**: 5-30 seconds for most analyses
- **Benchmark Tasks**: 10-120 seconds depending on iterations
- **Image Generation**: 60-300 seconds depending on quality/resolution
- **Video Generation**: 300-600 seconds for complex videos
- **Crypto Prediction**: 10-60 seconds for real-time predictions

### 2. Workflow Deadlines

- Set workflow deadlines 20-30% longer than sum of individual task estimates
- Account for network latency and service communication overhead
- Use `critical` priority for strict deadline requirements

### 3. Handling Deadline Exceeded

When a deadline is exceeded:

```python
# Check the response
if result.get('deadline_exceeded'):
    # Get partial results if available
    partial_results = [r for r in result['results'] if r.get('result')]
    
    # Log for monitoring
    logger.warning(f"Workflow {result['workflow_id']} exceeded deadline")
    
    # Implement retry logic if needed
    if result['tasks_executed'] == 0:
        # No tasks completed, retry with longer deadline
        retry_deadline = deadline * 2
```

### 4. Monitoring Deadline Performance

Track deadline metrics:

```python
# Calculate deadline utilization
duration = result['duration']
deadline = result['deadline']
utilization = (duration / deadline) * 100

if utilization > 90:
    logger.warning(f"Workflow {workflow_id} used {utilization}% of deadline")
```

## Integration with Existing Systems

### Supreme General Intelligence (SGI)

SGI can now send commands with deadlines:

```bash
curl -X POST http://localhost:5010/chat \
  -H "Content-Type: application/json" \
  -H "X-Owner-Secret: your_secret" \
  -d '{
    "message": "predict bitcoin price within 30 seconds",
    "context": {
      "deadline": 30
    }
  }'
```

### Spy-Orchestration

Scanning tasks can have deadlines:

```bash
curl -X POST http://localhost:5006/scan \
  -H "Content-Type: application/json" \
  -d '{
    "scan_type": "github",
    "parameters": {
      "query": "AI machine learning",
      "max_results": 50,
      "deadline": 120
    }
  }'
```

## Testing

A comprehensive test suite is provided in `test_deadline_enforcement.py`:

```bash
# Make the test script executable
chmod +x test_deadline_enforcement.py

# Run tests (requires services to be running)
python3 test_deadline_enforcement.py
```

The test suite includes:

1. Workflow with sufficient deadline (should complete)
2. Workflow with short deadline (should timeout)
3. Crawler task with sufficient deadline
4. Crawler task with very short deadline
5. Analysis task with deadline

## Troubleshooting

### Issue: Tasks Always Timing Out

**Solution**: Increase deadline values or check service performance

```bash
# Check service health
curl http://localhost:5007/system/health

# Review service logs
docker compose logs -f orchestrator
docker compose logs -f worker-pool
```

### Issue: Deadlines Not Being Enforced

**Solution**: Verify services are updated

```bash
# Rebuild and restart services
docker compose down
docker compose build orchestrator worker-pool
docker compose up -d
```

### Issue: Inconsistent Deadline Behavior

**Solution**: Check system time synchronization

```bash
# Verify system time
date -u

# Sync if needed
sudo ntpdate -s time.nist.gov
```

## Technical Details

### Deadline Storage

- Orchestrator stores deadlines in Redis with task metadata
- Workers track deadlines in memory during execution
- Deadline timestamps are in UTC ISO 8601 format

### Deadline Checking

Deadlines are checked at multiple points:

1. **Before Task Execution**: Validates deadline hasn't already passed
2. **During Execution**: For workflow-level deadlines
3. **After Execution**: Confirms task completed within deadline

### Performance Impact

Deadline enforcement has minimal overhead:

- < 1ms per deadline check
- No impact on task execution performance
- Efficient datetime comparisons

## Future Enhancements

Planned improvements:

- [ ] Deadline prediction based on historical data
- [ ] Automatic deadline adjustment for retry attempts
- [ ] Deadline alerts and notifications
- [ ] Dashboard for deadline metrics
- [ ] Per-service deadline defaults
- [ ] Dynamic deadline adjustment based on load

## License

MIT License - See LICENSE file for details
