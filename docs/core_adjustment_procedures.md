# Core Adjustment Procedures

## Overview

This document describes procedures for adjusting core framework components (Project Cortex, Decision Gate, Cost Guard) safely and incrementally.

## General Principles

### 1. Incremental Changes Only
- Make one change at a time
- Test after each change
- Validate before proceeding
- Rollback if issues arise

### 2. Logging Over Magic
- Log all configuration changes
- Document reasons for adjustments
- Track who made changes and when
- No hidden or implicit behaviors

### 3. Deterministic Behavior
- Same inputs → same outputs
- Reproducible configurations
- Explicit state management
- No randomness in core operations

### 4. Human Approval Required
- All core adjustments need approval
- Use Decision Gate for critical changes
- Document approval rationale
- Maintain change log

## Component Adjustment Procedures

## Project Cortex Adjustments

### Procedure: Create New Project

**When**: Starting a new project or initiative

**Steps**:
1. Define project requirements
2. Determine budget and quality preferences
3. Create project configuration
4. Validate settings
5. Activate project

**Code Example**:
```python
from core.project_cortex import ProjectManager

pm = ProjectManager()

# Step 1-3: Create with configuration
project = pm.create_project(
    project_id="new-feature-2024",
    name="New Feature Development 2024",
    description="Development of advanced analytics dashboard",
    budget_limit=2000.00,
    quality_preference="quality"  # Options: speed, balanced, quality
)

print(f"Created project: {project['id']}")

# Step 4: Validate
assert project['budget_limit'] == 2000.00
assert project['quality_preference'] == "quality"
assert project['state'] == "initializing"

# Step 5: Activate
pm.activate_project(project['id'])
print(f"Project activated: {project['id']}")
```

**Validation Checklist**:
- [ ] Project ID is unique
- [ ] Budget limit is reasonable
- [ ] Quality preference matches requirements
- [ ] Initial state is correct

### Procedure: Adjust Project Budget

**When**: Budget needs increase/decrease

**Steps**:
1. Assess current budget usage
2. Justify change
3. Request approval via Decision Gate
4. Update budget after approval
5. Notify stakeholders

**Code Example**:
```python
from core.project_cortex import ProjectManager
from core.decision_gate import ConfirmationWorkflow, DecisionManager

pm = ProjectManager()
dm = DecisionManager()
workflow = ConfirmationWorkflow(dm)

# Step 1: Assess current usage
project = pm.get_project("new-feature-2024")
current_budget = project['budget_limit']
current_usage = project['budget_used']

print(f"Current: ${current_usage:.2f} / ${current_budget:.2f}")

# Step 2-3: Request approval
new_budget = 3000.00
decision_id = workflow.confirm_budget_change(
    project_id=project['id'],
    current_budget=current_budget,
    new_budget=new_budget,
    justification="Scope expanded to include mobile app. Additional $1000 needed for development and testing."
)

print(f"Budget change requested: {decision_id}")

# Human approves via UI/CLI...

# Step 4: Update after approval
def update_project_budget(action):
    project_id = action['project_id']
    new_budget = action['new_budget']
    
    project = pm.get_project(project_id)
    project['budget_limit'] = new_budget
    pm._save_project(project_id)
    
    return {"updated": True, "new_budget": new_budget}

# After human approval
dm.approve_decision(decision_id, "finance-manager", "Approved")
result = dm.execute_decision(decision_id, update_project_budget, "budget-bot")

# Step 5: Notify
print(f"Budget updated to ${new_budget}")
```

**Validation Checklist**:
- [ ] Current budget usage documented
- [ ] Justification clear and complete
- [ ] Approval obtained from authorized person
- [ ] Budget update successful
- [ ] Stakeholders notified

### Procedure: Change Quality Preference

**When**: Performance or quality requirements change

**Steps**:
1. Review current preference and performance
2. Analyze impact of change
3. Update quality profile
4. Monitor results

**Code Example**:
```python
from core.project_cortex import ProjectManager
from core.project_cortex.quality_profile import QualityProfile

pm = ProjectManager()
project = pm.get_project("new-feature-2024")

# Step 1: Review current
qp = QualityProfile(project['id'], project['quality_preference'])
current_config = qp.get_config()
print(f"Current preference: {qp.preference.value}")
print(f"Current config: {current_config}")

# Step 2: Analyze impact
new_preference = "speed"  # Switching to faster execution
print(f"Switching to: {new_preference}")

# Impact analysis
if new_preference == "speed":
    print("Impact:")
    print("- Faster execution (50% reduction in timeouts)")
    print("- Lower quality outputs")
    print("- More use of caching")
    print("- Recommended for development/testing")

# Step 3: Update
qp.set_preference(new_preference)
project['quality_preference'] = new_preference
pm._save_project(project['id'])

print(f"Quality preference updated: {qp.preference.value}")
print(f"New config: {qp.get_config()}")

# Step 4: Monitor over next few operations
# TODO: Set up monitoring alerts for quality metrics
```

**Validation Checklist**:
- [ ] Impact understood and acceptable
- [ ] Change documented
- [ ] Monitoring in place
- [ ] Rollback plan ready

## Decision Gate Adjustments

### Procedure: Add New Decision Type

**When**: New type of critical operation needs approval

**Steps**:
1. Define decision type
2. Update DecisionType enum
3. Create workflow helper
4. Test workflow
5. Document usage

**Code Example**:
```python
# Step 1-2: Update decision_manager.py
# Add to DecisionType enum:
class DecisionType(Enum):
    # ... existing types ...
    VENDOR_INTEGRATION = "vendor_integration"  # New type

# Step 3: Create workflow helper
# Add to confirmation_workflow.py:
def confirm_vendor_integration(
    self,
    vendor_name: str,
    integration_type: str,
    data_shared: list,
    security_assessment: str
) -> str:
    """Request confirmation for vendor integration."""
    
    # Vendor integrations are high risk due to data sharing
    risk_level = "high" if data_shared else "medium"
    
    title = f"Integrate with vendor: {vendor_name}"
    description = f"""
Vendor Integration Request:
- Vendor: {vendor_name}
- Integration Type: {integration_type}
- Data Shared: {', '.join(data_shared)}

Security Assessment:
{security_assessment}

⚠️ This integration will share data with external vendor.
"""
    
    proposed_action = {
        "action_type": "vendor_integration",
        "vendor_name": vendor_name,
        "integration_type": integration_type,
        "data_shared": data_shared
    }
    
    return self.decision_manager.request_decision(
        decision_type=DecisionType.VENDOR_INTEGRATION,
        title=title,
        description=description,
        proposed_action=proposed_action,
        risk_level=risk_level,
        expiry_hours=48
    )

# Step 4: Test
from core.decision_gate import ConfirmationWorkflow, DecisionManager

dm = DecisionManager()
workflow = ConfirmationWorkflow(dm)

decision_id = workflow.confirm_vendor_integration(
    vendor_name="Analytics Co",
    integration_type="REST API",
    data_shared=["user_ids", "usage_metrics"],
    security_assessment="SOC 2 Type II certified, GDPR compliant"
)

print(f"Vendor integration approval requested: {decision_id}")
```

**Validation Checklist**:
- [ ] Decision type enum updated
- [ ] Workflow helper implemented
- [ ] Risk level appropriate
- [ ] Test case passes
- [ ] Documentation updated

### Procedure: Adjust Expiration Times

**When**: Default expiration times don't match operational needs

**Steps**:
1. Analyze current expiration patterns
2. Determine new defaults
3. Update configuration
4. Apply to new decisions

**Code Example**:
```python
from core.decision_gate import DecisionManager

# Step 1: Analyze current patterns
dm = DecisionManager()
history = dm.get_decision_history(limit=100)

expired_count = len([d for d in history if d['status'] == 'expired'])
print(f"Expired decisions: {expired_count}/100 ({expired_count}%)")

# If expiration rate is high, consider increasing defaults

# Step 2-3: Determine and update defaults
# Update in DecisionManager.__init__
dm = DecisionManager(
    default_expiry_hours=48  # Increased from 24
)

# Step 4: Apply to new decisions
# New decisions will use updated default
decision_id = dm.request_decision(
    decision_type=DecisionType.CONFIG_UPDATE,
    title="Update timeout config",
    description="Increase API timeout to 30s",
    proposed_action={"timeout": 30},
    # Uses default 48 hours if expiry_hours not specified
)
```

## Cost Guard Adjustments

### Procedure: Update Provider Costs

**When**: Provider pricing changes or new providers added

**Steps**:
1. Verify new pricing from provider
2. Update cost router configuration
3. Re-evaluate routing decisions
4. Monitor cost impact

**Code Example**:
```python
from core.cost_guard import CostRouter, RoutingStrategy

# Step 1: Verify new pricing
# Source: OpenAI pricing page updated 2024-01-15
new_gpt4_cost = 0.03  # per 1K tokens (unchanged)
new_gpt35_cost = 0.001  # per 1K tokens (reduced from 0.002)

# Step 2: Update configuration
router = CostRouter(strategy=RoutingStrategy.BEST_VALUE)

router.update_provider_costs(
    provider="gpt-3.5-turbo",
    cost=new_gpt35_cost,
    quality_score=0.80
)

print(f"Updated gpt-3.5-turbo: ${new_gpt35_cost} per 1K tokens")

# Step 3: Re-evaluate routing
provider, metadata = router.route_request(
    request_type="text_generation",
    quality_requirement=0.75,
    estimated_tokens=1000
)

print(f"Routing recommendation: {provider}")
print(f"Estimated cost: ${metadata['estimated_cost']:.4f}")

# Step 4: Monitor impact
stats = router.get_provider_stats()
print(f"Provider distribution: {stats['provider_distribution']}")
```

**Validation Checklist**:
- [ ] Pricing verified from official source
- [ ] Update applied correctly
- [ ] Routing behavior tested
- [ ] Cost monitoring active

### Procedure: Change Routing Strategy

**When**: Cost or quality priorities change

**Steps**:
1. Analyze current routing performance
2. Determine optimal strategy
3. Update router configuration
4. Validate new routing behavior

**Code Example**:
```python
from core.cost_guard import CostRouter, RoutingStrategy

# Step 1: Analyze current performance
router = CostRouter(strategy=RoutingStrategy.BEST_VALUE)
stats = router.get_provider_stats()

print(f"Current strategy: {stats['strategy']}")
print(f"Total requests: {stats['total_requests']}")
print(f"Provider distribution: {stats['provider_distribution']}")

# Step 2: Determine optimal strategy
# If cost is top priority → CHEAPEST
# If quality is top priority → QUALITY_FIRST
# If balanced → BEST_VALUE
# If spreading load → LOAD_BALANCED

new_strategy = RoutingStrategy.CHEAPEST

# Step 3: Update
router.set_strategy(new_strategy)
print(f"Strategy updated to: {new_strategy.value}")

# Step 4: Validate with test requests
test_requests = [
    {"quality_requirement": 0.7, "estimated_tokens": 1000},
    {"quality_requirement": 0.8, "estimated_tokens": 500},
    {"quality_requirement": 0.9, "estimated_tokens": 2000},
]

for req in test_requests:
    provider, metadata = router.route_request(
        request_type="text_generation",
        **req
    )
    print(f"Quality {req['quality_requirement']}: {provider} (${metadata['estimated_cost']:.4f})")
```

### Procedure: Adjust Cost Ceiling

**When**: Budget changes or spending patterns shift

**Steps**:
1. Review current spending
2. Request ceiling adjustment via Decision Gate
3. Update cost monitor
4. Verify enforcement

**Code Example**:
```python
from core.cost_guard import CostMonitor
from core.decision_gate import DecisionManager, DecisionType

monitor = CostMonitor(global_cost_ceiling=1000.00)

# Step 1: Review spending
report = monitor.get_cost_report()
print(f"Total spent: ${report['total_cost']:.2f}")
print(f"Current ceiling: ${report['cost_ceiling']:.2f}")
print(f"Utilization: {report['utilization_percentage']:.1f}%")

# Step 2: Request adjustment
new_ceiling = 2000.00
dm = DecisionManager()

decision_id = dm.request_decision(
    decision_type=DecisionType.BUDGET_CHANGE,
    title=f"Increase cost ceiling: ${monitor.global_cost_ceiling} → ${new_ceiling}",
    description=f"""
Cost ceiling adjustment needed:
- Current ceiling: ${monitor.global_cost_ceiling:.2f}
- Current usage: ${monitor.total_cost:.2f} ({report['utilization_percentage']:.1f}%)
- Proposed ceiling: ${new_ceiling:.2f}

Reason: Expanding to new markets requires increased API usage.
""",
    proposed_action={"new_ceiling": new_ceiling},
    risk_level="medium"
)

# Human approves...
dm.approve_decision(decision_id, "finance-manager", "Approved for Q1 expansion")

# Step 3: Update
monitor.set_cost_ceiling(new_ceiling)
print(f"Cost ceiling updated to ${new_ceiling:.2f}")

# Step 4: Verify enforcement
test_cost = 1500.00
can_afford = monitor.can_afford(test_cost)
print(f"Can afford ${test_cost}: {can_afford}")
```

## Emergency Procedures

### Emergency: Budget Exceeded

**Symptoms**: Cost ceiling breached, alerts triggered

**Immediate Actions**:
1. Pause expensive operations
2. Review recent transactions
3. Identify cost spike cause
4. Implement temporary limits

```python
from core.cost_guard import CostMonitor

monitor = CostMonitor()

if monitor.is_over_ceiling():
    print("⚠️ BUDGET EXCEEDED - Emergency procedures activated")
    
    # Review recent spending
    report = monitor.get_cost_report()
    top_services = monitor.get_top_spending_services(limit=5)
    
    print(f"Over budget by: ${report['total_cost'] - report['cost_ceiling']:.2f}")
    print(f"Top spending services: {top_services}")
    
    # TODO: Pause non-critical services
    # TODO: Alert finance team
    # TODO: Review and approve continued operations
```

### Emergency: Decision Backlog

**Symptoms**: Many pending decisions, system blocked

**Actions**:
1. Review pending decisions
2. Prioritize by risk level
3. Expedite approvals
4. Increase expiration times if needed

```python
from core.decision_gate import DecisionManager

dm = DecisionManager()

# Check pending count
pending = dm.list_pending_decisions()
critical = dm.list_pending_decisions(risk_level="critical")

if len(pending) > 20:
    print(f"⚠️ DECISION BACKLOG - {len(pending)} pending decisions")
    print(f"Critical: {len(critical)}")
    
    # Prioritize critical
    for decision in critical:
        print(f"URGENT: {decision['title']}")
        print(f"Created: {decision['created_at']}")
```

## Change Log Template

Always maintain a change log for core adjustments:

```markdown
## Change Log - Core Framework Adjustments

### 2024-01-20: Cost Ceiling Increase
- **Component**: Cost Guard
- **Change**: Increased global ceiling from $1000 to $2000
- **Reason**: Q1 market expansion
- **Approved By**: finance-manager@company.com
- **Decision ID**: abc-123-def

### 2024-01-18: Quality Preference Update
- **Component**: Project Cortex
- **Change**: Changed default quality from "balanced" to "quality"
- **Reason**: User feedback indicated quality issues
- **Approved By**: product-manager@company.com
- **Impact**: 20% slower execution, 30% better outputs
```

## Summary

Core framework adjustments must follow these principles:
- ✅ Incremental changes
- ✅ Logged and documented
- ✅ Approved through Decision Gate
- ✅ Tested and validated
- ✅ Monitored after deployment

Always remember: **Adjust carefully, log thoroughly, validate completely.**

---

For more information, see:
- [Architecture Overview](architecture_overview.md)
- [Decision Gate Workflows](decision_gate_workflows.md)
