"""
Research Factory Module
Provides interfaces and implementations for market analysis, research agents,
and data-driven research workflows.
"""

from typing import Dict, Any, Optional
from .base import ResearchFactory, ResearchType
from .market_analysis import MarketAnalysisWorkflow
from .research_agent import ResearchAgentWorkflow

__all__ = [
    "ResearchFactory",
    "ResearchType",
    "MarketAnalysisWorkflow",
    "ResearchAgentWorkflow",
]


class ResearchFactoryRegistry:
    """Central registry for research workflow factories"""
    
    _workflows = {
        ResearchType.MARKET_ANALYSIS: MarketAnalysisWorkflow,
        ResearchType.RESEARCH_AGENT: ResearchAgentWorkflow,
    }
    
    @classmethod
    def get_workflow(cls, research_type: ResearchType, config: Optional[Dict[str, Any]] = None):
        """
        Get a workflow instance for the specified research type.
        
        Args:
            research_type: Type of research workflow to create
            config: Optional configuration dictionary
            
        Returns:
            Instance of the requested workflow
            
        Raises:
            ValueError: If research_type is not supported
        """
        if research_type not in cls._workflows:
            raise ValueError(f"Unsupported research type: {research_type}")
        
        workflow_class = cls._workflows[research_type]
        return workflow_class(config or {})
    
    @classmethod
    def list_available_workflows(cls):
        """List all available research workflow types"""
        return list(cls._workflows.keys())
