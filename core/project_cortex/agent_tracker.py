"""
Agent Tracker - Manages agent assignments and activity for projects
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentTracker:
    """
    Tracks active agents and their assignments to projects
    Monitors agent activity and performance
    """
    
    def __init__(self):
        self.project_agents: Dict[str, List[Dict[str, Any]]] = {}
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        logger.info("AgentTracker initialized")
    
    def register_agent(
        self,
        agent_id: str,
        role: str,
        capabilities: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Register an agent in the system
        
        Args:
            agent_id: Unique agent identifier
            role: Agent role/type
            capabilities: List of agent capabilities
            metadata: Additional agent information
        """
        self.agent_registry[agent_id] = {
            'agent_id': agent_id,
            'role': role,
            'capabilities': capabilities,
            'status': 'available',
            'metadata': metadata or {},
            'registered_at': datetime.utcnow().isoformat(),
            'total_assignments': 0,
            'current_projects': []
        }
        
        logger.info(f"Registered agent {agent_id} with role '{role}'")
    
    def assign_agent_to_project(
        self,
        project_id: str,
        agent_id: str,
        assignment_details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Assign an agent to a project
        
        Args:
            project_id: Project identifier
            agent_id: Agent identifier
            assignment_details: Additional assignment information
            
        Returns:
            True if assignment successful
        """
        if agent_id not in self.agent_registry:
            logger.error(f"Agent {agent_id} not found in registry")
            return False
        
        # Initialize project agent list if needed
        if project_id not in self.project_agents:
            self.project_agents[project_id] = []
        
        # Check if already assigned
        for assignment in self.project_agents[project_id]:
            if assignment['agent_id'] == agent_id:
                logger.warning(
                    f"Agent {agent_id} already assigned to project {project_id}"
                )
                return False
        
        # Create assignment
        assignment = {
            'agent_id': agent_id,
            'role': self.agent_registry[agent_id]['role'],
            'assigned_at': datetime.utcnow().isoformat(),
            'status': 'active',
            'tasks_completed': 0,
            'last_activity': datetime.utcnow().isoformat(),
            'details': assignment_details or {}
        }
        
        self.project_agents[project_id].append(assignment)
        
        # Update agent registry
        self.agent_registry[agent_id]['total_assignments'] += 1
        self.agent_registry[agent_id]['current_projects'].append(project_id)
        self.agent_registry[agent_id]['status'] = 'assigned'
        
        logger.info(
            f"Assigned agent {agent_id} to project {project_id}"
        )
        
        return True
    
    def unassign_agent_from_project(
        self,
        project_id: str,
        agent_id: str
    ) -> bool:
        """Remove agent assignment from a project"""
        if project_id not in self.project_agents:
            return False
        
        # Find and remove assignment
        initial_count = len(self.project_agents[project_id])
        self.project_agents[project_id] = [
            a for a in self.project_agents[project_id]
            if a['agent_id'] != agent_id
        ]
        
        if len(self.project_agents[project_id]) < initial_count:
            # Update agent registry
            if agent_id in self.agent_registry:
                if project_id in self.agent_registry[agent_id]['current_projects']:
                    self.agent_registry[agent_id]['current_projects'].remove(project_id)
                
                # Update status if no more projects
                if not self.agent_registry[agent_id]['current_projects']:
                    self.agent_registry[agent_id]['status'] = 'available'
            
            logger.info(
                f"Unassigned agent {agent_id} from project {project_id}"
            )
            return True
        
        return False
    
    def get_project_agents(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all agents assigned to a project"""
        return self.project_agents.get(project_id, [])
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific agent"""
        return self.agent_registry.get(agent_id)
    
    def get_active_agents(self) -> List[Dict[str, Any]]:
        """Get all currently active/assigned agents"""
        return [
            agent for agent in self.agent_registry.values()
            if agent['status'] == 'assigned'
        ]
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get all available agents"""
        return [
            agent for agent in self.agent_registry.values()
            if agent['status'] == 'available'
        ]
    
    def update_agent_activity(
        self,
        project_id: str,
        agent_id: str,
        task_completed: bool = False
    ):
        """Update agent activity timestamp"""
        if project_id not in self.project_agents:
            return
        
        for assignment in self.project_agents[project_id]:
            if assignment['agent_id'] == agent_id:
                assignment['last_activity'] = datetime.utcnow().isoformat()
                if task_completed:
                    assignment['tasks_completed'] += 1
                break
    
    def get_agent_performance(
        self,
        agent_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get performance metrics for an agent"""
        if agent_id not in self.agent_registry:
            return None
        
        agent = self.agent_registry[agent_id]
        
        # Calculate total tasks across all projects
        total_tasks = 0
        for project_id in agent['current_projects']:
            if project_id in self.project_agents:
                for assignment in self.project_agents[project_id]:
                    if assignment['agent_id'] == agent_id:
                        total_tasks += assignment['tasks_completed']
        
        return {
            'agent_id': agent_id,
            'role': agent['role'],
            'status': agent['status'],
            'total_assignments': agent['total_assignments'],
            'current_project_count': len(agent['current_projects']),
            'total_tasks_completed': total_tasks,
            'registered_at': agent['registered_at']
        }
    
    def get_tracker_summary(self) -> Dict[str, Any]:
        """Get summary of all tracked agents"""
        total_agents = len(self.agent_registry)
        active_agents = len(self.get_active_agents())
        available_agents = len(self.get_available_agents())
        
        return {
            'total_agents': total_agents,
            'active_agents': active_agents,
            'available_agents': available_agents,
            'total_projects_with_agents': len(self.project_agents),
            'timestamp': datetime.utcnow().isoformat()
        }
