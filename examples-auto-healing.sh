#!/bin/bash
# Example usage of auto-healing and self-evolution services

echo "========================================"
echo "Auto-Healing and Self-Evolution Demo"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${YELLOW}Starting services...${NC}"
echo "To run this demo, first start the services with:"
echo "  docker-compose up -d health-monitor self-evolution"
echo "OR in separate terminals:"
echo "  cd services/health-monitor && python main.py"
echo "  cd services/self-evolution && python main.py"
echo ""

# Health Monitor Examples
echo -e "${GREEN}=== Health Monitor Service (Port 5006) ===${NC}"
echo ""

echo "1. Check health of the monitor itself:"
echo "   curl http://localhost:5006/health"
echo ""

echo "2. Check health of all monitored services:"
echo "   curl http://localhost:5006/check-services"
echo ""

echo "3. Get health statistics:"
echo "   curl http://localhost:5006/statistics"
echo ""

echo "4. View error history for all services:"
echo "   curl http://localhost:5006/error-history"
echo ""

echo "5. View error history for specific service:"
echo "   curl http://localhost:5006/error-history?service=crypto-prediction"
echo ""

echo "6. Get recovery action history:"
echo "   curl http://localhost:5006/recovery-history"
echo ""

echo "7. Manually trigger healing for a service:"
echo "   curl -X POST http://localhost:5006/trigger-heal/image-generation"
echo ""

# Self-Evolution Examples
echo -e "${GREEN}=== Self-Evolution Service (Port 5007) ===${NC}"
echo ""

echo "1. Check health of self-evolution service:"
echo "   curl http://localhost:5007/health"
echo ""

echo "2. Collect usage data (simulate 100 requests):"
cat << 'USAGE_SCRIPT'
   for i in {1..100}; do
     curl -X POST http://localhost:5007/collect-usage \
       -H "Content-Type: application/json" \
       -d "{
         \"service\": \"crypto-prediction\",
         \"endpoint\": \"/predict\",
         \"response_time\": $((RANDOM % 5 + 1)),
         \"status_code\": $((RANDOM % 100 < 10 ? 500 : 200))
       }"
   done
USAGE_SCRIPT
echo ""

echo "3. Analyze patterns and generate recommendations:"
echo "   curl -X POST http://localhost:5007/analyze"
echo ""

echo "4. View all recommendations:"
echo "   curl http://localhost:5007/recommendations | jq"
echo ""

echo "5. View only pending recommendations:"
echo "   curl http://localhost:5007/recommendations?status=pending | jq"
echo ""

echo "6. Apply a specific optimization (replace ID):"
echo "   curl -X POST http://localhost:5007/apply-optimization/abc123def456"
echo ""

echo "7. View applied optimizations:"
echo "   curl http://localhost:5007/applied-optimizations | jq"
echo ""

echo "8. Rollback an optimization if needed:"
echo "   curl -X POST http://localhost:5007/rollback/abc123def456"
echo ""

echo "9. View rollback history:"
echo "   curl http://localhost:5007/rollback-history | jq"
echo ""

echo "10. View performance baselines:"
echo "   curl http://localhost:5007/performance-baselines | jq"
echo ""

# Monitoring with Kibana
echo -e "${GREEN}=== Kibana Monitoring ===${NC}"
echo ""
echo "Access Kibana dashboard:"
echo "   http://localhost:5601"
echo ""
echo "Create index patterns for:"
echo "   - health-monitor-errors"
echo "   - health-monitor-recovery"
echo "   - self-evolution-usage"
echo "   - self-evolution-optimizations"
echo ""

# Complete workflow example
echo -e "${GREEN}=== Complete Workflow Example ===${NC}"
echo ""
echo "Simulate a complete auto-healing and optimization workflow:"
echo ""

cat << 'WORKFLOW'
# Step 1: Collect usage data
for i in {1..50}; do
  curl -s -X POST http://localhost:5007/collect-usage \
    -H "Content-Type: application/json" \
    -d "{
      \"service\": \"image-generation\",
      \"endpoint\": \"/generate\",
      \"response_time\": 3.5,
      \"status_code\": 200
    }"
done

# Step 2: Trigger analysis
curl -X POST http://localhost:5007/analyze

# Step 3: Get recommendations
RECOMMENDATIONS=$(curl -s http://localhost:5007/recommendations?status=pending)
echo "$RECOMMENDATIONS" | jq

# Step 4: Get first recommendation ID
REC_ID=$(echo "$RECOMMENDATIONS" | jq -r '.recommendations[0].id')

# Step 5: Apply the optimization
if [ -n "$REC_ID" ]; then
  curl -X POST http://localhost:5007/apply-optimization/$REC_ID
fi

# Step 6: Check service health
curl http://localhost:5006/check-services | jq

# Step 7: Monitor in Kibana
echo "Check Kibana for detailed logs and visualizations"
WORKFLOW

echo ""
echo -e "${YELLOW}For more details, see AUTO_HEALING_EVOLUTION.md${NC}"
echo "========================================"
