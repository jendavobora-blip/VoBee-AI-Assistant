"""
Example: Using Agent Registry

This example demonstrates how to use the Agent Registry system
for managing multiple agent roles and instances.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import AgentRegistry, AgentCapability
from agents.roles import initialize_default_roles

def main():
    # Initialize the registry
    registry = AgentRegistry()
    
    # Load predefined roles
    initialize_default_roles(registry)
    
    print(f"Loaded {len(registry.list_roles())} predefined roles")
    
    # Create custom agents
    research_role = registry.get_role_by_name("ResearchAnalyst")
    if research_role:
        agent1 = registry.create_agent(
            name="Research Agent Alpha",
            role_id=research_role.role_id,
            skills={"research", "analysis", "web-scraping"}
        )
        print(f"\nCreated agent: {agent1.name}")
    
    dev_role = registry.get_role_by_name("SoftwareEngineer")
    if dev_role:
        agent2 = registry.create_agent(
            name="Developer Agent Beta",
            role_id=dev_role.role_id,
            skills={"programming", "python", "testing", "software-design"}
        )
        print(f"Created agent: {agent2.name}")
    
    pm_role = registry.get_role_by_name("ProjectManager")
    if pm_role:
        agent3 = registry.create_agent(
            name="PM Agent Gamma",
            role_id=pm_role.role_id,
            skills={"planning", "coordination", "resource-management"}
        )
        print(f"Created agent: {agent3.name}")
    
    # Find agents by capability
    print("\n--- Finding agents by capability ---")
    roles = registry.find_roles_by_capability("code_development")
    print(f"Roles with code_development capability: {[r.name for r in roles]}")
    
    # Assign tasks
    print("\n--- Assigning tasks ---")
    task1 = "task-001"
    assigned_agent = registry.assign_task(
        task_id=task1,
        capability="code_development"
    )
    if assigned_agent:
        print(f"Task {task1} assigned to: {assigned_agent.name}")
    
    task2 = "task-002"
    assigned_agent = registry.assign_task(
        task_id=task2,
        role_id=research_role.role_id
    )
    if assigned_agent:
        print(f"Task {task2} assigned to: {assigned_agent.name}")
    
    # Complete a task
    if agent2:
        registry.complete_task(agent2.agent_id, task1)
        print(f"\nTask {task1} completed by {agent2.name}")
    
    # Get statistics
    stats = registry.get_statistics()
    print("\n--- Registry Statistics ---")
    print(f"Total Roles: {stats['total_roles']}")
    print(f"Total Agents: {stats['total_agents']}")
    print(f"Agents by Status: {stats['agents_by_status']}")
    print(f"Tasks Completed: {stats['total_tasks_completed']}")
    print(f"Active Tasks: {stats['active_tasks']}")
    
    # List all agents
    print("\n--- All Agents ---")
    for agent in registry.list_agents():
        print(f"{agent.name}:")
        print(f"  Role: {registry.get_role(agent.role_id).name}")
        print(f"  Status: {agent.status.value}")
        print(f"  Skills: {', '.join(agent.skills)}")
        print(f"  Completed Tasks: {agent.completed_tasks}")
    
    # Save state
    registry.save_state("/tmp/agent_registry_state.json")
    print("\nState saved to /tmp/agent_registry_state.json")


if __name__ == "__main__":
    main()
