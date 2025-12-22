"""
LifeSync Decision Assistant Module
Helps users make informed decisions based on multiple factors
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class DecisionFactor:
    """Represents a factor in decision making"""
    
    def __init__(self, name: str, weight: float, value: float, description: str = ""):
        self.name = name
        self.weight = weight  # 0.0 to 1.0
        self.value = value    # 0.0 to 1.0
        self.description = description
    
    def score(self) -> float:
        """Calculate weighted score"""
        return self.weight * self.value


class DecisionOption:
    """Represents a decision option"""
    
    def __init__(self, name: str, factors: List[DecisionFactor], metadata: Optional[Dict[str, Any]] = None):
        self.name = name
        self.factors = factors
        self.metadata = metadata or {}
    
    def total_score(self) -> float:
        """Calculate total weighted score"""
        return sum(factor.score() for factor in self.factors)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "total_score": self.total_score(),
            "factors": [
                {
                    "name": f.name,
                    "weight": f.weight,
                    "value": f.value,
                    "score": f.score(),
                    "description": f.description
                }
                for f in self.factors
            ],
            "metadata": self.metadata
        }


class LifeSyncModule:
    """Decision assistant for life choices"""
    
    def __init__(self):
        pass
    
    def analyze_decision(self, scenario: str, options: List[str], 
                        user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze a decision scenario and recommend best option
        
        Args:
            scenario: Description of the decision to make
            options: List of option names
            user_context: Optional user preferences and context
        
        Returns:
            Dict with recommendation, scores, and reasoning
        """
        
        logger.info(f"Analyzing decision: {scenario} ({len(options)} options)")
        
        if not options:
            return {
                "status": "error",
                "error": "No options provided"
            }
        
        # Create decision options with mock factors
        decision_options = []
        
        for opt_name in options:
            factors = self._generate_mock_factors(opt_name, scenario, user_context)
            option = DecisionOption(opt_name, factors)
            decision_options.append(option)
        
        # Sort by score
        decision_options.sort(key=lambda x: x.total_score(), reverse=True)
        
        # Get best option
        best_option = decision_options[0]
        
        # Generate reasoning
        reasoning = self._generate_reasoning(best_option, decision_options[1] if len(decision_options) > 1 else None)
        
        return {
            "status": "success",
            "scenario": scenario,
            "recommendation": best_option.name,
            "confidence": min(0.95, best_option.total_score() / 10.0),
            "reasoning": reasoning,
            "all_options": [opt.to_dict() for opt in decision_options],
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_mock_factors(self, option_name: str, scenario: str, 
                               user_context: Optional[Dict[str, Any]]) -> List[DecisionFactor]:
        """Generate mock decision factors"""
        
        import hashlib
        
        # Use hash to make deterministic but varied scores
        hash_val = int(hashlib.md5(f"{option_name}{scenario}".encode()).hexdigest(), 16)
        
        factors = [
            DecisionFactor(
                name="Financial Impact",
                weight=0.3,
                value=(hash_val % 100) / 100.0,
                description="Economic consequences of this choice"
            ),
            DecisionFactor(
                name="Time Investment",
                weight=0.2,
                value=((hash_val // 100) % 100) / 100.0,
                description="Time required for this option"
            ),
            DecisionFactor(
                name="Personal Growth",
                weight=0.25,
                value=((hash_val // 10000) % 100) / 100.0,
                description="Potential for personal development"
            ),
            DecisionFactor(
                name="Risk Level",
                weight=0.15,
                value=1.0 - ((hash_val // 1000000) % 100) / 100.0,  # Lower risk is better
                description="Associated risks and uncertainties"
            ),
            DecisionFactor(
                name="Alignment with Goals",
                weight=0.1,
                value=((hash_val // 100000000) % 100) / 100.0,
                description="How well this aligns with your goals"
            ),
        ]
        
        # Adjust based on user context
        if user_context:
            priority = user_context.get("priority", "balanced")
            
            if priority == "financial":
                factors[0].weight = 0.5  # Increase financial weight
                factors[2].weight = 0.1  # Decrease growth weight
            elif priority == "growth":
                factors[2].weight = 0.4  # Increase growth weight
                factors[0].weight = 0.2  # Decrease financial weight
            elif priority == "low_risk":
                factors[3].weight = 0.4  # Increase risk weight
        
        return factors
    
    def _generate_reasoning(self, best_option: DecisionOption, 
                           second_option: Optional[DecisionOption]) -> str:
        """Generate human-readable reasoning"""
        
        best_score = best_option.total_score()
        
        # Find strongest factor
        strongest_factor = max(best_option.factors, key=lambda f: f.score())
        
        reasoning = f"I recommend '{best_option.name}' based on comprehensive analysis. "
        reasoning += f"This option scores highest overall ({best_score:.2f}/10) with particular strength in {strongest_factor.name}. "
        
        if second_option:
            score_diff = best_score - second_option.total_score()
            if score_diff < 0.5:
                reasoning += f"Note that '{second_option.name}' is a close second (difference: {score_diff:.2f}), so consider your personal priorities carefully."
            else:
                reasoning += f"It clearly outperforms other options by a significant margin."
        
        return reasoning
    
    def track_decision(self, user_id: str, scenario: str, chosen_option: str, 
                      recommended_option: str) -> Dict[str, Any]:
        """Track decision for learning (future enhancement)"""
        
        logger.info(f"Decision tracked for {user_id}: {scenario} -> {chosen_option}")
        
        return {
            "status": "tracked",
            "user_id": user_id,
            "scenario": scenario,
            "chosen": chosen_option,
            "recommended": recommended_option,
            "followed_recommendation": chosen_option == recommended_option
        }


# Global instance
_lifesync_module = None


def get_lifesync_module() -> LifeSyncModule:
    """Get or create the global LifeSyncModule instance"""
    global _lifesync_module
    if _lifesync_module is None:
        _lifesync_module = LifeSyncModule()
    return _lifesync_module
