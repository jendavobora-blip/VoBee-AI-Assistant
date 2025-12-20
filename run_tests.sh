#!/bin/bash
# Test runner for invite-only system

echo "======================================"
echo "Running Invite-Only System Tests"
echo "======================================"
echo ""

# Run all test files
echo "1. Testing Waitlist Scoring Algorithm..."
python -m unittest tests.test_waitlist_scoring 2>&1
RESULT1=$?

echo ""
echo "2. Testing Invite Code Generation..."
python -m unittest tests.test_invite_codes 2>&1
RESULT2=$?

echo ""
echo "3. Testing Referral Quality..."
python -m unittest tests.test_referral_quality 2>&1
RESULT3=$?

echo ""
echo "4. Testing Quality Gates..."
python -m unittest tests.test_quality_gates 2>&1
RESULT4=$?

echo ""
echo "======================================"
echo "Test Summary"
echo "======================================"

if [ $RESULT1 -eq 0 ]; then
    echo "✓ Waitlist Scoring: PASSED"
else
    echo "✗ Waitlist Scoring: FAILED"
fi

if [ $RESULT2 -eq 0 ]; then
    echo "✓ Invite Codes: PASSED"
else
    echo "✗ Invite Codes: FAILED"
fi

if [ $RESULT3 -eq 0 ]; then
    echo "✓ Referral Quality: PASSED"
else
    echo "✗ Referral Quality: FAILED"
fi

if [ $RESULT4 -eq 0 ]; then
    echo "✓ Quality Gates: PASSED"
else
    echo "✗ Quality Gates: FAILED"
fi

echo ""

# Exit with error if any test failed
if [ $RESULT1 -ne 0 ] || [ $RESULT2 -ne 0 ] || [ $RESULT3 -ne 0 ] || [ $RESULT4 -ne 0 ]; then
    echo "Some tests failed!"
    exit 1
else
    echo "All tests passed!"
    exit 0
fi
