"""
VoBee AI Assistant - Multi-Agent System

This package contains logical AI role definitions for orchestrating 30-100 specialized agents.

Each agent is a logical role with:
- Defined responsibilities and scope
- Guardrails to prevent autonomous actions
- Artifact-based outputs only
- Human-in-the-loop for critical decisions

Agent Categories:
- Architecture & Design
- Development & Engineering
- Research & Analysis
- Compliance & Security
- Media & Content Generation
- Operations & Deployment
"""

__version__ = "1.0.0"

# Agent registry
AGENT_REGISTRY = {}


def register_agent(agent_class):
    """Register an agent in the global registry."""
    AGENT_REGISTRY[agent_class.ROLE_ID] = agent_class
    return agent_class


def get_agent(role_id: str):
    """Get an agent by role ID."""
    return AGENT_REGISTRY.get(role_id)


def list_agents():
    """List all registered agents."""
    return list(AGENT_REGISTRY.keys())
