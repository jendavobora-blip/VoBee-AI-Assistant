"""
Cost Tracker with Langfuse Integration
Tracks API usage and costs with configurable limits
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from langfuse import Langfuse

logger = logging.getLogger(__name__)

LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "pk-lf-mock-key")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "sk-lf-mock-key")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

DAILY_COST_LIMIT = float(os.getenv("DAILY_COST_LIMIT", "10.0"))
HOURLY_COST_LIMIT = float(os.getenv("HOURLY_COST_LIMIT", "2.0"))


class CostTracker:
    """Tracks costs and enforces limits"""
    
    def __init__(self):
        self.langfuse_client = None
        self.user_costs = defaultdict(lambda: {"hourly": 0.0, "daily": 0.0, "total": 0.0})
        self.user_timestamps = defaultdict(lambda: {"hourly_reset": datetime.utcnow(), 
                                                     "daily_reset": datetime.utcnow()})
        self._initialize_langfuse()
    
    def _initialize_langfuse(self):
        """Initialize Langfuse client"""
        try:
            self.langfuse_client = Langfuse(
                public_key=LANGFUSE_PUBLIC_KEY,
                secret_key=LANGFUSE_SECRET_KEY,
                host=LANGFUSE_HOST
            )
            logger.info("Langfuse client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Langfuse: {e}")
            if MOCK_MODE:
                logger.info("Running in mock mode without Langfuse")
    
    def _reset_counters_if_needed(self, user_id: str):
        """Reset hourly/daily counters if time period has elapsed"""
        now = datetime.utcnow()
        timestamps = self.user_timestamps[user_id]
        
        # Reset hourly
        if now - timestamps["hourly_reset"] > timedelta(hours=1):
            self.user_costs[user_id]["hourly"] = 0.0
            timestamps["hourly_reset"] = now
        
        # Reset daily
        if now - timestamps["daily_reset"] > timedelta(days=1):
            self.user_costs[user_id]["daily"] = 0.0
            timestamps["daily_reset"] = now
    
    def check_limits(self, user_id: str) -> Dict[str, Any]:
        """Check if user has exceeded cost limits"""
        self._reset_counters_if_needed(user_id)
        
        costs = self.user_costs[user_id]
        
        result = {
            "allowed": True,
            "reason": None,
            "hourly_usage": costs["hourly"],
            "hourly_limit": HOURLY_COST_LIMIT,
            "daily_usage": costs["daily"],
            "daily_limit": DAILY_COST_LIMIT,
            "total_usage": costs["total"]
        }
        
        if costs["hourly"] >= HOURLY_COST_LIMIT:
            result["allowed"] = False
            result["reason"] = f"Hourly limit exceeded: ${costs['hourly']:.2f} / ${HOURLY_COST_LIMIT:.2f}"
        elif costs["daily"] >= DAILY_COST_LIMIT:
            result["allowed"] = False
            result["reason"] = f"Daily limit exceeded: ${costs['daily']:.2f} / ${DAILY_COST_LIMIT:.2f}"
        
        return result
    
    def track_request(self, user_id: str, operation: str, cost: float, metadata: Optional[Dict[str, Any]] = None):
        """Track a request and its cost"""
        self._reset_counters_if_needed(user_id)
        
        # Update costs
        self.user_costs[user_id]["hourly"] += cost
        self.user_costs[user_id]["daily"] += cost
        self.user_costs[user_id]["total"] += cost
        
        # Log to Langfuse
        if self.langfuse_client:
            try:
                trace = self.langfuse_client.trace(
                    name=operation,
                    user_id=user_id,
                    metadata={
                        "cost": cost,
                        "hourly_total": self.user_costs[user_id]["hourly"],
                        "daily_total": self.user_costs[user_id]["daily"],
                        **(metadata or {})
                    }
                )
                
                # Add cost observation
                trace.generation(
                    name=f"{operation}_cost",
                    model="mock-model" if MOCK_MODE else "unknown",
                    usage={
                        "total": 1,
                        "cost": cost
                    }
                )
                
            except Exception as e:
                logger.warning(f"Failed to log to Langfuse: {e}")
        
        logger.info(f"Tracked request for {user_id}: {operation} (${cost:.4f})")
    
    def get_user_usage(self, user_id: str) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        self._reset_counters_if_needed(user_id)
        
        costs = self.user_costs[user_id]
        timestamps = self.user_timestamps[user_id]
        
        return {
            "user_id": user_id,
            "hourly_usage": costs["hourly"],
            "hourly_limit": HOURLY_COST_LIMIT,
            "hourly_remaining": max(0, HOURLY_COST_LIMIT - costs["hourly"]),
            "hourly_reset_at": timestamps["hourly_reset"].isoformat(),
            "daily_usage": costs["daily"],
            "daily_limit": DAILY_COST_LIMIT,
            "daily_remaining": max(0, DAILY_COST_LIMIT - costs["daily"]),
            "daily_reset_at": timestamps["daily_reset"].isoformat(),
            "total_usage": costs["total"]
        }


# Global instance
_cost_tracker = None


def get_cost_tracker() -> CostTracker:
    """Get or create the global CostTracker instance"""
    global _cost_tracker
    if _cost_tracker is None:
        _cost_tracker = CostTracker()
    return _cost_tracker
