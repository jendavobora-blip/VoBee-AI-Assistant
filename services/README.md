# AI Services

This directory contains all microservices that compose the AI Orchestration System.

## Services Overview

### 1. API Gateway (Port 8000)
**Technology**: FastAPI  
**Purpose**: Unified entry point for all AI services  

**Endpoints**:
- `GET /health` - Health check
- `GET /status` - Status of all services
- `POST /api/v1/generate/image` - Image generation
- `POST /api/v1/generate/video` - Video generation
- `POST /api/v1/crypto/predict` - Crypto price prediction
- `POST /api/v1/orchestrate` - Multi-task orchestration

**Resources**: 512Mi-1Gi RAM, 0.5-1 CPU

---

### 2. Image Generation (Port 5000)
**Technology**: PyTorch, Diffusers  
**Purpose**: Generate 3D/4D images with HDR and PBR rendering  

**Models Supported**:
- Stable Diffusion XL
- DALL-E 3 (via API)
- NVIDIA StyleGAN3
- DreamBooth fine-tuned models

**Endpoints**:
- `GET /health` - Health check
- `POST /generate` - Generate image from prompt
- `GET /models` - List available models
- `GET /styles` - List available styles

**Resources**: 4-8Gi RAM, 2-4 CPU, 1 GPU (A100 recommended)

---

### 3. Video Generation (Port 5001)
**Technology**: PyTorch, NeRF, Runway ML  
**Purpose**: Generate 8K videos with dynamic camera rendering  

**Models Supported**:
- Runway ML Gen-2 (via API)
- NeRF (Neural Radiance Fields)
- Video diffusion models

**Endpoints**:
- `GET /health` - Health check
- `POST /generate` - Generate video from prompt
- `GET /models` - List available models
- `GET /resolutions` - List supported resolutions

**Resources**: 8-16Gi RAM, 4-8 CPU, 1 GPU (A100 recommended)

---

### 4. Crypto Prediction (Port 5002)
**Technology**: PyTorch, LSTM, Transformers  
**Purpose**: Predict cryptocurrency prices using time-series models  

**Data Sources**:
- CoinGecko API
- Binance API
- Social media sentiment

**Endpoints**:
- `GET /health` - Health check
- `POST /predict` - Predict price
- `GET /sentiment/{symbol}` - Sentiment analysis
- `GET /risk/{symbol}` - Risk assessment
- `GET /supported-coins` - List supported coins

**Resources**: 2-4Gi RAM, 1-2 CPU

---

### 5. Orchestrator (Port 5003)
**Technology**: Flask, Redis, PostgreSQL  
**Purpose**: Coordinate tasks, manage queues, and handle workflows  

**Dependencies**:
- Redis for task queue
- PostgreSQL for persistent storage

**Endpoints**:
- `GET /health` - Health check
- `POST /orchestrate` - Execute workflow
- `GET /task/{task_id}` - Get task status
- `GET /services` - List available services

**Resources**: 1-2Gi RAM, 0.5-1 CPU

---

### 6. Auto-Scaler (Port 5005)
**Technology**: Flask, psutil  
**Purpose**: Monitor resources and provide scaling recommendations  

**Metrics Monitored**:
- CPU utilization
- Memory usage
- Disk usage

**Endpoints**:
- `GET /health` - Health check
- `GET /metrics` - Current system metrics
- `GET /scaling-decision` - Scaling recommendation

**Resources**: 256-512Mi RAM, 0.25-0.5 CPU

---

### 7. Fraud Detection (Port 5004)
**Technology**: Scikit-learn, XGBoost  
**Purpose**: Detect fraudulent transactions and network anomalies  

**Features**:
- Transaction analysis
- Network security monitoring
- Crypto trading fraud detection

**Endpoints**:
- `GET /health` - Health check
- `POST /analyze` - Analyze transaction for fraud

**Resources**: 1-2Gi RAM, 0.5-1 CPU

---

### 8. CDN (Port 8080)
**Technology**: Nginx  
**Purpose**: Fast content delivery with caching  

**Features**:
- Gzip compression
- 30-day caching for static content
- Range requests for video streaming
- Serve generated images and videos

**Resources**: 256-512Mi RAM, 0.25-0.5 CPU

---

## Development

### Building Individual Services

```bash
# Build specific service
docker build -t ai-orchestration/api-gateway services/api-gateway/

# Run service locally
docker run -p 8000:8000 ai-orchestration/api-gateway
```

### Testing Services

```bash
# Health check
curl http://localhost:8000/health

# Test image generation
curl -X POST http://localhost:8000/api/v1/generate/image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test image", "style": "realistic"}'
```

### Adding New Services

1. Create directory: `services/new-service/`
2. Add Dockerfile
3. Add requirements.txt (Python) or package.json (Node.js)
4. Add main.py or main.js
5. Update docker-compose.yml
6. Update kubernetes/01-deployments.yaml
7. Update API Gateway to route to new service

## Dependencies Between Services

```
API Gateway
    ├── depends on → Image Generation
    ├── depends on → Video Generation
    ├── depends on → Crypto Prediction
    ├── depends on → Fraud Detection
    └── depends on → Orchestrator
            ├── depends on → Redis
            ├── depends on → PostgreSQL
            └── depends on → All AI Services
```

## Environment Variables

Each service uses environment variables for configuration:

```bash
# Common
LOG_LEVEL=info
ENVIRONMENT=production

# Service URLs (for internal communication)
IMAGE_SERVICE_URL=http://image-generation:5000
VIDEO_SERVICE_URL=http://video-generation:5001
CRYPTO_SERVICE_URL=http://crypto-prediction:5002

# Database
REDIS_HOST=redis
REDIS_PORT=6379
POSTGRES_HOST=postgres
POSTGRES_DB=orchestrator_db

# API Keys (stored in secrets)
COINGECKO_API_KEY=your_key
BINANCE_API_KEY=your_key
OPENAI_API_KEY=your_key
```

## Monitoring

All services expose:
- `/health` endpoint for health checks
- Prometheus-compatible metrics (some services)
- Structured logging to stdout

Use ElasticSearch + Kibana stack for centralized logging and monitoring.

## Security

- All secrets should be stored in Kubernetes Secrets or .env files (not committed)
- Services communicate over internal network only
- API Gateway is the only public-facing service
- Use TLS/SSL for production deployments
- Regular security scanning with Trivy

## Performance Tuning

### Image Generation
- Adjust batch size based on GPU memory
- Use model quantization for faster inference
- Enable xFormers for memory-efficient attention

### Video Generation
- Reduce resolution/fps for faster generation
- Use lower precision (fp16) on GPUs
- Implement frame interpolation for smoother output

### Crypto Prediction
- Batch multiple predictions together
- Cache recent predictions
- Use smaller models for faster inference

## Troubleshooting

**Service won't start**:
- Check logs: `docker-compose logs <service-name>`
- Verify environment variables
- Check port conflicts

**GPU not detected**:
- Verify NVIDIA drivers: `nvidia-smi`
- Check Docker GPU support: `docker run --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`

**Out of memory**:
- Reduce batch size
- Lower model precision
- Increase container memory limits

**Slow inference**:
- Check GPU utilization
- Verify CUDA version compatibility
- Enable GPU acceleration in code
