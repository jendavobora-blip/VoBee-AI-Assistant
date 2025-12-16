"""
Example: Using Decision Gate

This example demonstrates how to use the Decision Gate system
for controlling critical actions with explicit confirmation.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.decision_gate import DecisionGate, DecisionType

def deploy_to_production(decision):
    """Example deployment function"""
    print(f"Deploying to production: {decision.context['service_name']}")
    return {"success": True, "deployment_id": "deploy-12345"}

def main():
    # Initialize the decision gate
    gate = DecisionGate(enable_auto_approval=False)
    
    # Request a critical decision
    decision1 = gate.request_decision(
        action_type="deploy",
        description="Deploy new version to production",
        decision_type=DecisionType.CRITICAL,
        context={"service_name": "api-gateway", "version": "2.0.0"}
    )
    
    print(f"Decision requested: {decision1.decision_id}")
    print(f"Description: {decision1.description}")
    print(f"Status: {decision1.status.value}")
    
    # Request a normal decision
    decision2 = gate.request_decision(
        action_type="cleanup",
        description="Clean up old logs",
        decision_type=DecisionType.NORMAL,
        context={"days_old": 30}
    )
    
    # List pending decisions
    pending = gate.list_pending_decisions()
    print(f"\nPending decisions: {len(pending)}")
    for dec in pending:
        print(f"  - {dec.decision_id}: {dec.description}")
    
    # Approve the critical decision
    gate.approve_decision(decision1.decision_id, approved_by="admin")
    print(f"\nDecision {decision1.decision_id} approved")
    
    # Execute the approved decision
    result = gate.execute_decision(decision1.decision_id, deploy_to_production)
    print(f"Execution result: {result}")
    
    # Reject the normal decision
    gate.reject_decision(decision2.decision_id, reason="Not needed at this time")
    print(f"\nDecision {decision2.decision_id} rejected")
    
    # View audit log
    audit_log = gate.get_audit_log(limit=5)
    print(f"\nRecent audit log entries:")
    for entry in audit_log:
        print(f"  {entry['timestamp']}: {entry['event_type']} - {entry['decision_id']}")
    
    # Save state
    gate.save_state("/tmp/decision_gate_state.json")
    print("\nState saved to /tmp/decision_gate_state.json")


if __name__ == "__main__":
    main()
