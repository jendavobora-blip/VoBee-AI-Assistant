# VoBee AI Assistant <img width="480" height="480" alt="image" src="https://github.com/user-attachments/assets/feb0de59-8c3c-4796-8b99-554155982991" />
Clarify VoBee MVP scope
A complete, autonomous AI orchestration system featuring:
- **Supreme General Intelligence (SGI)** - Owner-only chat interface with intent understanding and confirmation-driven actions
- **Spy-Orchestration Pipeline** - Automated discovery of AI models, research papers, and technologies
- **Self-Healing Architecture** - Automated health monitoring and service repair
- **Stateless Worker Pool** - Disposable workers for crawling, analysis, and benchmarking
- **Creative AI chatbot** PWA with pseudo-learning capabilities
- **3D/4D image and video generation** (Stable Diffusion, DALL-E, NeRF, Runway ML Gen-2)
- **Cryptocurrency prediction** with LSTM/Transformer models
- **Kubernetes-based** distributed infrastructure with GPU acceleration
- **Auto-scaling** and fraud detection capabilities
- **CDN pipeline** for fast content delivery

## 🚀 New: Autonomous System Features

### 🧠 Supreme General Intelligence (SGI)
- **Owner-only access** with encrypted secret authentication
- **Intent understanding** from natural language commands
- **Confirmation-driven execution** - all actions require approval
- **Permanent audit logging** of all actions and results
- **Voice capability support** (framework ready)

### 🔍 Spy-Orchestration Pipeline
- **Automated GitHub scanning** for AI repositories and projects
- **Research paper discovery** from arXiv and academic sources
- **Technology blog monitoring** for latest AI/ML developments
- **Intelligent deduplication** and relevance filtering
- **Automatic summarization** before decision-making

### 🏥 Self-Healing Architecture
- **Continuous health monitoring** (30-second intervals)
- **Automatic failure detection** with configurable thresholds
- **Auto-repair functionality** with container restart
- **Rollback support** for failed deployments
- **Proposed fix recommendations** for common issues

### ⚙️ Enhanced Orchestration (L19 Layer)
- **Task decomposition** - breaks complex tasks into subtasks
- **Priority management** - critical, high, normal, low priorities
- **Resource allocation** - intelligent CPU/memory/GPU assignment
- **Cross-domain routing** - seamless integration across services

### 👷 Worker Execution Layer
- **Stateless workers** - disposable and scalable
- **Multiple worker types**:
  - Crawler workers for web scraping
  - Analysis workers for data processing
  - Benchmark workers for performance testing
- **Auto-disposal** after task completion
- **Dynamic worker pool** management

## Features

### 🎨 Chatbot (PWA)
- High creativity in responses with diverse reply variations
- 18+ topic categories with pattern matching
- Pseudo-learning capability with IndexedDB
- Persistent conversation history
- Installable on mobile and desktop with offline support

### 🖼️ 3D/4D Image Generation
- **Stable Diffusion XL** and **DALL-E 3** integration
- **NVIDIA StyleGAN3** for photorealistic generation
- **DreamBooth** for personalized fine-tuned models
- HDR (High Dynamic Range) rendering
- PBR (Physically Based Rendering) support
- Multiple artistic styles (realistic, anime, oil-painting, etc.)

### 🎬 8K Video Generation
- **Runway ML Gen-2** for text/image-to-video
- **NeRF (Neural Radiance Fields)** for 3D scene rendering
- Dynamic camera rendering with view synthesis
- 8K resolution at 60fps
- H.265/HEVC encoding with HDR10+

### 📈 AI-Driven Cryptocurrency Predictions
- **LSTM/Transformer models** for time-series analysis
- Real-time data from **CoinGecko** and **Binance APIs**
- Sentiment analysis from social media
- Risk assessment and auto-balancing
- Technical indicators (RSI, MACD, Moving Averages)

### 🏗️ Infrastructure
- **Kubernetes orchestration** with horizontal pod autoscaling
- **NVIDIA GPU acceleration** (V100, A100 clusters)
- **Docker Compose** for local development
- **GitHub Actions** CI/CD pipeline
- Auto-scaling based on resource metrics

### 🔐 Security & Monitoring
- **Owner-only access control** with encrypted secrets
- **Complete audit logging** for all SGI actions
- **Fraud detection** models for network and crypto analysis
- **ElasticSearch + Kibana** for real-time monitoring
- Security scanning with Trivy
- Prometheus-compatible metrics

### 🚀 CDN & Output Management
- Nginx-based CDN with caching and compression
- Fast content delivery for generated media
- Range requests for video streaming
- Google Cloud integration (Cloud Run, BigQuery)

## Project Structure

```
VoBee-AI-Assistant/
├── index.html              # Main HTML entry point (PWA)
├── manifest.json           # PWA manifest
├── sw.js                   # Service Worker for offline support
├── deploy.sh               # One-command deployment script
├── test-system.sh          # Integration test script
├── AUTONOMOUS_SYSTEM.md    # Detailed autonomous system documentation
├── css/
│   └── styles.css          # Responsive styles
├── js/
│   ├── chatbot.js          # Main chatbot logic
│   └── response-patterns.js # Response templates
├── icons/                  # App icons
├── services/               # Microservices
│   ├── api-gateway/        # FastAPI gateway (port 8000)
│   ├── supreme-general-intelligence/  # SGI service (port 5010)
│   ├── spy-orchestration/  # Automated discovery (port 5006)
│   ├── self-healing/       # Health monitoring (port 5007)
│   ├── worker-pool/        # Stateless workers (port 5008)
│   ├── image-generation/   # Stable Diffusion, DALL-E (port 5000)
│   ├── video-generation/   # Runway ML, NeRF (port 5001)
│   ├── crypto-prediction/  # LSTM/Transformer (port 5002)
│   ├── orchestrator/       # Task orchestration (port 5003)
│   ├── fraud-detection/    # ML fraud detection (port 5004)
│   ├── auto-scaler/        # Resource auto-scaling (port 5005)
│   └── cdn/                # Nginx CDN (port 8080)
├── kubernetes/             # K8s manifests
│   ├── 00-namespace-config.yaml
│   ├── 01-deployments.yaml
│   ├── 02-infrastructure.yaml
│   └── 03-autoscaling.yaml
├── docker-compose.yml      # Local development setup
├── ARCHITECTURE.md         # Detailed architecture docs
└── DEPLOYMENT.md          # Deployment guide
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system architecture.  
See [AUTONOMOUS_SYSTEM.md](AUTONOMOUS_SYSTEM.md) for autonomous features documentation.

### High-Level Overview
```
Supreme General Intelligence (SGI) - Owner Interface
    ├── Intent Understanding & Confirmation
    └── Action Logging & Audit Trail
         │
         ├── Spy-Orchestration Pipeline
         │    ├── GitHub Scanner
         │    ├── Research Discovery (arXiv)
         │    └── Blog Monitoring
         │
         ├── API Gateway (FastAPI)
         │    ├── Image Generation (Stable Diffusion, DALL-E, StyleGAN3)
         │    ├── Video Generation (Runway ML Gen-2, NeRF)
         │    ├── Crypto Prediction (LSTM/Transformer)
         │    └── Fraud Detection (XGBoost)
         │
         ├── Enhanced Orchestrator (L19 Layer)
         │    ├── Task Decomposition
         │    ├── Priority Management
         │    ├── Resource Allocation
         │    └── Cross-Domain Routing
         │
         ├── Worker Pool
         │    ├── Crawler Workers
         │    ├── Analysis Workers
         │    └── Benchmark Workers
         │
         └── Self-Healing System
              ├── Health Monitoring
              ├── Failure Detection
              └── Auto-Repair
```

### Technologies Used
- **Backend**: Python 3.11, FastAPI, Flask
- **AI/ML**: PyTorch, Transformers, Diffusers, Scikit-learn
- **Infrastructure**: Docker, Kubernetes, NVIDIA GPU Operator
- **Monitoring**: ElasticSearch, Kibana, Prometheus
- **Storage**: PostgreSQL, Redis, Persistent Volumes
- **CDN**: Nginx with caching and compression
- **Security**: Owner-based authentication, encrypted secrets

### VoBeeChatbot Class (PWA)
The main chatbot engine that handles:
- Pattern matching via keyword mappings
- Random response selection for variety
- IndexedDB management for persistence
- Message processing pipeline

### ChatUI Class
Manages the user interface:
- Message display and animations
- Event handling (send, clear)
- Typing indicators
- Welcome messages

### IndexedDB Stores
1. **conversations**: Stores all chat messages with timestamps
2. **unrecognized_queries**: Logs unknown inputs with occurrence counts

## Quick Start

### Option 1: PWA Chatbot Only
1. Clone the repository
2. Serve the files using any HTTP server:
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js
   npx serve
   ```
3. Open `http://localhost:8080` in your browser

### Option 2: Full Autonomous AI System (Recommended - One Command)

**Important:** Before starting, configure your owner secret!

1. Clone the repository
   ```bash
   git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
   cd VoBee-AI-Assistant
   ```

2. Configure environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and IMPORTANT: set OWNER_SECRET
   nano .env
   ```

3. Deploy with one command
   ```bash
   ./deploy.sh
   ```

This script will:
- Check prerequisites (Docker)
- Build all services
- Start infrastructure (PostgreSQL, Redis)
- Deploy all microservices
- Verify system health
- Display service endpoints

4. Test the system
   ```bash
   ./test-system.sh
   ```

### Option 3: Manual Docker Compose Deployment

1. Clone and configure (steps 1-2 from Option 2)

2. Start all services
   ```bash
   docker compose up -d
   ```

3. Access services:
   - Supreme General Intelligence: http://localhost:5010
   - API Gateway: http://localhost:8000
   - Spy-Orchestration: http://localhost:5006
   - Self-Healing Monitor: http://localhost:5007
   - Worker Pool: http://localhost:5008
   - Kibana Dashboard: http://localhost:5601
   - CDN: http://localhost:8080

### Option 4: Production Kubernetes Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

```bash
# Quick deployment
kubectl apply -f kubernetes/00-namespace-config.yaml
kubectl apply -f kubernetes/02-infrastructure.yaml
kubectl apply -f kubernetes/01-deployments.yaml
kubectl apply -f kubernetes/03-autoscaling.yaml
```

## API Usage

### Autonomous System APIs

#### Supreme General Intelligence - Chat
```bash
# Send a command to SGI
curl -X POST http://localhost:5010/chat \
  -H "Content-Type: application/json" \
  -H "X-Owner-Secret: your_secure_owner_secret_key" \
  -d '{
    "message": "scan github for AI repositories",
    "context": {}
  }'
```

#### SGI - Confirm Action
```bash
# Confirm and execute an action
curl -X POST http://localhost:5010/confirm \
  -H "Content-Type: application/json" \
  -H "X-Owner-Secret: your_secure_owner_secret_key" \
  -d '{
    "action_id": "uuid-from-chat-response",
    "confirmed": true
  }'
```

#### Spy-Orchestration - GitHub Scan
```bash
# Start a GitHub repository scan
curl -X POST http://localhost:5006/scan \
  -H "Content-Type: application/json" \
  -d '{
    "scan_type": "github",
    "parameters": {
      "query": "AI machine learning stars:>100",
      "max_results": 50,
      "min_relevance": 0.5
    }
  }'
```

#### Self-Healing - System Health
```bash
# Check overall system health
curl http://localhost:5007/system/health

# Manually trigger repair
curl -X POST http://localhost:5007/service/api-gateway/repair
```

#### Worker Pool - Execute Task
```bash
# Execute a crawler task
curl -X POST http://localhost:5008/task/execute \
  -H "Content-Type: application/json" \
  -d '{
    "worker_type": "crawler",
    "task": {
      "url": "https://github.com",
      "depth": 1
    }
  }'
```

### AI Generation APIs

#### Generate Image
```bash
curl -X POST http://localhost:8000/api/v1/generate/image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic city with flying cars",
    "style": "realistic",
    "resolution": "1024x1024",
    "hdr": true,
    "pbr": true,
    "model": "stable-diffusion"
  }'
```

### Generate Video
```bash
curl -X POST http://localhost:8000/api/v1/generate/video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Flying through clouds at sunset",
    "duration": 5,
    "resolution": "8K",
    "fps": 60,
    "use_nerf": true
  }'
```

### Predict Cryptocurrency Price
```bash
curl -X POST http://localhost:8000/api/v1/crypto/predict \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC",
    "timeframe": "1h",
    "prediction_horizon": 24
  }'
```

### Orchestrate Multiple Tasks
```bash
curl -X POST http://localhost:8000/api/v1/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {
        "type": "image_generation",
        "params": {"prompt": "Sunset landscape"}
      },
      {
        "type": "crypto_prediction",
        "params": {"symbol": "ETH"}
      }
    ],
    "priority": "high"
  }'
```

## Resource Requirements

### Development
- CPU: 8 cores
- RAM: 16 GB
- GPU: 1x NVIDIA GPU (optional, for testing)
- Storage: 100 GB SSD

### Production
- CPU: 64 cores
- RAM: 256 GB
- GPU: 4x NVIDIA A100 (40GB VRAM each)
- Storage: 5 TB NVMe SSD
- Network: 10 Gbps

## Extending the Chatbot

### Adding New Response Categories
1. Add responses to `ResponsePatterns` in `js/response-patterns.js`:
   ```javascript
   newCategory: [
       "Response 1",
       "Response 2",
       // ...
   ]
   ```

2. Add keywords to `KeywordMappings`:
   ```javascript
   newCategory: ['keyword1', 'keyword2', 'phrase to match']
   ```

### Analyzing Unrecognized Queries
Access logged queries programmatically:
```javascript
const queries = await vobee.getUnrecognizedQueries();
console.log(queries);
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed system architecture and component descriptions
- [DEPLOYMENT.md](DEPLOYMENT.md) - Step-by-step deployment guide for all environments
- API Documentation - Available at `http://localhost:8000/docs` when running

## Monitoring & Observability

### Kibana Dashboards
Access at `http://localhost:5601` (Docker Compose) or via Kubernetes service

### Metrics
- Request latency and throughput
- Error rates by service
- GPU utilization and memory
- Model inference times
- Queue lengths and task completion rates

### Health Checks
- All services expose `/health` endpoints
- Kubernetes liveness and readiness probes
- Automatic service recovery on failure

## Browser Support
- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## License
MIT License - feel free to use and modify!
