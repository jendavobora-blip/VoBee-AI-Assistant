"""
Task Router
Intelligent routing of tasks to appropriate factories based on task type,
content, priority, and resource availability.
"""

from enum import Enum
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass


class RoutingStrategy(Enum):
    """Strategy for routing tasks to factories"""
    CONTENT_BASED = "content_based"  # Route based on task content/type
    PRIORITY_BASED = "priority_based"  # Route based on task priority
    LOAD_BALANCED = "load_balanced"  # Distribute based on load
    ROUND_ROBIN = "round_robin"  # Simple round-robin distribution
    CAPABILITY_BASED = "capability_based"  # Route based on capabilities


@dataclass
class RoutingRule:
    """Represents a routing rule"""
    rule_id: str
    name: str
    condition: Callable[[Dict[str, Any]], bool]
    target_factory: str
    priority: int = 0


class TaskRouter:
    """
    Intelligent task router for directing tasks to appropriate factories.
    Supports multiple routing strategies and custom rules.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the task router.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.strategy = RoutingStrategy[
            self.config.get("strategy", "CONTENT_BASED").upper()
        ]
        self._rules: List[RoutingRule] = []
        self._factory_loads: Dict[str, int] = {}
        self._round_robin_index = 0
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default routing rules"""
        # Media-related tasks
        self.add_rule(RoutingRule(
            rule_id="media_image",
            name="Route image tasks to Media Factory",
            condition=lambda task: self._is_media_task(task, "image"),
            target_factory="media",
            priority=10
        ))
        
        self.add_rule(RoutingRule(
            rule_id="media_video",
            name="Route video tasks to Media Factory",
            condition=lambda task: self._is_media_task(task, "video"),
            target_factory="media",
            priority=10
        ))
        
        self.add_rule(RoutingRule(
            rule_id="media_voice",
            name="Route voice tasks to Media Factory",
            condition=lambda task: self._is_media_task(task, "voice"),
            target_factory="media",
            priority=10
        ))
        
        # Research-related tasks
        self.add_rule(RoutingRule(
            rule_id="research_market",
            name="Route market analysis to Research Factory",
            condition=lambda task: self._is_research_task(task, "market"),
            target_factory="research",
            priority=10
        ))
        
        self.add_rule(RoutingRule(
            rule_id="research_discovery",
            name="Route discovery tasks to Research Factory",
            condition=lambda task: self._is_research_task(task, "discovery"),
            target_factory="research",
            priority=10
        ))
    
    def _is_media_task(self, task: Dict[str, Any], media_type: str) -> bool:
        """Check if task is a media task of specific type"""
        task_type = task.get("type", "").lower()
        keywords = task.get("keywords", [])
        
        media_keywords = {
            "image": ["image", "photo", "picture", "generate_image", "stable_diffusion"],
            "video": ["video", "animation", "generate_video", "nerf"],
            "voice": ["voice", "speech", "audio", "tts", "text-to-speech"]
        }
        
        if media_type in task_type:
            return True
        
        for keyword in keywords:
            if keyword.lower() in media_keywords.get(media_type, []):
                return True
        
        return False
    
    def _is_research_task(self, task: Dict[str, Any], research_type: str) -> bool:
        """Check if task is a research task of specific type"""
        task_type = task.get("type", "").lower()
        keywords = task.get("keywords", [])
        
        research_keywords = {
            "market": ["market", "competitive", "analysis", "trends"],
            "discovery": ["discover", "research", "find", "explore", "agent"]
        }
        
        if research_type in task_type:
            return True
        
        for keyword in keywords:
            if keyword.lower() in research_keywords.get(research_type, []):
                return True
        
        return False
    
    def add_rule(self, rule: RoutingRule):
        """
        Add a routing rule.
        
        Args:
            rule: RoutingRule to add
        """
        self._rules.append(rule)
        # Sort rules by priority (highest first)
        self._rules.sort(key=lambda r: r.priority, reverse=True)
    
    def remove_rule(self, rule_id: str) -> bool:
        """
        Remove a routing rule.
        
        Args:
            rule_id: ID of rule to remove
            
        Returns:
            True if removed, False if not found
        """
        initial_length = len(self._rules)
        self._rules = [r for r in self._rules if r.rule_id != rule_id]
        return len(self._rules) < initial_length
    
    def route(self, task: Dict[str, Any]) -> str:
        """
        Route a task to the appropriate factory.
        
        Args:
            task: Task to route
            
        Returns:
            Factory identifier (e.g., 'media', 'research')
        """
        if self.strategy == RoutingStrategy.CONTENT_BASED:
            return self._route_content_based(task)
        elif self.strategy == RoutingStrategy.PRIORITY_BASED:
            return self._route_priority_based(task)
        elif self.strategy == RoutingStrategy.LOAD_BALANCED:
            return self._route_load_balanced(task)
        elif self.strategy == RoutingStrategy.ROUND_ROBIN:
            return self._route_round_robin(task)
        elif self.strategy == RoutingStrategy.CAPABILITY_BASED:
            return self._route_capability_based(task)
        else:
            return self._route_content_based(task)
    
    def _route_content_based(self, task: Dict[str, Any]) -> str:
        """Route based on task content using rules"""
        # Apply rules in priority order
        for rule in self._rules:
            if rule.condition(task):
                return rule.target_factory
        
        # Default factory if no rules match
        return self.config.get("default_factory", "media")
    
    def _route_priority_based(self, task: Dict[str, Any]) -> str:
        """Route based on task priority"""
        priority = task.get("priority", "normal").lower()
        
        # High priority tasks might go to specific factories
        if priority in ["high", "critical"]:
            # Use content-based routing for high priority
            return self._route_content_based(task)
        else:
            # Use load balancing for normal/low priority
            return self._route_load_balanced(task)
    
    def _route_load_balanced(self, task: Dict[str, Any]) -> str:
        """Route based on factory load"""
        # Get eligible factories for this task
        eligible_factories = self._get_eligible_factories(task)
        
        if not eligible_factories:
            return self.config.get("default_factory", "media")
        
        # Find factory with lowest load
        min_load_factory = min(
            eligible_factories,
            key=lambda f: self._factory_loads.get(f, 0)
        )
        
        # Increment load
        self._factory_loads[min_load_factory] = \
            self._factory_loads.get(min_load_factory, 0) + 1
        
        return min_load_factory
    
    def _route_round_robin(self, task: Dict[str, Any]) -> str:
        """Route using round-robin distribution"""
        eligible_factories = self._get_eligible_factories(task)
        
        if not eligible_factories:
            return self.config.get("default_factory", "media")
        
        factory = eligible_factories[self._round_robin_index % len(eligible_factories)]
        self._round_robin_index += 1
        
        return factory
    
    def _route_capability_based(self, task: Dict[str, Any]) -> str:
        """Route based on factory capabilities"""
        # Use content-based routing to find capable factory
        return self._route_content_based(task)
    
    def _get_eligible_factories(self, task: Dict[str, Any]) -> List[str]:
        """Get list of factories eligible to handle this task"""
        eligible = []
        
        for rule in self._rules:
            if rule.condition(task):
                if rule.target_factory not in eligible:
                    eligible.append(rule.target_factory)
        
        return eligible if eligible else ["media", "research"]
    
    def update_factory_load(self, factory: str, load: int):
        """
        Update the load for a factory.
        
        Args:
            factory: Factory identifier
            load: Current load value
        """
        self._factory_loads[factory] = load
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """
        Get routing statistics.
        
        Returns:
            Dictionary with routing statistics
        """
        return {
            "strategy": self.strategy.value,
            "total_rules": len(self._rules),
            "factory_loads": self._factory_loads.copy(),
            "round_robin_index": self._round_robin_index
        }
