"""
Integration Example: VoBee Core Architecture

This example demonstrates how the three core components work together:
- Project Cortex: Multi-project management
- Decision Gate: Approval and control system
- Agent Registry: Role-based agent management

MAX_SPEED Implementation - Foundational Skeleton
"""

from core.project_cortex import ProjectCortex, ProjectStatus, AgentStatus as ProjectAgentStatus
from core.decision_gate import DecisionGate, GateRule, GateRulePriority, GateDecision
from agents import AgentRegistry, Agent, AgentRole, AgentStatus


def example_complete_workflow():
    """
    Demonstrates a complete workflow integrating all three systems.
    
    Scenario: Creating a new AI backend project with approval gates
    and agent assignments.
    """
    print("=" * 70)
    print("VoBee Core Architecture - Integration Example")
    print("=" * 70)
    print()
    
    # =========================================================================
    # 1. Initialize Core Systems
    # =========================================================================
    print("1. Initializing Core Systems...")
    
    cortex = ProjectCortex()
    decision_gate = DecisionGate()
    agent_registry = AgentRegistry()
    
    print("   ✓ Project Cortex initialized")
    print("   ✓ Decision Gate initialized")
    print("   ✓ Agent Registry initialized")
    print()
    
    # =========================================================================
    # 2. Register Agents with Capabilities
    # =========================================================================
    print("2. Registering Agents...")
    
    # Create architect agent
    architect = Agent(
        name="Senior System Architect",
        role=AgentRole.ARCHITECT,
        description="Designs scalable microservices architectures"
    )
    architect.add_capability("system_design", "Design distributed systems", proficiency=9)
    architect.add_capability("microservices", "Microservices patterns", proficiency=9)
    architect.add_capability("cloud_architecture", "Cloud-native design", proficiency=8)
    agent_registry.register_agent(architect)
    print(f"   ✓ Registered: {architect.name} ({architect.role.value})")
    
    # Create backend builder
    backend_dev = Agent(
        name="Backend Developer",
        role=AgentRole.BACKEND_BUILDER,
        description="Python/FastAPI backend specialist"
    )
    backend_dev.add_capability("python", "Python programming", proficiency=9)
    backend_dev.add_capability("fastapi", "FastAPI framework", proficiency=8)
    backend_dev.add_capability("postgresql", "PostgreSQL databases", proficiency=7)
    agent_registry.register_agent(backend_dev)
    print(f"   ✓ Registered: {backend_dev.name} ({backend_dev.role.value})")
    
    # Create QA engineer
    qa_engineer = Agent(
        name="QA Engineer",
        role=AgentRole.QA_ENGINEER,
        description="Automated testing specialist"
    )
    qa_engineer.add_capability("test_automation", "Automated testing", proficiency=9)
    qa_engineer.add_capability("pytest", "Pytest framework", proficiency=8)
    qa_engineer.add_capability("ci_cd", "CI/CD pipelines", proficiency=7)
    agent_registry.register_agent(qa_engineer)
    print(f"   ✓ Registered: {qa_engineer.name} ({qa_engineer.role.value})")
    
    stats = agent_registry.get_statistics()
    print(f"   Total agents: {stats['total_agents']}")
    print()
    
    # =========================================================================
    # 3. Configure Decision Gate Rules
    # =========================================================================
    print("3. Configuring Decision Gate Rules...")
    
    # Budget validation rule
    budget_rule = GateRule(
        name="Budget Validation",
        description="Ensure project budget is within limits",
        priority=GateRulePriority.HIGH
    )
    
    def validate_budget(context: dict) -> bool:
        budget = context.get('budget', 0)
        max_budget = context.get('max_budget', 50000)
        return budget <= max_budget
    
    budget_rule.set_evaluation_function(validate_budget)
    decision_gate.add_rule(budget_rule)
    print(f"   ✓ Added rule: {budget_rule.name} (Priority: {budget_rule.priority.value})")
    
    # Security check rule
    security_rule = GateRule(
        name="Security Review Required",
        description="Ensure security review is completed",
        priority=GateRulePriority.CRITICAL
    )
    
    def validate_security(context: dict) -> bool:
        return context.get('security_reviewed', False)
    
    security_rule.set_evaluation_function(validate_security)
    decision_gate.add_rule(security_rule)
    print(f"   ✓ Added rule: {security_rule.name} (Priority: {security_rule.priority.value})")
    
    # Agent availability rule
    agent_rule = GateRule(
        name="Agent Availability",
        description="Ensure required agents are available",
        priority=GateRulePriority.MEDIUM
    )
    
    def validate_agents(context: dict) -> bool:
        required_roles = context.get('required_roles', [])
        for role_name in required_roles:
            try:
                role = AgentRole(role_name)
                agents = agent_registry.find_agents_by_role(role, status=AgentStatus.AVAILABLE)
                if not agents:
                    return False
            except ValueError:
                return False
        return True
    
    agent_rule.set_evaluation_function(validate_agents)
    decision_gate.add_rule(agent_rule)
    print(f"   ✓ Added rule: {agent_rule.name} (Priority: {agent_rule.priority.value})")
    print()
    
    # =========================================================================
    # 4. Request Approval for New Project
    # =========================================================================
    print("4. Requesting Approval for New Project...")
    
    request = decision_gate.request_approval(
        action="create_project",
        description="Create AI-powered backend service project",
        context={
            'project_name': 'AI Backend Service',
            'budget': 25000,
            'max_budget': 50000,
            'security_reviewed': True,
            'required_roles': ['architect', 'backend_builder', 'qa_engineer']
        }
    )
    print(f"   Request ID: {request.id}")
    print(f"   Action: {request.action}")
    print(f"   Initial Status: {request.decision.value}")
    
    # Evaluate the request
    decision = decision_gate.evaluate_request(request.id)
    print(f"   ✓ Evaluation Complete: {decision.value}")
    print(f"   Reason: {request.decision_reason}")
    print()
    
    # =========================================================================
    # 5. Create Project (if approved)
    # =========================================================================
    if decision == GateDecision.APPROVED:
        print("5. Creating Project...")
        
        project = cortex.create_project(
            name="AI Backend Service",
            description="AI-powered backend service with microservices architecture",
            budget=25000.0
        )
        print(f"   ✓ Project created: {project.name}")
        print(f"   Project ID: {project.id}")
        print(f"   Budget: ${project.budget}")
        print()
        
        # Add project goals
        print("6. Adding Project Goals...")
        goal1 = project.add_goal(
            goal="Design system architecture",
            priority=1,
            metadata={'estimated_hours': 40}
        )
        goal2 = project.add_goal(
            goal="Implement core backend services",
            priority=2,
            metadata={'estimated_hours': 120}
        )
        goal3 = project.add_goal(
            goal="Set up automated testing",
            priority=3,
            metadata={'estimated_hours': 60}
        )
        print(f"   ✓ Added {len(project.goals)} goals")
        print()
        
        # Assign agents to project
        print("7. Assigning Agents to Project...")
        
        # Assign architect
        architect.assign_task(task_id="design-architecture", project_id=project.id)
        project.track_agent(architect.id, "architect", ProjectAgentStatus.ACTIVE)
        print(f"   ✓ Assigned: {architect.name} to {project.name}")
        
        # Assign backend developer
        backend_dev.assign_task(task_id="implement-backend", project_id=project.id)
        project.track_agent(backend_dev.id, "backend_builder", ProjectAgentStatus.ACTIVE)
        print(f"   ✓ Assigned: {backend_dev.name} to {project.name}")
        
        # Assign QA engineer
        qa_engineer.assign_task(task_id="setup-testing", project_id=project.id)
        project.track_agent(qa_engineer.id, "qa_engineer", ProjectAgentStatus.ACTIVE)
        print(f"   ✓ Assigned: {qa_engineer.name} to {project.name}")
        print()
        
        # Update project memory
        print("8. Updating Project Memory...")
        project.update_memory("technology_stack", {
            "backend": "Python + FastAPI",
            "database": "PostgreSQL",
            "testing": "Pytest",
            "deployment": "Kubernetes"
        })
        project.update_memory("architecture_pattern", "Microservices")
        print("   ✓ Technology stack stored in project memory")
        print("   ✓ Architecture pattern stored")
        print()
        
        # Track budget expenditure
        print("9. Tracking Budget...")
        project.update_budget(500.0)  # Initial setup costs
        print(f"   ✓ Budget spent: ${project.budget_spent}")
        print(f"   ✓ Budget remaining: ${project.get_budget_remaining()}")
        print()
        
        # Display project summary
        print("10. Project Summary...")
        print(f"   Name: {project.name}")
        print(f"   Status: {project.status.value}")
        print(f"   Active Agents: {len(project.active_agents)}")
        print(f"   Goals: {len(project.goals)}")
        print(f"   Budget: ${project.budget}")
        print(f"   Spent: ${project.budget_spent}")
        print(f"   Remaining: ${project.get_budget_remaining()}")
        print()
        
        # Demonstrate sleep/wake
        print("11. Demonstrating Sleep/Wake Capabilities...")
        print(f"   Current status: {project.status.value}")
        project.sleep()
        print(f"   ✓ Project put to sleep: {project.status.value}")
        project.wake()
        print(f"   ✓ Project woken up: {project.status.value}")
        print()
    
    # =========================================================================
    # Final Statistics
    # =========================================================================
    print("=" * 70)
    print("Final System Statistics")
    print("=" * 70)
    
    # Cortex stats
    cortex_stats = cortex.to_dict()
    print(f"Project Cortex:")
    print(f"  Total Projects: {cortex_stats['total_projects']}")
    print(f"  Active Projects: {cortex_stats['active_projects']}")
    print(f"  Total Budget Spent: ${cortex_stats['total_budget_spent']}")
    print()
    
    # Decision Gate stats
    gate_stats = decision_gate.to_dict()
    print(f"Decision Gate:")
    print(f"  Total Rules: {gate_stats['total_rules']}")
    print(f"  Enabled Rules: {gate_stats['enabled_rules']}")
    print(f"  Total Requests: {gate_stats['total_requests']}")
    print(f"  Pending Requests: {gate_stats['pending_requests']}")
    print()
    
    # Agent Registry stats
    agent_stats = agent_registry.get_statistics()
    print(f"Agent Registry:")
    print(f"  Total Agents: {agent_stats['total_agents']}")
    print(f"  Available Agents: {agent_stats['available_agents']}")
    print(f"  Busy Agents: {agent_stats['busy_agents']}")
    print()
    
    print("=" * 70)
    print("Integration Example Complete!")
    print("=" * 70)


if __name__ == "__main__":
    example_complete_workflow()
