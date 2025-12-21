#!/bin/bash

# Vobio AI Studio - Start Script
# This script starts both backend and frontend components

set -e

echo "=========================================="
echo "  Vobio AI Studio - Starting Application"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo -e "${YELLOW}[1/4]${NC} Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found${NC}"

# Check Node.js
echo -e "${YELLOW}[2/4]${NC} Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

# Setup Backend
echo -e "${YELLOW}[3/4]${NC} Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Backend setup complete${NC}"

# Start Backend
echo "Starting backend server..."
python api_server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
echo "Waiting for backend to start..."
sleep 3
if curl -s http://127.0.0.1:8000/health > /dev/null; then
    echo -e "${GREEN}✓ Backend is running on http://127.0.0.1:8000${NC}"
else
    echo -e "${RED}Error: Backend failed to start${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Setup and Start Frontend
echo -e "${YELLOW}[4/4]${NC} Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install --silent
fi

cd electron
if [ ! -d "node_modules" ]; then
    echo "Installing Electron dependencies..."
    npm install --silent
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""
echo "=========================================="
echo "  Starting Electron Application"
echo "=========================================="
echo ""

# Start Electron
npm start

# Cleanup on exit
echo ""
echo "Shutting down backend..."
kill $BACKEND_PID 2>/dev/null || true
wait $BACKEND_PID 2>/dev/null || true

echo -e "${GREEN}Application stopped successfully${NC}"
