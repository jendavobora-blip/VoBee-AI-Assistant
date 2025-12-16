"""
Decision Gate - Confirmation and control system for critical actions.

This module provides a minimal confirmation system for controlling
critical actions through YES/NO gates with modular rule support.
"""

from .gate import DecisionGate, GateRule, GateDecision, GateRulePriority, DecisionRequest

__all__ = ['DecisionGate', 'GateRule', 'GateDecision', 'GateRulePriority', 'DecisionRequest']
