"""
Agent Registry - Role-based agent management system.

This package provides capabilities for managing AI agents with
role-based definitions, avoiding vendor dependencies.
"""

from .registry import AgentRegistry, Agent, AgentRole, AgentStatus, AgentCapability

__all__ = ['AgentRegistry', 'Agent', 'AgentRole', 'AgentStatus', 'AgentCapability']
