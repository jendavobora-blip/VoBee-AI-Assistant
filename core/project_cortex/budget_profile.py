"""
Budget Profile - Per-project budget management and tracking.

Monitors costs, enforces limits, and provides budget analytics.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class BudgetProfile:
    """
    Manages budget tracking and limits for a project.
    
    Features:
    - Cost tracking by category
    - Budget limit enforcement
    - Spending analytics
    - Alert thresholds
    """
    
    def __init__(
        self,
        project_id: str,
        budget_limit: Optional[float] = None,
        storage_path: str = "data/projects/budgets"
    ):
        """
        Initialize budget profile.
        
        Args:
            project_id: Unique project identifier
            budget_limit: Maximum budget in dollars (None for unlimited)
            storage_path: Directory for budget data storage
        """
        self.project_id = project_id
        self.budget_limit = budget_limit
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.total_spent: float = 0.0
        self.spending_by_category: Dict[str, float] = {}
        self.transactions: List[Dict] = []
        
        # Alert thresholds (percentages of budget limit)
        self.alert_thresholds = [0.5, 0.75, 0.9, 1.0]
        self.triggered_alerts: List[float] = []
        
        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.{project_id}")
        self.logger.setLevel(logging.INFO)
        
        # Load existing budget data
        self._load_budget()
        
        self.logger.info(
            f"BudgetProfile initialized for project: {project_id}, "
            f"limit: ${budget_limit if budget_limit else 'unlimited'}"
        )
    
    def add_transaction(
        self,
        amount: float,
        category: str,
        description: str = "",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Record a budget transaction.
        
        Args:
            amount: Transaction amount in dollars
            category: Spending category (e.g., 'api_calls', 'compute', 'storage')
            description: Transaction description
            metadata: Optional additional data
            
        Returns:
            Transaction record
        """
        transaction = {
            "amount": amount,
            "category": category,
            "description": description,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update totals
        self.total_spent += amount
        self.spending_by_category[category] = \
            self.spending_by_category.get(category, 0.0) + amount
        
        self.transactions.append(transaction)
        
        # Check budget alerts
        self._check_alerts()
        
        self._save_budget()
        
        self.logger.info(
            f"Transaction recorded: ${amount:.4f} ({category}) - "
            f"Total: ${self.total_spent:.2f}"
        )
        
        return transaction
    
    def get_remaining_budget(self) -> Optional[float]:
        """
        Get remaining budget.
        
        Returns:
            Remaining budget or None if unlimited
        """
        if self.budget_limit is None:
            return None
        
        return max(0.0, self.budget_limit - self.total_spent)
    
    def get_budget_utilization(self) -> Optional[float]:
        """
        Get budget utilization percentage.
        
        Returns:
            Utilization percentage or None if unlimited
        """
        if self.budget_limit is None or self.budget_limit == 0:
            return None
        
        return (self.total_spent / self.budget_limit) * 100
    
    def is_over_budget(self) -> bool:
        """Check if spending exceeds budget limit."""
        if self.budget_limit is None:
            return False
        
        return self.total_spent > self.budget_limit
    
    def can_afford(self, amount: float) -> bool:
        """
        Check if a transaction is affordable within budget.
        
        Args:
            amount: Amount to check
            
        Returns:
            True if affordable, False otherwise
        """
        if self.budget_limit is None:
            return True
        
        return (self.total_spent + amount) <= self.budget_limit
    
    def get_spending_report(self) -> Dict:
        """
        Generate a spending report.
        
        Returns:
            Dictionary with spending analytics
        """
        report = {
            "project_id": self.project_id,
            "total_spent": self.total_spent,
            "budget_limit": self.budget_limit,
            "remaining_budget": self.get_remaining_budget(),
            "utilization_percentage": self.get_budget_utilization(),
            "is_over_budget": self.is_over_budget(),
            "spending_by_category": self.spending_by_category,
            "transaction_count": len(self.transactions),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return report
    
    def get_transactions(
        self,
        category: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get transaction history with optional filters.
        
        Args:
            category: Filter by category
            limit: Maximum number of transactions to return
            
        Returns:
            List of transactions
        """
        transactions = self.transactions
        
        if category:
            transactions = [t for t in transactions if t["category"] == category]
        
        if limit:
            transactions = transactions[-limit:]
        
        return transactions
    
    def _check_alerts(self):
        """Check and trigger budget alerts."""
        if self.budget_limit is None:
            return
        
        utilization = self.get_budget_utilization()
        if utilization is None:
            return
        
        for threshold in self.alert_thresholds:
            threshold_percent = threshold * 100
            
            if utilization >= threshold_percent and threshold not in self.triggered_alerts:
                self.triggered_alerts.append(threshold)
                
                self.logger.warning(
                    f"Budget alert: {threshold_percent}% threshold reached "
                    f"(${self.total_spent:.2f} / ${self.budget_limit:.2f})"
                )
                
                # TODO: Integrate with notification system for critical alerts
    
    def _save_budget(self):
        """Save budget data to disk."""
        budget_data = {
            "project_id": self.project_id,
            "budget_limit": self.budget_limit,
            "total_spent": self.total_spent,
            "spending_by_category": self.spending_by_category,
            "transactions": self.transactions,
            "triggered_alerts": self.triggered_alerts
        }
        
        budget_file = self.storage_path / f"{self.project_id}.json"
        with open(budget_file, 'w') as f:
            json.dump(budget_data, f, indent=2)
    
    def _load_budget(self):
        """Load budget data from disk."""
        budget_file = self.storage_path / f"{self.project_id}.json"
        
        if budget_file.exists():
            with open(budget_file, 'r') as f:
                budget_data = json.load(f)
                
                self.total_spent = budget_data.get("total_spent", 0.0)
                self.spending_by_category = budget_data.get("spending_by_category", {})
                self.transactions = budget_data.get("transactions", [])
                self.triggered_alerts = budget_data.get("triggered_alerts", [])
