"""
Agent Registry - Role-based agent management.

Manages AI agents with logical role definitions, avoiding direct
vendor dependencies and focusing on capabilities and responsibilities.
"""

from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from enum import Enum
import uuid


class AgentRole(Enum):
    """
    Logical agent roles based on capabilities and responsibilities.
    
    These roles are vendor-agnostic and focus on what agents do,
    not which specific AI provider implements them.
    """
    # Architecture & Design
    ARCHITECT = "architect"
    DESIGNER = "designer"
    SYSTEM_PLANNER = "system_planner"
    
    # Development
    BACKEND_BUILDER = "backend_builder"
    FRONTEND_BUILDER = "frontend_builder"
    FULL_STACK_BUILDER = "full_stack_builder"
    DATABASE_ENGINEER = "database_engineer"
    
    # Quality & Testing
    TESTER = "tester"
    QA_ENGINEER = "qa_engineer"
    SECURITY_AUDITOR = "security_auditor"
    
    # Operations
    DEVOPS_ENGINEER = "devops_engineer"
    DEPLOYMENT_MANAGER = "deployment_manager"
    MONITORING_SPECIALIST = "monitoring_specialist"
    
    # Content & Documentation
    TECHNICAL_WRITER = "technical_writer"
    DOCUMENTATION_MANAGER = "documentation_manager"
    
    # Analysis & Research
    DATA_ANALYST = "data_analyst"
    RESEARCHER = "researcher"
    CODE_REVIEWER = "code_reviewer"
    
    # Management & Coordination
    PROJECT_MANAGER = "project_manager"
    COORDINATOR = "coordinator"
    
    # Specialized
    AI_TRAINER = "ai_trainer"
    MODEL_OPTIMIZER = "model_optimizer"
    CUSTOM = "custom"


class AgentStatus(Enum):
    """Agent operational status."""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AgentCapability:
    """
    Represents a specific capability an agent possesses.
    
    Capabilities are vendor-agnostic descriptions of what an agent can do.
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        proficiency: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a capability.
        
        Args:
            name: Capability name
            description: Detailed description
            proficiency: Skill level (1-10, where 10 is expert)
            metadata: Additional capability metadata
        """
        self.name = name
        self.description = description
        self.proficiency = max(1, min(10, proficiency))  # Clamp to 1-10
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'name': self.name,
            'description': self.description,
            'proficiency': self.proficiency,
            'metadata': self.metadata
        }


class Agent:
    """
    Represents an AI agent with role-based capabilities.
    
    Agents are defined by their roles and capabilities, not by
    specific vendor implementations.
    """
    
    def __init__(
        self,
        name: str,
        role: AgentRole,
        description: str = "",
        agent_id: Optional[str] = None
    ):
        """
        Initialize an agent.
        
        Args:
            name: Agent name
            role: Primary agent role
            description: Agent description
            agent_id: Unique identifier (auto-generated if not provided)
        """
        self.id = agent_id or str(uuid.uuid4())
        self.name = name
        self.role = role
        self.description = description
        self.status = AgentStatus.AVAILABLE
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Capabilities and configuration
        self.capabilities: List[AgentCapability] = []
        self.secondary_roles: Set[AgentRole] = set()
        self.metadata: Dict[str, Any] = {}
        
        # Task tracking
        self.current_task: Optional[str] = None
        self.assigned_project: Optional[str] = None
        self.tasks_completed: int = 0
        
        # Performance metrics (placeholder for future)
        self.metrics: Dict[str, Any] = {
            'success_rate': 0.0,
            'avg_task_time': 0.0,
            'total_tasks': 0
        }
    
    def add_capability(
        self,
        name: str,
        description: str = "",
        proficiency: int = 5
    ) -> AgentCapability:
        """
        Add a capability to the agent.
        
        Args:
            name: Capability name
            description: Capability description
            proficiency: Proficiency level (1-10)
            
        Returns:
            Created capability
        """
        capability = AgentCapability(name, description, proficiency)
        self.capabilities.append(capability)
        self.updated_at = datetime.now()
        return capability
    
    def add_secondary_role(self, role: AgentRole) -> None:
        """
        Add a secondary role to the agent.
        
        Args:
            role: Secondary role
        """
        self.secondary_roles.add(role)
        self.updated_at = datetime.now()
    
    def assign_task(self, task_id: str, project_id: Optional[str] = None) -> None:
        """
        Assign a task to the agent.
        
        Args:
            task_id: Task identifier
            project_id: Optional project identifier
        """
        self.current_task = task_id
        if project_id:
            self.assigned_project = project_id
        self.status = AgentStatus.BUSY
        self.updated_at = datetime.now()
    
    def complete_task(self) -> None:
        """Mark current task as complete."""
        self.current_task = None
        self.tasks_completed += 1
        self.status = AgentStatus.AVAILABLE
        self.updated_at = datetime.now()
    
    def set_status(self, status: AgentStatus) -> None:
        """
        Update agent status.
        
        Args:
            status: New status
        """
        self.status = status
        self.updated_at = datetime.now()
    
    def get_all_roles(self) -> List[AgentRole]:
        """
        Get all roles (primary and secondary).
        
        Returns:
            List of all roles
        """
        return [self.role] + list(self.secondary_roles)
    
    def has_capability(self, capability_name: str, min_proficiency: int = 1) -> bool:
        """
        Check if agent has a specific capability.
        
        Args:
            capability_name: Capability to check
            min_proficiency: Minimum required proficiency
            
        Returns:
            True if agent has capability at required level
        """
        for cap in self.capabilities:
            if cap.name == capability_name and cap.proficiency >= min_proficiency:
                return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert agent to dictionary representation.
        
        Returns:
            Dictionary with agent data
        """
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role.value,
            'secondary_roles': [r.value for r in self.secondary_roles],
            'description': self.description,
            'status': self.status.value,
            'capabilities': [c.to_dict() for c in self.capabilities],
            'current_task': self.current_task,
            'assigned_project': self.assigned_project,
            'tasks_completed': self.tasks_completed,
            'metrics': self.metrics,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class AgentRegistry:
    """
    Central registry for managing AI agents.
    
    Provides role-based agent management without vendor lock-in.
    Agents are defined by capabilities and logical roles.
    """
    
    def __init__(self):
        """Initialize the agent registry."""
        self.agents: Dict[str, Agent] = {}
        self.role_index: Dict[AgentRole, Set[str]] = {role: set() for role in AgentRole}
        self.created_at = datetime.now()
    
    def register_agent(self, agent: Agent) -> None:
        """
        Register an agent in the registry.
        
        Args:
            agent: Agent to register
        """
        self.agents[agent.id] = agent
        # Index by primary role
        self.role_index[agent.role].add(agent.id)
        # Index by secondary roles
        for role in agent.secondary_roles:
            self.role_index[role].add(agent.id)
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        Remove an agent from the registry.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if removed, False if not found
        """
        agent = self.agents.get(agent_id)
        if not agent:
            return False
        
        # Remove from role indices
        for role in agent.get_all_roles():
            if agent_id in self.role_index[role]:
                self.role_index[role].remove(agent_id)
        
        # Remove from main registry
        del self.agents[agent_id]
        return True
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        Get a specific agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent or None if not found
        """
        return self.agents.get(agent_id)
    
    def find_agents_by_role(
        self,
        role: AgentRole,
        status: Optional[AgentStatus] = None
    ) -> List[Agent]:
        """
        Find all agents with a specific role.
        
        Args:
            role: Agent role to search for
            status: Optional status filter
            
        Returns:
            List of matching agents
        """
        agent_ids = self.role_index.get(role, set())
        agents = [self.agents[aid] for aid in agent_ids if aid in self.agents]
        
        if status:
            agents = [a for a in agents if a.status == status]
        
        return agents
    
    def find_agents_by_capability(
        self,
        capability: str,
        min_proficiency: int = 1,
        status: Optional[AgentStatus] = None
    ) -> List[Agent]:
        """
        Find agents with a specific capability.
        
        Args:
            capability: Capability name
            min_proficiency: Minimum proficiency level
            status: Optional status filter
            
        Returns:
            List of matching agents
        """
        matching_agents = []
        for agent in self.agents.values():
            if agent.has_capability(capability, min_proficiency):
                if status is None or agent.status == status:
                    matching_agents.append(agent)
        return matching_agents
    
    def find_available_agent(
        self,
        role: AgentRole,
        required_capabilities: Optional[List[str]] = None
    ) -> Optional[Agent]:
        """
        Find an available agent for a role with optional capability requirements.
        
        Args:
            role: Required agent role
            required_capabilities: Optional list of required capabilities
            
        Returns:
            First available matching agent or None
        """
        agents = self.find_agents_by_role(role, status=AgentStatus.AVAILABLE)
        
        if required_capabilities:
            for agent in agents:
                if all(agent.has_capability(cap) for cap in required_capabilities):
                    return agent
            return None
        
        return agents[0] if agents else None
    
    def list_agents(
        self,
        status: Optional[AgentStatus] = None,
        role: Optional[AgentRole] = None
    ) -> List[Agent]:
        """
        List all agents with optional filtering.
        
        Args:
            status: Filter by status
            role: Filter by role
            
        Returns:
            List of agents
        """
        agents = list(self.agents.values())
        
        if status:
            agents = [a for a in agents if a.status == status]
        
        if role:
            agents = [a for a in agents if role in a.get_all_roles()]
        
        return agents
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get registry statistics.
        
        Returns:
            Statistics dictionary
        """
        total_agents = len(self.agents)
        status_counts = {status: 0 for status in AgentStatus}
        role_counts = {role: 0 for role in AgentRole}
        
        for agent in self.agents.values():
            status_counts[agent.status] += 1
            for role in agent.get_all_roles():
                role_counts[role] += 1
        
        return {
            'total_agents': total_agents,
            'available_agents': status_counts[AgentStatus.AVAILABLE],
            'busy_agents': status_counts[AgentStatus.BUSY],
            'status_distribution': {s.value: c for s, c in status_counts.items()},
            'role_distribution': {r.value: c for r, c in role_counts.items() if c > 0}
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert registry to dictionary representation.
        
        Returns:
            Dictionary with registry data
        """
        return {
            'statistics': self.get_statistics(),
            'agents': {aid: agent.to_dict() for aid, agent in self.agents.items()},
            'created_at': self.created_at.isoformat()
        }
