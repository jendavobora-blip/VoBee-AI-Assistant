"""
Decision Gate - Explicit YES/NO confirmation system.

Ensures human oversight for critical operations before execution.
"""

from .decision_manager import DecisionManager, DecisionType, DecisionStatus
from .confirmation_workflow import ConfirmationWorkflow

__all__ = [
    "DecisionManager",
    "DecisionType",
    "DecisionStatus",
    "ConfirmationWorkflow",
]
