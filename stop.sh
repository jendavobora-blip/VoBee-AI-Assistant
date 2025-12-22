#!/bin/bash

# Vobio AI Studio - Stop Script
# Stops all services gracefully

set -e

echo "=========================================="
echo "  Vobio AI Studio - Stopping Services"
echo "=========================================="
echo ""

cd vobio-ai-studio

# Stop services
echo "Stopping all services..."
docker-compose down

echo ""
echo "✓ All services stopped"
echo ""
echo "To remove volumes (will delete data):"
echo "  docker-compose -f vobio-ai-studio/docker-compose.yml down -v"
echo ""
