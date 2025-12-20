#!/bin/bash
#
# Test New AI Modules
# Tests all 30+ newly added AI modules
#

set -e

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

TESTS_PASSED=0
TESTS_FAILED=0

echo ""
echo "========================================================"
echo "  VoBee AI Assistant - New Modules Tests"
echo "========================================================"
echo ""

# Array of all new modules
MODULES=(
    "email-ai:5100"
    "facebook-ai:5101"
    "marketing-ai:5102"
    "seo-ai:5103"
    "content-ai:5104"
    "analytics-ai:5105"
    "finance-ai:5110"
    "invoice-ai:5111"
    "budget-ai:5112"
    "tax-ai:5113"
    "cashflow-ai:5114"
    "research-ai:5120"
    "web-scraper-ai:5121"
    "data-mining-ai:5122"
    "sentiment-ai:5123"
    "trend-ai:5124"
    "email-response-ai:5130"
    "chat-support-ai:5131"
    "translation-ai:5132"
    "voice-ai:5133"
    "meeting-ai:5134"
    "music-ai:5140"
    "design-ai:5141"
    "animation-ai:5142"
    "presentation-ai:5143"
    "podcast-ai:5144"
    "code-review-ai:5150"
    "documentation-ai:5151"
    "testing-ai:5152"
    "deployment-ai:5153"
)

# Test each module
for MODULE_PORT in "${MODULES[@]}"; do
    IFS=':' read -r MODULE PORT <<< "$MODULE_PORT"
    
    print_test "Testing $MODULE health endpoint..."
    
    # Try to connect (service might not be running, which is OK for this test)
    if curl -s -f "http://localhost:$PORT/health" > /dev/null 2>&1; then
        RESPONSE=$(curl -s "http://localhost:$PORT/health")
        
        # Check if response contains expected fields
        if echo "$RESPONSE" | grep -q "status.*healthy" && echo "$RESPONSE" | grep -q "service.*$MODULE"; then
            print_pass "$MODULE health check OK"
            ((TESTS_PASSED++))
        else
            print_fail "$MODULE health check returned invalid response"
            ((TESTS_FAILED++))
        fi
    else
        print_fail "$MODULE not reachable (service may not be running)"
        ((TESTS_FAILED++))
    fi
done

# Test Finance AI READ-ONLY mode
print_test "Testing Finance AI READ-ONLY mode..."
if curl -s -f "http://localhost:5110/status" > /dev/null 2>&1; then
    RESPONSE=$(curl -s "http://localhost:5110/status")
    if echo "$RESPONSE" | grep -q "READ_ONLY"; then
        print_pass "Finance AI is in READ-ONLY mode"
        ((TESTS_PASSED++))
    else
        print_fail "Finance AI READ-ONLY mode not confirmed"
        ((TESTS_FAILED++))
    fi
else
    print_fail "Finance AI not reachable"
    ((TESTS_FAILED++))
fi

# Test module process endpoints
print_test "Testing email-ai process endpoint..."
if curl -s -f "http://localhost:5100/process" -X POST -H "Content-Type: application/json" -d '{"action":"test"}' > /dev/null 2>&1; then
    print_pass "email-ai process endpoint OK"
    ((TESTS_PASSED++))
else
    print_fail "email-ai process endpoint failed"
    ((TESTS_FAILED++))
fi

# Test module status endpoints
print_test "Testing content-ai status endpoint..."
if curl -s -f "http://localhost:5104/status" > /dev/null 2>&1; then
    RESPONSE=$(curl -s "http://localhost:5104/status")
    if echo "$RESPONSE" | grep -q "active"; then
        print_pass "content-ai status endpoint OK"
        ((TESTS_PASSED++))
    else
        print_fail "content-ai status endpoint invalid response"
        ((TESTS_FAILED++))
    fi
else
    print_fail "content-ai status endpoint failed"
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
    echo -e "${GREEN}All new module tests passed! ✓${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Services may not be running yet.${NC}"
    echo "This is expected if services haven't been deployed."
    echo "Run 'docker-compose up -d' to start all services."
    exit 1
fi
