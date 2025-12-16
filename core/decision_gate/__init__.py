"""
Decision Gate - Strict YES/NO Confirmation System

Controls all critical actions with explicit user confirmation.
"""

from .confirmation_system import DecisionGate, Decision, DecisionType, DecisionStatus

__all__ = ["DecisionGate", "Decision", "DecisionType", "DecisionStatus"]
