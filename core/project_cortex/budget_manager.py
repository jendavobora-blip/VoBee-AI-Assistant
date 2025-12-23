"""
Budget Manager - Handles financial tracking and budget allocation
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TransactionType(Enum):
    """Types of budget transactions"""
    ALLOCATION = "allocation"
    EXPENSE = "expense"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"


class BudgetManager:
    """
    Manages budget profiles and financial tracking for projects
    Supports multiple currencies and transaction history
    """
    
    def __init__(self):
        self.project_budgets: Dict[str, Dict[str, Any]] = {}
        logger.info("BudgetManager initialized")
    
    def create_budget_profile(
        self,
        project_id: str,
        total_budget: float,
        currency: str = "USD"
    ):
        """
        Create a budget profile for a project
        
        Args:
            project_id: Project identifier
            total_budget: Total budget allocation
            currency: Currency code (USD, EUR, etc.)
        """
        self.project_budgets[project_id] = {
            'project_id': project_id,
            'total': total_budget,
            'spent': 0.0,
            'remaining': total_budget,
            'reserved': 0.0,  # Reserved but not spent
            'currency': currency,
            'transactions': [],
            'created_at': datetime.utcnow().isoformat(),
            'last_updated': datetime.utcnow().isoformat()
        }
        
        # Record initial allocation
        self._record_transaction(
            project_id,
            TransactionType.ALLOCATION,
            total_budget,
            f"Initial budget allocation"
        )
        
        logger.info(
            f"Created budget profile for project {project_id}: "
            f"{total_budget} {currency}"
        )
    
    def get_budget(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get budget information for a project"""
        return self.project_budgets.get(project_id)
    
    def record_expense(
        self,
        project_id: str,
        amount: float,
        description: str = "",
        category: str = "general"
    ) -> bool:
        """
        Record an expense against project budget
        
        Args:
            project_id: Project identifier
            amount: Expense amount
            description: Expense description
            category: Expense category
            
        Returns:
            True if expense recorded, False if insufficient budget
        """
        if project_id not in self.project_budgets:
            logger.error(f"Budget profile not found for project {project_id}")
            return False
        
        budget = self.project_budgets[project_id]
        
        # Check if sufficient budget
        if budget['remaining'] < amount:
            logger.warning(
                f"Insufficient budget for project {project_id}: "
                f"Requested {amount} {budget['currency']}, "
                f"Available {budget['remaining']} {budget['currency']}"
            )
            return False
        
        # Record expense
        budget['spent'] += amount
        budget['remaining'] -= amount
        budget['last_updated'] = datetime.utcnow().isoformat()
        
        self._record_transaction(
            project_id,
            TransactionType.EXPENSE,
            amount,
            description,
            category
        )
        
        logger.info(
            f"Recorded expense for project {project_id}: "
            f"{amount} {budget['currency']} - {description}"
        )
        
        return True
    
    def add_budget(
        self,
        project_id: str,
        amount: float,
        description: str = "Budget increase"
    ) -> bool:
        """Add additional budget to a project"""
        if project_id not in self.project_budgets:
            return False
        
        budget = self.project_budgets[project_id]
        budget['total'] += amount
        budget['remaining'] += amount
        budget['last_updated'] = datetime.utcnow().isoformat()
        
        self._record_transaction(
            project_id,
            TransactionType.ALLOCATION,
            amount,
            description
        )
        
        logger.info(
            f"Added budget to project {project_id}: "
            f"{amount} {budget['currency']}"
        )
        
        return True
    
    def reserve_budget(
        self,
        project_id: str,
        amount: float,
        description: str = ""
    ) -> bool:
        """
        Reserve budget for planned expenses
        
        Args:
            project_id: Project identifier
            amount: Amount to reserve
            description: Reservation description
            
        Returns:
            True if reserved successfully
        """
        if project_id not in self.project_budgets:
            return False
        
        budget = self.project_budgets[project_id]
        
        if budget['remaining'] < amount:
            return False
        
        budget['reserved'] += amount
        budget['remaining'] -= amount
        budget['last_updated'] = datetime.utcnow().isoformat()
        
        logger.info(
            f"Reserved budget for project {project_id}: "
            f"{amount} {budget['currency']}"
        )
        
        return True
    
    def release_reservation(
        self,
        project_id: str,
        amount: float
    ) -> bool:
        """Release reserved budget back to available"""
        if project_id not in self.project_budgets:
            return False
        
        budget = self.project_budgets[project_id]
        
        if budget['reserved'] < amount:
            return False
        
        budget['reserved'] -= amount
        budget['remaining'] += amount
        budget['last_updated'] = datetime.utcnow().isoformat()
        
        return True
    
    def get_transaction_history(
        self,
        project_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get transaction history for a project"""
        if project_id not in self.project_budgets:
            return []
        
        transactions = self.project_budgets[project_id]['transactions']
        
        if limit:
            return transactions[-limit:]
        
        return transactions
    
    def get_budget_summary(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive budget summary"""
        if project_id not in self.project_budgets:
            return None
        
        budget = self.project_budgets[project_id]
        
        utilization = 0
        if budget['total'] > 0:
            utilization = (budget['spent'] / budget['total']) * 100
        
        return {
            'project_id': project_id,
            'total_budget': budget['total'],
            'spent': budget['spent'],
            'remaining': budget['remaining'],
            'reserved': budget['reserved'],
            'currency': budget['currency'],
            'utilization_percent': round(utilization, 2),
            'transaction_count': len(budget['transactions']),
            'created_at': budget['created_at'],
            'last_updated': budget['last_updated']
        }
    
    def _record_transaction(
        self,
        project_id: str,
        transaction_type: TransactionType,
        amount: float,
        description: str = "",
        category: str = "general"
    ):
        """Internal method to record a transaction"""
        if project_id not in self.project_budgets:
            return
        
        transaction = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': transaction_type.value,
            'amount': amount,
            'description': description,
            'category': category
        }
        
        self.project_budgets[project_id]['transactions'].append(transaction)
