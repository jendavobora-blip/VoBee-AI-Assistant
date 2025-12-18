#!/bin/bash
#
# Quick Start Script for VOBee Testing Framework
# 
# This script helps you get started with testing quickly
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "========================================================================"
echo "  VOBee Testing Framework - Quick Start"
echo "========================================================================"
echo ""

# Check if dependencies are installed
echo -e "${BLUE}Checking dependencies...${NC}"

if ! python -c "import aiohttp, requests, psutil" 2>/dev/null; then
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Check if services are running
echo ""
echo -e "${BLUE}Checking if services are running...${NC}"

SERVICES_UP=0
for port in 5010 5011 5012 5013 5020 5030 5040 5050; do
    if curl -s -f http://localhost:$port/health > /dev/null 2>&1; then
        ((SERVICES_UP++))
    fi
done

echo -e "${GREEN}✓ $SERVICES_UP/8 services are running${NC}"

if [ $SERVICES_UP -eq 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  No services are running!${NC}"
    echo ""
    echo "To start services, run:"
    echo "  docker compose up -d"
    echo ""
    echo "Or to see what tests do when services are down:"
    echo "  python tests/run_all_tests.py quick"
    echo ""
    exit 1
fi

# Ask user what test to run
echo ""
echo "What would you like to test?"
echo ""
echo "  1) Quick smoke test (30 seconds)"
echo "  2) Functional tests (all endpoints)"
echo "  3) Load test (300 users, ~5 minutes)"
echo "  4) Stress test (5000 operations)"
echo "  5) Integration tests"
echo "  6) All tests (10-15 minutes)"
echo "  7) Exit"
echo ""
read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Running quick smoke test...${NC}"
        python tests/run_all_tests.py quick
        ;;
    2)
        echo ""
        echo -e "${BLUE}Running functional tests...${NC}"
        python tests/run_all_tests.py functional
        ;;
    3)
        echo ""
        echo -e "${BLUE}Running load test (this will take ~5 minutes)...${NC}"
        python tests/run_all_tests.py load
        ;;
    4)
        echo ""
        echo -e "${BLUE}Running stress test...${NC}"
        python tests/run_all_tests.py stress
        ;;
    5)
        echo ""
        echo -e "${BLUE}Running integration tests...${NC}"
        python tests/run_all_tests.py integration
        ;;
    6)
        echo ""
        echo -e "${BLUE}Running all tests (this will take 10-15 minutes)...${NC}"
        python tests/run_all_tests.py all --report
        ;;
    7)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

# Show results
echo ""
echo "========================================================================"
echo "  Test Results"
echo "========================================================================"
echo ""

if [ -f test_results/summary.json ]; then
    echo "Summary saved to: test_results/summary.json"
fi

if [ -f test_results/functional_test_report.html ]; then
    echo "HTML report: test_results/functional_test_report.html"
fi

if [ -f test_results/load_test_report.html ]; then
    echo "Load test report: test_results/load_test_report.html"
fi

if [ -f test_results/stress_test_report.html ]; then
    echo "Stress test report: test_results/stress_test_report.html"
fi

if [ -f test_results/integration_test_report.html ]; then
    echo "Integration test report: test_results/integration_test_report.html"
fi

echo ""
echo "To view HTML reports, open them in your browser:"
echo "  open test_results/*.html"
echo ""
echo "For more options, see: tests/README.md"
echo ""
