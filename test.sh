#!/bin/bash

# Vobio AI Studio - E2E Test Script
# Tests all critical functionality

set -e

echo "=========================================="
echo "  Vobio AI Studio - E2E Tests"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
API_URL="http://localhost:8000"
LANGFUSE_URL="http://localhost:3000"
QDRANT_URL="http://localhost:6333"

TEST_USER_ID="test-user-$(date +%s)"
PASSED=0
FAILED=0

# Helper function for tests
run_test() {
    local test_name="$1"
    local command="$2"
    
    echo -n "Testing: $test_name... "
    
    if eval "$command" &> /dev/null; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((FAILED++))
        return 1
    fi
}

# Wait for services
echo "Waiting for services to be ready..."
sleep 15

echo ""
echo "Running tests..."
echo ""

# Test 1: API Health
run_test "API Health Check" \
    "curl -f -s $API_URL/health"

# Test 2: Qdrant Health
run_test "Qdrant Health Check" \
    "curl -f -s $QDRANT_URL/health"

# Test 3: Langfuse Health
run_test "Langfuse Health Check" \
    "curl -f -s $LANGFUSE_URL/api/health"

# Test 4: Feature Flags
run_test "Feature Flags Endpoint" \
    "curl -f -s $API_URL/api/features"

# Test 5: Login (Mock)
run_test "Mock Passkey Login" \
    "curl -f -s -X POST $API_URL/api/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"test_user\"}'"

# Test 6: Chat
run_test "Chat Endpoint" \
    "curl -f -s -X POST $API_URL/api/chat -H 'Content-Type: application/json' -H 'X-User-ID: $TEST_USER_ID' -d '{\"message\":\"Hello\"}'"

# Test 7: Image Generation
run_test "Image Generation" \
    "curl -f -s -X POST $API_URL/api/generate/image -H 'Content-Type: application/json' -H 'X-User-ID: $TEST_USER_ID' -d '{\"prompt\":\"test image\"}'"

# Test 8: Video Generation
run_test "Video Generation" \
    "curl -f -s -X POST $API_URL/api/generate/video -H 'Content-Type: application/json' -H 'X-User-ID: $TEST_USER_ID' -d '{\"prompt\":\"test video\"}'"

# Test 9: LifeSync Decision
run_test "LifeSync Decision Assistant" \
    "curl -f -s -X POST $API_URL/api/lifesync/decision -H 'Content-Type: application/json' -H 'X-User-ID: $TEST_USER_ID' -d '{\"scenario\":\"test\",\"options\":[\"A\",\"B\"]}'"

# Test 10: Code Validation
run_test "Code Safety Validation" \
    "curl -f -s -X POST $API_URL/api/safety/validate-code -H 'Content-Type: application/json' -H 'X-User-ID: $TEST_USER_ID' -d '{\"code\":\"print(\\\"hello\\\")\"}'"

# Test 11: Cost Tracking
run_test "Cost Usage Endpoint" \
    "curl -f -s $API_URL/api/costs/usage -H 'X-User-ID: $TEST_USER_ID'"

# Test 12: Memory Context
run_test "Memory Context Retrieval" \
    "curl -f -s $API_URL/api/memory/context -H 'X-User-ID: $TEST_USER_ID'"

# Test 13: Pending Approvals
run_test "Approval Queue" \
    "curl -f -s $API_URL/api/approvals/pending -H 'X-User-ID: $TEST_USER_ID'"

echo ""
echo "=========================================="
echo "  Test Results"
echo "=========================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    echo ""
    echo "Check logs:"
    echo "  docker-compose -f vobio-ai-studio/docker-compose.yml logs vobio-api"
    echo ""
    exit 1
fi
