# Deployment Guide - AI Orchestration System

This guide provides step-by-step instructions for deploying the AI Orchestration System.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Local Development Deployment](#local-development-deployment)
4. [Production Kubernetes Deployment](#production-kubernetes-deployment)
5. [Google Cloud Platform Deployment](#google-cloud-platform-deployment)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Scaling and Optimization](#scaling-and-optimization)

## Prerequisites

### Hardware Requirements
- **Development**: 16GB RAM, 8 CPU cores, 1 GPU (optional)
- **Production**: 256GB RAM, 64 CPU cores, 4x NVIDIA A100 GPUs

### Software Requirements
- Docker 24.0+
- Docker Compose 2.0+
- Kubernetes 1.28+
- kubectl 1.28+
- NVIDIA GPU Operator (for GPU support)
- Python 3.11+

### Cloud Requirements (Optional)
- Google Cloud Platform account
- GKE cluster with GPU node pools
- Cloud Storage bucket

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
# Database
POSTGRES_PASSWORD=your_secure_password

# Crypto APIs
COINGECKO_API_KEY=your_coingecko_api_key
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret

# AI APIs
OPENAI_API_KEY=your_openai_api_key
STABILITY_API_KEY=your_stability_ai_key
RUNWAY_API_KEY=your_runway_ml_key

# Google Cloud
GOOGLE_CLOUD_PROJECT=your_project_id
```

### 3. Install NVIDIA GPU Support (if using GPUs)
```bash
# Install NVIDIA drivers
sudo ubuntu-drivers autoinstall

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

## Local Development Deployment

### Using Docker Compose

1. **Build Images**
```bash
docker-compose build
```

2. **Start Services**
```bash
docker-compose up -d
```

3. **View Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api-gateway
```

4. **Access Services**
- API Gateway: http://localhost:8000
- Kibana Dashboard: http://localhost:5601
- CDN: http://localhost:8080

5. **Test API**
```bash
# Health check
curl http://localhost:8000/health

# Status of all services
curl http://localhost:8000/status

# Generate image
curl -X POST http://localhost:8000/api/v1/generate/image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "style": "realistic",
    "resolution": "1024x1024"
  }'
```

6. **Stop Services**
```bash
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Production Kubernetes Deployment

### 1. Prepare Kubernetes Cluster

#### Option A: Google Kubernetes Engine (GKE)
```bash
# Create GKE cluster with GPU support
gcloud container clusters create ai-orchestration \
  --zone us-central1-a \
  --machine-type n1-standard-8 \
  --num-nodes 3 \
  --accelerator type=nvidia-tesla-a100,count=1 \
  --enable-autoscaling \
  --min-nodes 3 \
  --max-nodes 10

# Get credentials
gcloud container clusters get-credentials ai-orchestration \
  --zone us-central1-a
```

#### Option B: On-Premise Cluster
```bash
# Configure kubectl for your cluster
export KUBECONFIG=/path/to/kubeconfig
kubectl config use-context my-cluster
```

### 2. Install NVIDIA GPU Operator
```bash
# Add NVIDIA Helm repository
helm repo add nvidia https://nvidia.github.io/gpu-operator
helm repo update

# Install GPU operator
helm install --wait --generate-name \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator
```

### 3. Deploy the System

```bash
# Create namespace and configurations
kubectl apply -f kubernetes/00-namespace-config.yaml

# Update secrets with your actual values
kubectl create secret generic ai-secrets \
  --from-literal=POSTGRES_PASSWORD=your_password \
  --from-literal=COINGECKO_API_KEY=your_key \
  --from-literal=BINANCE_API_KEY=your_key \
  --from-literal=BINANCE_API_SECRET=your_secret \
  --from-literal=OPENAI_API_KEY=your_key \
  --from-literal=STABILITY_API_KEY=your_key \
  --from-literal=RUNWAY_API_KEY=your_key \
  -n ai-orchestration \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy infrastructure services
kubectl apply -f kubernetes/02-infrastructure.yaml

# Wait for infrastructure to be ready
kubectl wait --for=condition=ready pod -l app=redis -n ai-orchestration --timeout=300s
kubectl wait --for=condition=ready pod -l app=postgres -n ai-orchestration --timeout=300s

# Deploy AI services
kubectl apply -f kubernetes/01-deployments.yaml

# Configure autoscaling
kubectl apply -f kubernetes/03-autoscaling.yaml
```

### 4. Monitor Deployment
```bash
# Check pod status
kubectl get pods -n ai-orchestration -w

# Check service endpoints
kubectl get svc -n ai-orchestration

# View logs
kubectl logs -f deployment/api-gateway -n ai-orchestration
```

### 5. Access Services

```bash
# Get API Gateway external IP
kubectl get svc api-gateway-service -n ai-orchestration

# Port forward for testing
kubectl port-forward svc/api-gateway-service 8000:80 -n ai-orchestration

# Access Kibana
kubectl port-forward svc/kibana-service 5601:5601 -n ai-orchestration
```

## Google Cloud Platform Deployment

### 1. Setup GCP Project
```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable container.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable bigquery.googleapis.com
```

### 2. Create Cloud Storage for Models
```bash
# Create bucket
gsutil mb -l us-central1 gs://ai-orchestration-models

# Upload models (if you have pre-trained models)
gsutil -m cp -r /path/to/models/* gs://ai-orchestration-models/
```

### 3. Deploy to Cloud Run (Serverless Option)
```bash
# Build and deploy API Gateway
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/api-gateway services/api-gateway

gcloud run deploy api-gateway \
  --image gcr.io/YOUR_PROJECT_ID/api-gateway \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

### 4. Setup BigQuery for Analytics
```bash
# Create dataset
bq mk -d ai_analytics

# Create tables for logs and metrics
bq mk -t ai_analytics.service_logs \
  timestamp:TIMESTAMP,service:STRING,level:STRING,message:STRING

bq mk -t ai_analytics.predictions \
  timestamp:TIMESTAMP,symbol:STRING,predicted_price:FLOAT,confidence:FLOAT
```

## Post-Deployment Verification

### 1. Health Checks
```bash
# Test all services
curl http://<API_GATEWAY_IP>/status

# Test image generation
curl -X POST http://<API_GATEWAY_IP>/api/v1/generate/image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test image",
    "style": "realistic"
  }'

# Test crypto prediction
curl -X POST http://<API_GATEWAY_IP>/api/v1/crypto/predict \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC",
    "timeframe": "1h"
  }'
```

### 2. Load Testing
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test API Gateway
ab -n 1000 -c 10 http://<API_GATEWAY_IP>/health

# Test with POST requests
ab -n 100 -c 5 -p payload.json -T application/json \
  http://<API_GATEWAY_IP>/api/v1/crypto/predict
```

### 3. Monitor Logs
```bash
# Kubernetes logs
kubectl logs -f -l app=api-gateway -n ai-orchestration

# View in Kibana
# Access http://<KIBANA_IP>:5601
# Create index pattern: logstash-*
# Explore logs in Discover
```

## Scaling and Optimization

### 1. Scale Services
```bash
# Manual scaling
kubectl scale deployment api-gateway --replicas=5 -n ai-orchestration

# Update HPA thresholds
kubectl edit hpa api-gateway-hpa -n ai-orchestration
```

### 2. Optimize GPU Usage
```bash
# Check GPU utilization
kubectl exec -it <pod-name> -n ai-orchestration -- nvidia-smi

# Adjust GPU memory limits in deployments
kubectl edit deployment image-generation -n ai-orchestration
```

### 3. Update Services
```bash
# Build new image
docker build -t ai-orchestration/api-gateway:v2 services/api-gateway/

# Push to registry
docker tag ai-orchestration/api-gateway:v2 gcr.io/PROJECT/api-gateway:v2
docker push gcr.io/PROJECT/api-gateway:v2

# Update deployment
kubectl set image deployment/api-gateway \
  api-gateway=gcr.io/PROJECT/api-gateway:v2 \
  -n ai-orchestration

# Monitor rollout
kubectl rollout status deployment/api-gateway -n ai-orchestration
```

## Troubleshooting

### Common Issues

**Pods stuck in Pending**
```bash
# Check events
kubectl describe pod <pod-name> -n ai-orchestration

# Check resource availability
kubectl top nodes
kubectl describe node <node-name>
```

**GPU not detected**
```bash
# Verify GPU operator
kubectl get pods -n gpu-operator

# Check node labels
kubectl get nodes -o json | jq '.items[].metadata.labels'
```

**Service connectivity issues**
```bash
# Test from within cluster
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://image-generation-service:5000/health

# Check service endpoints
kubectl get endpoints -n ai-orchestration
```

**High memory usage**
```bash
# Check resource usage
kubectl top pods -n ai-orchestration

# Increase memory limits
kubectl edit deployment <deployment-name> -n ai-orchestration
```

## Maintenance

### Backup
```bash
# Backup PostgreSQL
kubectl exec -it postgres-0 -n ai-orchestration -- \
  pg_dump -U orchestrator orchestrator_db > backup.sql

# Backup persistent volumes
kubectl get pvc -n ai-orchestration
# Use your cloud provider's snapshot feature
```

### Updates
```bash
# Update Kubernetes manifests
git pull
kubectl apply -f kubernetes/

# Update Docker Compose
git pull
docker-compose pull
docker-compose up -d
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/jendavobora-blip/VoBee-AI-Assistant/issues
- Documentation: See ARCHITECTURE.md
- API Reference: http://<API_GATEWAY>/docs (when available)
