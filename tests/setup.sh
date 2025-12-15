#!/bin/bash
# Quick start script for VoBee AI Assistant QA Testing

set -e

echo "================================="
echo "VoBee AI Assistant - QA Test Setup"
echo "================================="
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the tests/ directory"
    exit 1
fi

echo "Step 1: Installing test dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

echo "Step 2: Validating test framework..."
python -c "
from utils.test_utils import TestMetrics, ResourceMonitor
print('✓ Test utilities validated')
"
echo ""

echo "Step 3: Listing available tests..."
python run_tests.py --list
echo ""

echo "================================="
echo "Setup Complete! 🎉"
echo "================================="
echo ""
echo "Next Steps:"
echo "  1. Ensure services are running: docker-compose up -d"
echo "  2. Run quick validation: python run_tests.py quick"
echo "  3. Run demo: python demo.py"
echo "  4. Run full tests: python run_tests.py all"
echo ""
echo "For more information, see README.md"
echo "================================="
