"""
Identity Keeper - Maintains VOBee personality & unified voice across all interactions.

This module ensures that despite the complexity of the underlying AI swarm,
VOBee maintains a consistent, unified personality in all communications.
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class IdentityKeeper:
    """
    Maintains VOBee's consistent personality and voice across all agent interactions.
    
    Core personality traits:
    - Professional but approachable
    - Intelligent and capable
    - Honest about limitations
    - Proactive in suggesting improvements
    - Respectful of human oversight
    """
    
    def __init__(self):
        self.personality_traits = {
            "name": "VOBee",
            "role": "Self-Evolving AI Assistant",
            "communication_style": "professional_friendly",
            "core_values": [
                "transparency",
                "continuous_improvement",
                "human_oversight",
                "cost_efficiency",
                "innovation"
            ],
            "capabilities": [
                "multi-agent_orchestration",
                "autonomous_learning",
                "tech_scouting",
                "content_generation",
                "predictive_analytics"
            ]
        }
        self.interaction_history: List[Dict[str, Any]] = []
    
    def apply_personality(self, raw_response: str, context: Dict[str, Any]) -> str:
        """
        Apply VOBee's personality to a raw response from the agent swarm.
        
        Args:
            raw_response: Unprocessed response from agents
            context: Context about the interaction
            
        Returns:
            Response with VOBee's personality applied
        """
        # Add personality markers
        if context.get("requires_approval"):
            response = self._add_approval_language(raw_response)
        else:
            response = self._add_conversational_tone(raw_response)
        
        # Log interaction for consistency
        self._log_interaction(response, context)
        
        return response
    
    def _add_approval_language(self, text: str) -> str:
        """Add human-in-the-loop approval language."""
        return f"""I've analyzed your request and prepared an action plan.

{text}

Please confirm if you'd like me to proceed with this action."""
    
    def _add_conversational_tone(self, text: str) -> str:
        """Add conversational, professional tone."""
        # Add greeting if first interaction
        if not self.interaction_history:
            return f"""Hello! I'm VOBee, your self-evolving AI assistant.

{text}

How can I help you further?"""
        return text
    
    def _log_interaction(self, response: str, context: Dict[str, Any]):
        """Log interaction for personality consistency."""
        self.interaction_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "response": response[:200],  # First 200 chars for memory
            "context": context,
            "personality_applied": True
        })
        
        # Keep only last 100 interactions
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]
    
    def get_introduction(self) -> str:
        """Get VOBee's introduction message."""
        return f"""Hello! I'm {self.personality_traits['name']}, a {self.personality_traits['role']}.

I'm powered by a sophisticated multi-agent system that can:
- Scout and integrate new technologies autonomously
- Learn from any data source at high speed
- Generate media (images, videos, voice)
- Optimize costs automatically
- Run simulations to test strategies

I operate with human oversight for critical decisions, ensuring transparency and control.

How can I assist you today?"""
    
    def validate_response_consistency(self, response: str) -> bool:
        """
        Validate that a response is consistent with VOBee's personality.
        
        Args:
            response: Response to validate
            
        Returns:
            True if consistent with personality
        """
        # Check for anti-patterns (things VOBee wouldn't say)
        anti_patterns = [
            "I am unable to",  # VOBee tries to find solutions
            "That's not possible",  # VOBee is proactive
            "I don't know",  # VOBee investigates
        ]
        
        for pattern in anti_patterns:
            if pattern.lower() in response.lower():
                logger.warning(f"Response contains anti-pattern: {pattern}")
                return False
        
        return True
    
    def get_personality_stats(self) -> Dict[str, Any]:
        """Get statistics about personality application."""
        return {
            "total_interactions": len(self.interaction_history),
            "personality_traits": self.personality_traits,
            "consistency_maintained": True
        }
