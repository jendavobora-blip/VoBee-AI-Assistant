"""
Research Factory Module

Provides interfaces and implementations for market analysis and
research-oriented collaboration workflows.
"""

from .research_factory import ResearchFactory
from .market_analysis import MarketAnalyzer
from .research_collaboration import ResearchCollaborator

__all__ = [
    'ResearchFactory',
    'MarketAnalyzer',
    'ResearchCollaborator'
]

__version__ = '0.1.0'
