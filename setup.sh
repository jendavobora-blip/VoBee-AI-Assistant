#!/bin/bash

# Vobio AI Studio - One-Command Setup Script
# Prepares the environment for first run

set -e

echo "=========================================="
echo "  Vobio AI Studio - Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found${NC}"

# Check Python (for local dev)
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python 3 found${NC}"
else
    echo -e "${YELLOW}⚠ Python 3 not found (optional for local dev)${NC}"
fi

# Check Node.js (for frontend)
if command -v node &> /dev/null; then
    echo -e "${GREEN}✓ Node.js found${NC}"
else
    echo -e "${YELLOW}⚠ Node.js not found (optional for local frontend dev)${NC}"
fi

echo ""

# Create .env file if it doesn't exist
if [ ! -f "vobio-ai-studio/.env" ]; then
    echo "Creating .env file from .env.example..."
    cp vobio-ai-studio/.env.example vobio-ai-studio/.env
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists, skipping${NC}"
fi

echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p vobio-ai-studio/backend/quarantine
mkdir -p vobio-ai-studio/backend/logs
mkdir -p vobio-ai-studio/backend/temp
mkdir -p vobio-ai-studio/backend/skills
mkdir -p vobio-ai-studio/backend/knowledge
echo -e "${GREEN}✓ Directories created${NC}"

echo ""

# Pull Docker images
echo "Pulling Docker images (this may take a few minutes)..."
cd vobio-ai-studio
docker-compose pull
echo -e "${GREEN}✓ Docker images pulled${NC}"

echo ""

# Build the Vobio API image
echo "Building Vobio API image..."
docker-compose build vobio-api
echo -e "${GREEN}✓ Vobio API image built${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review and customize vobio-ai-studio/.env if needed"
echo "  2. Run: ./start.sh to start all services"
echo "  3. Access the API at: http://localhost:8000"
echo "  4. Access Langfuse at: http://localhost:3000"
echo ""
echo "For more information, see README.md"
echo ""
