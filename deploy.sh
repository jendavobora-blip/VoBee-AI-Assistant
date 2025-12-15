#!/bin/bash
#
# VoBee AI Assistant - One-Command Setup and Deployment
# This script sets up and deploys the complete autonomous system
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Header
echo ""
echo "========================================================"
echo "  VoBee AI Assistant - Autonomous System Deployment"
echo "========================================================"
echo ""

# Step 1: Check prerequisites
print_info "Checking prerequisites..."

if ! command_exists docker; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Prerequisites check passed"

# Step 2: Check for .env file
print_info "Checking environment configuration..."

if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_warning "Please edit .env file with your API keys and secrets before continuing."
    read -p "Press Enter when you have configured .env file..."
fi

print_success "Environment configuration found"

# Step 3: Create necessary directories
print_info "Creating data directories..."

mkdir -p data/models
mkdir -p data/outputs/images
mkdir -p data/outputs/videos
mkdir -p data/crypto-data

print_success "Data directories created"

# Step 4: Pull base images
print_info "Pulling base Docker images..."

docker pull python:3.11-slim
docker pull postgres:15-alpine
docker pull redis:7-alpine
docker pull nginx:alpine

print_success "Base images pulled"

# Step 5: Build services
print_info "Building service containers..."

docker-compose build --parallel

print_success "Service containers built"

# Step 6: Start infrastructure services first
print_info "Starting infrastructure services (PostgreSQL, Redis, ElasticSearch)..."

docker-compose up -d postgres redis elasticsearch

print_info "Waiting for database to be ready..."
sleep 10

# Check if PostgreSQL is ready
until docker-compose exec -T postgres pg_isready -U orchestrator; do
    print_info "Waiting for PostgreSQL..."
    sleep 2
done

print_success "Infrastructure services started"

# Step 7: Start all services
print_info "Starting all services..."

docker-compose up -d

print_success "All services started"

# Step 8: Wait for services to be healthy
print_info "Waiting for services to become healthy..."
sleep 15

# Step 9: Verify deployment
print_info "Verifying deployment..."

SERVICES=("api-gateway:8000" "supreme-general-intelligence:5010" "spy-orchestration:5006" "self-healing:5007")
ALL_HEALTHY=true

for service in "${SERVICES[@]}"; do
    SERVICE_NAME="${service%:*}"
    SERVICE_PORT="${service#*:}"
    
    if curl -s -f "http://localhost:${SERVICE_PORT}/health" > /dev/null 2>&1; then
        print_success "${SERVICE_NAME} is healthy"
    else
        print_warning "${SERVICE_NAME} health check failed"
        ALL_HEALTHY=false
    fi
done

# Step 10: Display deployment information
echo ""
echo "========================================================"
echo "  Deployment Complete!"
echo "========================================================"
echo ""
echo "Service Endpoints:"
echo "  - API Gateway:               http://localhost:8000"
echo "  - Supreme General Intel:     http://localhost:5010"
echo "  - Spy Orchestration:         http://localhost:5006"
echo "  - Self-Healing Monitor:      http://localhost:5007"
echo "  - Kibana Dashboard:          http://localhost:5601"
echo "  - CDN Service:               http://localhost:8080"
echo ""
echo "API Documentation:"
echo "  - Gateway API Docs:          http://localhost:8000/docs"
echo "  - SGI API Docs:              http://localhost:5010/docs"
echo "  - Spy API Docs:              http://localhost:5006/docs"
echo ""
echo "Database:"
echo "  - PostgreSQL:                localhost:5432"
echo "  - Redis:                     localhost:6379"
echo ""

if [ "$ALL_HEALTHY" = true ]; then
    print_success "All services are healthy and running!"
else
    print_warning "Some services may need additional time to start. Check logs with:"
    echo "  docker-compose logs -f"
fi

echo ""
echo "To view logs:     docker-compose logs -f [service-name]"
echo "To stop:          docker-compose down"
echo "To restart:       docker-compose restart [service-name]"
echo ""

# Step 11: Display next steps
echo "========================================================"
echo "  Next Steps"
echo "========================================================"
echo ""
echo "1. Access the SGI (Supreme General Intelligence) interface:"
echo "   curl -X POST http://localhost:5010/chat \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -H 'X-Owner-Secret: your_secure_owner_secret_key' \\"
echo "     -d '{\"message\": \"scan github for AI repositories\"}'"
echo ""
echo "2. View system health:"
echo "   curl http://localhost:5007/system/health"
echo ""
echo "3. Start a spy-orchestration scan:"
echo "   curl -X POST http://localhost:5006/scan \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"scan_type\": \"github\", \"parameters\": {\"query\": \"AI machine learning\"}}'"
echo ""
echo "4. Explore the API documentation in your browser:"
echo "   http://localhost:8000/docs"
echo ""

print_success "Setup complete! The autonomous system is ready."
