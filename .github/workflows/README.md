# Super Swarm Workflow Documentation

## Overview

The **Super Swarm** workflow is a high-performance GitHub Actions workflow designed to manage and deploy 20,000 virtual bots for the VoBee AI Assistant repository. This workflow optimizes operations, manages extensive workloads, and improves reliability through auto-scaling infrastructure.

## Workflow File

- **Location**: `.github/workflows/super-swarm.yml`
- **Name**: Super Swarm - High Performance Virtual Bots

## Features

### 1. Automated Triggers

- **Scheduled Execution**: Runs automatically every 5 minutes using cron schedule (`*/5 * * * *`)
- **Manual Trigger**: Can be triggered manually via `workflow_dispatch` with customizable parameters:
  - `bot_count`: Number of bots to deploy (default: 20,000)
  - `deployment_mode`: Deployment mode (auto-scale, fixed, or test)

### 2. Bot Capabilities

The deployed bots provide:
- ✅ Compute resources for large data operations
- ✅ Massive user interaction simulations
- ✅ Auto-scale infrastructure with zero downtime
- ✅ Distributed workload management
- ✅ Centralized logging and monitoring

### 3. Architecture

#### Multi-Job Workflow

1. **Initialize Job**
   - Generates unique deployment ID
   - Configures deployment parameters
   - Validates environment and secrets
   - Calculates optimal matrix size for parallel execution

2. **Deploy-Bots Job**
   - Uses matrix strategy for parallel execution (up to 256 concurrent runners)
   - Each runner manages a subset of bots
   - Implements batch processing for resource management
   - Generates individual bot logs and metrics

3. **Monitor-and-Aggregate Job**
   - Collects logs from all runners
   - Aggregates deployment metrics
   - Generates comprehensive deployment reports
   - Performs health checks and performance analysis

### 4. Scalability

- **Parallel Execution**: Up to 256 concurrent GitHub Actions runners
- **Dynamic Allocation**: Bots are automatically distributed across available runners
- **Batch Processing**: Bots are spawned in batches of 100 to optimize resource usage
- **Fault Tolerance**: Individual bot failures don't affect overall deployment

### 5. Monitoring & Logging

- **Centralized Logging**: All bot activities are logged to individual log files
- **Metrics Collection**: Success/failure counts tracked per runner
- **Artifact Preservation**: Logs preserved for 7 days, reports for 30 days
- **Real-time Monitoring**: Status updates throughout deployment process

## Required Secrets

Configure these secrets in your GitHub repository settings:

- `LUCRE_API_KEY`: API key for Lucre service integration
- `FANVUE_TOKENS`: Authentication tokens for Fanvue services

> **Note**: The workflow will warn if secrets are not configured but will continue execution.

## Manual Execution

### Via GitHub UI

1. Navigate to **Actions** tab in your repository
2. Select **Super Swarm - High Performance Virtual Bots** workflow
3. Click **Run workflow**
4. Configure parameters:
   - Set bot count (default: 20,000)
   - Choose deployment mode (auto-scale, fixed, or test)
5. Click **Run workflow** button

### Via GitHub CLI

```bash
gh workflow run super-swarm.yml \
  --ref main \
  -f bot_count=20000 \
  -f deployment_mode=auto-scale
```

## Deployment Process

### 1. Initialization Phase

```
Initialize → Generate Deployment ID → Configure Parameters → Validate Environment
```

### 2. Deployment Phase

For each runner in the matrix:
```
Allocate Bots → Spawn Bot Processes → Execute Workload → Collect Metrics → Upload Logs
```

### 3. Monitoring Phase

```
Download Logs → Aggregate Metrics → Generate Report → Health Check → Finalize
```

## Output Artifacts

### Bot Logs (7-day retention)

- **Name**: `bot-logs-runner-{runner_id}`
- **Contents**: Individual bot logs and summary JSON
- **Location**: `logs/swarm/{deployment_id}/runner-{runner_id}/`

### Deployment Reports (30-day retention)

- **Name**: `deployment-report-{deployment_id}`
- **Contents**: Comprehensive deployment analysis in Markdown format
- **Includes**:
  - Deployment information and timestamp
  - Performance metrics
  - Success/failure statistics
  - Bot capabilities summary
  - Architecture overview

## Performance Metrics

The workflow tracks and reports:

- **Total Bots Deployed**: Count of successfully deployed bots
- **Failed Deployments**: Count of failed bot deployments
- **Success Rate**: Percentage of successful deployments
- **Bots per Runner**: Average distribution across runners
- **Active Runners**: Number of parallel runners used
- **Deployment Duration**: Time taken for complete deployment

## Health Checks

The workflow automatically performs health checks:

- **Success Rate Threshold**: Warns if success rate falls below 95%
- **Environment Validation**: Checks for required secrets
- **Log Integrity**: Validates log file generation
- **Metric Aggregation**: Ensures all runner metrics are collected

## Bot Management Script

The workflow generates and executes `scripts/swarm/bot-manager.sh` for each runner, which:

1. Spawns bot processes in configurable batches
2. Manages process lifecycle and monitoring
3. Generates individual bot logs
4. Creates summary metrics in JSON format
5. Handles graceful shutdown and cleanup

## Troubleshooting

### Low Success Rate

If deployment success rate is below 95%:
1. Check runner logs in artifacts
2. Review individual bot failure logs
3. Verify secrets are configured correctly
4. Check for resource constraints

### Workflow Failures

If the workflow fails to complete:
1. Check the initialization job for parameter validation errors
2. Review runner allocation and matrix configuration
3. Verify GitHub Actions quotas and limits
4. Check artifact upload/download steps

### Missing Logs

If logs are not available:
1. Verify artifact retention settings
2. Check workflow permissions
3. Review upload-artifact steps for errors

## Customization

### Adjusting Bot Count

Edit the workflow file or use manual trigger with custom bot_count:

```yaml
env:
  BOT_COUNT: 20000  # Change this value
```

### Modifying Schedule

Edit the cron expression:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
  # Examples:
  # - cron: '0 * * * *'    # Every hour
  # - cron: '0 0 * * *'    # Daily at midnight
  # - cron: '0 0 * * 0'    # Weekly on Sunday
```

### Changing Parallel Runners

Adjust the maximum parallel runners:

```yaml
strategy:
  max-parallel: 256  # Reduce for slower deployments
```

### Batch Size Configuration

Modify batch size in the bot manager script:

```bash
BATCH_SIZE=100  # Adjust based on runner capacity
```

## Best Practices

1. **Start Small**: Test with smaller bot counts before scaling to 20,000
2. **Monitor Resources**: Watch GitHub Actions usage and quotas
3. **Review Logs**: Regularly check deployment reports for issues
4. **Optimize Secrets**: Ensure API keys have appropriate rate limits
5. **Schedule Wisely**: Adjust cron schedule based on actual needs

## Security Considerations

- Secrets are never exposed in logs or outputs
- Bot processes run in isolated GitHub Actions runners
- Logs are automatically cleaned up after retention period
- All network calls should use encrypted connections

## Support and Maintenance

- **Artifact Cleanup**: Logs automatically deleted after 7 days
- **Report Archive**: Deployment reports kept for 30 days
- **Workflow Updates**: Review and update actions versions periodically
- **Monitoring**: Set up alerts for workflow failures

## License

This workflow is part of the VoBee AI Assistant project and follows the project's MIT License.
