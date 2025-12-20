# Quality Gates Guide

## Overview

Quality gates are automated checkpoints that monitor system health and control invite flow to maintain platform quality. They prevent runaway growth that could degrade user experience or introduce security risks.

## Purpose

Quality gates serve to:

1. **Protect Platform Quality**: Prevent overwhelming system capacity
2. **Detect Issues Early**: Identify problems before they escalate
3. **Maintain Trust**: Ensure consistent, high-quality user experience
4. **Control Growth**: Manage growth rate based on capacity
5. **Security**: Detect and prevent abuse patterns

## Monitored Metrics

### 1. Trust Score (0.0 - 1.0)

A composite metric reflecting overall system health:

```python
def calculate_trust_score(metrics):
    score = 1.0
    
    # Churn rate impact
    if churn_rate > 0.15:
        score -= (churn_rate - 0.15) * 2
    
    # Fraud rate impact
    if fraud_rate > 0.05:
        score -= (fraud_rate - 0.05) * 3
    
    # Engagement impact
    if engagement_rate < 0.5:
        score -= (0.5 - engagement_rate)
    
    return max(0.0, min(1.0, score))
```

**Interpretation:**
- 0.9 - 1.0: Excellent
- 0.8 - 0.9: Good
- 0.7 - 0.8: Warning
- < 0.7: Critical

### 2. Churn Rate

Percentage of users who stop using the platform:

```
churn_rate = inactive_users / total_users
```

**Thresholds:**
- < 0.10: Healthy
- 0.10 - 0.15: Warning
- 0.15 - 0.20: Critical
- > 0.20: Invites paused

### 3. Fraud Rate

Percentage of detected fraudulent activity:

```
fraud_rate = fraud_incidents / total_transactions
```

**Thresholds:**
- < 0.02: Healthy
- 0.02 - 0.05: Warning
- > 0.05: Critical

### 4. Engagement Rate

Percentage of active users:

```
engagement_rate = active_users / total_users
```

**Thresholds:**
- > 0.70: Excellent
- 0.50 - 0.70: Good
- 0.30 - 0.50: Warning
- < 0.30: Critical

### 5. System Load

Infrastructure utilization:

```
system_load = (cpu_usage + memory_usage + disk_io) / 3
```

**Thresholds:**
- < 60%: Normal
- 60% - 80%: Elevated
- 80% - 90%: High
- > 90%: Critical

## Gate Actions

### Automatic Responses

Based on metric thresholds, gates automatically:

#### 1. Normal Operation (Green)
- All invites proceed normally
- Standard processing times
- Full feature availability

#### 2. Warning State (Yellow)
- Alert administrators
- Increased monitoring frequency
- Slow down invite processing (50%)
- Log detailed metrics

#### 3. Critical State (Red)
- Pause all new invites
- Alert on-call team
- Intensive logging
- Emergency response protocols

## API Endpoints

### Get Trust Score

```bash
curl http://localhost:8000/api/quality/trust-score
```

Response:
```json
{
  "trust_score": 0.83,
  "churn_rate": 0.12,
  "fraud_rate": 0.02,
  "engagement_rate": 0.75,
  "invites_paused": false,
  "health_status": "healthy"
}
```

### Evaluate Gate

```bash
curl -X POST http://localhost:8000/api/quality/evaluate-gate
```

Response:
```json
{
  "invites_allowed": true,
  "trust_score": 0.83,
  "metrics": {
    "churn_rate": 0.12,
    "fraud_rate": 0.02,
    "engagement_rate": 0.75,
    "active_users": 1000,
    "new_signups_today": 25
  },
  "alerts": []
}
```

### Update Metrics (Admin Only)

```bash
curl -X POST http://localhost:8000/api/quality/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "churn_rate": 0.12,
    "fraud_rate": 0.02,
    "engagement_rate": 0.75
  }'
```

### Get Active Alerts

```bash
curl http://localhost:8000/api/quality/alerts
```

Response:
```json
{
  "alerts": [
    {
      "id": "2025-12-20T10:30:00",
      "severity": "warning",
      "message": "Churn rate exceeds warning threshold",
      "metric": "churn_rate",
      "value": 0.16,
      "threshold": 0.15,
      "timestamp": "2025-12-20T10:30:00Z"
    }
  ],
  "count": 1
}
```

## Alert System

### Alert Levels

#### Info
- Minor threshold breaches
- Non-urgent notifications
- Logged for analysis

#### Warning
- Important metrics trending wrong direction
- Admin notification
- Increased monitoring
- No immediate action required

#### Critical
- Severe threshold violations
- Immediate admin alert
- Automatic protective measures
- Requires urgent attention

### Alert Types

1. **Churn Rate Alerts**
   - Warning: > 0.15
   - Critical: > 0.20

2. **Trust Score Alerts**
   - Warning: < 0.80
   - Critical: < 0.70

3. **Fraud Rate Alerts**
   - Critical: > 0.05

4. **System Load Alerts**
   - Warning: > 80%
   - Critical: > 90%

5. **Engagement Alerts**
   - Warning: < 0.50
   - Critical: < 0.30

## Integration with Invite System

### Decision Flow

```
New Invite Request
    ↓
Evaluate Quality Gates
    ↓
Trust Score < 0.7? → YES → Pause Invite
    ↓ NO
Churn Rate > 0.2? → YES → Pause Invite
    ↓ NO
System Load > 90%? → YES → Pause Invite
    ↓ NO
Allow Invite
```

### Code Example

```python
async def should_allow_invite():
    response = await client.get('/api/quality/trust-score')
    data = response.json()
    
    if data['invites_paused']:
        return False, "Invites temporarily paused for quality control"
    
    if data['trust_score'] < 0.7:
        return False, "System trust score too low"
    
    return True, "Invite allowed"
```

## Monitoring & Dashboards

### Key Visualizations

1. **Trust Score Trend**
   - Line chart over time
   - Threshold markers
   - Alert annotations

2. **Metric Breakdown**
   - Gauges for each metric
   - Color-coded thresholds
   - Real-time updates

3. **Alert History**
   - Timeline of all alerts
   - Resolution tracking
   - Pattern analysis

4. **Invite Flow**
   - Approved vs paused
   - Processing rates
   - Backlog size

### Recommended Tools

- **Grafana**: For visualization
- **Prometheus**: For metrics collection
- **ELK Stack**: For log aggregation
- **PagerDuty**: For alert routing

## Configuration

### Environment Variables

```bash
# Threshold overrides
QUALITY_TRUST_THRESHOLD=0.7
QUALITY_CHURN_THRESHOLD=0.2
QUALITY_FRAUD_THRESHOLD=0.05

# Alert settings
ALERT_EMAIL=ops@vobee.ai
ALERT_WEBHOOK_URL=https://hooks.slack.com/...
ALERT_CHECK_INTERVAL=60
```

### Custom Thresholds

```python
# In quality-gates/monitor.py
custom_thresholds = {
    'trust_score': 0.75,  # Stricter than default
    'churn_rate': 0.15,   # More lenient
    'fraud_rate': 0.03    # Stricter
}
```

## Response Procedures

### When Invites Are Paused

1. **Immediate Actions**
   - Notify on-call engineer
   - Check infrastructure health
   - Review recent changes
   - Analyze metric trends

2. **Investigation**
   - Identify root cause
   - Check for attacks/abuse
   - Review error logs
   - Query database health

3. **Resolution**
   - Fix underlying issue
   - Verify metrics improving
   - Test system stability
   - Resume invites gradually

4. **Post-Mortem**
   - Document incident
   - Identify improvements
   - Update thresholds if needed
   - Share learnings

### Escalation Path

```
Alert Triggered
    ↓
On-Call Engineer (5 min)
    ↓ (if unresolved after 15 min)
Engineering Manager
    ↓ (if unresolved after 30 min)
VP Engineering / CTO
```

## Testing Quality Gates

### Simulation Mode

```bash
# Test critical thresholds
curl -X POST http://localhost:8000/api/quality/metrics \
  -d '{
    "churn_rate": 0.25,
    "fraud_rate": 0.10,
    "engagement_rate": 0.20
  }'

# Check if invites are paused
curl http://localhost:8000/api/quality/evaluate-gate
```

### Load Testing

```bash
# Simulate high load
for i in {1..1000}; do
  curl -X POST http://localhost:8000/api/quality/evaluate-gate &
done
wait
```

## Best Practices

### 1. Regular Monitoring
- Check dashboards daily
- Review trends weekly
- Adjust thresholds quarterly

### 2. Proactive Management
- Act on warnings before critical
- Trend analysis for predictions
- Capacity planning based on gates

### 3. Communication
- Alert relevant teams promptly
- Share metric trends in standups
- Include quality gates in planning

### 4. Continuous Improvement
- Review false positives
- Tune thresholds based on data
- Add new metrics as needed
- Document all changes

## Future Enhancements

1. **Machine Learning**: Predictive alerts before thresholds breach
2. **Auto-Scaling**: Automatic capacity adjustments
3. **Self-Healing**: Automatic remediation for common issues
4. **Advanced Analytics**: Deeper pattern recognition
5. **Multi-Region**: Geographic quality tracking
6. **A/B Testing**: Quality gates for experiments
7. **User Segmentation**: Different thresholds per segment

## Troubleshooting

### Common Issues

**False Positive Alerts:**
- Review threshold settings
- Check for data collection issues
- Verify metric calculations

**Missed Issues:**
- Thresholds too lenient
- Missing important metrics
- Alert notification failures

**Frequent Pauses:**
- Infrastructure undersized
- Growth too rapid
- Onboarding issues

## Support

For quality gate issues:
- Slack: #quality-gates
- Email: platform-ops@vobee.ai
- PagerDuty: Quality Gates rotation
- Documentation: /docs/quality-gates
