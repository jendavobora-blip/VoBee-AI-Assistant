# Auto-Healing and Self-Evolution System

## Overview

The VoBee AI Assistant now includes an advanced auto-healing and self-evolution system that automatically monitors service health, recovers from failures, and optimizes performance based on usage patterns.

## Components

### 1. Health Monitor Service (Port 5006)

The Health Monitor continuously monitors all services in the system and automatically triggers recovery mechanisms when failures are detected.

#### Features

- **Continuous Health Monitoring**: Checks all services every 30 seconds (configurable)
- **Failure Detection**: Tracks consecutive failures and triggers auto-healing after threshold
- **Auto-Healing Recovery**: Automatically restarts failed services and updates configurations
- **Comprehensive Logging**: All actions logged to ElasticSearch for full traceability
- **Service Statistics**: Real-time statistics on service health and availability

#### Configuration

Environment variables:
- `HEALTH_CHECK_INTERVAL`: Interval between health checks in seconds (default: 30)
- `MAX_FAILURES_BEFORE_RECOVERY`: Number of failures before triggering recovery (default: 3)
- `RECOVERY_TIMEOUT`: Minimum time between recovery attempts in seconds (default: 60)
- `ELASTICSEARCH_ENABLED`: Enable logging to ElasticSearch (default: true)
- `ELASTICSEARCH_URL`: ElasticSearch connection URL (default: http://elasticsearch:9200)

#### API Endpoints

- `GET /health` - Health check for the monitor itself
- `GET /check-services` - Check health of all monitored services
- `GET /service-status` - Get current status of all services
- `GET /statistics` - Get health statistics
- `GET /error-history?service=<name>` - Get error history for a service or all services
- `GET /recovery-history` - Get recovery action history
- `POST /trigger-heal/<service_name>` - Manually trigger healing for a specific service

#### Example Usage

```bash
# Check all services
curl http://localhost:5006/check-services

# Get statistics
curl http://localhost:5006/statistics

# Get error history for a specific service
curl http://localhost:5006/error-history?service=crypto-prediction

# Manually trigger healing
curl -X POST http://localhost:5006/trigger-heal/image-generation
```

### 2. Self-Evolution Service (Port 5007)

The Self-Evolution service analyzes usage patterns, identifies performance bottlenecks, and automatically optimizes the system.

#### Features

- **Usage Pattern Analysis**: Collects and analyzes service usage data
- **Inefficiency Detection**: Identifies slow responses, high error rates, and traffic patterns
- **Optimization Recommendations**: Generates actionable optimization suggestions
- **Auto-Apply Optimizations**: Can automatically apply optimizations (disabled by default)
- **Performance Baselines**: Captures performance metrics before optimizations
- **Rollback Capability**: Can rollback problematic optimizations to baseline
- **Comprehensive Logging**: All optimizations logged to ElasticSearch

#### Configuration

Environment variables:
- `ANALYSIS_WINDOW_HOURS`: Time window for pattern analysis (default: 24)
- `OPTIMIZATION_THRESHOLD`: Minimum improvement threshold for recommendations (default: 0.15)
- `AUTO_APPLY_OPTIMIZATIONS`: Auto-apply high-priority optimizations (default: false)
- `ELASTICSEARCH_ENABLED`: Enable logging to ElasticSearch (default: true)
- `ELASTICSEARCH_URL`: ElasticSearch connection URL (default: http://elasticsearch:9200)

#### API Endpoints

- `GET /health` - Health check for the service
- `POST /collect-usage` - Collect usage data for analysis
  ```json
  {
    "service": "image-generation",
    "endpoint": "/generate",
    "response_time": 2.5,
    "status_code": 200
  }
  ```
- `POST /analyze` - Analyze patterns and generate recommendations
- `GET /recommendations?status=<pending|applied|rolled_back>` - Get recommendations
- `POST /apply-optimization/<recommendation_id>` - Apply a specific optimization
- `POST /rollback/<recommendation_id>` - Rollback an optimization
- `GET /applied-optimizations` - Get history of applied optimizations
- `GET /rollback-history` - Get rollback history
- `GET /performance-baselines` - Get performance baselines

#### Example Usage

```bash
# Collect usage data
curl -X POST http://localhost:5007/collect-usage \
  -H "Content-Type: application/json" \
  -d '{
    "service": "crypto-prediction",
    "endpoint": "/predict",
    "response_time": 3.2,
    "status_code": 200
  }'

# Trigger analysis
curl -X POST http://localhost:5007/analyze

# Get pending recommendations
curl http://localhost:5007/recommendations?status=pending

# Apply an optimization
curl -X POST http://localhost:5007/apply-optimization/abc123def456

# Rollback if needed
curl -X POST http://localhost:5007/rollback/abc123def456
```

### 3. Background Daemons

Both services include background daemons for continuous operation:

#### Health Monitor Daemon
- Continuously monitors service health
- Runs in the background alongside the Flask API
- Configurable check interval

#### Self-Evolution Daemon
- Periodically analyzes usage patterns
- Generates optimization recommendations
- Can auto-apply high-priority optimizations

## Deployment

### Docker Compose

The new services are included in the main `docker-compose.yml`:

```bash
# Start all services including auto-healing and self-evolution
docker-compose up -d

# View logs
docker-compose logs -f health-monitor
docker-compose logs -f self-evolution

# Check service status
curl http://localhost:5006/service-status
curl http://localhost:5007/recommendations
```

### Kubernetes

Deploy the new services to Kubernetes:

```bash
# Deploy auto-healing and self-evolution services
kubectl apply -f kubernetes/04-auto-healing-evolution.yaml

# Check deployment
kubectl get pods -n ai-orchestration | grep -E 'health-monitor|self-evolution'

# View logs
kubectl logs -f -n ai-orchestration deployment/health-monitor
kubectl logs -f -n ai-orchestration deployment/self-evolution

# Access services
kubectl port-forward -n ai-orchestration service/health-monitor-service 5006:5006
kubectl port-forward -n ai-orchestration service/self-evolution-service 5007:5007
```

## Monitoring and Logging

### ElasticSearch Indices

The system creates the following indices in ElasticSearch:

1. **health-monitor-errors**: Service error logs
2. **health-monitor-recovery**: Auto-healing actions
3. **self-evolution-usage**: Usage pattern data
4. **self-evolution-optimizations**: Applied optimizations

### Kibana Dashboards

Access Kibana at `http://localhost:5601` to view:
- Service health trends
- Recovery actions over time
- Applied optimizations
- Performance improvements

Create visualizations for:
- Service uptime percentage
- Mean time to recovery (MTTR)
- Number of auto-healing actions
- Optimization impact metrics

## Safety Mechanisms

### Auto-Healing Safety

1. **Failure Threshold**: Requires multiple consecutive failures before triggering recovery
2. **Recovery Timeout**: Prevents rapid repeated recovery attempts
3. **Comprehensive Logging**: All actions logged for audit trail
4. **Manual Override**: Supports manual triggering of recovery actions

### Self-Evolution Safety

1. **Manual Approval**: Auto-apply disabled by default, requires explicit enabling
2. **Performance Baselines**: Captures metrics before any optimization
3. **Rollback Capability**: Can revert to baseline if optimization causes issues
4. **Priority-Based Application**: Only high-priority optimizations auto-applied
5. **Improvement Threshold**: Only applies optimizations with estimated significant impact

## Testing

### Testing Auto-Healing

```bash
# Simulate a service failure by stopping a service
docker-compose stop crypto-prediction

# Monitor the health monitor logs
docker-compose logs -f health-monitor

# The health monitor will detect the failure and log recovery actions
# Check the error history
curl http://localhost:5006/error-history?service=crypto-prediction

# Restart the service
docker-compose start crypto-prediction
```

### Testing Self-Evolution

```bash
# Generate some usage data
for i in {1..100}; do
  curl -X POST http://localhost:5007/collect-usage \
    -H "Content-Type: application/json" \
    -d "{
      \"service\": \"test-service\",
      \"endpoint\": \"/test\",
      \"response_time\": $((RANDOM % 5 + 1)),
      \"status_code\": 200
    }"
done

# Trigger analysis
curl -X POST http://localhost:5007/analyze

# View recommendations
curl http://localhost:5007/recommendations | jq
```

## Best Practices

1. **Start Conservative**: Keep auto-apply disabled initially
2. **Monitor Regularly**: Review Kibana dashboards daily
3. **Test Rollbacks**: Periodically test rollback functionality
4. **Adjust Thresholds**: Tune thresholds based on your workload
5. **Review Recommendations**: Manually review before enabling auto-apply
6. **Maintain Baselines**: Keep performance baseline data for comparison
7. **Document Changes**: Log all manual interventions

## Troubleshooting

### Health Monitor Issues

**Services not being monitored:**
- Check service URLs in environment variables
- Verify network connectivity between services
- Check ElasticSearch connectivity

**Recovery not triggering:**
- Verify `MAX_FAILURES_BEFORE_RECOVERY` threshold
- Check `RECOVERY_TIMEOUT` setting
- Review logs for error messages

### Self-Evolution Issues

**No recommendations generated:**
- Ensure sufficient usage data collected
- Check analysis window configuration
- Verify optimization threshold settings

**Optimizations not applying:**
- Confirm auto-apply is enabled if desired
- Check recommendation priority levels
- Review logs for application errors

## Integration with Existing Services

The auto-healing and self-evolution services integrate seamlessly with existing services:

- **API Gateway**: Can collect usage metrics and forward to self-evolution
- **Orchestrator**: Can be monitored and auto-healed
- **ElasticSearch/Kibana**: Used for all logging and visualization
- **Auto-Scaler**: Can be triggered by self-evolution recommendations

## Security Considerations

1. **Access Control**: Restrict access to admin endpoints
2. **Secrets Management**: Use Kubernetes secrets for sensitive data
3. **Audit Logging**: All actions logged to ElasticSearch
4. **Rate Limiting**: Prevent abuse of manual trigger endpoints
5. **Validation**: Input validation on all API endpoints

## Future Enhancements

Planned improvements:
- Machine learning models for failure prediction
- Advanced anomaly detection
- Multi-region support
- Integration with external monitoring tools
- Automated A/B testing for optimizations
- Cost optimization recommendations
- Predictive scaling based on patterns

## License

MIT License - See main repository LICENSE file
