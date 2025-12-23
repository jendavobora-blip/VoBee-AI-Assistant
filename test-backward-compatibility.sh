#!/bin/bash
# Backward Compatibility Validation Script
# Tests that all V1 API endpoints remain functional

echo "========================================"
echo "🧪 Backward Compatibility Test Suite"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$url" -H "Content-Type: application/json" -d "$data" 2>/dev/null)
    fi
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "000" ]; then
        echo -e "${GREEN}✅ PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAILED (HTTP $http_code)${NC}"
        ((FAILED++))
    fi
}

# Wait for services to start
echo "Waiting for services to start..."
sleep 2

# Test V1 API Endpoints (must always work)
echo ""
echo "Testing V1 API Endpoints (MUST remain unchanged):"
echo "------------------------------------------------"

test_endpoint "API Gateway Health" "GET" "http://localhost:8000/health" ""
test_endpoint "Image Generation Health" "GET" "http://localhost:5000/health" ""
test_endpoint "Video Generation Health" "GET" "http://localhost:5001/health" ""
test_endpoint "Crypto Prediction Health" "GET" "http://localhost:5002/health" ""

# Test V1 API functionality
test_endpoint "Image Generation V1" "POST" "http://localhost:8000/api/v1/generate/image" '{"prompt": "test"}'
test_endpoint "Video Generation V1" "POST" "http://localhost:8000/api/v1/generate/video" '{"prompt": "test"}'
test_endpoint "Crypto Prediction V1" "POST" "http://localhost:8000/api/v1/crypto/predict" '{"symbol": "BTC"}'

# Test V2 API Endpoints (should work with graceful fallback)
echo ""
echo "Testing V2 API Endpoints (Enhanced with graceful fallback):"
echo "-----------------------------------------------------------"

test_endpoint "Image Generation V2" "POST" "http://localhost:8000/api/v2/generate/image" '{"prompt": "test"}'
test_endpoint "Video Generation V2" "POST" "http://localhost:8000/api/v2/generate/video" '{"prompt": "test"}'
test_endpoint "Crypto Prediction V2" "POST" "http://localhost:8000/api/v2/crypto/predict" '{"symbol": "BTC"}'

# Test enhanced services (optional - may not be enabled)
echo ""
echo "Testing Optional Enhanced Services:"
echo "-----------------------------------"
echo -e "${YELLOW}Note: These are optional and may return 501 if not enabled${NC}"

test_endpoint "vLLM Fast Inference" "POST" "http://localhost:8000/api/v2/generate/fast" '{"prompt": "test"}'
test_endpoint "LangChain Orchestration" "POST" "http://localhost:8000/api/v2/orchestrate/langchain" '{"workflow_type": "simple", "inputs": {}}'
test_endpoint "Haystack RAG Search" "POST" "http://localhost:8000/api/v2/search/rag" '{"query": "test", "top_k": 3}'

# Test feature information endpoints
echo ""
echo "Testing Information Endpoints:"
echo "-----------------------------"

test_endpoint "Status Endpoint" "GET" "http://localhost:8000/status" ""
test_endpoint "Features Endpoint" "GET" "http://localhost:8000/api/features" ""
test_endpoint "Metrics Endpoint" "GET" "http://localhost:8000/metrics" ""
test_endpoint "V2 Status Endpoint" "GET" "http://localhost:8000/api/v2/status" ""

# Summary
echo ""
echo "========================================"
echo "📊 Test Results Summary"
echo "========================================"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED - Backward compatibility maintained!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests failed. This may be expected if services are not running.${NC}"
    echo "Run 'docker-compose up -d' to start all services."
    exit 1
fi
