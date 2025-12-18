"""
Output Composer - Composes unified responses from agent swarm outputs.

This module takes outputs from multiple agents and composes them into
a coherent, unified response that maintains VOBee's voice.
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentOutput:
    """Represents output from a single agent."""
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        output: Any,
        confidence: float,
        processing_time: float
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.output = output
        self.confidence = confidence
        self.processing_time = processing_time
        self.timestamp = datetime.utcnow()


class OutputComposer:
    """
    Composes unified responses from multiple agent outputs.
    
    Features:
    - Multi-agent output aggregation
    - Confidence-weighted synthesis
    - Format standardization
    - Quality validation
    """
    
    def __init__(self):
        self.composition_strategies = {
            "consensus": self._consensus_strategy,
            "highest_confidence": self._highest_confidence_strategy,
            "weighted_average": self._weighted_average_strategy,
            "comprehensive": self._comprehensive_strategy,
        }
    
    def compose(
        self,
        agent_outputs: List[AgentOutput],
        strategy: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Compose unified response from agent outputs.
        
        Args:
            agent_outputs: List of outputs from different agents
            strategy: Composition strategy to use
            
        Returns:
            Unified, composed response
        """
        if not agent_outputs:
            return {
                "success": False,
                "message": "No agent outputs to compose",
                "data": None
            }
        
        # Select composition strategy
        composer = self.composition_strategies.get(
            strategy,
            self._comprehensive_strategy
        )
        
        # Compose response
        composed = composer(agent_outputs)
        
        # Add metadata
        composed["meta"] = self._generate_metadata(agent_outputs)
        
        return composed
    
    def _consensus_strategy(self, outputs: List[AgentOutput]) -> Dict[str, Any]:
        """
        Use consensus among agents.
        Only include results that multiple agents agree on.
        """
        # Group outputs by similarity
        result_groups = self._group_similar_outputs(outputs)
        
        # Find largest consensus group
        consensus_group = max(result_groups, key=len) if result_groups else []
        
        if len(consensus_group) < 2:
            return {
                "success": False,
                "message": "No consensus reached among agents",
                "data": None,
                "strategy": "consensus"
            }
        
        # Use highest confidence output from consensus group
        best_output = max(consensus_group, key=lambda x: x.confidence)
        
        return {
            "success": True,
            "message": f"Consensus reached by {len(consensus_group)} agents",
            "data": best_output.output,
            "confidence": best_output.confidence,
            "strategy": "consensus",
            "consensus_size": len(consensus_group)
        }
    
    def _highest_confidence_strategy(self, outputs: List[AgentOutput]) -> Dict[str, Any]:
        """
        Use output from agent with highest confidence.
        Simple but effective for single-answer queries.
        """
        best_output = max(outputs, key=lambda x: x.confidence)
        
        return {
            "success": True,
            "message": f"Selected output from {best_output.agent_type} agent",
            "data": best_output.output,
            "confidence": best_output.confidence,
            "strategy": "highest_confidence",
            "agent_id": best_output.agent_id
        }
    
    def _weighted_average_strategy(self, outputs: List[AgentOutput]) -> Dict[str, Any]:
        """
        Combine outputs using confidence-weighted averaging.
        Works for numerical outputs.
        """
        total_weight = sum(o.confidence for o in outputs)
        
        if total_weight == 0:
            return self._highest_confidence_strategy(outputs)
        
        # Attempt weighted average (works for numerical data)
        try:
            weighted_sum = sum(
                float(o.output) * o.confidence 
                for o in outputs
            )
            result = weighted_sum / total_weight
            
            return {
                "success": True,
                "message": f"Weighted average of {len(outputs)} agent outputs",
                "data": result,
                "confidence": total_weight / len(outputs),
                "strategy": "weighted_average"
            }
        except (TypeError, ValueError):
            # Fall back to highest confidence if not numerical
            return self._highest_confidence_strategy(outputs)
    
    def _comprehensive_strategy(self, outputs: List[AgentOutput]) -> Dict[str, Any]:
        """
        Comprehensive strategy that combines all relevant outputs.
        Best for complex queries requiring multiple perspectives.
        """
        # Separate outputs by type
        categorized = self._categorize_outputs(outputs)
        
        # Build comprehensive response
        comprehensive_data = {}
        
        for category, cat_outputs in categorized.items():
            if len(cat_outputs) == 1:
                comprehensive_data[category] = cat_outputs[0].output
            else:
                # Use consensus or highest confidence within category
                best = max(cat_outputs, key=lambda x: x.confidence)
                comprehensive_data[category] = best.output
        
        avg_confidence = sum(o.confidence for o in outputs) / len(outputs)
        
        return {
            "success": True,
            "message": f"Comprehensive synthesis from {len(outputs)} agents",
            "data": comprehensive_data,
            "confidence": avg_confidence,
            "strategy": "comprehensive",
            "categories": list(categorized.keys())
        }
    
    def _group_similar_outputs(self, outputs: List[AgentOutput]) -> List[List[AgentOutput]]:
        """Group outputs by similarity."""
        # Simple grouping by string representation
        groups = {}
        
        for output in outputs:
            key = str(output.output)
            if key not in groups:
                groups[key] = []
            groups[key].append(output)
        
        return list(groups.values())
    
    def _categorize_outputs(self, outputs: List[AgentOutput]) -> Dict[str, List[AgentOutput]]:
        """Categorize outputs by agent type."""
        categorized = {}
        
        for output in outputs:
            category = output.agent_type
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(output)
        
        return categorized
    
    def _generate_metadata(self, outputs: List[AgentOutput]) -> Dict[str, Any]:
        """Generate metadata about the composition."""
        return {
            "agent_count": len(outputs),
            "agent_types": list(set(o.agent_type for o in outputs)),
            "avg_confidence": sum(o.confidence for o in outputs) / len(outputs) if outputs else 0,
            "total_processing_time": sum(o.processing_time for o in outputs),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def validate_output(self, composed: Dict[str, Any]) -> bool:
        """
        Validate composed output meets quality standards.
        
        Args:
            composed: Composed output to validate
            
        Returns:
            True if output is valid
        """
        # Check minimum requirements
        if not composed.get("success"):
            return False
        
        if composed.get("data") is None:
            return False
        
        # Check confidence threshold
        min_confidence = 0.3
        if composed.get("confidence", 0) < min_confidence:
            logger.warning(f"Output confidence below threshold: {composed.get('confidence')}")
            return False
        
        return True
    
    def format_for_user(self, composed: Dict[str, Any]) -> str:
        """
        Format composed output for user presentation.
        
        Args:
            composed: Composed output
            
        Returns:
            User-friendly formatted string
        """
        if not composed.get("success"):
            return f"❌ {composed.get('message', 'Operation failed')}"
        
        data = composed.get("data")
        confidence = composed.get("confidence", 0)
        
        # Format based on data type
        if isinstance(data, dict):
            lines = ["✅ Result:"]
            for key, value in data.items():
                lines.append(f"  • {key}: {value}")
            lines.append(f"\n🎯 Confidence: {confidence:.1%}")
            return "\n".join(lines)
        
        elif isinstance(data, list):
            lines = ["✅ Results:"]
            for i, item in enumerate(data, 1):
                lines.append(f"  {i}. {item}")
            lines.append(f"\n🎯 Confidence: {confidence:.1%}")
            return "\n".join(lines)
        
        else:
            return f"✅ Result: {data}\n🎯 Confidence: {confidence:.1%}"
