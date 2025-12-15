#!/bin/bash
# Integration test script for auto-healing and self-evolution services

set -e

echo "========================================"
echo "Auto-Healing & Self-Evolution Integration Tests"
echo "========================================"

echo ""
echo "1. Testing Health Monitor Service..."
cd services/health-monitor

# Start the service in background
echo "   Starting health-monitor service..."
python main.py > /tmp/health-monitor.log 2>&1 &
HEALTH_PID=$!
sleep 3

# Test health endpoint
echo "   Testing /health endpoint..."
if curl -s http://localhost:5006/health | grep -q "healthy"; then
    echo "   ✓ Health check passed"
else
    echo "   ✗ Health check failed"
    kill $HEALTH_PID 2>/dev/null || true
    exit 1
fi

# Test statistics endpoint
echo "   Testing /statistics endpoint..."
if curl -s http://localhost:5006/statistics | grep -q "total_services"; then
    echo "   ✓ Statistics endpoint works"
else
    echo "   ✗ Statistics endpoint failed"
    kill $HEALTH_PID 2>/dev/null || true
    exit 1
fi

# Stop service
kill $HEALTH_PID 2>/dev/null || true
echo "   ✓ Health Monitor tests passed"

echo ""
echo "2. Testing Self-Evolution Service..."
cd ../self-evolution

# Start the service in background
echo "   Starting self-evolution service..."
python main.py > /tmp/self-evolution.log 2>&1 &
EVOLUTION_PID=$!
sleep 3

# Test health endpoint
echo "   Testing /health endpoint..."
if curl -s http://localhost:5007/health | grep -q "healthy"; then
    echo "   ✓ Health check passed"
else
    echo "   ✗ Health check failed"
    kill $EVOLUTION_PID 2>/dev/null || true
    exit 1
fi

# Test collect usage endpoint
echo "   Testing /collect-usage endpoint..."
RESPONSE=$(curl -s -X POST http://localhost:5007/collect-usage \
    -H "Content-Type: application/json" \
    -d '{"service":"test","endpoint":"/test","response_time":1.5,"status_code":200}')
if echo "$RESPONSE" | grep -q "collected"; then
    echo "   ✓ Collect usage endpoint works"
else
    echo "   ✗ Collect usage endpoint failed"
    kill $EVOLUTION_PID 2>/dev/null || true
    exit 1
fi

# Test recommendations endpoint
echo "   Testing /recommendations endpoint..."
if curl -s http://localhost:5007/recommendations | grep -q "count"; then
    echo "   ✓ Recommendations endpoint works"
else
    echo "   ✗ Recommendations endpoint failed"
    kill $EVOLUTION_PID 2>/dev/null || true
    exit 1
fi

# Stop service
kill $EVOLUTION_PID 2>/dev/null || true
echo "   ✓ Self-Evolution tests passed"

echo ""
echo "========================================"
echo "✓ All integration tests passed!"
echo "========================================"
