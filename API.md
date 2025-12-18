# Self-Evolving AI Organism - API Reference

Complete API documentation for all 8 core services.

---

## 1. Supreme Brain (Port 5010)

Core consciousness service that maintains VOBee's personality and orchestrates all decisions.

### Endpoints

#### `POST /chat`
Chat with VOBee and get intelligent responses with optional action proposals.

**Request:**
```json
{
  "message": "Generate a marketing campaign for my AI product",
  "context": {
    "budget": 5000,
    "timeline": "30 days"
  }
}
```

**Response:**
```json
{
  "response": "I've analyzed your request...",
  "action_id": "a1b2c3d4",
  "requires_approval": true,
  "estimated_cost": 0.15,
  "estimated_duration": 120
}
```

#### `POST /approve`
Approve or reject a pending action.

**Request:**
```json
{
  "action_id": "a1b2c3d4",
  "approved": true
}
```

#### `POST /decompose`
Decompose a complex goal into 2000+ micro-tasks.

**Request:**
```json
{
  "goal": "Launch a new AI product",
  "context": {},
  "max_tasks": 2000
}
```

**Response:**
```json
{
  "total_tasks": 1847,
  "parallelizable_tasks": 1203,
  "task_preview": [...]
}
```

#### `POST /compose`
Compose unified output from multiple agent responses.

**Request:**
```json
{
  "outputs": [
    {
      "agent_id": "agent-123",
      "agent_type": "learning",
      "output": "Result data",
      "confidence": 0.92,
      "processing_time": 1.5
    }
  ],
  "strategy": "comprehensive"
}
```

---

## 2. Agent Ecosystem (Port 5011)

Manages 2000+ AI agents with dynamic scaling and capability-based task matching.

### Endpoints

#### `POST /task/assign`
Assign a task to an available agent.

**Request:**
```json
{
  "task_type": "data_analysis",
  "capability": "data_ingestion",
  "parameters": {
    "source": "database",
    "filters": {}
  },
  "priority": 3
}
```

**Response:**
```json
{
  "task_id": "task-xyz",
  "agent_id": "agent-456",
  "status": "assigned"
}
```

#### `POST /task/complete`
Mark a task as completed.

**Request:**
```json
{
  "task_id": "task-xyz",
  "agent_id": "agent-456",
  "success": true,
  "processing_time": 2.3,
  "result": {}
}
```

#### `POST /agent/spawn`
Manually spawn a new agent.

**Request:**
```json
{
  "agent_type": "tech_scout",
  "capabilities": ["tech_scouting", "code_analysis"],
  "max_concurrent_tasks": 3
}
```

#### `GET /stats`
Get detailed agent ecosystem statistics.

**Response:**
```json
{
  "total_agents": 1247,
  "idle_agents": 823,
  "busy_agents": 424,
  "total_tasks_processed": 45892,
  "success_rate": 0.986
}
```

---

## 3. Tech Scouting Engine (Port 5020)

Autonomously discovers and evaluates emerging technologies.

### Endpoints

#### `POST /scan`
Trigger technology scouting scan.

**Request:**
```json
{
  "sources": ["github", "arxiv", "hackernews", "producthunt"],
  "query": "AI agents",
  "max_results": 100
}
```

**Response:**
```json
{
  "scan_id": "scan-abc",
  "discoveries_found": 87,
  "message": "Scan completed across 4 sources"
}
```

#### `GET /discoveries`
Get discovered technologies with filtering.

**Query Parameters:**
- `source` - Filter by source (github, arxiv, etc.)
- `min_relevance` - Minimum relevance score (0.0-1.0)
- `limit` - Max results to return

**Response:**
```json
{
  "total_discoveries": 345,
  "filtered_count": 87,
  "discoveries": [
    {
      "source": "github",
      "name": "ai-agent-framework",
      "url": "https://github.com/...",
      "relevance_score": 0.92,
      "discovered_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### `POST /benchmark`
Benchmark a discovered technology.

**Request:**
```json
{
  "tech_name": "new-ai-model",
  "tech_url": "https://github.com/...",
  "benchmark_type": "performance"
}
```

**Response:**
```json
{
  "results": {
    "metrics": {
      "latency_ms": 145,
      "throughput_qps": 1200,
      "quality_score": 0.87
    },
    "recommendation": "integrate"
  }
}
```

---

## 4. Hyper-Learning System (Port 5030)

Ultra-fast parallel data ingestion with 10:1 compression ratio.

### Endpoints

#### `POST /ingest`
Ingest and process data from various sources.

**Request:**
```json
{
  "source_type": "text",
  "source_url": "https://example.com/article",
  "source_content": "Long article content...",
  "compression_ratio": 10.0,
  "validate": true
}
```

**Response:**
```json
{
  "job_id": "job-123",
  "processed": true,
  "compression_achieved": "10:1",
  "knowledge_id": "know-456",
  "validation": {
    "accuracy": 0.96,
    "passed": true
  }
}
```

#### `POST /query`
Query the knowledge base using RAG.

**Request:**
```json
{
  "query": "What are the best practices for AI agents?",
  "top_k": 5,
  "min_confidence": 0.7
}
```

**Response:**
```json
{
  "results_found": 12,
  "results": [
    {
      "knowledge_id": "know-789",
      "summary": "Best practices include...",
      "confidence": 0.89,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "avg_confidence": 0.85
}
```

#### `GET /stats`
Get learning system statistics.

**Response:**
```json
{
  "stats": {
    "total_jobs": 1247,
    "knowledge_items": 8934,
    "total_data_ingested_mb": 125000,
    "compressed_data_mb": 12500,
    "avg_compression_ratio": 10.0
  }
}
```

---

## 5. Media Factory Intelligence (Port 5012)

Real-time AI-powered media generation.

### Endpoints

#### `POST /media/image/generate`
Generate images using SDXL Turbo.

**Request:**
```json
{
  "prompt": "A futuristic city at sunset",
  "style": "realistic",
  "resolution": "1024x1024",
  "num_images": 2
}
```

**Response:**
```json
{
  "media_id": "img-abc",
  "images": [
    "https://storage.vobee.ai/images/img-abc_0.png",
    "https://storage.vobee.ai/images/img-abc_1.png"
  ],
  "generation_time_ms": 850
}
```

#### `POST /media/video/generate`
Generate videos using Runway Gen-3.

**Request:**
```json
{
  "prompt": "Flying through clouds",
  "duration": 5,
  "resolution": "1080p",
  "fps": 30
}
```

**Response:**
```json
{
  "media_id": "vid-xyz",
  "video_url": "https://storage.vobee.ai/videos/vid-xyz.mp4",
  "duration": 5,
  "generation_time_ms": 30000
}
```

#### `POST /media/voice/generate`
Generate speech using ElevenLabs.

**Request:**
```json
{
  "text": "Hello, I am VOBee, your AI assistant.",
  "voice_id": "default",
  "language": "en",
  "speed": 1.0
}
```

**Response:**
```json
{
  "media_id": "voice-123",
  "audio_url": "https://storage.vobee.ai/voice/voice-123.mp3",
  "duration": 3.2,
  "generation_time_ms": 1200
}
```

---

## 6. Marketing Brain Intelligence (Port 5013)

Automated marketing campaign generation and optimization.

### Endpoints

#### `POST /campaign/create`
Create a complete marketing campaign.

**Request:**
```json
{
  "product_name": "AI Assistant Pro",
  "target_audience": "Tech-savvy professionals",
  "budget": 5000,
  "duration_days": 30,
  "channels": ["email", "social", "ads"]
}
```

**Response:**
```json
{
  "campaign_id": "camp-abc",
  "strategy": {
    "objective": "Launch and promote AI Assistant Pro",
    "key_messages": [...]
  },
  "budget_allocation": {
    "email": 1500,
    "social": 2000,
    "ads": 1500
  },
  "content_pieces_planned": 45,
  "estimated_reach": 750000
}
```

#### `POST /content/generate`
Generate SEO-optimized content.

**Request:**
```json
{
  "content_type": "blog",
  "topic": "AI-powered productivity tools",
  "target_keywords": ["AI", "productivity", "automation"],
  "tone": "professional"
}
```

**Response:**
```json
{
  "content_id": "cont-xyz",
  "content": "# AI-powered productivity tools\n\n...",
  "seo_score": 0.87,
  "readability_score": 0.92,
  "word_count": 1247
}
```

#### `GET /campaign/{campaign_id}/analytics`
Get campaign performance analytics.

**Response:**
```json
{
  "analytics": {
    "performance": {
      "impressions": 125000,
      "clicks": 3500,
      "conversions": 245,
      "ctr": 0.028,
      "roi": 2.4
    },
    "recommendations": [
      "Increase budget on email channel",
      "Optimize social media ad creative"
    ]
  }
}
```

---

## 7. Simulation Universe (Port 5040)

Massive parallel testing with 1000+ scenarios.

### Endpoints

#### `POST /simulate`
Run parallel simulations.

**Request:**
```json
{
  "simulation_type": "load_test",
  "num_scenarios": 1000,
  "parameters": {
    "virtual_users": 10000,
    "duration": 300
  },
  "duration_seconds": 60
}
```

**Response:**
```json
{
  "sim_id": "sim-abc",
  "scenarios_executed": 1000,
  "analysis": {
    "success_rate": 0.987,
    "avg_performance": 0.92,
    "recommendation": "deploy"
  },
  "recommended_strategy": {
    "scenario_id": 487,
    "score": 0.96,
    "confidence": 0.95
  }
}
```

#### `POST /chaos/inject`
Inject failures for chaos testing.

**Request:**
```json
{
  "target_service": "api-gateway",
  "failure_type": "network_latency",
  "intensity": 0.5,
  "duration_seconds": 60
}
```

**Response:**
```json
{
  "chaos_id": "chaos-xyz",
  "results": {
    "impacts": {
      "latency_increase_ms": 250,
      "error_rate_increase": 0.075
    },
    "system_resilience_score": 0.85
  }
}
```

#### `POST /deploy/safe`
Execute safe deployment with testing.

**Request:**
```json
{
  "strategy": "canary",
  "service_name": "api-gateway",
  "new_version": "v2.0.0",
  "rollout_percentage": 10
}
```

**Response:**
```json
{
  "deployment_id": "deploy-abc",
  "deployment": {
    "phases": [
      {"phase": 1, "percentage": 10, "health": "healthy"},
      {"phase": 2, "percentage": 25, "health": "healthy"},
      {"phase": 3, "percentage": 50, "health": "healthy"},
      {"phase": 4, "percentage": 100, "health": "healthy"}
    ],
    "success_rate": 0.99
  }
}
```

---

## 8. Cost Guard (Port 5050)

Intelligent cost optimization achieving 50%+ reduction.

### Endpoints

#### `POST /inference`
Execute optimized inference with cost control.

**Request:**
```json
{
  "prompt": "Analyze this data...",
  "model": "auto",
  "max_cost": 0.10,
  "priority": 2
}
```

**Response:**
```json
{
  "result": "Analysis complete...",
  "source": "local_vllm",
  "cost": 0.0001,
  "savings": 0.0019,
  "cached": true
}
```

#### `POST /batch`
Process multiple requests in a batch.

**Request:**
```json
{
  "requests": [
    {"prompt": "Query 1", "model": "auto"},
    {"prompt": "Query 2", "model": "auto"}
  ],
  "max_wait_seconds": 10
}
```

**Response:**
```json
{
  "batch_id": "batch-xyz",
  "requests_processed": 2,
  "total_cost": 0.0026,
  "savings": 0.0014,
  "savings_percentage": 35.0
}
```

#### `POST /roi/evaluate`
Evaluate if operation should proceed based on ROI.

**Request:**
```json
{
  "operation": "complex_analysis",
  "estimated_cost": 0.05,
  "expected_value": 0.20
}
```

**Response:**
```json
{
  "decision": {
    "roi": 3.0,
    "roi_percentage": 300,
    "should_proceed": true,
    "recommendation": "approve"
  }
}
```

#### `GET /cache/stats`
Get cache performance statistics.

**Response:**
```json
{
  "cache_stats": {
    "total_entries": 8934,
    "hit_rate": 0.91,
    "target_hit_rate": 0.90,
    "estimated_savings": 17.87
  }
}
```

#### `GET /cost/summary`
Get cost summary for specified period.

**Query Parameters:**
- `period_hours` - Time period (default: 24)

**Response:**
```json
{
  "cost_summary": {
    "total_operations": 12847,
    "total_cost": 12.34,
    "baseline_cost": 25.69,
    "savings": 13.35,
    "savings_percentage": 52.0,
    "target_achieved": true
  }
}
```

---

## Common Response Patterns

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information"
}
```

### Pagination
Many endpoints support pagination:
- `page` - Page number (default: 1)
- `limit` or `per_page` - Results per page (default: 50, max: 100)

---

## Authentication

Future versions will support:
- JWT tokens (RS256)
- API keys with rotation
- OAuth 2.0 for third-party integrations

Current version: No authentication required for local development.

---

## Rate Limiting

Recommended rate limits for production:
- Standard endpoints: 100 requests/minute
- Media generation: 10 requests/minute
- Batch operations: 5 requests/minute
- Heavy operations (simulations): 2 requests/minute

---

## Best Practices

1. **Cost Optimization**: Always route requests through Cost Guard (5050) first
2. **Task Decomposition**: Use Supreme Brain (5010) for complex multi-step operations
3. **Parallel Execution**: Leverage Agent Ecosystem (5011) for concurrent tasks
4. **Testing**: Use Simulation Universe (5040) before production deployment
5. **Monitoring**: Check `/stats` and `/health` endpoints regularly

---

## Error Codes

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized (future)
- `403` - Forbidden (future)
- `404` - Not Found
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error
- `503` - Service Unavailable

---

For more examples and integration guides, see the [DEVELOPMENT.md](DEVELOPMENT.md) documentation.
