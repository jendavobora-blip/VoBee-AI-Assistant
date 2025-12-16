"""
Project Cortex - Core project management system.

Manages multiple projects with isolated memory, goals, and budget profiles.
Includes agent tracking and sleep/wake capabilities.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import uuid


class ProjectStatus(Enum):
    """Project lifecycle status."""
    ACTIVE = "active"
    SLEEPING = "sleeping"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class AgentStatus(Enum):
    """Agent activity status."""
    ACTIVE = "active"
    IDLE = "idle"
    SLEEPING = "sleeping"
    ERROR = "error"


class Project:
    """
    Represents a single project with isolated context.
    
    Each project maintains its own memory, goals, budget, and agent assignments.
    Projects can be put to sleep and woken up to manage resource allocation.
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        budget: Optional[float] = None,
        project_id: Optional[str] = None
    ):
        """
        Initialize a new project.
        
        Args:
            name: Project name
            description: Project description
            budget: Allocated budget for the project
            project_id: Unique identifier (auto-generated if not provided)
        """
        self.id = project_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.budget = budget
        self.status = ProjectStatus.ACTIVE
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Isolated project context
        self.memory: Dict[str, Any] = {}
        self.goals: List[Dict[str, Any]] = []
        self.budget_spent: float = 0.0
        
        # Agent tracking
        self.active_agents: Dict[str, Dict[str, Any]] = {}
        
    def add_goal(self, goal: str, priority: int = 1, metadata: Optional[Dict] = None) -> str:
        """
        Add a goal to the project.
        
        Args:
            goal: Goal description
            priority: Priority level (1=highest)
            metadata: Additional goal metadata
            
        Returns:
            Goal ID
        """
        goal_id = str(uuid.uuid4())
        self.goals.append({
            'id': goal_id,
            'description': goal,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now(),
            'metadata': metadata or {}
        })
        self.updated_at = datetime.now()
        return goal_id
    
    def update_memory(self, key: str, value: Any) -> None:
        """
        Update project memory with key-value pair.
        
        Args:
            key: Memory key
            value: Memory value
        """
        self.memory[key] = value
        self.updated_at = datetime.now()
    
    def get_memory(self, key: str, default: Any = None) -> Any:
        """
        Retrieve value from project memory.
        
        Args:
            key: Memory key
            default: Default value if key not found
            
        Returns:
            Stored value or default
        """
        return self.memory.get(key, default)
    
    def track_agent(self, agent_id: str, role: str, status: AgentStatus = AgentStatus.ACTIVE) -> None:
        """
        Track an active agent assigned to this project.
        
        Args:
            agent_id: Unique agent identifier
            role: Agent role (e.g., 'architect', 'backend_builder')
            status: Agent status
        """
        self.active_agents[agent_id] = {
            'role': role,
            'status': status.value,
            'assigned_at': datetime.now(),
            'last_active': datetime.now()
        }
        self.updated_at = datetime.now()
    
    def update_agent_status(self, agent_id: str, status: AgentStatus) -> None:
        """
        Update the status of a tracked agent.
        
        Args:
            agent_id: Agent identifier
            status: New agent status
        """
        if agent_id in self.active_agents:
            self.active_agents[agent_id]['status'] = status.value
            self.active_agents[agent_id]['last_active'] = datetime.now()
            self.updated_at = datetime.now()
    
    def remove_agent(self, agent_id: str) -> None:
        """
        Remove an agent from project tracking.
        
        Args:
            agent_id: Agent identifier
        """
        if agent_id in self.active_agents:
            del self.active_agents[agent_id]
            self.updated_at = datetime.now()
    
    def sleep(self) -> None:
        """Put the project to sleep to conserve resources."""
        self.status = ProjectStatus.SLEEPING
        # Put all active agents to sleep
        for agent_id in self.active_agents:
            self.active_agents[agent_id]['status'] = AgentStatus.SLEEPING.value
        self.updated_at = datetime.now()
    
    def wake(self) -> None:
        """Wake up the project from sleep."""
        self.status = ProjectStatus.ACTIVE
        # Wake up all sleeping agents
        for agent_id in self.active_agents:
            if self.active_agents[agent_id]['status'] == AgentStatus.SLEEPING.value:
                self.active_agents[agent_id]['status'] = AgentStatus.ACTIVE.value
        self.updated_at = datetime.now()
    
    def update_budget(self, amount: float) -> None:
        """
        Track budget expenditure.
        
        Args:
            amount: Amount spent
        """
        self.budget_spent += amount
        self.updated_at = datetime.now()
    
    def get_budget_remaining(self) -> Optional[float]:
        """
        Get remaining budget.
        
        Returns:
            Remaining budget or None if no budget set
        """
        if self.budget is None:
            return None
        return self.budget - self.budget_spent
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert project to dictionary representation.
        
        Returns:
            Dictionary with project data
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'budget': self.budget,
            'budget_spent': self.budget_spent,
            'budget_remaining': self.get_budget_remaining(),
            'goals': self.goals,
            'active_agents': self.active_agents,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class ProjectCortex:
    """
    Central management system for multiple projects.
    
    Provides capabilities for:
    - Managing multiple isolated projects
    - Resource allocation across projects
    - Project lifecycle management (sleep/wake)
    - Agent coordination across projects
    """
    
    def __init__(self):
        """Initialize the Project Cortex."""
        self.projects: Dict[str, Project] = {}
        self.created_at = datetime.now()
    
    def create_project(
        self,
        name: str,
        description: str = "",
        budget: Optional[float] = None
    ) -> Project:
        """
        Create a new project.
        
        Args:
            name: Project name
            description: Project description
            budget: Project budget
            
        Returns:
            Created project instance
        """
        project = Project(name=name, description=description, budget=budget)
        self.projects[project.id] = project
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """
        Retrieve a project by ID.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Project instance or None
        """
        return self.projects.get(project_id)
    
    def list_projects(self, status: Optional[ProjectStatus] = None) -> List[Project]:
        """
        List all projects, optionally filtered by status.
        
        Args:
            status: Filter by project status
            
        Returns:
            List of projects
        """
        if status:
            return [p for p in self.projects.values() if p.status == status]
        return list(self.projects.values())
    
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            True if deleted, False if not found
        """
        if project_id in self.projects:
            del self.projects[project_id]
            return True
        return False
    
    def sleep_project(self, project_id: str) -> bool:
        """
        Put a project to sleep.
        
        Args:
            project_id: Project identifier
            
        Returns:
            True if successful, False if project not found
        """
        project = self.get_project(project_id)
        if project:
            project.sleep()
            return True
        return False
    
    def wake_project(self, project_id: str) -> bool:
        """
        Wake a project from sleep.
        
        Args:
            project_id: Project identifier
            
        Returns:
            True if successful, False if project not found
        """
        project = self.get_project(project_id)
        if project:
            project.wake()
            return True
        return False
    
    def get_active_projects_count(self) -> int:
        """
        Get count of active projects.
        
        Returns:
            Number of active projects
        """
        return len([p for p in self.projects.values() if p.status == ProjectStatus.ACTIVE])
    
    def get_total_budget_spent(self) -> float:
        """
        Get total budget spent across all projects.
        
        Returns:
            Total budget spent
        """
        return sum(p.budget_spent for p in self.projects.values())
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert cortex state to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'total_projects': len(self.projects),
            'active_projects': self.get_active_projects_count(),
            'total_budget_spent': self.get_total_budget_spent(),
            'projects': {pid: p.to_dict() for pid, p in self.projects.items()},
            'created_at': self.created_at.isoformat()
        }
