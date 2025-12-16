"""
Cost Monitor - Real-time cost tracking and alerting.

Monitors spending across services and enforces cost ceilings.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from collections import defaultdict


class CostMonitor:
    """
    Monitors and enforces cost limits.
    
    Features:
    - Real-time cost tracking
    - Cost ceiling enforcement
    - Alert thresholds
    - Spending analytics
    """
    
    def __init__(
        self,
        global_cost_ceiling: Optional[float] = None,
        alert_thresholds: Optional[List[float]] = None
    ):
        """
        Initialize cost monitor.
        
        Args:
            global_cost_ceiling: Maximum total spending allowed (None for unlimited)
            alert_thresholds: Alert at these percentages of ceiling (e.g., [0.5, 0.75, 0.9])
        """
        self.global_cost_ceiling = global_cost_ceiling
        self.alert_thresholds = alert_thresholds or [0.5, 0.75, 0.9]
        
        self.total_cost: float = 0.0
        self.cost_by_service: Dict[str, float] = defaultdict(float)
        self.cost_by_project: Dict[str, float] = defaultdict(float)
        self.transactions: List[Dict] = []
        
        self.triggered_alerts: List[float] = []
        self.alert_callbacks: List[Callable] = []
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        self.logger.info(
            f"CostMonitor initialized with ceiling: "
            f"${global_cost_ceiling if global_cost_ceiling else 'unlimited'}"
        )
    
    def record_cost(
        self,
        amount: float,
        service: str,
        project_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Record a cost transaction.
        
        Args:
            amount: Cost amount in dollars
            service: Service that incurred the cost
            project_id: Associated project (if any)
            metadata: Additional transaction metadata
            
        Returns:
            True if transaction was allowed, False if blocked by ceiling
        """
        # Check if this would exceed ceiling
        if self.global_cost_ceiling:
            if (self.total_cost + amount) > self.global_cost_ceiling:
                self.logger.error(
                    f"Cost transaction BLOCKED: ${amount:.4f} would exceed ceiling "
                    f"(${self.total_cost:.2f} + ${amount:.4f} > ${self.global_cost_ceiling:.2f})"
                )
                return False
        
        # Record transaction
        transaction = {
            "amount": amount,
            "service": service,
            "project_id": project_id,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.transactions.append(transaction)
        self.total_cost += amount
        self.cost_by_service[service] += amount
        
        if project_id:
            self.cost_by_project[project_id] += amount
        
        # Check alert thresholds
        self._check_alerts()
        
        self.logger.debug(
            f"Cost recorded: ${amount:.4f} ({service}) - Total: ${self.total_cost:.2f}"
        )
        
        return True
    
    def can_afford(self, amount: float) -> bool:
        """
        Check if an operation can be afforded within the ceiling.
        
        Args:
            amount: Amount to check
            
        Returns:
            True if affordable, False otherwise
        """
        if self.global_cost_ceiling is None:
            return True
        
        return (self.total_cost + amount) <= self.global_cost_ceiling
    
    def get_remaining_budget(self) -> Optional[float]:
        """
        Get remaining budget before hitting ceiling.
        
        Returns:
            Remaining budget or None if unlimited
        """
        if self.global_cost_ceiling is None:
            return None
        
        return max(0.0, self.global_cost_ceiling - self.total_cost)
    
    def get_utilization(self) -> Optional[float]:
        """
        Get cost ceiling utilization percentage.
        
        Returns:
            Utilization percentage or None if unlimited
        """
        if self.global_cost_ceiling is None or self.global_cost_ceiling == 0:
            return None
        
        return (self.total_cost / self.global_cost_ceiling) * 100
    
    def is_over_ceiling(self) -> bool:
        """Check if spending has exceeded ceiling."""
        if self.global_cost_ceiling is None:
            return False
        
        return self.total_cost > self.global_cost_ceiling
    
    def get_cost_report(
        self,
        time_range: Optional[timedelta] = None
    ) -> Dict:
        """
        Generate a cost report.
        
        Args:
            time_range: Optional time range for report (e.g., last 24 hours)
            
        Returns:
            Cost report dictionary
        """
        transactions = self.transactions
        
        # Filter by time range if specified
        if time_range:
            cutoff = datetime.utcnow() - time_range
            transactions = [
                t for t in transactions
                if datetime.fromisoformat(t["timestamp"]) >= cutoff
            ]
        
        # Calculate costs from filtered transactions
        if time_range:
            total = sum(t["amount"] for t in transactions)
            by_service = defaultdict(float)
            by_project = defaultdict(float)
            
            for t in transactions:
                by_service[t["service"]] += t["amount"]
                if t["project_id"]:
                    by_project[t["project_id"]] += t["amount"]
        else:
            total = self.total_cost
            by_service = dict(self.cost_by_service)
            by_project = dict(self.cost_by_project)
        
        report = {
            "total_cost": total,
            "cost_ceiling": self.global_cost_ceiling,
            "remaining_budget": self.get_remaining_budget(),
            "utilization_percentage": self.get_utilization(),
            "is_over_ceiling": self.is_over_ceiling(),
            "cost_by_service": by_service,
            "cost_by_project": by_project,
            "transaction_count": len(transactions),
            "time_range": str(time_range) if time_range else "all_time",
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return report
    
    def get_top_spending_services(self, limit: int = 5) -> List[Dict]:
        """
        Get top spending services.
        
        Args:
            limit: Number of top services to return
            
        Returns:
            List of services with their spending
        """
        sorted_services = sorted(
            self.cost_by_service.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {"service": service, "cost": cost}
            for service, cost in sorted_services[:limit]
        ]
    
    def register_alert_callback(self, callback: Callable):
        """
        Register a callback for cost alerts.
        
        Args:
            callback: Function to call when alert triggered (receives threshold and cost)
        """
        self.alert_callbacks.append(callback)
        self.logger.info("Alert callback registered")
    
    def set_cost_ceiling(self, ceiling: Optional[float]):
        """
        Update the global cost ceiling.
        
        Args:
            ceiling: New ceiling (None for unlimited)
        """
        old_ceiling = self.global_cost_ceiling
        self.global_cost_ceiling = ceiling
        
        # Reset triggered alerts when ceiling changes
        self.triggered_alerts = []
        
        self.logger.info(
            f"Cost ceiling updated: "
            f"${old_ceiling if old_ceiling else 'unlimited'} → "
            f"${ceiling if ceiling else 'unlimited'}"
        )
        
        # Check if we're already over the new ceiling
        if ceiling and self.total_cost > ceiling:
            self.logger.warning(
                f"Current spending (${self.total_cost:.2f}) "
                f"exceeds new ceiling (${ceiling:.2f})"
            )
    
    def _check_alerts(self):
        """Check and trigger cost alerts."""
        if self.global_cost_ceiling is None:
            return
        
        utilization = self.get_utilization()
        if utilization is None:
            return
        
        for threshold in self.alert_thresholds:
            threshold_percent = threshold * 100
            
            if utilization >= threshold_percent and threshold not in self.triggered_alerts:
                self.triggered_alerts.append(threshold)
                
                self.logger.warning(
                    f"💰 COST ALERT: {threshold_percent}% threshold reached! "
                    f"(${self.total_cost:.2f} / ${self.global_cost_ceiling:.2f})"
                )
                
                # Call registered callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(threshold, self.total_cost)
                    except Exception as e:
                        self.logger.error(f"Alert callback failed: {e}")
