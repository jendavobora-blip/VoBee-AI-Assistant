"""
Agents System - Role-Based Agent Registry
Supports 30-100 logical roles with flexible architecture
"""

from .agent_registry import AgentRegistry
from .agent_roles import AgentRole, RoleCategory
from .base_agent import BaseAgent

__all__ = [
    'AgentRegistry',
    'AgentRole',
    'RoleCategory',
    'BaseAgent'
]
