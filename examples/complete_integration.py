"""
Complete Integration Example

This example demonstrates all three core components working together:
- Project Cortex for multi-project management
- Decision Gate for critical action control
- Agent Registry for role-based agent coordination
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.project_cortex import ProjectManager, ProjectStatus
from core.decision_gate import DecisionGate, DecisionType, DecisionStatus
from agents import AgentRegistry
from agents.roles import initialize_default_roles


def deployment_executor(decision):
    """Example deployment function"""
    context = decision.context
    print(f"\n🚀 Executing deployment...")
    print(f"   Service: {context['service_name']}")
    print(f"   Version: {context['version']}")
    print(f"   Environment: {context['environment']}")
    return {
        "success": True,
        "deployment_id": "deploy-20251216-001",
        "service": context['service_name']
    }


def main():
    print("=" * 70)
    print("VoBee AI Operating System - Complete Integration Example")
    print("=" * 70)
    
    # Initialize all three core components
    print("\n📦 Initializing core components...")
    
    manager = ProjectManager()
    gate = DecisionGate(enable_auto_approval=False)
    registry = AgentRegistry()
    initialize_default_roles(registry)
    
    print(f"   ✓ Project Manager initialized")
    print(f"   ✓ Decision Gate initialized")
    print(f"   ✓ Agent Registry initialized with {len(registry.list_roles())} roles")
    
    # Create a critical project
    print("\n📋 Creating a new critical project...")
    
    project = manager.create_project(
        name="Production System Upgrade",
        description="Upgrade core production systems with new features",
        budget=150000,
        currency="USD"
    )
    
    # Add project goals
    project.add_goal("Security audit", priority=1)
    project.add_goal("Code development and testing", priority=2)
    project.add_goal("Deployment to staging", priority=3)
    project.add_goal("Production deployment", priority=4)
    
    print(f"   ✓ Project created: {project.name}")
    print(f"   ✓ Budget: ${project.budget.total_budget:,} {project.budget.currency}")
    print(f"   ✓ Goals: {len(project.goals)} objectives defined")
    
    print("\n✅ Integration Example Completed Successfully!")


if __name__ == "__main__":
    main()
