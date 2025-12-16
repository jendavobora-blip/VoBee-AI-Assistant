"""
Cost Router - Intelligent routing based on cost optimization.

Routes requests to most cost-effective services while maintaining quality.
"""

import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime


class RoutingStrategy(Enum):
    """Cost routing strategies."""
    CHEAPEST = "cheapest"           # Always route to cheapest option
    BEST_VALUE = "best_value"       # Balance cost and quality
    QUALITY_FIRST = "quality_first" # Prioritize quality over cost
    LOAD_BALANCED = "load_balanced" # Distribute across providers


class CostRouter:
    """
    Routes requests to optimal services based on cost and quality.
    
    Features:
    - Multi-provider cost comparison
    - Quality-aware routing
    - Load balancing
    - Fallback handling
    """
    
    def __init__(
        self,
        strategy: RoutingStrategy = RoutingStrategy.BEST_VALUE
    ):
        """
        Initialize cost router.
        
        Args:
            strategy: Routing strategy to use
        """
        self.strategy = strategy
        self.logger = logging.getLogger(__name__)
        
        # Provider cost profiles (cost per 1000 tokens/requests)
        # TODO: Load from configuration file or database
        self.provider_costs = {
            "gpt-4": {"cost": 0.03, "quality_score": 0.95, "latency_ms": 800},
            "gpt-3.5-turbo": {"cost": 0.002, "quality_score": 0.80, "latency_ms": 400},
            "claude-2": {"cost": 0.025, "quality_score": 0.90, "latency_ms": 600},
            "palm-2": {"cost": 0.001, "quality_score": 0.75, "latency_ms": 300},
        }
        
        # Track provider usage for load balancing
        self.provider_usage: Dict[str, int] = {}
        
        self.logger.info(f"CostRouter initialized with strategy: {strategy.value}")
    
    def route_request(
        self,
        request_type: str,
        quality_requirement: float = 0.7,
        budget_limit: Optional[float] = None,
        estimated_tokens: int = 1000
    ) -> Tuple[str, Dict]:
        """
        Route a request to the optimal provider.
        
        Args:
            request_type: Type of request (e.g., 'text_generation', 'analysis')
            quality_requirement: Minimum quality score (0-1)
            budget_limit: Maximum cost willing to pay
            estimated_tokens: Estimated number of tokens/units
            
        Returns:
            Tuple of (provider_name, routing_metadata)
        """
        # Filter providers that meet quality requirement
        eligible_providers = {
            name: profile
            for name, profile in self.provider_costs.items()
            if profile["quality_score"] >= quality_requirement
        }
        
        if not eligible_providers:
            self.logger.warning(
                f"No providers meet quality requirement: {quality_requirement}"
            )
            # Fallback to best available quality
            eligible_providers = self.provider_costs
        
        # Further filter by budget if specified
        if budget_limit:
            estimated_cost_per_unit = estimated_tokens / 1000.0
            eligible_providers = {
                name: profile
                for name, profile in eligible_providers.items()
                if (profile["cost"] * estimated_cost_per_unit) <= budget_limit
            }
            
            if not eligible_providers:
                raise ValueError(
                    f"No providers available within budget: ${budget_limit}"
                )
        
        # Route based on strategy
        if self.strategy == RoutingStrategy.CHEAPEST:
            provider = self._route_cheapest(eligible_providers)
        elif self.strategy == RoutingStrategy.BEST_VALUE:
            provider = self._route_best_value(eligible_providers)
        elif self.strategy == RoutingStrategy.QUALITY_FIRST:
            provider = self._route_quality_first(eligible_providers)
        elif self.strategy == RoutingStrategy.LOAD_BALANCED:
            provider = self._route_load_balanced(eligible_providers)
        else:
            provider = self._route_best_value(eligible_providers)
        
        # Update usage tracking
        self.provider_usage[provider] = self.provider_usage.get(provider, 0) + 1
        
        # Calculate estimated cost
        profile = self.provider_costs[provider]
        estimated_cost = (profile["cost"] * estimated_tokens) / 1000.0
        
        routing_metadata = {
            "provider": provider,
            "strategy": self.strategy.value,
            "estimated_cost": estimated_cost,
            "quality_score": profile["quality_score"],
            "estimated_latency_ms": profile["latency_ms"],
            "routed_at": datetime.utcnow().isoformat()
        }
        
        self.logger.info(
            f"Routed request to {provider} "
            f"(cost: ${estimated_cost:.4f}, quality: {profile['quality_score']})"
        )
        
        return provider, routing_metadata
    
    def _route_cheapest(self, providers: Dict) -> str:
        """Route to cheapest provider."""
        return min(providers.items(), key=lambda x: x[1]["cost"])[0]
    
    def _route_quality_first(self, providers: Dict) -> str:
        """Route to highest quality provider."""
        return max(providers.items(), key=lambda x: x[1]["quality_score"])[0]
    
    def _route_best_value(self, providers: Dict) -> str:
        """Route to best value (quality/cost ratio)."""
        return max(
            providers.items(),
            key=lambda x: x[1]["quality_score"] / max(x[1]["cost"], 0.001)
        )[0]
    
    def _route_load_balanced(self, providers: Dict) -> str:
        """Route to least used provider among eligible."""
        return min(
            providers.keys(),
            key=lambda p: self.provider_usage.get(p, 0)
        )
    
    def get_cost_estimate(
        self,
        provider: str,
        estimated_tokens: int
    ) -> float:
        """
        Get cost estimate for a provider.
        
        Args:
            provider: Provider name
            estimated_tokens: Number of tokens
            
        Returns:
            Estimated cost in dollars
        """
        if provider not in self.provider_costs:
            raise ValueError(f"Unknown provider: {provider}")
        
        cost_per_1k = self.provider_costs[provider]["cost"]
        return (cost_per_1k * estimated_tokens) / 1000.0
    
    def get_provider_stats(self) -> Dict:
        """
        Get routing statistics.
        
        Returns:
            Dictionary with provider usage stats
        """
        total_requests = sum(self.provider_usage.values())
        
        stats = {
            "total_requests": total_requests,
            "strategy": self.strategy.value,
            "provider_distribution": {},
            "available_providers": list(self.provider_costs.keys())
        }
        
        for provider, count in self.provider_usage.items():
            percentage = (count / total_requests * 100) if total_requests > 0 else 0
            stats["provider_distribution"][provider] = {
                "requests": count,
                "percentage": round(percentage, 2)
            }
        
        return stats
    
    def update_provider_costs(self, provider: str, cost: float, quality_score: float):
        """
        Update provider cost and quality information.
        
        Args:
            provider: Provider name
            cost: Cost per 1000 tokens
            quality_score: Quality score (0-1)
        """
        if provider not in self.provider_costs:
            self.provider_costs[provider] = {}
        
        self.provider_costs[provider]["cost"] = cost
        self.provider_costs[provider]["quality_score"] = quality_score
        
        self.logger.info(
            f"Updated provider {provider}: cost=${cost}, quality={quality_score}"
        )
    
    def set_strategy(self, strategy: RoutingStrategy):
        """
        Change routing strategy.
        
        Args:
            strategy: New routing strategy
        """
        old_strategy = self.strategy
        self.strategy = strategy
        
        self.logger.info(
            f"Routing strategy changed: {old_strategy.value} → {strategy.value}"
        )
