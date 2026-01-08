#!/bin/bash
#
# VoBee AI Assistant - System Integration Test
# Tests all components of the autonomous system
#

set -e

# CI/Swarm execution guard - fail fast for worker/bot tests
check_execution_guards() {
    if [ "$CI" = "true" ] || [ "$GITHUB_ACTIONS" = "true" ] || [ "$SWARM_EXECUTION_DISABLED" = "true" ]; then
        echo "⚠️  WARNING: Some tests skipped due to CI execution guards"
        if [ "$CI" = "true" ] || [ "$GITHUB_ACTIONS" = "true" ]; then
            echo "CI environment detected"
        fi
        if [ "$SWARM_EXECUTION_DISABLED" = "true" ]; then
            echo "Swarm execution disabled"
        fi
        echo "Worker pool and bot-triggering tests will be skipped"
        return 1
    fi
    return 0
}

# Store guard check result
GUARDS_ACTIVE=0
if ! check_execution_guards; then
    GUARDS_ACTIVE=1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Configuration
OWNER_SECRET="${OWNER_SECRET:-your_secure_owner_secret_key}"
TESTS_PASSED=0
TESTS_FAILED=0

echo ""
echo "========================================================"
echo "  VoBee AI Assistant - Integration Tests"
echo "========================================================"
echo ""

# Test 1: API Gateway Health
print_test "Testing API Gateway health..."
if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
    print_pass "API Gateway is healthy"
    ((TESTS_PASSED++))
else
    print_fail "API Gateway health check failed"
    ((TESTS_FAILED++))
fi

# Test 2: Supreme General Intelligence Health
print_test "Testing SGI service health..."
if curl -s -f http://localhost:5010/health > /dev/null 2>&1; then
    print_pass "SGI service is healthy"
    ((TESTS_PASSED++))
else
    print_fail "SGI service health check failed"
    ((TESTS_FAILED++))
fi

# Test 3: Spy-Orchestration Health
print_test "Testing Spy-Orchestration service health..."
if curl -s -f http://localhost:5006/health > /dev/null 2>&1; then
    print_pass "Spy-Orchestration service is healthy"
    ((TESTS_PASSED++))
else
    print_fail "Spy-Orchestration service health check failed"
    ((TESTS_FAILED++))
fi

# Test 4: Self-Healing Health
print_test "Testing Self-Healing service health..."
if curl -s -f http://localhost:5007/health > /dev/null 2>&1; then
    print_pass "Self-Healing service is healthy"
    ((TESTS_PASSED++))
else
    print_fail "Self-Healing service health check failed"
    ((TESTS_FAILED++))
fi

# Test 5: Worker Pool Health
print_test "Testing Worker Pool service health..."
if curl -s -f http://localhost:5008/health > /dev/null 2>&1; then
    print_pass "Worker Pool service is healthy"
    ((TESTS_PASSED++))
else
    print_fail "Worker Pool service health check failed"
    ((TESTS_FAILED++))
fi

# Test 6: System Health Summary
print_test "Testing system health summary..."
RESPONSE=$(curl -s http://localhost:5007/system/health)
if echo "$RESPONSE" | grep -q "total_services"; then
    print_pass "System health summary retrieved"
    echo "    System Status: $(echo $RESPONSE | grep -o '"overall_health":"[^"]*"' | cut -d'"' -f4)"
    ((TESTS_PASSED++))
else
    print_fail "System health summary failed"
    ((TESTS_FAILED++))
fi

# Test 7: SGI Chat (Intent Understanding)
print_test "Testing SGI chat interface..."
RESPONSE=$(curl -s -X POST http://localhost:5010/chat \
    -H "Content-Type: application/json" \
    -H "X-Owner-Secret: $OWNER_SECRET" \
    -d '{"message": "scan github for AI repositories"}' 2>&1)

if echo "$RESPONSE" | grep -q "intent"; then
    print_pass "SGI intent understanding works"
    echo "    Detected intent: $(echo $RESPONSE | grep -o '"type":"[^"]*"' | head -1 | cut -d'"' -f4)"
    ((TESTS_PASSED++))
else
    print_fail "SGI chat interface failed"
    echo "    Response: $RESPONSE"
    ((TESTS_FAILED++))
fi

# Test 8: Worker Pool Status
if [ $GUARDS_ACTIVE -eq 1 ]; then
    print_test "Skipping worker pool status test (guards active)..."
    echo "    Worker pool tests skipped in CI environment"
else
    print_test "Testing worker pool status..."
    RESPONSE=$(curl -s http://localhost:5008/pool/status)
    if echo "$RESPONSE" | grep -q "total_workers"; then
        print_pass "Worker pool status retrieved"
        echo "    Total workers: $(echo $RESPONSE | grep -o '"total_workers":[0-9]*' | cut -d':' -f2)"
        ((TESTS_PASSED++))
    else
        print_fail "Worker pool status failed"
        ((TESTS_FAILED++))
    fi
fi

# Test 9: Create Worker
if [ $GUARDS_ACTIVE -eq 1 ]; then
    print_test "Skipping worker creation test (guards active)..."
    echo "    Worker creation tests skipped in CI environment"
else
    print_test "Testing worker creation..."
    RESPONSE=$(curl -s -X POST http://localhost:5008/worker/create \
        -H "Content-Type: application/json" \
        -d '{"worker_type": "crawler"}')
    
    if echo "$RESPONSE" | grep -q "worker_id"; then
        print_pass "Worker created successfully"
        WORKER_ID=$(echo $RESPONSE | grep -o '"worker_id":"[^"]*"' | cut -d'"' -f4)
        echo "    Worker ID: $WORKER_ID"
        ((TESTS_PASSED++))
    else
        print_fail "Worker creation failed"
        ((TESTS_FAILED++))
    fi
fi

# Test 10: Execute Worker Task
if [ $GUARDS_ACTIVE -eq 1 ]; then
    print_test "Skipping worker task execution test (guards active)..."
    echo "    Worker task tests skipped in CI environment"
elif [ -n "$WORKER_ID" ]; then
    print_test "Testing worker task execution..."
    RESPONSE=$(curl -s -X POST http://localhost:5008/task/execute \
        -H "Content-Type: application/json" \
        -d '{"worker_type": "crawler", "task": {"url": "https://github.com", "depth": 1}}')
    
    if echo "$RESPONSE" | grep -q "status"; then
        print_pass "Worker task executed"
        ((TESTS_PASSED++))
    else
        print_fail "Worker task execution failed"
        ((TESTS_FAILED++))
    fi
fi

# Test 11: Spy Stats
print_test "Testing spy-orchestration statistics..."
RESPONSE=$(curl -s http://localhost:5006/stats)
if echo "$RESPONSE" | grep -q "total_discoveries"; then
    print_pass "Spy-orchestration stats retrieved"
    ((TESTS_PASSED++))
else
    print_fail "Spy-orchestration stats failed"
    ((TESTS_FAILED++))
fi

# Test 12: Orchestrator Health
print_test "Testing orchestrator service..."
RESPONSE=$(curl -s http://localhost:5003/health)
if echo "$RESPONSE" | grep -q "status"; then
    print_pass "Orchestrator is healthy"
    ((TESTS_PASSED++))
else
    print_fail "Orchestrator health check failed"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "========================================================"
echo "  Test Summary"
echo "========================================================"
echo -e "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Please check the services.${NC}"
    echo "Run 'docker compose logs -f' to see detailed logs."
    exit 1
fi
