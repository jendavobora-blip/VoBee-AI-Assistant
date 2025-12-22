#!/bin/bash

# Vobio AI Studio - One-Command Start Script
# Starts all services with Docker Compose

set -e

echo "=========================================="
echo "  Vobio AI Studio - Starting Services"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if setup was run
if [ ! -f "vobio-ai-studio/.env" ]; then
    echo -e "${YELLOW}⚠ .env file not found. Running setup first...${NC}"
    ./setup.sh
    echo ""
fi

# Start services
echo "Starting all services..."
cd vobio-ai-studio
docker-compose up -d

echo ""
echo "Waiting for services to become healthy..."
sleep 10

# Check service health
echo ""
echo "Service Status:"
docker-compose ps

echo ""
echo "=========================================="
echo -e "${GREEN}✓ All services started!${NC}"
echo "=========================================="
echo ""
echo "Service URLs:"
echo "  • Vobio API:       http://localhost:8000"
echo "  • API Health:      http://localhost:8000/health"
echo "  • Langfuse:        http://localhost:3000"
echo "  • Qdrant:          http://localhost:6333"
echo "  • OTEL Collector:  http://localhost:4317 (gRPC)"
echo ""
echo "View logs:"
echo "  docker-compose -f vobio-ai-studio/docker-compose.yml logs -f"
echo ""
echo "Stop services:"
echo "  ./stop.sh"
echo ""
echo "Run tests:"
echo "  ./test.sh"
echo ""
