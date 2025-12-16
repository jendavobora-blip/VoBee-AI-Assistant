"""
Base Agent - Abstract base class for all agents
Placeholder structure with no hard-wired vendor dependencies
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system
    Provides common interface and functionality
    No vendor-specific implementations - placeholder structure only
    """
    
    def __init__(
        self,
        agent_id: str,
        role: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize base agent
        
        Args:
            agent_id: Unique identifier for the agent
            role: Role definition from AgentRole
            config: Optional configuration dictionary
        """
        self.agent_id = agent_id
        self.role = role
        self.config = config or {}
        self.status = "initialized"
        self.created_at = datetime.utcnow().isoformat()
        self.last_activity = datetime.utcnow().isoformat()
        self.task_history: List[Dict[str, Any]] = []
        
        logger.info(
            f"Initialized agent {agent_id} with role '{role['name']}'"
        )
    
    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task assigned to this agent
        
        Args:
            task: Task definition with parameters
            
        Returns:
            Task execution result
        """
        pass
    
    @abstractmethod
    def validate_capability(self, capability: str) -> bool:
        """
        Check if agent has a specific capability
        
        Args:
            capability: Capability to check
            
        Returns:
            True if agent has the capability
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            'agent_id': self.agent_id,
            'role': self.role['name'],
            'category': self.role['category'].value,
            'status': self.status,
            'capabilities': self.role['capabilities'],
            'required_skills': self.role['required_skills'],
            'created_at': self.created_at,
            'last_activity': self.last_activity,
            'total_tasks': len(self.task_history)
        }
    
    def update_status(self, status: str):
        """Update agent status"""
        self.status = status
        self.last_activity = datetime.utcnow().isoformat()
        logger.info(f"Agent {self.agent_id} status updated to '{status}'")
    
    def record_task(self, task: Dict[str, Any], result: Dict[str, Any]):
        """Record task execution in history"""
        task_record = {
            'task': task,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.task_history.append(task_record)
        self.last_activity = datetime.utcnow().isoformat()
    
    def get_task_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get task execution history"""
        if limit:
            return self.task_history[-limit:]
        return self.task_history
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        return self.role['capabilities']
    
    def get_required_skills(self) -> List[str]:
        """Get list of required skills"""
        return self.role['required_skills']


class PlaceholderAgent(BaseAgent):
    """
    Placeholder agent implementation for demonstration
    No vendor-specific code - can be replaced with actual implementations
    """
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Placeholder task execution
        
        In a real implementation, this would call vendor-specific APIs
        or execute actual agent logic
        """
        self.update_status("executing")
        
        result = {
            'status': 'completed',
            'message': f'Task executed by {self.role["name"]}',
            'task_id': task.get('task_id', 'unknown'),
            'timestamp': datetime.utcnow().isoformat(),
            'note': 'This is a placeholder implementation'
        }
        
        self.record_task(task, result)
        self.update_status("ready")
        
        return result
    
    def validate_capability(self, capability: str) -> bool:
        """Check if agent has a capability"""
        return capability in self.role['capabilities']
