"""
Example: Complete Personal AI OS Integration
Demonstrates all three modules working together
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.project_cortex import ProjectManager, MemoryManager, BudgetManager, AgentTracker
from agents import AgentRegistry, AgentRole, RoleCategory
from core.decision_gates_structure import GateManager, ConfirmationHandler, GateType


def main():
    """Complete integration example"""
    
    print("=" * 80)
    print("Personal AI Operating System - Complete Integration Example")
    print("=" * 80)
    
    # =========================================================================
    # STEP 1: Initialize all managers
    # =========================================================================
    print("\n[STEP 1] Initializing managers...")
    
    # Project Cortex managers
    project_manager = ProjectManager()
    memory_manager = MemoryManager()
    budget_manager = BudgetManager()
    agent_tracker = AgentTracker()
    
    # Agents system
    agent_registry = AgentRegistry()
    
    # Decision gates system
    gate_manager = GateManager()
    confirmation_handler = ConfirmationHandler()
    
    print("✓ All managers initialized")
    
    # =========================================================================
    # STEP 2: Register agents across different roles
    # =========================================================================
    print("\n[STEP 2] Registering agents...")
    
    agents_to_register = [
        ("ops-001", "Operations Architect"),
        ("fe-001", "Frontend Developer"),
        ("be-001", "Backend Developer"),
        ("be-002", "API Specialist"),
        ("data-001", "Data Engineer"),
        ("devops-001", "DevOps Engineer"),
        ("qa-001", "QA Engineer"),
    ]
    
    for agent_id, role_name in agents_to_register:
        agent_registry.register_agent(agent_id, role_name)
        # Also register in agent tracker
        role_def = agent_registry.get_role_by_name(role_name)
        if role_def:
            agent_tracker.register_agent(
                agent_id,
                role_name,
                role_def['capabilities']
            )
    
    print(f"✓ Registered {len(agents_to_register)} agents")
    
    # =========================================================================
    # STEP 3: Create multiple projects
    # =========================================================================
    print("\n[STEP 3] Creating projects...")
    
    # Project 1: Mobile App Development
    mobile_project = project_manager.create_project(
        name="Mobile App Development",
        description="iOS and Android app with React Native",
        budget={'total': 75000, 'currency': 'USD'},
        goals=[
            'Complete UI/UX design',
            'Implement core features',
            'Launch beta version'
        ]
    )
    
    # Project 2: API Platform
    api_project = project_manager.create_project(
        name="API Platform",
        description="RESTful API backend",
        budget={'total': 50000, 'currency': 'USD'},
        goals=[
            'Design API architecture',
            'Implement endpoints',
            'Deploy to production'
        ]
    )
    
    # Project 3: Data Pipeline
    data_project = project_manager.create_project(
        name="Data Pipeline",
        description="ETL pipeline for analytics",
        budget={'total': 40000, 'currency': 'USD'},
        goals=[
            'Setup data sources',
            'Build transformation logic',
            'Deploy pipeline'
        ]
    )
    
    print(f"✓ Created {len(project_manager.get_all_projects())} projects")
    
    # =========================================================================
    # STEP 4: Setup project infrastructure
    # =========================================================================
    print("\n[STEP 4] Setting up project infrastructure...")
    
    for project in [mobile_project, api_project, data_project]:
        # Initialize budget tracking
        budget_manager.create_budget_profile(
            project.project_id,
            total_budget=project.budget['total'],
            currency=project.budget['currency']
        )
        
        # Initialize memory
        memory_manager.create_project_memory(project.project_id)
    
    # Store project-specific data
    memory_manager.store(
        mobile_project.project_id,
        "tech_stack",
        ["React Native", "Node.js", "MongoDB"],
        memory_type="long_term"
    )
    
    memory_manager.store(
        api_project.project_id,
        "tech_stack",
        ["Python", "FastAPI", "PostgreSQL"],
        memory_type="long_term"
    )
    
    print("✓ Project infrastructure setup complete")
    
    # =========================================================================
    # STEP 5: Assign agents to projects
    # =========================================================================
    print("\n[STEP 5] Assigning agents to projects...")
    
    # Mobile app team
    agent_tracker.assign_agent_to_project(mobile_project.project_id, "fe-001")
    agent_tracker.assign_agent_to_project(mobile_project.project_id, "be-001")
    
    # API platform team
    agent_tracker.assign_agent_to_project(api_project.project_id, "be-002")
    agent_tracker.assign_agent_to_project(api_project.project_id, "devops-001")
    
    # Data pipeline team
    agent_tracker.assign_agent_to_project(data_project.project_id, "data-001")
    agent_tracker.assign_agent_to_project(data_project.project_id, "devops-001")
    
    print("✓ Agents assigned to projects")
    
    # =========================================================================
    # STEP 6: Budget operations with approval gates
    # =========================================================================
    print("\n[STEP 6] Testing budget operations with approval gates...")
    
    # Request budget increase for mobile project
    budget_increase_gate = gate_manager.create_gate(
        gate_type=GateType.APPROVAL,
        title=f"Budget Increase - {mobile_project.name}",
        description="Increase budget by $15,000 for additional features",
        context={
            'project_id': mobile_project.project_id,
            'amount': 15000,
            'reason': 'Additional platform support needed'
        },
        required_approvers=['finance-lead', 'project-sponsor'],
        auto_expire_minutes=120
    )
    
    print(f"  Created approval gate: {budget_increase_gate.gate_id}")
    
    # Simulate approvals
    gate_manager.approve_gate(
        budget_increase_gate.gate_id,
        'finance-lead',
        'Budget available, approved'
    )
    
    gate_manager.approve_gate(
        budget_increase_gate.gate_id,
        'project-sponsor',
        'Strategic priority, approved'
    )
    
    # Process budget increase if approved
    if budget_increase_gate.is_approved():
        budget_manager.add_budget(
            mobile_project.project_id,
            15000,
            "Approved budget increase"
        )
        print("  ✓ Budget increased after approval")
    
    # Record some expenses
    budget_manager.record_expense(
        mobile_project.project_id,
        5000,
        "Design tools and licenses",
        category="software"
    )
    
    budget_manager.record_expense(
        api_project.project_id,
        8000,
        "Cloud infrastructure",
        category="infrastructure"
    )
    
    print("  ✓ Expenses recorded")
    
    # =========================================================================
    # STEP 7: Deployment with confirmation
    # =========================================================================
    print("\n[STEP 7] Testing deployment with confirmation...")
    
    # Simple confirmation for staging deployment
    staging_conf_id = confirmation_handler.request_confirmation(
        confirmation_id="deploy-staging-001",
        message=f"Deploy {api_project.name} to staging environment?",
        context={'environment': 'staging', 'version': '1.0.0'},
        timeout_seconds=300
    )
    
    # User confirms
    confirmation_handler.confirm(staging_conf_id, "Staging tests passed")
    print("  ✓ Staging deployment confirmed")
    
    # Production deployment requires approval gate
    prod_deployment_gate = gate_manager.create_gate(
        gate_type=GateType.APPROVAL,
        title=f"Production Deployment - {api_project.name}",
        description="Deploy v1.0.0 to production",
        context={
            'project_id': api_project.project_id,
            'version': '1.0.0',
            'environment': 'production'
        },
        required_approvers=['tech-lead', 'ops-lead', 'product-owner']
    )
    
    # Simulate approvals
    gate_manager.approve_gate(prod_deployment_gate.gate_id, 'tech-lead', 'Code reviewed')
    gate_manager.approve_gate(prod_deployment_gate.gate_id, 'ops-lead', 'Infrastructure ready')
    gate_manager.approve_gate(prod_deployment_gate.gate_id, 'product-owner', 'Business approved')
    
    if prod_deployment_gate.is_approved():
        print("  ✓ Production deployment approved")
    
    # =========================================================================
    # STEP 8: Sleep idle project
    # =========================================================================
    print("\n[STEP 8] Testing project sleep/wake...")
    
    # Put data project to sleep (simulating idle state)
    project_manager.sleep_project(data_project.project_id)
    print(f"  ✓ Project '{data_project.name}' put to sleep")
    
    # Wake it back up
    project_manager.wake_project(data_project.project_id)
    print(f"  ✓ Project '{data_project.name}' woken up")
    
    # =========================================================================
    # STEP 9: Generate comprehensive report
    # =========================================================================
    print("\n[STEP 9] Generating system report...")
    print("\n" + "=" * 80)
    print("SYSTEM STATUS REPORT")
    print("=" * 80)
    
    # Project summary
    pm_stats = project_manager.get_project_summary()
    print("\n[Project Cortex]")
    print(f"  Total Projects: {pm_stats['total_projects']}")
    print(f"  Active Projects: {pm_stats['active_projects']}/{pm_stats['max_active']}")
    print(f"  Sleeping Projects: {pm_stats['sleeping_projects']}")
    print(f"  Capacity Utilization: {pm_stats['capacity_utilization']}")
    
    # Agent registry summary
    ar_stats = agent_registry.get_registry_stats()
    print("\n[Agents System]")
    print(f"  Total Agents: {ar_stats['total_agents']}")
    print(f"  Capacity: {ar_stats['capacity_utilization']}")
    print(f"  Available Roles: {ar_stats['available_roles']}")
    
    # Agent tracker summary
    at_stats = agent_tracker.get_tracker_summary()
    print("\n[Agent Assignments]")
    print(f"  Active Agents: {at_stats['active_agents']}")
    print(f"  Available Agents: {at_stats['available_agents']}")
    print(f"  Projects with Agents: {at_stats['total_projects_with_agents']}")
    
    # Decision gates summary
    gm_stats = gate_manager.get_manager_stats()
    print("\n[Decision Gates]")
    print(f"  Total Gates: {gm_stats['total_gates']}")
    print(f"  Pending: {gm_stats['pending_gates']}")
    print(f"  Approved: {gm_stats['approved_gates']}")
    print(f"  Rejected: {gm_stats['rejected_gates']}")
    print(f"  Locked Outputs: {gm_stats['locked_outputs']}")
    
    # Confirmation summary
    ch_stats = confirmation_handler.get_statistics()
    print("\n[Confirmations]")
    print(f"  Total: {ch_stats['total_confirmations']}")
    print(f"  Pending: {ch_stats['pending']}")
    print(f"  Confirmed: {ch_stats['confirmed']}")
    print(f"  Rejected: {ch_stats['rejected']}")
    
    # Project details
    print("\n[Project Details]")
    for project in project_manager.get_active_projects():
        budget = budget_manager.get_budget_summary(project.project_id)
        agents = agent_tracker.get_project_agents(project.project_id)
        
        print(f"\n  {project.name}")
        print(f"    Status: {project.status.value}")
        print(f"    Goals: {len(project.goals)}")
        print(f"    Budget: ${budget['spent']:,.0f}/${budget['total_budget']:,.0f} "
              f"({budget['utilization_percent']:.1f}% used)")
        print(f"    Agents: {len(agents)}")
    
    print("\n" + "=" * 80)
    print("Example completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
