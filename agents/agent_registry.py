"""
Agent Registry - Central registry for managing all agents
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .agent_roles import AgentRole, RoleCategory
from .base_agent import BaseAgent, PlaceholderAgent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Central registry for managing 30-100 logical agent roles
    Provides agent lookup, assignment, and lifecycle management
    """
    
    MAX_AGENTS = 100
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.role_definitions = AgentRole.get_all_roles()
        self.created_at = datetime.utcnow().isoformat()
        
        logger.info(
            f"AgentRegistry initialized with {len(self.role_definitions)} "
            f"available roles"
        )
    
    def register_agent(
        self,
        agent_id: str,
        role_name: str,
        agent_class: type = PlaceholderAgent,
        config: Optional[Dict[str, Any]] = None
    ) -> Optional[BaseAgent]:
        """
        Register a new agent in the system
        
        Args:
            agent_id: Unique identifier for the agent
            role_name: Name of the role from AgentRole
            agent_class: Agent class to instantiate (defaults to PlaceholderAgent)
            config: Optional configuration for the agent
            
        Returns:
            Registered agent instance or None if failed
        """
        if len(self.agents) >= self.MAX_AGENTS:
            logger.error(f"Maximum agent limit ({self.MAX_AGENTS}) reached")
            return None
        
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} already registered")
            return None
        
        # Find role definition
        role_def = None
        for role in self.role_definitions:
            if role['name'] == role_name:
                role_def = role
                break
        
        if not role_def:
            logger.error(f"Role '{role_name}' not found")
            return None
        
        # Create agent instance
        try:
            agent = agent_class(agent_id, role_def, config)
            self.agents[agent_id] = agent
            logger.info(
                f"Registered agent {agent_id} with role '{role_name}'"
            )
            return agent
        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            return None
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Remove an agent from the registry"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            logger.info(f"Unregistered agent {agent_id}")
            return True
        return False
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[BaseAgent]:
        """Get all registered agents"""
        return list(self.agents.values())
    
    def get_agents_by_role(self, role_name: str) -> List[BaseAgent]:
        """Get all agents with a specific role"""
        return [
            agent for agent in self.agents.values()
            if agent.role['name'] == role_name
        ]
    
    def get_agents_by_category(self, category: RoleCategory) -> List[BaseAgent]:
        """Get all agents in a category"""
        return [
            agent for agent in self.agents.values()
            if agent.role['category'] == category
        ]
    
    def get_agents_with_capability(self, capability: str) -> List[BaseAgent]:
        """Find agents with a specific capability"""
        return [
            agent for agent in self.agents.values()
            if agent.validate_capability(capability)
        ]
    
    def get_available_roles(self) -> List[Dict[str, Any]]:
        """Get all available role definitions"""
        return self.role_definitions
    
    def get_role_by_name(self, role_name: str) -> Optional[Dict[str, Any]]:
        """Get role definition by name"""
        for role in self.role_definitions:
            if role['name'] == role_name:
                return role
        return None
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        category_counts = {}
        for category in RoleCategory:
            count = len(self.get_agents_by_category(category))
            category_counts[category.value] = count
        
        return {
            'total_agents': len(self.agents),
            'max_agents': self.MAX_AGENTS,
            'capacity_utilization': f"{(len(self.agents)/self.MAX_AGENTS)*100:.1f}%",
            'available_roles': len(self.role_definitions),
            'agents_by_category': category_counts,
            'created_at': self.created_at,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def find_best_agent(
        self,
        required_capabilities: List[str],
        preferred_category: Optional[RoleCategory] = None
    ) -> Optional[BaseAgent]:
        """
        Find the best agent for a task based on capabilities
        
        Args:
            required_capabilities: List of required capabilities
            preferred_category: Optional preferred category
            
        Returns:
            Best matching agent or None
        """
        candidates = []
        
        for agent in self.agents.values():
            # Check capability match
            capability_match = sum(
                1 for cap in required_capabilities
                if agent.validate_capability(cap)
            )
            
            if capability_match == 0:
                continue
            
            # Calculate score
            score = capability_match / len(required_capabilities)
            
            # Bonus for preferred category
            if preferred_category and agent.role['category'] == preferred_category:
                score += 0.2
            
            candidates.append((agent, score))
        
        if not candidates:
            return None
        
        # Sort by score and return best match
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    def get_agent_summary(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed summary for an agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            return None
        
        return {
            **agent.get_info(),
            'recent_tasks': agent.get_task_history(limit=5)
        }
