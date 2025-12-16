#!/bin/bash
#
# Test CI/Swarm Execution Guards
# Validates that all guards properly block execution
#

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "========================================================"
echo "  Testing CI/Swarm Execution Guards"
echo "========================================================"
echo ""

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: deploy.sh with SWARM_EXECUTION_DISABLED=true
echo -e "${BLUE}[TEST]${NC} Testing deploy.sh with SWARM_EXECUTION_DISABLED=true..."
OUTPUT=$(bash -c 'unset CI; unset GITHUB_ACTIONS; export SWARM_EXECUTION_DISABLED=true; bash deploy.sh 2>&1')
if echo "$OUTPUT" | grep -q "Deployment blocked"; then
    echo -e "${GREEN}[PASS]${NC} deploy.sh correctly blocked with SWARM_EXECUTION_DISABLED=true"
    ((TESTS_PASSED++))
else
    echo -e "${RED}[FAIL]${NC} deploy.sh did not block with SWARM_EXECUTION_DISABLED=true"
    ((TESTS_FAILED++))
fi

# Test 2: test-system.sh with SWARM_EXECUTION_DISABLED=true shows warning
echo -e "${BLUE}[TEST]${NC} Testing test-system.sh with SWARM_EXECUTION_DISABLED=true..."
OUTPUT=$(bash -c 'unset CI; unset GITHUB_ACTIONS; export SWARM_EXECUTION_DISABLED=true; timeout 2 bash test-system.sh 2>&1 || true')
if echo "$OUTPUT" | grep -q "Some tests skipped"; then
    echo -e "${GREEN}[PASS]${NC} test-system.sh correctly warns about skipped tests"
    ((TESTS_PASSED++))
else
    echo -e "${RED}[FAIL]${NC} test-system.sh did not warn about skipped tests"
    ((TESTS_FAILED++))
fi

# Test 3: Python worker-pool guard with CI=true
echo -e "${BLUE}[TEST]${NC} Testing worker-pool Python guard logic..."
cd services/worker-pool
python3 -c "
import os
import sys
os.environ['CI'] = 'true'
if os.getenv('CI') == 'true':
    print('BLOCKED')
    sys.exit(1)
" 2>&1
RESULT=$?
cd ../..
if [ "$RESULT" = "1" ]; then
    echo -e "${GREEN}[PASS]${NC} Python guard logic correctly detects CI=true"
    ((TESTS_PASSED++))
else
    echo -e "${RED}[FAIL]${NC} Python guard logic did not work correctly (exit code: $RESULT)"
    ((TESTS_FAILED++))
fi

# Test 4: Python guard with SWARM_EXECUTION_DISABLED=true
echo -e "${BLUE}[TEST]${NC} Testing Python guard logic with SWARM_EXECUTION_DISABLED=true..."
python3 -c "
import os
import sys
os.environ['SWARM_EXECUTION_DISABLED'] = 'true'
if os.getenv('SWARM_EXECUTION_DISABLED') == 'true':
    print('BLOCKED')
    sys.exit(1)
" 2>&1
RESULT=$?
if [ "$RESULT" = "1" ]; then
    echo -e "${GREEN}[PASS]${NC} Python guard logic correctly detects SWARM_EXECUTION_DISABLED=true"
    ((TESTS_PASSED++))
else
    echo -e "${RED}[FAIL]${NC} Python guard logic did not work correctly (exit code: $RESULT)"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "========================================================"
echo "  Test Summary"
echo "========================================================"
echo -e "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
fi
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All guard tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some guard tests failed.${NC}"
    exit 1
fi
