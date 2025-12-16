"""
Agent Registry - Role-based Multi-Agent System

Manages 30-100 logical agent roles without hard-coding API dependencies.
"""

from .registry import AgentRegistry, Agent, AgentRole, AgentCapability

__all__ = ["AgentRegistry", "Agent", "AgentRole", "AgentCapability"]
