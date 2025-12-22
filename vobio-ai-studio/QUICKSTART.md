# Vobio AI Studio - Quick Start Guide

## Prerequisites

Before starting, ensure you have:

- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher  
- **4GB RAM**: Minimum free memory
- **10GB Disk**: For Docker images and volumes

Check your installations:

```bash
docker --version
docker-compose --version
```

## 🚀 One-Command Installation

```bash
# 1. Clone the repository
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant

# 2. Run setup (pulls images, builds API)
./setup.sh

# 3. Start all services
./start.sh
```

That's it! All services will start automatically.

## ✅ Verify Installation

Check service health:

```bash
# API Health
curl http://localhost:8000/health

# Qdrant Health  
curl http://localhost:6333/health

# Langfuse Health
curl http://localhost:3000/api/health
```

All should return healthy status.

## 🎯 Your First API Call

### 1. Login (Mock Mode)

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "your_name"}'
```

Response includes your `user_id` - save it!

### 2. Chat with AI

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "X-User-ID: user-abc123" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'
```

### 3. Generate Image

```bash
curl -X POST http://localhost:8000/api/generate/image \
  -H "X-User-ID: user-abc123" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A beautiful sunset", "style": "realistic"}'
```

### 4. LifeSync Decision

```bash
curl -X POST http://localhost:8000/api/lifesync/decision \
  -H "X-User-ID: user-abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "Should I buy or rent?",
    "options": ["Buy house", "Rent apartment", "Buy condo"]
  }'
```

## 📊 Access Dashboards

### Langfuse (Observability)

Open browser: **http://localhost:3000**

- View API traces
- Monitor costs
- Analyze usage patterns

### Qdrant (Vector DB)

Open browser: **http://localhost:6333/dashboard**

- Browse collections
- View stored memories

## 🧪 Run Tests

```bash
./test.sh
```

This runs 13 end-to-end tests covering:
- Health checks
- Authentication
- All AI operations
- Safety system
- Cost tracking
- Memory service

## 🛑 Stop Services

```bash
./stop.sh
```

## 🔧 Configuration

### Change Cost Limits

Edit `vobio-ai-studio/.env`:

```bash
DAILY_COST_LIMIT=20.0    # Increase to $20/day
HOURLY_COST_LIMIT=5.0    # Increase to $5/hour
```

Restart services:

```bash
./stop.sh && ./start.sh
```

### Enable Code Execution

⚠️ **Warning**: Only enable if you trust the code!

Edit `vobio-ai-studio/.env`:

```bash
ENABLE_CODE_EXECUTION=true
```

Restart services.

### Change Ports

Edit `vobio-ai-studio/docker-compose.yml`:

```yaml
vobio-api:
  ports:
    - "8080:8000"  # Change host port
```

## 📖 Next Steps

### Learn the System

1. **Architecture**: Read [ARCHITECTURE.md](vobio-ai-studio/ARCHITECTURE.md)
2. **Safety**: Read [SAFETY.md](vobio-ai-studio/SAFETY.md)
3. **API**: Read [API.md](vobio-ai-studio/API.md)

### Explore Features

```bash
# Check feature flags
curl http://localhost:8000/api/features

# View cost usage
curl http://localhost:8000/api/costs/usage \
  -H "X-User-ID: user-abc123"

# Get user context
curl http://localhost:8000/api/memory/context \
  -H "X-User-ID: user-abc123"

# Check pending approvals
curl http://localhost:8000/api/approvals/pending \
  -H "X-User-ID: user-abc123"
```

### Develop Custom Skills

Create files in `vobio-ai-studio/backend/skills/`:

```python
# my_skill.py
def process(input_data):
    """Your custom logic"""
    return {"result": "processed"}
```

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose -f vobio-ai-studio/docker-compose.yml logs

# Check specific service
docker-compose -f vobio-ai-studio/docker-compose.yml logs vobio-api

# Restart service
docker-compose -f vobio-ai-studio/docker-compose.yml restart vobio-api
```

### Port Already in Use

```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process or change port in docker-compose.yml
```

### Docker Image Build Fails

```bash
# Rebuild without cache
cd vobio-ai-studio
docker-compose build --no-cache vobio-api
```

### Tests Fail

```bash
# Wait longer for services
sleep 60

# Run tests again
./test.sh

# Check individual service health
curl http://localhost:8000/health
curl http://localhost:6333/health
curl http://localhost:3000/api/health
```

### Out of Memory

```bash
# Check Docker memory
docker stats

# Increase Docker memory in Docker Desktop settings
# Recommended: 4GB minimum, 8GB optimal
```

### Reset Everything

```bash
# Stop and remove all data
./stop.sh
docker-compose -f vobio-ai-studio/docker-compose.yml down -v

# Start fresh
./setup.sh
./start.sh
```

## 💡 Tips

### Development Mode

```bash
# Follow logs in real-time
docker-compose -f vobio-ai-studio/docker-compose.yml logs -f

# Restart API without rebuilding
docker-compose -f vobio-ai-studio/docker-compose.yml restart vobio-api

# Enter API container
docker exec -it vobio-api bash
```

### Production Checklist

Before deploying to production:

1. ✅ Change `.env` secrets
2. ✅ Set `MOCK_MODE=false` (requires real AI providers)
3. ✅ Configure proper authentication
4. ✅ Setup SSL/TLS certificates
5. ✅ Enable firewall rules
6. ✅ Configure log aggregation
7. ✅ Setup monitoring alerts
8. ✅ Regular backups of volumes

### Performance Tuning

```yaml
# docker-compose.yml
vobio-api:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G
```

## 📞 Support

### Check Status

```bash
# View all services
docker-compose -f vobio-ai-studio/docker-compose.yml ps

# Check health
curl http://localhost:8000/health
```

### View Logs

```bash
# All services
docker-compose -f vobio-ai-studio/docker-compose.yml logs

# Specific service
docker-compose -f vobio-ai-studio/docker-compose.yml logs vobio-api

# Last 100 lines
docker-compose -f vobio-ai-studio/docker-compose.yml logs --tail=100 vobio-api

# Follow live
docker-compose -f vobio-ai-studio/docker-compose.yml logs -f vobio-api
```

### Debug Mode

Edit `vobio-ai-studio/.env`:

```bash
LOG_LEVEL=DEBUG
```

Restart services to see detailed logs.

## 🎓 Learning Path

1. **Day 1**: Setup, run tests, explore API
2. **Day 2**: Read architecture, understand components
3. **Day 3**: Experiment with LifeSync, try custom scenarios
4. **Day 4**: Review safety system, test code validation
5. **Day 5**: Monitor costs in Langfuse, optimize usage

## 🚀 Ready to Go!

You now have a fully functional AI orchestration platform!

### Quick Commands Reference

```bash
./setup.sh   # First time setup
./start.sh   # Start services
./stop.sh    # Stop services
./test.sh    # Run tests
```

### Service URLs

- API: http://localhost:8000
- Langfuse: http://localhost:3000
- Qdrant: http://localhost:6333

### Example Workflow

```bash
# 1. Start
./start.sh

# 2. Login & get user_id
USER_ID=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice"}' | jq -r '.user.user_id')

# 3. Use AI
curl -X POST http://localhost:8000/api/chat \
  -H "X-User-ID: $USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# 4. Check costs
curl http://localhost:8000/api/costs/usage -H "X-User-ID: $USER_ID"

# 5. Stop when done
./stop.sh
```

Happy building! 🐝
