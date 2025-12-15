# Quick Start Guide

This guide will help you get VoBee AI Assistant up and running in minutes.

## ✨ What's New

VoBee now includes:
- 🤖 **AI-Level Quality Assurance** - Autonomous testing and validation
- 🧠 **Intelligent Optimization** - Automatic caching and learning
- 📱 **Mobile Ready** - Native Android and iOS apps
- ⚡ **Background Learning** - Continuous self-improvement
- 📊 **Real-time Metrics** - Performance monitoring dashboard

## 🧪 Test the New Features

```bash
# Clone and navigate
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant

# Install dependencies (for testing)
npm install

# Run AI quality tests
npm run test:quality

# Run optimization tests
npm run optimize
```

## 🚀 Three Ways to Run VoBee

### Option 1: Web App (Fastest - No Installation Required)

```bash
# Clone the repository
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant

# Start web server
python3 -m http.server 8080
# OR
npx http-server -p 8080
```

Open http://localhost:8080 in your browser and start chatting!

### Option 2: Mobile App (Android/iOS)

See [MOBILE_DEPLOYMENT.md](MOBILE_DEPLOYMENT.md) for complete guide.

```bash
# Install dependencies
npm install

# Build for Android
npm run mobile:build:android

# Build for iOS (macOS only)
npm run mobile:build:ios
```

### Option 3: Full AI System with Backend Services

### Option 3: Full AI System with Backend Services

## Prerequisites (for Full System)

- Docker Desktop installed and running
- Docker Compose installed
- At least 16GB RAM available
- (Optional) NVIDIA GPU with CUDA support

## 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant

# Copy environment configuration
cp .env.example .env
```

## 2. Configure API Keys (Optional)

Edit `.env` and add your API keys:

```bash
# For crypto predictions
COINGECKO_API_KEY=your_key_here
BINANCE_API_KEY=your_key_here

# For AI generation (if using external APIs)
OPENAI_API_KEY=your_key_here
STABILITY_API_KEY=your_key_here
RUNWAY_API_KEY=your_key_here
```

**Note**: The system will work without these keys, but functionality will be limited to placeholder responses.

## 3. Start the System

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

Wait 2-3 minutes for all services to initialize.

## 4. Verify Services

Check that all services are running:

```bash
# Check service status
docker-compose ps

# Test API Gateway
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "version": "1.0.0"
}
```

## 5. Test the API

### Generate an Image

```bash
curl -X POST http://localhost:8000/api/v1/generate/image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "style": "realistic",
    "resolution": "1024x1024",
    "hdr": true
  }'
```

### Generate a Video

```bash
curl -X POST http://localhost:8000/api/v1/generate/video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Flying through clouds",
    "duration": 5,
    "resolution": "4K",
    "fps": 30
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

### Get Sentiment Analysis

```bash
curl http://localhost:8000/api/v1/crypto/sentiment/BTC
```

## 6. Access Monitoring

### Kibana Dashboard
Open http://localhost:5601 in your browser

### Service Status
```bash
curl http://localhost:8000/status
```

### System Metrics
```bash
curl http://localhost:8000/metrics
```

## 7. Stop the System

```bash
# Stop all services
docker-compose down

# Stop and remove all data
docker-compose down -v
```

## Common Issues

### Port Already in Use
If you see "port already allocated" errors:
```bash
# Change ports in docker-compose.yml
# Or stop conflicting services
```

### Out of Memory
If containers crash due to memory:
```bash
# Reduce replica counts in docker-compose.yml
# Or allocate more memory to Docker Desktop
```

### GPU Not Detected
If you have an NVIDIA GPU but it's not being used:
```bash
# Install nvidia-container-toolkit
# Restart Docker
# Verify: docker run --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

## Next Steps

1. **Explore the API**: See [ARCHITECTURE.md](ARCHITECTURE.md) for all endpoints
2. **Deploy to Production**: See [DEPLOYMENT.md](DEPLOYMENT.md) for Kubernetes deployment
3. **Monitor Performance**: Access Kibana at http://localhost:5601
4. **View Chatbot**: Open http://localhost:8080 for the PWA chatbot

## API Documentation

Once running, explore the interactive API docs:
- Swagger UI: http://localhost:8000/docs (if enabled)
- ReDoc: http://localhost:8000/redoc (if enabled)

## Troubleshooting

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api-gateway
docker-compose logs -f image-generation
```

### Restart a Service
```bash
docker-compose restart api-gateway
```

### Check Service Health
```bash
# API Gateway
curl http://localhost:8000/health

# Image Generation
curl http://localhost:5000/health

# Video Generation
curl http://localhost:5001/health

# Crypto Prediction
curl http://localhost:5002/health
```

### Rebuild After Changes
```bash
# Rebuild specific service
docker-compose build api-gateway

# Rebuild all
docker-compose build

# Rebuild and restart
docker-compose up -d --build
```

## Development Mode

To develop a specific service:

```bash
# Stop the service in Docker
docker-compose stop api-gateway

# Run it locally with hot reload
cd services/api-gateway
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Production Deployment

For production deployment on Kubernetes, see [DEPLOYMENT.md](DEPLOYMENT.md).

Quick Kubernetes deployment:
```bash
kubectl apply -f kubernetes/
```

## Support

- **Documentation**: See ARCHITECTURE.md and DEPLOYMENT.md
- **Issues**: https://github.com/jendavobora-blip/VoBee-AI-Assistant/issues
- **Service README**: See services/README.md for service-specific docs

## What You've Built

You now have a complete AI orchestration system running with:
- ✅ API Gateway for unified access
- ✅ Image generation (Stable Diffusion, DALL-E)
- ✅ Video generation (NeRF, Runway ML)
- ✅ Crypto predictions (LSTM/Transformer)
- ✅ Fraud detection
- ✅ Auto-scaling
- ✅ Real-time monitoring
- ✅ CDN for content delivery

Enjoy building with the AI Orchestration System! 🚀
