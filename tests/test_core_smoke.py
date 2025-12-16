"""
Basic smoke tests for VoBee Core Architecture components.

Tests the foundational functionality of:
- Project Cortex
- Decision Gate
- Agent Registry
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.project_cortex import ProjectCortex, Project, ProjectStatus, AgentStatus as ProjectAgentStatus
from core.decision_gate import DecisionGate, GateRule, GateRulePriority, GateDecision
from agents import AgentRegistry, Agent, AgentRole, AgentStatus


def test_project_cortex_basic():
    """Test basic Project Cortex functionality."""
    print("Testing Project Cortex...")
    
    cortex = ProjectCortex()
    
    # Test project creation
    project = cortex.create_project(
        name="Test Project",
        description="A test project",
        budget=1000.0
    )
    assert project.name == "Test Project"
    assert project.budget == 1000.0
    assert project.status == ProjectStatus.ACTIVE
    
    # Test goal management
    goal_id = project.add_goal("Test goal", priority=1)
    assert len(project.goals) == 1
    assert project.goals[0]['description'] == "Test goal"
    
    # Test memory operations
    project.update_memory("key1", "value1")
    assert project.get_memory("key1") == "value1"
    assert project.get_memory("nonexistent", "default") == "default"
    
    # Test budget tracking
    project.update_budget(100.0)
    assert project.budget_spent == 100.0
    assert project.get_budget_remaining() == 900.0
    
    # Test sleep/wake
    project.sleep()
    assert project.status == ProjectStatus.SLEEPING
    project.wake()
    assert project.status == ProjectStatus.ACTIVE
    
    # Test agent tracking
    project.track_agent("agent-1", "tester", ProjectAgentStatus.ACTIVE)
    assert "agent-1" in project.active_agents
    project.remove_agent("agent-1")
    assert "agent-1" not in project.active_agents
    
    # Test cortex operations
    assert cortex.get_project(project.id) == project
    assert len(cortex.list_projects()) == 1
    assert cortex.get_active_projects_count() == 1
    
    print("  ✓ Project Cortex tests passed")


def test_decision_gate_basic():
    """Test basic Decision Gate functionality."""
    print("Testing Decision Gate...")
    
    gate = DecisionGate()
    
    # Test rule creation and management
    rule = GateRule(
        name="Test Rule",
        description="A test rule",
        priority=GateRulePriority.MEDIUM
    )
    
    def test_eval(context):
        return context.get('approved', False)
    
    rule.set_evaluation_function(test_eval)
    gate.add_rule(rule)
    
    assert len(gate.list_rules()) == 1
    assert gate.get_rule(rule.id) == rule
    
    # Test request approval
    request = gate.request_approval(
        action="test_action",
        description="Test action",
        context={'approved': True}
    )
    assert request.decision == GateDecision.PENDING
    
    # Test evaluation
    decision = gate.evaluate_request(request.id)
    assert decision == GateDecision.APPROVED
    
    # Test rejection
    reject_request = gate.request_approval(
        action="test_action_2",
        description="Test action 2",
        context={'approved': False}
    )
    decision2 = gate.evaluate_request(reject_request.id)
    assert decision2 == GateDecision.REJECTED
    
    # Test manual approval
    manual_request = gate.request_approval(
        action="manual_test",
        description="Manual test"
    )
    gate.approve_request(manual_request.id, "Manual approval")
    assert manual_request.decision == GateDecision.APPROVED
    
    # Test auto-approve mode
    auto_gate = DecisionGate(auto_approve_mode=True)
    auto_request = auto_gate.request_approval(
        action="auto_test",
        description="Auto test"
    )
    assert auto_request.decision == GateDecision.BYPASSED
    
    print("  ✓ Decision Gate tests passed")


def test_agent_registry_basic():
    """Test basic Agent Registry functionality."""
    print("Testing Agent Registry...")
    
    registry = AgentRegistry()
    
    # Test agent creation and registration
    agent = Agent(
        name="Test Agent",
        role=AgentRole.BACKEND_BUILDER,
        description="A test agent"
    )
    
    # Test capabilities
    cap = agent.add_capability("python", "Python programming", proficiency=8)
    assert len(agent.capabilities) == 1
    assert agent.has_capability("python", min_proficiency=7)
    assert not agent.has_capability("python", min_proficiency=9)
    assert not agent.has_capability("nonexistent")
    
    # Test secondary roles
    agent.add_secondary_role(AgentRole.FULL_STACK_BUILDER)
    assert AgentRole.FULL_STACK_BUILDER in agent.secondary_roles
    assert len(agent.get_all_roles()) == 2
    
    # Register agent
    registry.register_agent(agent)
    assert registry.get_agent(agent.id) == agent
    
    # Test role-based search
    agents = registry.find_agents_by_role(AgentRole.BACKEND_BUILDER)
    assert len(agents) == 1
    assert agents[0] == agent
    
    # Test capability-based search
    python_agents = registry.find_agents_by_capability("python", min_proficiency=7)
    assert len(python_agents) == 1
    
    # Test task assignment
    assert agent.status == AgentStatus.AVAILABLE
    agent.assign_task("task-1", "project-1")
    assert agent.status == AgentStatus.BUSY
    assert agent.current_task == "task-1"
    agent.complete_task()
    assert agent.status == AgentStatus.AVAILABLE
    assert agent.tasks_completed == 1
    
    # Test finding available agents
    agent2 = Agent(
        name="Test Agent 2",
        role=AgentRole.BACKEND_BUILDER,
        description="Another test agent"
    )
    agent2.add_capability("python", "Python programming", proficiency=9)
    registry.register_agent(agent2)
    
    available = registry.find_available_agent(
        role=AgentRole.BACKEND_BUILDER,
        required_capabilities=["python"]
    )
    assert available is not None
    assert available.status == AgentStatus.AVAILABLE
    
    # Test statistics
    stats = registry.get_statistics()
    assert stats['total_agents'] == 2
    assert stats['available_agents'] == 2
    
    # Test unregistration
    registry.unregister_agent(agent.id)
    assert registry.get_agent(agent.id) is None
    
    print("  ✓ Agent Registry tests passed")


def test_integration():
    """Test integration between all three systems."""
    print("Testing Integration...")
    
    cortex = ProjectCortex()
    gate = DecisionGate()
    registry = AgentRegistry()
    
    # Create and register an agent
    agent = Agent(
        name="Integration Agent",
        role=AgentRole.ARCHITECT,
        description="Test architect"
    )
    registry.register_agent(agent)
    
    # Create a rule that checks agent availability
    rule = GateRule(
        name="Agent Check",
        description="Check if architect is available",
        priority=GateRulePriority.HIGH
    )
    
    def check_agent_available(context):
        agents = registry.find_agents_by_role(AgentRole.ARCHITECT, status=AgentStatus.AVAILABLE)
        return len(agents) > 0
    
    rule.set_evaluation_function(check_agent_available)
    gate.add_rule(rule)
    
    # Request approval
    request = gate.request_approval(
        action="create_architecture_project",
        description="Create new architecture project"
    )
    
    decision = gate.evaluate_request(request.id)
    assert decision == GateDecision.APPROVED
    
    # Create project if approved
    if decision == GateDecision.APPROVED:
        project = cortex.create_project(
            name="Architecture Project",
            description="Test project",
            budget=5000.0
        )
        
        # Assign agent to project
        agent.assign_task("architecture-task", project.id)
        project.track_agent(agent.id, "architect", ProjectAgentStatus.ACTIVE)
        
        assert len(project.active_agents) == 1
        assert agent.status == AgentStatus.BUSY
        assert agent.assigned_project == project.id
    
    print("  ✓ Integration tests passed")


def run_all_tests():
    """Run all smoke tests."""
    print("=" * 70)
    print("Running VoBee Core Architecture Smoke Tests")
    print("=" * 70)
    print()
    
    try:
        test_project_cortex_basic()
        test_decision_gate_basic()
        test_agent_registry_basic()
        test_integration()
        
        print()
        print("=" * 70)
        print("All Tests Passed! ✓")
        print("=" * 70)
        return 0
    except AssertionError as e:
        print()
        print("=" * 70)
        print(f"Test Failed! ✗")
        print(f"Error: {e}")
        print("=" * 70)
        return 1
    except Exception as e:
        print()
        print("=" * 70)
        print(f"Test Error! ✗")
        print(f"Error: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(run_all_tests())
