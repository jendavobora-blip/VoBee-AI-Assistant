"""
Research Factory Core Implementation

Main factory class for coordinating market analysis and research workflows.
Provides a modular, interface-driven approach for future extensions.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchFactory:
    """
    Core Research Factory class for managing market analysis and research workflows.
    
    This factory coordinates market analysis, research collaboration, and data-driven
    insights, providing a unified interface for research operations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Research Factory.
        
        Args:
            config: Optional configuration dictionary for factory settings
        """
        self.config = config or {}
        self.analyzers = {}
        self.collaborators = {}
        self.research_queue = []
        self.initialized = False
        
        logger.info("Initializing Research Factory")
        self._setup_components()
    
    def _setup_components(self):
        """Initialize research components."""
        from .market_analysis import MarketAnalyzer
        from .research_collaboration import ResearchCollaborator
        
        self.analyzers['market'] = MarketAnalyzer(self.config.get('market', {}))
        self.collaborators['research'] = ResearchCollaborator(self.config.get('collaboration', {}))
        
        self.initialized = True
        logger.info("Research Factory components initialized")
    
    def analyze_market(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform market analysis.
        
        Args:
            params: Parameters for market analysis (symbol, timeframe, metrics, etc.)
        
        Returns:
            Dictionary containing the analysis results
        """
        logger.info(f"Starting market analysis with params: {params}")
        
        analyzer = self.analyzers['market']
        result = analyzer.analyze(params)
        
        return {
            'status': 'success',
            'analysis_type': 'market',
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def initiate_research(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate a research collaboration workflow.
        
        Args:
            params: Parameters for research workflow (topic, sources, collaboration_type, etc.)
        
        Returns:
            Dictionary containing the research workflow result
        """
        logger.info(f"Initiating research workflow with params: {params}")
        
        collaborator = self.collaborators['research']
        result = collaborator.collaborate(params)
        
        return {
            'status': 'success',
            'workflow_type': 'research',
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_analyzer(self, analyzer_type: str):
        """
        Get a specific analyzer.
        
        Args:
            analyzer_type: Type of analyzer to retrieve
        
        Returns:
            The requested analyzer instance
        """
        return self.analyzers.get(analyzer_type)
    
    def get_collaborator(self, collaborator_type: str):
        """
        Get a specific collaborator.
        
        Args:
            collaborator_type: Type of collaborator to retrieve
        
        Returns:
            The requested collaborator instance
        """
        return self.collaborators.get(collaborator_type)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Research Factory.
        
        Returns:
            Dictionary containing factory status information
        """
        return {
            'initialized': self.initialized,
            'analyzers': list(self.analyzers.keys()),
            'collaborators': list(self.collaborators.keys()),
            'research_queue_size': len(self.research_queue),
            'timestamp': datetime.utcnow().isoformat()
        }
