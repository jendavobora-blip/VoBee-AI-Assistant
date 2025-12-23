"""
Project Cortex - Multi-Project Management System

This module provides the core functionality for managing multiple projects
with isolated memory, goals, budget profiles, and active agent tracking.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from uuid import uuid4
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ProjectStatus(Enum):
    """Project status enumeration"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class BudgetProfile:
    """Budget profile for a project"""
    total_budget: float = 0.0
    currency: str = "USD"
    spent: float = 0.0
    allocated: Dict[str, float] = field(default_factory=dict)
    
    def remaining(self) -> float:
        """Calculate remaining budget"""
        return self.total_budget - self.spent
    
    def allocate(self, category: str, amount: float) -> bool:
        """Allocate budget to a category"""
        if amount > self.remaining():
            return False
        self.allocated[category] = self.allocated.get(category, 0) + amount
        return True
    
    def spend(self, amount: float, category: Optional[str] = None) -> bool:
        """Record spending"""
        if amount > self.remaining():
            return False
        self.spent += amount
        if category and category in self.allocated:
            self.allocated[category] = max(0, self.allocated[category] - amount)
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "total_budget": self.total_budget,
            "currency": self.currency,
            "spent": self.spent,
            "remaining": self.remaining(),
            "allocated": self.allocated
        }


@dataclass
class ProjectGoal:
    """Individual goal within a project"""
    goal_id: str = field(default_factory=lambda: str(uuid4()))
    description: str = ""
    priority: int = 1
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None
    
    def complete(self):
        """Mark goal as completed"""
        self.completed = True
        self.completed_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class AgentAssignment:
    """Agent assignment to a project"""
    agent_id: str
    role: str
    status: str = "active"
    assigned_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tasks_completed: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class Project:
    """
    Represents a single project with isolated memory, goals, budget, and agents.
    
    Each project maintains:
    - Unique ID and metadata
    - Isolated memory/context
    - Goals and objectives
    - Budget profile
    - Active agent tracking
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        project_id: Optional[str] = None
    ):
        self.project_id = project_id or str(uuid4())
        self.name = name
        self.description = description
        self.status = ProjectStatus.ACTIVE
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
        
        # Isolated memory/context for this project
        self.memory: Dict[str, Any] = {}
        
        # Project goals
        self.goals: List[ProjectGoal] = []
        
        # Budget profile
        self.budget = BudgetProfile()
        
        # Active agents assigned to this project
        self.agents: Dict[str, AgentAssignment] = {}
        
        logger.info(f"Created new project: {self.name} (ID: {self.project_id})")
    
    def add_goal(self, description: str, priority: int = 1) -> ProjectGoal:
        """Add a new goal to the project"""
        goal = ProjectGoal(description=description, priority=priority)
        self.goals.append(goal)
        self._update_timestamp()
        logger.info(f"Added goal to project {self.name}: {description}")
        return goal
    
    def complete_goal(self, goal_id: str) -> bool:
        """Mark a goal as completed"""
        for goal in self.goals:
            if goal.goal_id == goal_id:
                goal.complete()
                self._update_timestamp()
                logger.info(f"Completed goal {goal_id} in project {self.name}")
                return True
        return False
    
    def assign_agent(self, agent_id: str, role: str) -> bool:
        """Assign an agent to this project"""
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} already assigned to project {self.name}")
            return False
        
        self.agents[agent_id] = AgentAssignment(agent_id=agent_id, role=role)
        self._update_timestamp()
        logger.info(f"Assigned agent {agent_id} ({role}) to project {self.name}")
        return True
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from this project"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self._update_timestamp()
            logger.info(f"Removed agent {agent_id} from project {self.name}")
            return True
        return False
    
    def update_agent_status(self, agent_id: str, status: str) -> bool:
        """Update agent status"""
        if agent_id in self.agents:
            self.agents[agent_id].status = status
            self._update_timestamp()
            return True
        return False
    
    def increment_agent_tasks(self, agent_id: str) -> bool:
        """Increment completed tasks for an agent"""
        if agent_id in self.agents:
            self.agents[agent_id].tasks_completed += 1
            self._update_timestamp()
            return True
        return False
    
    def set_budget(self, total: float, currency: str = "USD"):
        """Set the project budget"""
        self.budget.total_budget = total
        self.budget.currency = currency
        self._update_timestamp()
        logger.info(f"Set budget for project {self.name}: {total} {currency}")
    
    def store_memory(self, key: str, value: Any):
        """Store data in project memory"""
        self.memory[key] = value
        self._update_timestamp()
    
    def retrieve_memory(self, key: str, default: Any = None) -> Any:
        """Retrieve data from project memory"""
        return self.memory.get(key, default)
    
    def clear_memory(self):
        """Clear project memory"""
        self.memory.clear()
        self._update_timestamp()
        logger.info(f"Cleared memory for project {self.name}")
    
    def change_status(self, status: ProjectStatus):
        """Change project status"""
        self.status = status
        self._update_timestamp()
        logger.info(f"Changed status of project {self.name} to {status.value}")
    
    def get_active_agents(self) -> List[AgentAssignment]:
        """Get all active agents"""
        return [
            agent for agent in self.agents.values()
            if agent.status == "active"
        ]
    
    def get_pending_goals(self) -> List[ProjectGoal]:
        """Get all pending (incomplete) goals"""
        return [goal for goal in self.goals if not goal.completed]
    
    def _update_timestamp(self):
        """Update the last modified timestamp"""
        self.updated_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "goals": [goal.to_dict() for goal in self.goals],
            "budget": self.budget.to_dict(),
            "agents": {
                agent_id: agent.to_dict()
                for agent_id, agent in self.agents.items()
            },
            "memory_keys": list(self.memory.keys())
        }


class ProjectManager:
    """
    Central manager for all projects in the system.
    
    Provides:
    - Project creation and lifecycle management
    - Project isolation and context switching
    - Cross-project resource tracking
    - Persistence and state management
    """
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self.active_project_id: Optional[str] = None
        logger.info("ProjectManager initialized")
    
    def create_project(
        self,
        name: str,
        description: str = "",
        budget: float = 0.0,
        currency: str = "USD"
    ) -> Project:
        """Create a new project"""
        project = Project(name=name, description=description)
        if budget > 0:
            project.set_budget(budget, currency)
        
        self.projects[project.project_id] = project
        
        # Set as active if it's the first project
        if self.active_project_id is None:
            self.active_project_id = project.project_id
        
        logger.info(f"Created project: {name} (ID: {project.project_id})")
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID"""
        return self.projects.get(project_id)
    
    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name"""
        for project in self.projects.values():
            if project.name == name:
                return project
        return None
    
    def list_projects(self, status: Optional[ProjectStatus] = None) -> List[Project]:
        """List all projects, optionally filtered by status"""
        if status:
            return [
                p for p in self.projects.values()
                if p.status == status
            ]
        return list(self.projects.values())
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        if project_id in self.projects:
            project_name = self.projects[project_id].name
            del self.projects[project_id]
            
            # Update active project if deleted
            if self.active_project_id == project_id:
                self.active_project_id = None
                if self.projects:
                    self.active_project_id = next(iter(self.projects.keys()))
            
            logger.info(f"Deleted project: {project_name} (ID: {project_id})")
            return True
        return False
    
    def set_active_project(self, project_id: str) -> bool:
        """Set the active project"""
        if project_id in self.projects:
            self.active_project_id = project_id
            logger.info(f"Set active project to: {self.projects[project_id].name}")
            return True
        return False
    
    def get_active_project(self) -> Optional[Project]:
        """Get the currently active project"""
        if self.active_project_id:
            return self.projects.get(self.active_project_id)
        return None
    
    def get_all_active_agents(self) -> Dict[str, List[AgentAssignment]]:
        """Get all active agents across all projects"""
        result = {}
        for project_id, project in self.projects.items():
            active = project.get_active_agents()
            if active:
                result[project_id] = active
        return result
    
    def save_state(self, filepath: str):
        """Save all projects to a JSON file"""
        state = {
            "active_project_id": self.active_project_id,
            "projects": {
                project_id: project.to_dict()
                for project_id, project in self.projects.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Saved ProjectManager state to {filepath}")
    
    def load_state(self, filepath: str):
        """Load projects from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
            
            self.active_project_id = state.get("active_project_id")
            self.projects.clear()
            
            for project_id, project_data in state.get("projects", {}).items():
                project = Project(
                    name=project_data["name"],
                    description=project_data["description"],
                    project_id=project_id
                )
                
                project.status = ProjectStatus(project_data["status"])
                project.created_at = project_data["created_at"]
                project.updated_at = project_data["updated_at"]
                
                # Restore budget
                budget_data = project_data.get("budget", {})
                project.budget = BudgetProfile(
                    total_budget=budget_data.get("total_budget", 0.0),
                    currency=budget_data.get("currency", "USD"),
                    spent=budget_data.get("spent", 0.0),
                    allocated=budget_data.get("allocated", {})
                )
                
                # Restore goals
                for goal_data in project_data.get("goals", []):
                    goal = ProjectGoal(**goal_data)
                    project.goals.append(goal)
                
                # Restore agents
                for agent_id, agent_data in project_data.get("agents", {}).items():
                    project.agents[agent_id] = AgentAssignment(**agent_data)
                
                self.projects[project_id] = project
            
            logger.info(f"Loaded ProjectManager state from {filepath}")
            logger.info(f"Loaded {len(self.projects)} projects")
        
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            raise
