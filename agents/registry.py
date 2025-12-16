"""
Agent Registry - Role-based Multi-Agent System

This module provides a flexible, extensible system for managing multiple
agent roles without hard-coding API dependencies.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Callable
from uuid import uuid4
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status enumeration"""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


@dataclass
class AgentCapability:
    """
    Represents a capability that an agent can perform.
    """
    name: str
    description: str
    required_skills: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class AgentRole:
    """
    Defines a logical role in the system.
    
    Roles are independent of specific API implementations.
    """
    role_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    capabilities: List[AgentCapability] = field(default_factory=list)
    required_skills: Set[str] = field(default_factory=set)
    priority: int = 1
    max_concurrent_tasks: int = 1
    
    def add_capability(self, capability: AgentCapability):
        """Add a capability to this role"""
        self.capabilities.append(capability)
        self.required_skills.update(capability.required_skills)
    
    def can_perform(self, capability_name: str) -> bool:
        """Check if this role can perform a capability"""
        return any(c.name == capability_name for c in self.capabilities)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "role_id": self.role_id,
            "name": self.name,
            "description": self.description,
            "capabilities": [c.to_dict() for c in self.capabilities],
            "required_skills": list(self.required_skills),
            "priority": self.priority,
            "max_concurrent_tasks": self.max_concurrent_tasks
        }


@dataclass
class Agent:
    """
    Represents an individual agent instance.
    
    Agents are API-agnostic and can be backed by different implementations.
    """
    agent_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    role_id: str = ""
    status: AgentStatus = AgentStatus.AVAILABLE
    skills: Set[str] = field(default_factory=set)
    current_tasks: List[str] = field(default_factory=list)
    completed_tasks: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_active: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # API configuration (flexible, not hard-coded)
    api_config: Dict[str, Any] = field(default_factory=dict)
    
    # Custom execution handler (optional)
    executor: Optional[Callable] = None
    
    def update_status(self, status: AgentStatus):
        """Update agent status"""
        self.status = status
        self.last_active = datetime.utcnow().isoformat()
    
    def assign_task(self, task_id: str) -> bool:
        """Assign a task to this agent"""
        if self.status == AgentStatus.AVAILABLE or self.status == AgentStatus.BUSY:
            self.current_tasks.append(task_id)
            self.status = AgentStatus.BUSY
            self.last_active = datetime.utcnow().isoformat()
            return True
        return False
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed"""
        if task_id in self.current_tasks:
            self.current_tasks.remove(task_id)
            self.completed_tasks += 1
            
            # Update status
            if not self.current_tasks:
                self.status = AgentStatus.AVAILABLE
            
            self.last_active = datetime.utcnow().isoformat()
            return True
        return False
    
    def has_skill(self, skill: str) -> bool:
        """Check if agent has a specific skill"""
        return skill in self.skills
    
    def has_skills(self, skills: Set[str]) -> bool:
        """Check if agent has all required skills"""
        return skills.issubset(self.skills)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role_id": self.role_id,
            "status": self.status.value,
            "skills": list(self.skills),
            "current_tasks": self.current_tasks,
            "completed_tasks": self.completed_tasks,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "api_config": self.api_config
        }


class AgentRegistry:
    """
    Central registry for all agent roles and instances.
    
    Features:
    - Role-based architecture (30-100+ roles)
    - API-agnostic design
    - Dynamic agent assignment
    - Capability-based routing
    - Flexible execution model
    """
    
    def __init__(self):
        self.roles: Dict[str, AgentRole] = {}
        self.agents: Dict[str, Agent] = {}
        self.capability_index: Dict[str, List[str]] = {}  # capability -> role_ids
        logger.info("AgentRegistry initialized")
    
    def register_role(self, role: AgentRole) -> str:
        """
        Register a new agent role.
        
        Args:
            role: AgentRole to register
        
        Returns:
            Role ID
        """
        self.roles[role.role_id] = role
        
        # Index capabilities
        for capability in role.capabilities:
            if capability.name not in self.capability_index:
                self.capability_index[capability.name] = []
            self.capability_index[capability.name].append(role.role_id)
        
        logger.info(f"Registered role: {role.name} (ID: {role.role_id})")
        return role.role_id
    
    def create_role(
        self,
        name: str,
        description: str,
        capabilities: Optional[List[AgentCapability]] = None,
        priority: int = 1,
        max_concurrent_tasks: int = 1
    ) -> AgentRole:
        """
        Create and register a new role.
        
        Args:
            name: Role name
            description: Role description
            capabilities: List of capabilities
            priority: Role priority (higher = more important)
            max_concurrent_tasks: Max tasks per agent instance
        
        Returns:
            Created AgentRole
        """
        role = AgentRole(
            name=name,
            description=description,
            priority=priority,
            max_concurrent_tasks=max_concurrent_tasks
        )
        
        if capabilities:
            for capability in capabilities:
                role.add_capability(capability)
        
        self.register_role(role)
        return role
    
    def get_role(self, role_id: str) -> Optional[AgentRole]:
        """Get a role by ID"""
        return self.roles.get(role_id)
    
    def get_role_by_name(self, name: str) -> Optional[AgentRole]:
        """Get a role by name"""
        for role in self.roles.values():
            if role.name == name:
                return role
        return None
    
    def list_roles(self) -> List[AgentRole]:
        """List all registered roles"""
        return list(self.roles.values())
    
    def find_roles_by_capability(self, capability_name: str) -> List[AgentRole]:
        """Find all roles that can perform a capability"""
        role_ids = self.capability_index.get(capability_name, [])
        return [self.roles[rid] for rid in role_ids if rid in self.roles]
    
    def register_agent(self, agent: Agent) -> str:
        """
        Register a new agent instance.
        
        Args:
            agent: Agent to register
        
        Returns:
            Agent ID
        """
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.name} (ID: {agent.agent_id})")
        return agent.agent_id
    
    def create_agent(
        self,
        name: str,
        role_id: str,
        skills: Optional[Set[str]] = None,
        api_config: Optional[Dict[str, Any]] = None,
        executor: Optional[Callable] = None
    ) -> Optional[Agent]:
        """
        Create and register a new agent.
        
        Args:
            name: Agent name
            role_id: ID of the role this agent fulfills
            skills: Set of skills the agent has
            api_config: API configuration (flexible dict)
            executor: Custom execution function
        
        Returns:
            Created Agent or None if role doesn't exist
        """
        role = self.get_role(role_id)
        if not role:
            logger.error(f"Cannot create agent: role {role_id} not found")
            return None
        
        agent = Agent(
            name=name,
            role_id=role_id,
            skills=skills or set(),
            api_config=api_config or {},
            executor=executor
        )
        
        self.register_agent(agent)
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID"""
        return self.agents.get(agent_id)
    
    def list_agents(
        self,
        role_id: Optional[str] = None,
        status: Optional[AgentStatus] = None
    ) -> List[Agent]:
        """
        List agents, optionally filtered.
        
        Args:
            role_id: Filter by role ID
            status: Filter by status
        
        Returns:
            List of matching agents
        """
        agents = list(self.agents.values())
        
        if role_id:
            agents = [a for a in agents if a.role_id == role_id]
        
        if status:
            agents = [a for a in agents if a.status == status]
        
        return agents
    
    def find_available_agent(
        self,
        role_id: Optional[str] = None,
        capability: Optional[str] = None,
        required_skills: Optional[Set[str]] = None
    ) -> Optional[Agent]:
        """
        Find an available agent matching criteria.
        
        Args:
            role_id: Required role ID
            capability: Required capability
            required_skills: Required skills
        
        Returns:
            First matching available agent or None
        """
        # Filter by role if specified
        if role_id:
            candidates = [
                a for a in self.agents.values()
                if a.role_id == role_id and a.status == AgentStatus.AVAILABLE
            ]
        else:
            candidates = [
                a for a in self.agents.values()
                if a.status == AgentStatus.AVAILABLE
            ]
        
        # Filter by capability if specified
        if capability:
            valid_role_ids = set(self.capability_index.get(capability, []))
            candidates = [a for a in candidates if a.role_id in valid_role_ids]
        
        # Filter by skills if specified
        if required_skills:
            candidates = [a for a in candidates if a.has_skills(required_skills)]
        
        # Return first match
        return candidates[0] if candidates else None
    
    def assign_task(
        self,
        task_id: str,
        agent_id: Optional[str] = None,
        role_id: Optional[str] = None,
        capability: Optional[str] = None,
        required_skills: Optional[Set[str]] = None
    ) -> Optional[Agent]:
        """
        Assign a task to an agent.
        
        Args:
            task_id: Task ID
            agent_id: Specific agent ID (optional)
            role_id: Required role (optional)
            capability: Required capability (optional)
            required_skills: Required skills (optional)
        
        Returns:
            Agent that received the task or None
        """
        # Use specific agent if provided
        if agent_id:
            agent = self.get_agent(agent_id)
            if agent and agent.assign_task(task_id):
                logger.info(f"Assigned task {task_id} to agent {agent.name}")
                return agent
            return None
        
        # Find an available agent
        agent = self.find_available_agent(role_id, capability, required_skills)
        if agent and agent.assign_task(task_id):
            logger.info(f"Assigned task {task_id} to agent {agent.name}")
            return agent
        
        logger.warning(f"No available agent found for task {task_id}")
        return None
    
    def complete_task(self, agent_id: str, task_id: str) -> bool:
        """
        Mark a task as completed for an agent.
        
        Args:
            agent_id: Agent ID
            task_id: Task ID
        
        Returns:
            True if successful
        """
        agent = self.get_agent(agent_id)
        if agent:
            success = agent.complete_task(task_id)
            if success:
                logger.info(f"Agent {agent.name} completed task {task_id}")
            return success
        return False
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the registry"""
        if agent_id in self.agents:
            agent_name = self.agents[agent_id].name
            del self.agents[agent_id]
            logger.info(f"Removed agent: {agent_name}")
            return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics"""
        total_agents = len(self.agents)
        by_status = {}
        by_role = {}
        
        for agent in self.agents.values():
            # Count by status
            status_key = agent.status.value
            by_status[status_key] = by_status.get(status_key, 0) + 1
            
            # Count by role
            role = self.get_role(agent.role_id)
            if role:
                role_name = role.name
                by_role[role_name] = by_role.get(role_name, 0) + 1
        
        return {
            "total_roles": len(self.roles),
            "total_agents": total_agents,
            "agents_by_status": by_status,
            "agents_by_role": by_role,
            "total_tasks_completed": sum(a.completed_tasks for a in self.agents.values()),
            "active_tasks": sum(len(a.current_tasks) for a in self.agents.values())
        }
    
    def save_state(self, filepath: str):
        """Save registry state to a JSON file"""
        state = {
            "roles": {
                role_id: role.to_dict()
                for role_id, role in self.roles.items()
            },
            "agents": {
                agent_id: agent.to_dict()
                for agent_id, agent in self.agents.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Saved AgentRegistry state to {filepath}")
    
    def load_state(self, filepath: str):
        """Load registry state from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
            
            # Clear existing data
            self.roles.clear()
            self.agents.clear()
            self.capability_index.clear()
            
            # Restore roles
            for role_id, role_data in state.get("roles", {}).items():
                role = AgentRole(
                    role_id=role_id,
                    name=role_data["name"],
                    description=role_data["description"],
                    priority=role_data.get("priority", 1),
                    max_concurrent_tasks=role_data.get("max_concurrent_tasks", 1)
                )
                
                # Restore capabilities
                for cap_data in role_data.get("capabilities", []):
                    capability = AgentCapability(**cap_data)
                    role.add_capability(capability)
                
                self.register_role(role)
            
            # Restore agents
            for agent_id, agent_data in state.get("agents", {}).items():
                agent = Agent(
                    agent_id=agent_id,
                    name=agent_data["name"],
                    role_id=agent_data["role_id"],
                    status=AgentStatus(agent_data["status"]),
                    skills=set(agent_data.get("skills", [])),
                    current_tasks=agent_data.get("current_tasks", []),
                    completed_tasks=agent_data.get("completed_tasks", 0),
                    api_config=agent_data.get("api_config", {})
                )
                agent.created_at = agent_data["created_at"]
                agent.last_active = agent_data["last_active"]
                
                self.register_agent(agent)
            
            logger.info(f"Loaded AgentRegistry state from {filepath}")
            logger.info(f"Loaded {len(self.roles)} roles and {len(self.agents)} agents")
        
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            raise
