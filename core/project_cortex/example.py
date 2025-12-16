"""
Example: Using Project Cortex

This example demonstrates how to use the Project Cortex system
for managing multiple projects with isolated contexts.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.project_cortex import ProjectManager, Project

def main():
    # Initialize the project manager
    manager = ProjectManager()
    
    # Create projects
    project1 = manager.create_project(
        name="Website Redesign",
        description="Redesign company website with modern UI",
        budget=50000,
        currency="USD"
    )
    
    project2 = manager.create_project(
        name="Mobile App Development",
        description="Build native mobile application",
        budget=100000,
        currency="USD"
    )
    
    # Add goals to projects
    project1.add_goal("Create wireframes", priority=1)
    project1.add_goal("Implement new design", priority=2)
    project1.add_goal("User testing", priority=3)
    
    project2.add_goal("Setup development environment", priority=1)
    project2.add_goal("Implement core features", priority=2)
    
    # Assign agents to projects
    project1.assign_agent("agent-001", "UI Designer")
    project1.assign_agent("agent-002", "Frontend Developer")
    
    project2.assign_agent("agent-003", "Mobile Developer")
    
    # Store project-specific memory
    project1.store_memory("design_system", {"primary_color": "#007bff"})
    project2.store_memory("target_platforms", ["iOS", "Android"])
    
    # Spend some budget
    project1.budget.spend(5000, "design")
    
    # Print project status
    print(f"Active Project: {manager.get_active_project().name}")
    print(f"\nTotal Projects: {len(manager.list_projects())}")
    
    for project in manager.list_projects():
        print(f"\nProject: {project.name}")
        print(f"  Budget Remaining: ${project.budget.remaining()}")
        print(f"  Goals: {len(project.goals)} total, {len(project.get_pending_goals())} pending")
        print(f"  Active Agents: {len(project.get_active_agents())}")
    
    # Save state
    manager.save_state("/tmp/project_cortex_state.json")
    print("\nState saved to /tmp/project_cortex_state.json")


if __name__ == "__main__":
    main()
