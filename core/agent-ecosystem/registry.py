"""
Agent Registry - Manages lifecycle of 2000+ AI agents.

This module handles dynamic agent spawning, termination, capability matching,
and performance tracking.
"""

from typing import Dict, Any, List, Optional, Set
from enum import Enum
from datetime import datetime
import logging
import uuid
import asyncio

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent lifecycle status."""
    INITIALIZING = "initializing"
    IDLE = "idle"
    BUSY = "busy"
    TERMINATING = "terminating"
    TERMINATED = "terminated"


class AgentCapability(Enum):
    """Agent capabilities."""
    DATA_INGESTION = "data_ingestion"
    TECH_SCOUTING = "tech_scouting"
    CODE_ANALYSIS = "code_analysis"
    CONTENT_GENERATION = "content_generation"
    COST_OPTIMIZATION = "cost_optimization"
    BUSINESS_ANALYSIS = "business_analysis"
    EXPERIMENTATION = "experimentation"
    FEEDBACK_ANALYSIS = "feedback_analysis"
    STRATEGY_EVOLUTION = "strategy_evolution"
    INTEGRATION_TESTING = "integration_testing"


class Agent:
    """Represents a single AI agent in the ecosystem."""
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: Set[AgentCapability],
        max_concurrent_tasks: int = 1
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.max_concurrent_tasks = max_concurrent_tasks
        self.status = AgentStatus.INITIALIZING
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.current_tasks: List[str] = []
        self.performance_score = 1.0  # 0.0 - 1.0
        self.total_processing_time = 0.0
    
    def can_accept_task(self) -> bool:
        """Check if agent can accept more tasks."""
        return (
            self.status == AgentStatus.IDLE and
            len(self.current_tasks) < self.max_concurrent_tasks
        )
    
    def assign_task(self, task_id: str):
        """Assign a task to this agent."""
        self.current_tasks.append(task_id)
        self.status = AgentStatus.BUSY
        self.last_active = datetime.utcnow()
    
    def complete_task(self, task_id: str, success: bool, processing_time: float):
        """Mark a task as completed."""
        if task_id in self.current_tasks:
            self.current_tasks.remove(task_id)
        
        if success:
            self.tasks_completed += 1
        else:
            self.tasks_failed += 1
        
        self.total_processing_time += processing_time
        self.last_active = datetime.utcnow()
        
        # Update performance score
        self._update_performance_score()
        
        # Update status
        if not self.current_tasks:
            self.status = AgentStatus.IDLE
    
    def _update_performance_score(self):
        """Update agent performance score."""
        total_tasks = self.tasks_completed + self.tasks_failed
        if total_tasks > 0:
            success_rate = self.tasks_completed / total_tasks
            # Weighted average with previous score
            self.performance_score = (self.performance_score * 0.7) + (success_rate * 0.3)


class AgentRegistry:
    """
    Central registry for managing 2000+ AI agents.
    
    Features:
    - Dynamic agent spawning based on workload
    - Automatic scaling (10 to 2000+ agents)
    - Capability-based task matching
    - Performance tracking and optimization
    - Auto-termination of idle agents
    """
    
    def __init__(
        self,
        min_agents: int = 10,
        max_agents: int = 2000,
        scale_up_threshold: int = 50,  # Queue depth to trigger scale-up
        scale_down_threshold: int = 10  # Queue depth to trigger scale-down
    ):
        self.agents: Dict[str, Agent] = {}
        self.min_agents = min_agents
        self.max_agents = max_agents
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.task_queue_depth = 0
        
        # Initialize minimum agents
        self._initialize_min_agents()
    
    def _initialize_min_agents(self):
        """Initialize minimum number of agents."""
        agent_types = [
            ("learning", {AgentCapability.DATA_INGESTION}),
            ("tech_scout", {AgentCapability.TECH_SCOUTING}),
            ("cost_optimizer", {AgentCapability.COST_OPTIMIZATION}),
            ("experimenter", {AgentCapability.EXPERIMENTATION}),
        ]
        
        agents_per_type = self.min_agents // len(agent_types)
        
        for agent_type, capabilities in agent_types:
            for i in range(agents_per_type):
                self.spawn_agent(agent_type, capabilities)
        
        logger.info(f"Initialized {len(self.agents)} agents")
    
    def spawn_agent(
        self,
        agent_type: str,
        capabilities: Set[AgentCapability],
        max_concurrent_tasks: int = 1
    ) -> Optional[Agent]:
        """
        Spawn a new agent.
        
        Args:
            agent_type: Type of agent to spawn
            capabilities: Agent capabilities
            max_concurrent_tasks: Max concurrent tasks
            
        Returns:
            Spawned agent or None if max limit reached
        """
        if len(self.agents) >= self.max_agents:
            logger.warning(f"Cannot spawn agent: max limit ({self.max_agents}) reached")
            return None
        
        agent_id = str(uuid.uuid4())
        agent = Agent(
            agent_id=agent_id,
            agent_type=agent_type,
            capabilities=capabilities,
            max_concurrent_tasks=max_concurrent_tasks
        )
        
        self.agents[agent_id] = agent
        agent.status = AgentStatus.IDLE
        
        logger.info(f"Spawned {agent_type} agent: {agent_id}")
        return agent
    
    def terminate_agent(self, agent_id: str) -> bool:
        """
        Terminate an agent.
        
        Args:
            agent_id: ID of agent to terminate
            
        Returns:
            True if terminated successfully
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        
        # Don't terminate if busy
        if agent.current_tasks:
            logger.warning(f"Cannot terminate busy agent: {agent_id}")
            return False
        
        agent.status = AgentStatus.TERMINATED
        del self.agents[agent_id]
        
        logger.info(f"Terminated agent: {agent_id}")
        return True
    
    def find_available_agent(
        self,
        required_capability: AgentCapability
    ) -> Optional[Agent]:
        """
        Find an available agent with required capability.
        
        Args:
            required_capability: Required capability
            
        Returns:
            Available agent or None
        """
        # Sort by performance score (best first)
        available_agents = [
            agent for agent in self.agents.values()
            if required_capability in agent.capabilities and agent.can_accept_task()
        ]
        
        if not available_agents:
            return None
        
        # Return best performing available agent
        return max(available_agents, key=lambda a: a.performance_score)
    
    def assign_task(
        self,
        task_id: str,
        required_capability: AgentCapability
    ) -> Optional[str]:
        """
        Assign task to an available agent.
        
        Args:
            task_id: Task ID to assign
            required_capability: Required capability
            
        Returns:
            Agent ID that received the task, or None
        """
        # Find available agent
        agent = self.find_available_agent(required_capability)
        
        # If no agent available, try to spawn one
        if not agent:
            agent = self._try_spawn_for_capability(required_capability)
        
        if not agent:
            logger.warning(f"No agent available for task {task_id}")
            return None
        
        # Assign task
        agent.assign_task(task_id)
        logger.info(f"Assigned task {task_id} to agent {agent.agent_id}")
        
        return agent.agent_id
    
    def complete_task(
        self,
        agent_id: str,
        task_id: str,
        success: bool,
        processing_time: float
    ):
        """
        Mark a task as completed.
        
        Args:
            agent_id: Agent ID
            task_id: Task ID
            success: Whether task succeeded
            processing_time: Processing time in seconds
        """
        if agent_id not in self.agents:
            logger.error(f"Agent not found: {agent_id}")
            return
        
        agent = self.agents[agent_id]
        agent.complete_task(task_id, success, processing_time)
        
        logger.info(f"Task {task_id} completed by {agent_id} (success={success})")
    
    def _try_spawn_for_capability(
        self,
        capability: AgentCapability
    ) -> Optional[Agent]:
        """Try to spawn a new agent for a capability."""
        if len(self.agents) >= self.max_agents:
            return None
        
        # Map capability to agent type
        capability_to_type = {
            AgentCapability.DATA_INGESTION: "learning",
            AgentCapability.TECH_SCOUTING: "tech_scout",
            AgentCapability.COST_OPTIMIZATION: "cost_optimizer",
            AgentCapability.EXPERIMENTATION: "experimenter",
            AgentCapability.CODE_ANALYSIS: "integration",
            AgentCapability.CONTENT_GENERATION: "content",
            AgentCapability.BUSINESS_ANALYSIS: "business",
            AgentCapability.FEEDBACK_ANALYSIS: "feedback",
            AgentCapability.STRATEGY_EVOLUTION: "evolution",
        }
        
        agent_type = capability_to_type.get(capability, "generic")
        return self.spawn_agent(agent_type, {capability})
    
    def auto_scale(self, queue_depth: int):
        """
        Automatically scale agents based on queue depth.
        
        Args:
            queue_depth: Current task queue depth
        """
        self.task_queue_depth = queue_depth
        
        # Scale up if needed
        if queue_depth > self.scale_up_threshold:
            num_to_spawn = min(
                queue_depth // 10,  # Spawn 1 agent per 10 queued tasks
                self.max_agents - len(self.agents)
            )
            
            if num_to_spawn > 0:
                logger.info(f"Scaling up: spawning {num_to_spawn} agents")
                
                # Spawn generic agents that can handle various tasks
                for _ in range(num_to_spawn):
                    self.spawn_agent(
                        "generic",
                        {
                            AgentCapability.DATA_INGESTION,
                            AgentCapability.CONTENT_GENERATION
                        }
                    )
        
        # Scale down if needed
        elif queue_depth < self.scale_down_threshold and len(self.agents) > self.min_agents:
            idle_agents = [
                agent for agent in self.agents.values()
                if agent.status == AgentStatus.IDLE and not agent.current_tasks
            ]
            
            # Terminate lowest performing idle agents
            if idle_agents:
                num_to_terminate = min(
                    len(idle_agents),
                    len(self.agents) - self.min_agents
                )
                
                if num_to_terminate > 0:
                    logger.info(f"Scaling down: terminating {num_to_terminate} agents")
                    
                    # Sort by performance (worst first)
                    idle_agents.sort(key=lambda a: a.performance_score)
                    
                    for agent in idle_agents[:num_to_terminate]:
                        self.terminate_agent(agent.agent_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        active_agents = [a for a in self.agents.values() if a.status != AgentStatus.TERMINATED]
        idle_agents = [a for a in active_agents if a.status == AgentStatus.IDLE]
        busy_agents = [a for a in active_agents if a.status == AgentStatus.BUSY]
        
        total_tasks = sum(a.tasks_completed + a.tasks_failed for a in active_agents)
        successful_tasks = sum(a.tasks_completed for a in active_agents)
        
        return {
            "total_agents": len(active_agents),
            "idle_agents": len(idle_agents),
            "busy_agents": len(busy_agents),
            "min_agents": self.min_agents,
            "max_agents": self.max_agents,
            "total_tasks_processed": total_tasks,
            "successful_tasks": successful_tasks,
            "success_rate": successful_tasks / total_tasks if total_tasks > 0 else 0,
            "avg_performance_score": sum(a.performance_score for a in active_agents) / len(active_agents) if active_agents else 0,
            "queue_depth": self.task_queue_depth
        }
    
    def get_agents_by_capability(
        self,
        capability: AgentCapability
    ) -> List[Agent]:
        """Get all agents with a specific capability."""
        return [
            agent for agent in self.agents.values()
            if capability in agent.capabilities
        ]
