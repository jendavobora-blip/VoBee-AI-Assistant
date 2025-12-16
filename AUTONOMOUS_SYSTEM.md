# Autonomous System Architecture Guide

This document describes the new autonomous, owner-controlled AI orchestration system with self-healing capabilities.

## Overview

The VoBee AI Assistant has been enhanced with a complete autonomous architecture featuring:

1. **Supreme General Intelligence (SGI)** - Primary chat interface with intent understanding
2. **Spy-Orchestration Pipeline** - Automated scouting for AI models and research
3. **Enhanced Orchestration** - Cross-domain task decomposition and priority management
4. **Self-Healing Architecture** - Automated health monitoring and repair
5. **Owner-Only Access** - Encrypted secrets and audit logging

## Architecture Components

### 1. Supreme General Intelligence (SGI) Service

**Port:** 5010  
**Purpose:** Owner-only chat interface with confirmation-driven actions

#### Features:
- Natural language intent understanding
- Action summarization before execution
- Confirmation-based execution (user must approve)
- Permanent logging of all actions and results
- Voice capability support (future enhancement)

#### API Endpoints:

**Chat with SGI:**
```bash
curl -X POST http://localhost:5010/chat \
  -H 'Content-Type: application/json' \
  -H 'X-Owner-Secret: your_secure_owner_secret_key' \
  -d '{
    "message": "generate an image of a futuristic city",
    "context": {}
  }'
```

**Confirm and Execute Action:**
```bash
curl -X POST http://localhost:5010/confirm \
  -H 'Content-Type: application/json' \
  -H 'X-Owner-Secret: your_secure_owner_secret_key' \
  -d '{
    "action_id": "uuid-from-chat-response",
    "confirmed": true,
    "modifications": {}
  }'
```

**View Action Logs:**
```bash
curl http://localhost:5010/logs/{action_id} \
  -H 'X-Owner-Secret: your_secure_owner_secret_key'
```

**List All Actions:**
```bash
curl http://localhost:5010/actions?status=completed \
  -H 'X-Owner-Secret: your_secure_owner_secret_key'
```

#### Intent Understanding:

The SGI analyzes your messages to understand:
- **Actions:** generate, predict, analyze, scan, deploy, monitor, repair
- **Entities:** image, video, crypto, github, research, fraud
- **Confidence:** How certain the system is about the intent

Example intents:
- "scan github for AI repositories" → `scan_github`
- "generate an image of sunset" → `generate_image`
- "predict bitcoin price" → `predict_crypto`
- "analyze for fraud" → `analyze_fraud`

### 2. Spy-Orchestration Pipeline Service

**Port:** 5006  
**Purpose:** Automated discovery and intelligence gathering

#### Features:
- GitHub repository scanning
- Research paper discovery (arXiv)
- Technology blog monitoring
- Automatic deduplication
- Relevance scoring and filtering
- Summarization before decision-making

#### API Endpoints:

**Start GitHub Scan:**
```bash
curl -X POST http://localhost:5006/scan \
  -H 'Content-Type: application/json' \
  -d '{
    "scan_type": "github",
    "parameters": {
      "query": "AI machine learning stars:>100",
      "max_results": 50,
      "min_relevance": 0.5,
      "keywords": ["ai", "ml", "neural"]
    }
  }'
```

**Start Research Paper Scan:**
```bash
curl -X POST http://localhost:5006/scan \
  -H 'Content-Type: application/json' \
  -d '{
    "scan_type": "research",
    "parameters": {
      "query": "artificial intelligence",
      "category": "cs.AI",
      "max_results": 30
    }
  }'
```

**Check Scan Status:**
```bash
curl http://localhost:5006/scan/{scan_id}
```

**View Discoveries:**
```bash
curl http://localhost:5006/discoveries?scan_type=github&min_relevance=0.7
```

**Get Statistics:**
```bash
curl http://localhost:5006/stats
```

#### Scan Types:

1. **GitHub Scanning:**
   - Discovers relevant repositories
   - Scores based on stars, recency, topics
   - Extracts metadata (language, license, topics)
   - Filters by relevance threshold

2. **Research Scanning:**
   - Searches arXiv for papers
   - Filters by category and keywords
   - Extracts authors and publication dates
   - Scores based on keyword matching

3. **Blog Scanning:**
   - Monitors technology blogs
   - Can be extended with RSS feeds
   - Tracks AI/ML news and updates

### 3. Self-Healing Service

**Port:** 5007  
**Purpose:** Automated health monitoring and service repair

#### Features:
- Continuous health monitoring (30s intervals)
- Automatic failure detection
- Auto-repair with container restart
- Rollback support
- Proposed fix recommendations
- Repair history tracking

#### API Endpoints:

**Get System Health:**
```bash
curl http://localhost:5007/system/health
```

**Check Specific Service:**
```bash
curl http://localhost:5007/service/api-gateway/health
```

**Manually Trigger Repair:**
```bash
curl -X POST http://localhost:5007/service/orchestrator/repair
```

**Get Proposed Fixes:**
```bash
curl http://localhost:5007/service/api-gateway/fixes
```

**View Repair History:**
```bash
curl http://localhost:5007/repairs/history?limit=20
```

**Toggle Monitoring:**
```bash
curl -X POST http://localhost:5007/monitoring/toggle \
  -H 'Content-Type: application/json' \
  -d '{"enabled": true}'
```

#### Auto-Healing Process:

1. **Detection:** Service fails health check 3 times
2. **Analysis:** System analyzes failure type
3. **Repair:** Attempts to restart container
4. **Verification:** Confirms service is healthy
5. **Logging:** Records repair attempt and result

### 4. Enhanced Orchestration

The existing orchestrator has been enhanced to work with SGI and spy-orchestration:

- Receives tasks from SGI after confirmation
- Routes to appropriate services
- Manages priorities
- Handles cross-domain workflows
- Returns results to SGI for logging

## Deployment

### Quick Start (One Command)

```bash
./deploy.sh
```

This script will:
1. Check prerequisites (Docker, Docker Compose)
2. Set up environment configuration
3. Create necessary directories
4. Build all service containers
5. Start infrastructure (PostgreSQL, Redis)
6. Start all services
7. Verify health of services
8. Display access information

### Manual Deployment

1. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and secrets
   nano .env
   ```

2. **Build Services:**
   ```bash
   docker-compose build
   ```

3. **Start Services:**
   ```bash
   docker-compose up -d
   ```

4. **Verify Health:**
   ```bash
   curl http://localhost:5007/system/health
   ```

### Environment Variables

Required in `.env` file:

```bash
# Database
POSTGRES_PASSWORD=your_secure_password

# Owner Authentication (IMPORTANT!)
OWNER_SECRET=your_secure_owner_secret_key

# GitHub Integration
GITHUB_TOKEN=your_github_personal_access_token

# External APIs (optional)
COINGECKO_API_KEY=your_key
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
OPENAI_API_KEY=your_key
```

## Security

### Owner-Only Access

The SGI service requires owner authentication via the `X-Owner-Secret` header:

```bash
curl http://localhost:5010/chat \
  -H 'X-Owner-Secret: your_secure_owner_secret_key' \
  -H 'Content-Type: application/json' \
  -d '{"message": "your command"}'
```

**Important:** Change the default `OWNER_SECRET` in your `.env` file immediately!

### Audit Logging

All actions processed through SGI are permanently logged:
- Action ID
- Intent and parameters
- Confirmation status
- Execution results
- Timestamps
- Complete audit trail

Access logs:
```bash
curl http://localhost:5010/logs/{action_id} \
  -H 'X-Owner-Secret: your_secret'
```

### Encrypted Secrets

- Store all API keys in `.env` file
- Never commit `.env` to version control
- Use strong passwords for POSTGRES_PASSWORD
- Use a unique, strong OWNER_SECRET

## Usage Examples

### Example 1: Autonomous GitHub Scanning

```bash
# 1. Request GitHub scan via SGI
curl -X POST http://localhost:5010/chat \
  -H 'Content-Type: application/json' \
  -H 'X-Owner-Secret: your_secret' \
  -d '{
    "message": "scan github for neural network repositories"
  }'

# Response includes action_id and summary

# 2. Confirm the action
curl -X POST http://localhost:5010/confirm \
  -H 'Content-Type: application/json' \
  -H 'X-Owner-Secret: your_secret' \
  -d '{
    "action_id": "received-action-id",
    "confirmed": true
  }'

# 3. Check results
curl http://localhost:5006/discoveries?scan_type=github&min_relevance=0.7
```

### Example 2: System Health Monitoring

```bash
# Check overall system health
curl http://localhost:5007/system/health

# If a service is unhealthy, get proposed fixes
curl http://localhost:5007/service/api-gateway/fixes

# Manually trigger repair if needed
curl -X POST http://localhost:5007/service/api-gateway/repair
```

### Example 3: Research Paper Discovery

```bash
# Start research scan
curl -X POST http://localhost:5006/scan \
  -H 'Content-Type: application/json' \
  -d '{
    "scan_type": "research",
    "parameters": {
      "query": "transformer neural networks",
      "category": "cs.AI",
      "max_results": 20,
      "keywords": ["transformer", "attention", "bert"]
    }
  }'

# Check scan status
curl http://localhost:5006/scan/{scan_id}

# View discovered papers
curl http://localhost:5006/discoveries?scan_type=research
```

## Monitoring

### Service Health

Access Kibana dashboard:
```
http://localhost:5601
```

### System Metrics

Get overall health:
```bash
curl http://localhost:5007/system/health
```

### Logs

View service logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f supreme-general-intelligence
docker-compose logs -f spy-orchestration
docker-compose logs -f self-healing
```

## Maintenance

### Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart supreme-general-intelligence

# Scale a service
docker-compose up -d --scale orchestrator=2
```

### Database Maintenance

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U orchestrator -d orchestrator_db

# View SGI actions
SELECT action_id, summary, status, created_at FROM sgi_actions ORDER BY created_at DESC LIMIT 10;

# View spy discoveries
SELECT title, scan_type, relevance_score FROM spy_discoveries ORDER BY relevance_score DESC LIMIT 10;
```

### Cleanup

```bash
# Remove old containers and volumes
docker-compose down -v

# Prune unused Docker resources
docker system prune -a
```

## Troubleshooting

### Service Won't Start

1. Check logs:
   ```bash
   docker-compose logs service-name
   ```

2. Verify environment variables:
   ```bash
   docker-compose config
   ```

3. Check port conflicts:
   ```bash
   netstat -tulpn | grep LISTEN
   ```

### Database Connection Issues

1. Verify PostgreSQL is running:
   ```bash
   docker-compose ps postgres
   ```

2. Test connection:
   ```bash
   docker-compose exec postgres pg_isready -U orchestrator
   ```

### Self-Healing Not Working

1. Verify Docker socket is mounted:
   ```bash
   docker-compose exec self-healing ls -la /var/run/docker.sock
   ```

2. Check monitoring status:
   ```bash
   curl http://localhost:5007/health
   ```

## Future Enhancements

- [ ] Voice interface integration
- [ ] Advanced NLP for intent understanding
- [ ] Multi-language support
- [ ] Advanced rollback mechanisms
- [ ] Distributed worker pools
- [ ] GPU optimization for workers
- [ ] Advanced security with OAuth2
- [ ] Kubernetes deployment templates
- [ ] Real-time websocket notifications
- [ ] Advanced analytics dashboard

## Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- System health: `curl http://localhost:5007/system/health`
- Review documentation: `ARCHITECTURE.md`, `DEPLOYMENT.md`

## License

MIT License - See LICENSE file for details
