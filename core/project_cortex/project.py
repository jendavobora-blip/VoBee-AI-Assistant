"""
Project Entity - Represents a single project with isolated context
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
import json


class ProjectStatus(Enum):
    """Project lifecycle states"""
    ACTIVE = "active"
    SLEEPING = "sleeping"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project:
    """
    Individual project with isolated memory, goals, budget, and agents
    Supports sleep/wake capabilities for resource optimization
    """
    
    def __init__(
        self,
        project_id: str,
        name: str,
        description: str = "",
        budget: Optional[Dict[str, Any]] = None,
        goals: Optional[List[str]] = None
    ):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.status = ProjectStatus.ACTIVE
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
        self.last_active_at = datetime.utcnow().isoformat()
        
        # Isolated project context
        self.memory = {}  # Project-specific memory storage
        self.goals = goals or []  # Project objectives
        self.budget = budget or {
            'total': 0,
            'spent': 0,
            'remaining': 0,
            'currency': 'USD'
        }
        self.active_agents = []  # Agents assigned to this project
        self.metadata = {}  # Additional project metadata
        
        # Sleep/wake tracking
        self.sleep_count = 0
        self.wake_count = 0
        self.total_sleep_duration = 0  # in seconds
    
    def sleep(self):
        """Put project into sleep mode to free resources"""
        if self.status == ProjectStatus.ACTIVE:
            self.status = ProjectStatus.SLEEPING
            self.sleep_count += 1
            self.updated_at = datetime.utcnow().isoformat()
            return True
        return False
    
    def wake(self):
        """Wake project from sleep mode"""
        if self.status == ProjectStatus.SLEEPING:
            self.status = ProjectStatus.ACTIVE
            self.wake_count += 1
            self.last_active_at = datetime.utcnow().isoformat()
            self.updated_at = datetime.utcnow().isoformat()
            return True
        return False
    
    def is_active(self) -> bool:
        """Check if project is actively running"""
        return self.status == ProjectStatus.ACTIVE
    
    def is_sleeping(self) -> bool:
        """Check if project is in sleep mode"""
        return self.status == ProjectStatus.SLEEPING
    
    def add_goal(self, goal: str):
        """Add a new goal to the project"""
        if goal not in self.goals:
            self.goals.append(goal)
            self.updated_at = datetime.utcnow().isoformat()
    
    def remove_goal(self, goal: str):
        """Remove a goal from the project"""
        if goal in self.goals:
            self.goals.remove(goal)
            self.updated_at = datetime.utcnow().isoformat()
    
    def update_budget(self, amount: float, operation: str = "spend"):
        """Update project budget"""
        if operation == "spend":
            self.budget['spent'] += amount
            self.budget['remaining'] = self.budget['total'] - self.budget['spent']
        elif operation == "add":
            self.budget['total'] += amount
            self.budget['remaining'] = self.budget['total'] - self.budget['spent']
        self.updated_at = datetime.utcnow().isoformat()
    
    def assign_agent(self, agent_id: str, agent_role: str):
        """Assign an agent to this project"""
        agent_info = {
            'agent_id': agent_id,
            'role': agent_role,
            'assigned_at': datetime.utcnow().isoformat()
        }
        if agent_info not in self.active_agents:
            self.active_agents.append(agent_info)
            self.updated_at = datetime.utcnow().isoformat()
    
    def unassign_agent(self, agent_id: str):
        """Remove an agent from this project"""
        self.active_agents = [
            agent for agent in self.active_agents 
            if agent['agent_id'] != agent_id
        ]
        self.updated_at = datetime.utcnow().isoformat()
    
    def store_memory(self, key: str, value: Any):
        """Store data in project-specific memory"""
        self.memory[key] = {
            'value': value,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.updated_at = datetime.utcnow().isoformat()
    
    def retrieve_memory(self, key: str) -> Optional[Any]:
        """Retrieve data from project-specific memory"""
        if key in self.memory:
            return self.memory[key]['value']
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary representation"""
        return {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_active_at': self.last_active_at,
            'memory': self.memory,
            'goals': self.goals,
            'budget': self.budget,
            'active_agents': self.active_agents,
            'metadata': self.metadata,
            'sleep_count': self.sleep_count,
            'wake_count': self.wake_count,
            'total_sleep_duration': self.total_sleep_duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create project instance from dictionary"""
        project = cls(
            project_id=data['project_id'],
            name=data['name'],
            description=data.get('description', ''),
            budget=data.get('budget'),
            goals=data.get('goals')
        )
        project.status = ProjectStatus(data.get('status', 'active'))
        project.created_at = data.get('created_at', project.created_at)
        project.updated_at = data.get('updated_at', project.updated_at)
        project.last_active_at = data.get('last_active_at', project.last_active_at)
        project.memory = data.get('memory', {})
        project.active_agents = data.get('active_agents', [])
        project.metadata = data.get('metadata', {})
        project.sleep_count = data.get('sleep_count', 0)
        project.wake_count = data.get('wake_count', 0)
        project.total_sleep_duration = data.get('total_sleep_duration', 0)
        return project
