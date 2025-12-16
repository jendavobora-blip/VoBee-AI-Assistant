"""
Project Cortex - Multi-project management with isolated contexts.

This module provides capabilities for managing multiple projects
with isolated memory, goals, and budget profiles.
"""

from .project_manager import ProjectCortex, Project

__all__ = ['ProjectCortex', 'Project']
