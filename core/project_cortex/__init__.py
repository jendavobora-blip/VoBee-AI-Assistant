"""
Project Cortex - Multi-Project Management Brain
Handles 1-50 parallel projects with isolated memory, goals, budgets, and agents
"""

from .project_manager import ProjectManager
from .project import Project
from .memory_manager import MemoryManager
from .budget_manager import BudgetManager
from .agent_tracker import AgentTracker

__all__ = [
    'ProjectManager',
    'Project',
    'MemoryManager',
    'BudgetManager',
    'AgentTracker'
]
