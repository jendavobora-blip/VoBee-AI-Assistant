"""
Core Orchestration Module

Provides interfaces and implementations for project-level workflow coordination
and factory orchestration across Application, Media, and Research Factories.
"""

from .orchestrator import ProjectOrchestrator
from .workflow_manager import WorkflowManager
from .factory_coordinator import FactoryCoordinator

__all__ = [
    'ProjectOrchestrator',
    'WorkflowManager',
    'FactoryCoordinator'
]

__version__ = '0.1.0'
