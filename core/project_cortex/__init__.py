"""
Project Cortex - Multi-Project Management System

Handles multiple projects with isolated memory, goals, budget profiles,
and active agent tracking.
"""

from .project_manager import ProjectManager, Project

__all__ = ["ProjectManager", "Project"]
