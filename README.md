# VoBee AI Assistant <img width="480" height="480" alt="image" src="https://github.com/user-attachments/assets/feb0de59-8c3c-4796-8b99-554155982991" />

A complete AI orchestration system featuring:
- **L20 Supreme Brain** - Advanced mega-scale orchestration at level 20
- **Master Intelligences (L18)** - Specialized subsystems for content, marketing, web/app building, and advanced media
- **AI Swarm Coordinator** - Handles millions of micro-tasks with intelligent bot orchestration
- **Creative AI chatbot** PWA with pseudo-learning capabilities
- **3D/4D image and video generation** (Stable Diffusion, DALL-E, NeRF, Runway ML Gen-2)
- **Cryptocurrency prediction** with LSTM/Transformer models
- **Kubernetes-based** distributed infrastructure with GPU acceleration
- **Auto-scaling** and fraud detection capabilities
- **CDN pipeline** for fast content delivery

## Features

### 🧠 L20 Supreme Brain Orchestration
- **Strategic Planning** - High-level objective decomposition and planning
- **Intelligent Prioritization** - Multi-factor task priority analysis
- **Cross-Domain Coordination** - Seamless orchestration across all AI services
- **Resource Optimization** - Dynamic allocation based on requirements and priorities
- **Performance Analytics** - Real-time metrics and optimization recommendations

### 🎯 Master Intelligences (L18 Subsystems)
Specialized AI modules for different domains:

1. **Product Content Generation**
   - Automated product descriptions and catalogs
   - SEO-optimized marketing copy
   - Multi-style content variations
   - Technical specifications generation

2. **Cross-Industry Marketing**
   - Multi-channel campaign creation (social, email, web, video)
   - Audience targeting and segmentation
   - Budget allocation optimization
   - KPI definition and tracking

3. **Autonomous Web/App Builder**
   - Full-stack application architecture design
   - Component and page generation
   - API endpoint and database schema creation
   - Deployment automation

4. **Advanced Media Generation**
   - Ultra-high-resolution (8K, 16K) image generation
   - Real-time video generation up to 120 FPS
   - HDR and PBR rendering integration

### 🐝 AI Swarm Coordinator
- **Dynamic Bot Swarm** - Scalable from 10 to millions of bots
- **Intelligent Task Distribution** - Priority-based queue management
- **Load Balancing** - Automatic bot allocation based on capabilities
- **Performance Monitoring** - Real-time metrics and optimization
- **Auto-Scaling** - Responsive to queue length and load

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
├── css/
│   └── styles.css          # Responsive styles
├── js/
│   ├── chatbot.js          # Main chatbot logic
│   └── response-patterns.js # Response templates
├── icons/                  # App icons
├── services/               # Microservices
│   ├── api-gateway/        # FastAPI gateway (port 8000)
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

### High-Level Overview
```
API Gateway (FastAPI)
    ├── Image Generation (Stable Diffusion, DALL-E, StyleGAN3)
    ├── Video Generation (Runway ML Gen-2, NeRF)
    ├── Crypto Prediction (LSTM/Transformer)
    ├── Fraud Detection (XGBoost)
    └── Orchestrator (Redis, PostgreSQL)
         ├── Task Queue Management
         ├── Workflow Coordination
         └── Service Discovery
```

### Technologies Used
- **Backend**: Python 3.11, FastAPI, Flask
- **AI/ML**: PyTorch, Transformers, Diffusers, Scikit-learn
- **Infrastructure**: Docker, Kubernetes, NVIDIA GPU Operator
- **Monitoring**: ElasticSearch, Kibana, Prometheus
- **Storage**: PostgreSQL, Redis, Persistent Volumes
- **CDN**: Nginx with caching and compression

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

### Option 2: Full AI Orchestration System (Docker Compose)
1. Clone the repository
   ```bash
   git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
   cd VoBee-AI-Assistant
   ```

2. Configure environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Start all services
   ```bash
   docker-compose up -d
   ```

4. Access services:
   - API Gateway: http://localhost:8000
   - Kibana Dashboard: http://localhost:5601
   - CDN: http://localhost:8080

### Option 3: Production Kubernetes Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

```bash
# Quick deployment
kubectl apply -f kubernetes/00-namespace-config.yaml
kubectl apply -f kubernetes/02-infrastructure.yaml
kubectl apply -f kubernetes/01-deployments.yaml
kubectl apply -f kubernetes/03-autoscaling.yaml
```

## API Usage

### Generate Image
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

### L20 Strategic Planning
```bash
curl -X POST http://localhost:8000/api/v1/l20/strategize \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "Launch new product with integrated marketing campaign",
    "constraints": {
      "budget": 50000,
      "timeline": "30 days"
    }
  }'
```

### Cross-Domain Coordination
```bash
curl -X POST http://localhost:8000/api/v1/l20/coordinate \
  -H "Content-Type: application/json" \
  -d '{
    "domains": ["image_generation", "video_generation", "marketing"],
    "task_specs": {
      "image_generation": {"prompt": "Product showcase", "resolution": "8K"},
      "marketing": {"campaign_type": "product_launch"}
    }
  }'
```

### Product Content Generation
```bash
curl -X POST http://localhost:8000/api/v1/intelligence/product_content/execute \
  -H "Content-Type: application/json" \
  -d '{
    "product_details": {
      "name": "Smart Watch Pro",
      "category": "Wearables",
      "features": ["Heart rate monitoring", "GPS", "Water resistant"]
    },
    "content_type": "description",
    "tone": "professional"
  }'
```

### Marketing Campaign Creation
```bash
curl -X POST http://localhost:8000/api/v1/intelligence/marketing/execute \
  -H "Content-Type: application/json" \
  -d '{
    "product": {"name": "Smart Watch Pro"},
    "target_audience": {"age": "25-45", "interests": ["fitness", "tech"]},
    "channels": ["social", "email", "web"],
    "budget": 25000
  }'
```

### Dispatch Micro-Tasks to AI Swarm
```bash
curl -X POST http://localhost:8000/api/v1/swarm/dispatch \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {"type": "data_processing", "data": {"record_count": 1000}, "priority": "high"},
      {"type": "image_processing", "data": {"filters": ["blur", "sharpen"]}}
    ]
  }'
```

### Get AI Swarm Status
```bash
curl http://localhost:8000/api/v1/swarm/status
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
