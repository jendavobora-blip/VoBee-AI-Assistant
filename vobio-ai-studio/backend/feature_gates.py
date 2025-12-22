"""
OpenFeature Integration for Feature Flags
Provides runtime feature toggles without code deployment
"""

import os
import logging
from typing import Dict, Any, Optional
from openfeature import api
from openfeature.provider.in_memory_provider import InMemoryProvider, InMemoryFlag

logger = logging.getLogger(__name__)


class FeatureGates:
    """Feature flag management using OpenFeature"""
    
    def __init__(self):
        self.client = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Setup OpenFeature with in-memory provider"""
        
        # Define default feature flags
        default_flags = {
            "enable_code_execution": InMemoryFlag(
                variants={"on": True, "off": False},
                default_variant="off",
                context_evaluator=None
            ),
            "enable_image_generation": InMemoryFlag(
                variants={"on": True, "off": False},
                default_variant="on",
                context_evaluator=None
            ),
            "enable_video_generation": InMemoryFlag(
                variants={"on": True, "off": False},
                default_variant="on",
                context_evaluator=None
            ),
            "enable_lifesync": InMemoryFlag(
                variants={"on": True, "off": False},
                default_variant="on",
                context_evaluator=None
            ),
            "enable_human_approval": InMemoryFlag(
                variants={"on": True, "off": False},
                default_variant="on",
                context_evaluator=None
            ),
            "enable_cost_tracking": InMemoryFlag(
                variants={"on": True, "off": False},
                default_variant="on",
                context_evaluator=None
            ),
            "enable_safety_checks": InMemoryFlag(
                variants={"on": True, "off": False},
                default_variant="on",
                context_evaluator=None
            ),
        }
        
        # Override from environment
        code_exec_enabled = os.getenv("ENABLE_CODE_EXECUTION", "false").lower() == "true"
        if code_exec_enabled:
            default_flags["enable_code_execution"] = InMemoryFlag(
                variants={"on": True, "off": False},
                default_variant="on",
                context_evaluator=None
            )
        
        # Set provider
        provider = InMemoryProvider(default_flags)
        api.set_provider(provider)
        self.client = api.get_client()
        
        logger.info("OpenFeature initialized with default flags")
    
    def is_enabled(self, feature_name: str, default: bool = False) -> bool:
        """Check if a feature is enabled"""
        try:
            return self.client.get_boolean_value(feature_name, default)
        except Exception as e:
            logger.warning(f"Error checking feature {feature_name}: {e}")
            return default
    
    def get_features_status(self) -> Dict[str, bool]:
        """Get status of all features"""
        features = [
            "enable_code_execution",
            "enable_image_generation",
            "enable_video_generation",
            "enable_lifesync",
            "enable_human_approval",
            "enable_cost_tracking",
            "enable_safety_checks",
        ]
        
        return {
            feature: self.is_enabled(feature)
            for feature in features
        }


# Global instance
_feature_gates = None


def get_feature_gates() -> FeatureGates:
    """Get or create the global FeatureGates instance"""
    global _feature_gates
    if _feature_gates is None:
        _feature_gates = FeatureGates()
    return _feature_gates
