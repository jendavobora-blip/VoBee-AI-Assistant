# Cost Guard Configuration

## Provider Cost Profiles

This file defines cost and quality profiles for AI service providers.
Update this file when provider pricing changes.

### Configuration Format

Each provider entry includes:
- `cost`: Cost per 1000 tokens/requests (in USD)
- `quality_score`: Quality rating from 0.0 to 1.0
- `latency_ms`: Average response latency in milliseconds

### Provider Profiles

**Last Updated**: 2024-01-20

```json
{
  "providers": {
    "gpt-4": {
      "cost": 0.03,
      "quality_score": 0.95,
      "latency_ms": 800,
      "notes": "Highest quality, best for complex tasks"
    },
    "gpt-3.5-turbo": {
      "cost": 0.002,
      "quality_score": 0.80,
      "latency_ms": 400,
      "notes": "Good balance of cost and quality"
    },
    "claude-2": {
      "cost": 0.025,
      "quality_score": 0.90,
      "latency_ms": 600,
      "notes": "Strong reasoning, good for analysis"
    },
    "palm-2": {
      "cost": 0.001,
      "quality_score": 0.75,
      "latency_ms": 300,
      "notes": "Lowest cost, best for simple tasks"
    }
  },
  "routing_strategies": {
    "cheapest": {
      "description": "Always route to cheapest provider",
      "use_case": "Cost-sensitive workloads, simple tasks"
    },
    "best_value": {
      "description": "Optimize quality/cost ratio",
      "use_case": "Balanced requirements (default)"
    },
    "quality_first": {
      "description": "Prioritize highest quality",
      "use_case": "Complex tasks, production outputs"
    },
    "load_balanced": {
      "description": "Distribute across providers",
      "use_case": "High volume, availability concerns"
    }
  },
  "update_instructions": [
    "1. Verify new pricing from official provider documentation",
    "2. Update cost values in this file",
    "3. Commit changes with reference to pricing source",
    "4. Monitor cost impact after deployment",
    "5. Adjust routing strategy if needed"
  ]
}
```

## TODO: Load Configuration at Runtime

The CostRouter currently has hard-coded provider profiles. To enable runtime updates:

1. Load this configuration file in `CostRouter.__init__()`
2. Add method to reload configuration without restart
3. Implement configuration validation
4. Add monitoring for configuration changes

**Priority**: Medium - Important for production cost optimization

## Configuration Update Procedure

When updating provider costs:

1. **Document the source**: Include link to pricing page
2. **Request approval**: Use Decision Gate for cost changes
3. **Update configuration**: Modify this file
4. **Test routing**: Verify routing decisions are correct
5. **Monitor impact**: Track cost changes in Cost Monitor

Example update:
```
Date: 2024-01-25
Source: https://openai.com/pricing
Change: gpt-3.5-turbo cost reduced from $0.002 to $0.001 per 1K tokens
Approved by: cost-manager@company.com
Decision ID: abc-123-def
```

## Notes

- Costs are in USD per 1000 tokens/units
- Quality scores are subjective - adjust based on testing
- Latency values are averages - actual may vary
- Add new providers as needed
- Remove deprecated providers

---

This configuration enables cost optimization without code changes.
