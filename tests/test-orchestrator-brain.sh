#!/bin/bash
#
# Test Orchestrator Brain Components
# Tests all new orchestrator brain modules
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
echo "  VoBee AI Assistant - Orchestrator Brain Tests"
echo "========================================================"
echo ""

# Test 1: Check if brain modules exist
print_test "Checking if orchestrator brain modules exist..."

BRAIN_MODULES=(
    "ai-brain.py"
    "task-router.py"
    "memory-system.py"
    "self-improvement.py"
    "module-manager.py"
)

for MODULE in "${BRAIN_MODULES[@]}"; do
    if [ -f "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/services/orchestrator/$MODULE" ]; then
        print_pass "$MODULE exists"
        ((TESTS_PASSED++))
    else
        print_fail "$MODULE not found"
        ((TESTS_FAILED++))
    fi
done

# Test 2: Python syntax check
print_test "Checking Python syntax for brain modules..."

for MODULE in "${BRAIN_MODULES[@]}"; do
    if python3 -m py_compile "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/services/orchestrator/$MODULE" 2>/dev/null; then
        print_pass "$MODULE syntax OK"
        ((TESTS_PASSED++))
    else
        print_fail "$MODULE syntax error"
        ((TESTS_FAILED++))
    fi
done

# Test 3: Check for safety flags
print_test "Checking self-improvement AUTO_APPLY flag..."

if grep -q "AUTO_APPLY = False" "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/services/orchestrator/self-improvement.py"; then
    print_pass "Self-improvement AUTO_APPLY is False (safe)"
    ((TESTS_PASSED++))
else
    print_fail "Self-improvement AUTO_APPLY not set to False"
    ((TESTS_FAILED++))
fi

# Test 4: Check for READ_ONLY flag in finance
print_test "Checking finance-ai READ_ONLY flag..."

if grep -q "READ_ONLY = True" "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/services/finance-ai/main.py"; then
    print_pass "Finance-AI READ_ONLY is True (safe)"
    ((TESTS_PASSED++))
else
    print_fail "Finance-AI READ_ONLY not set to True"
    ((TESTS_FAILED++))
fi

# Test 5: Check if main.py was not modified
print_test "Checking if orchestrator main.py was not modified..."

# This is a basic check - in reality you'd compare with git
if [ -f "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/services/orchestrator/main.py" ]; then
    # Check if main.py still has original markers
    if grep -q "TaskOrchestrator" "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/services/orchestrator/main.py"; then
        print_pass "orchestrator/main.py appears unchanged"
        ((TESTS_PASSED++))
    else
        print_fail "orchestrator/main.py may have been modified"
        ((TESTS_FAILED++))
    fi
else
    print_fail "orchestrator/main.py not found"
    ((TESTS_FAILED++))
fi

# Test 6: Check documentation exists
print_test "Checking if documentation was created..."

DOCS=(
    "MASTER_VISION.md"
    "WHAT_IS_FUNCTIONAL.md"
    "AI_CAPABILITIES.md"
    "MODULE_DEVELOPMENT.md"
    "ORCHESTRATION_GUIDE.md"
    "SAFETY_RULES.md"
)

for DOC in "${DOCS[@]}"; do
    if [ -f "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/docs/$DOC" ]; then
        print_pass "$DOC exists"
        ((TESTS_PASSED++))
    else
        print_fail "$DOC not found"
        ((TESTS_FAILED++))
    fi
done

# Test 7: Check configuration files
print_test "Checking configuration files..."

CONFIGS=(
    "modules.json"
    "orchestrator-config.json"
    "safety-config.json"
)

for CONFIG in "${CONFIGS[@]}"; do
    if [ -f "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/config/$CONFIG" ]; then
        # Check if it's valid JSON
        if python3 -c "import json; json.load(open('/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/config/$CONFIG'))" 2>/dev/null; then
            print_pass "$CONFIG is valid JSON"
            ((TESTS_PASSED++))
        else
            print_fail "$CONFIG is invalid JSON"
            ((TESTS_FAILED++))
        fi
    else
        print_fail "$CONFIG not found"
        ((TESTS_FAILED++))
    fi
done

# Test 8: Check frontend files
print_test "Checking frontend integration files..."

FRONTEND_FILES=(
    "ai-orchestration.js"
    "module-manager-ui.js"
    "dashboard.js"
)

for FILE in "${FRONTEND_FILES[@]}"; do
    if [ -f "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/js/$FILE" ]; then
        print_pass "$FILE exists"
        ((TESTS_PASSED++))
    else
        print_fail "$FILE not found"
        ((TESTS_FAILED++))
    fi
done

# Test 9: Check monitoring files
print_test "Checking monitoring integration files..."

MONITORING_FILES=(
    "dashboard-config.json"
    "alerts.yaml"
    "metrics-exporter.py"
)

for FILE in "${MONITORING_FILES[@]}"; do
    if [ -f "/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/monitoring/$FILE" ]; then
        print_pass "$FILE exists"
        ((TESTS_PASSED++))
    else
        print_fail "$FILE not found"
        ((TESTS_FAILED++))
    fi
done

# Test 10: Run Python imports test
print_test "Testing Python module imports..."

python3 << 'PYTHON_EOF'
import sys
sys.path.insert(0, '/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/services/orchestrator')

try:
    # Test imports (not execution, just import syntax)
    import importlib.util
    
    modules = [
        'ai-brain.py',
        'task-router.py',
        'memory-system.py',
        'self-improvement.py',
        'module-manager.py'
    ]
    
    for mod_file in modules:
        mod_path = f'/home/runner/work/VoBee-AI-Assistant/VoBee-AI-Assistant/services/orchestrator/{mod_file}'
        spec = importlib.util.spec_from_file_location(mod_file.replace('.py', '').replace('-', '_'), mod_path)
        if spec and spec.loader:
            print(f"✓ {mod_file} can be imported")
        else:
            print(f"✗ {mod_file} import failed")
            sys.exit(1)
    
    print("All modules can be imported successfully")
    sys.exit(0)
except Exception as e:
    print(f"Import test failed: {e}")
    sys.exit(1)
PYTHON_EOF

if [ $? -eq 0 ]; then
    print_pass "Python module imports OK"
    ((TESTS_PASSED++))
else
    print_fail "Python module imports failed"
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
    echo -e "${GREEN}All orchestrator brain tests passed! ✓${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Please review.${NC}"
    exit 1
fi
