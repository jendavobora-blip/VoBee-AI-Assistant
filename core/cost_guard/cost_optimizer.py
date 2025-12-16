"""
Cost Optimizer - Provides recommendations for cost reduction.

Analyzes spending patterns and suggests optimizations.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter


class CostOptimizer:
    """
    Analyzes costs and provides optimization recommendations.
    
    Features:
    - Spending pattern analysis
    - Optimization recommendations
    - Cost-saving strategies
    - ROI analysis
    """
    
    def __init__(self):
        """Initialize cost optimizer."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        self.logger.info("CostOptimizer initialized")
    
    def analyze_spending_patterns(
        self,
        transactions: List[Dict],
        time_window: timedelta = timedelta(days=7)
    ) -> Dict:
        """
        Analyze spending patterns.
        
        Args:
            transactions: List of cost transactions
            time_window: Time window for analysis
            
        Returns:
            Analysis results
        """
        # Filter recent transactions
        cutoff = datetime.utcnow() - time_window
        recent_transactions = [
            t for t in transactions
            if datetime.fromisoformat(t["timestamp"]) >= cutoff
        ]
        
        if not recent_transactions:
            return {
                "pattern": "insufficient_data",
                "message": "Not enough transaction data for analysis"
            }
        
        # Analyze by service
        service_costs = Counter()
        for t in recent_transactions:
            service_costs[t["service"]] += t["amount"]
        
        total_cost = sum(service_costs.values())
        
        # Find dominant services (>50% of spending)
        dominant_services = [
            service for service, cost in service_costs.items()
            if (cost / total_cost) > 0.5
        ]
        
        # Calculate daily average
        days = max(1, time_window.days)
        daily_average = total_cost / days
        
        analysis = {
            "time_window_days": days,
            "total_transactions": len(recent_transactions),
            "total_cost": total_cost,
            "daily_average": daily_average,
            "service_breakdown": dict(service_costs),
            "dominant_services": dominant_services,
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        return analysis
    
    def get_optimization_recommendations(
        self,
        cost_report: Dict,
        transactions: List[Dict]
    ) -> List[Dict]:
        """
        Generate cost optimization recommendations.
        
        Args:
            cost_report: Cost report from CostMonitor
            transactions: Transaction history
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check ceiling utilization
        utilization = cost_report.get("utilization_percentage")
        if utilization and utilization > 80:
            recommendations.append({
                "priority": "high",
                "category": "budget_management",
                "title": "Approaching cost ceiling",
                "description": (
                    f"You've used {utilization:.1f}% of your budget ceiling. "
                    "Consider reviewing high-cost services or increasing the ceiling."
                ),
                "potential_savings": None
            })
        
        # Analyze service costs
        cost_by_service = cost_report.get("cost_by_service", {})
        if cost_by_service:
            total_cost = cost_report["total_cost"]
            
            for service, cost in sorted(
                cost_by_service.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                percentage = (cost / total_cost) * 100 if total_cost > 0 else 0
                
                # High-cost service recommendations
                if percentage > 50:
                    recommendations.append({
                        "priority": "medium",
                        "category": "service_optimization",
                        "title": f"{service} accounts for {percentage:.1f}% of costs",
                        "description": (
                            f"Consider optimizing {service} usage, implementing "
                            "caching, or exploring cheaper alternatives."
                        ),
                        "potential_savings": cost * 0.3  # Estimated 30% savings
                    })
        
        # Check for frequent small transactions (inefficient)
        small_transactions = [
            t for t in transactions
            if t["amount"] < 0.01
        ]
        
        if len(small_transactions) > len(transactions) * 0.5:
            recommendations.append({
                "priority": "low",
                "category": "efficiency",
                "title": "Many small transactions detected",
                "description": (
                    "Consider batching requests to reduce overhead and "
                    "potentially negotiate better rates for bulk operations."
                ),
                "potential_savings": None
            })
        
        # Check for unused services
        recent_cutoff = datetime.utcnow() - timedelta(days=7)
        recent_services = set()
        
        for t in transactions:
            if datetime.fromisoformat(t["timestamp"]) >= recent_cutoff:
                recent_services.add(t["service"])
        
        all_services = set(cost_by_service.keys())
        inactive_services = all_services - recent_services
        
        if inactive_services:
            total_inactive_cost = sum(
                cost_by_service.get(s, 0) for s in inactive_services
            )
            
            if total_inactive_cost > 0:
                recommendations.append({
                    "priority": "medium",
                    "category": "resource_cleanup",
                    "title": f"{len(inactive_services)} services inactive for 7+ days",
                    "description": (
                        f"Services {', '.join(inactive_services)} haven't been used recently. "
                        "Consider deactivating or reviewing their necessity."
                    ),
                    "potential_savings": total_inactive_cost
                })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda r: priority_order.get(r["priority"], 3))
        
        return recommendations
    
    def estimate_monthly_cost(
        self,
        transactions: List[Dict],
        lookback_days: int = 7
    ) -> Dict:
        """
        Estimate monthly cost based on recent spending.
        
        Args:
            transactions: Transaction history
            lookback_days: Days to use for projection
            
        Returns:
            Monthly cost estimate
        """
        # Get recent transactions
        cutoff = datetime.utcnow() - timedelta(days=lookback_days)
        recent_transactions = [
            t for t in transactions
            if datetime.fromisoformat(t["timestamp"]) >= cutoff
        ]
        
        if not recent_transactions:
            return {
                "estimated_monthly_cost": 0.0,
                "confidence": "none",
                "message": "Insufficient data for estimation"
            }
        
        # Calculate daily average
        total_cost = sum(t["amount"] for t in recent_transactions)
        daily_average = total_cost / lookback_days
        
        # Project to 30 days
        estimated_monthly = daily_average * 30
        
        # Determine confidence based on data availability
        if lookback_days >= 7:
            confidence = "high"
        elif lookback_days >= 3:
            confidence = "medium"
        else:
            confidence = "low"
        
        return {
            "estimated_monthly_cost": estimated_monthly,
            "daily_average": daily_average,
            "lookback_days": lookback_days,
            "transaction_count": len(recent_transactions),
            "confidence": confidence,
            "estimated_at": datetime.utcnow().isoformat()
        }
    
    def calculate_roi(
        self,
        cost: float,
        value_generated: float,
        time_period: str = "unknown"
    ) -> Dict:
        """
        Calculate return on investment.
        
        Args:
            cost: Total cost incurred
            value_generated: Value generated (in dollars or equivalent metric)
            time_period: Time period for the calculation
            
        Returns:
            ROI analysis
        """
        if cost == 0:
            return {
                "roi_percentage": float('inf'),
                "net_value": value_generated,
                "message": "Zero cost - infinite ROI"
            }
        
        roi_percentage = ((value_generated - cost) / cost) * 100
        net_value = value_generated - cost
        
        # Determine ROI category
        if roi_percentage > 100:
            category = "excellent"
        elif roi_percentage > 50:
            category = "good"
        elif roi_percentage > 0:
            category = "positive"
        else:
            category = "negative"
        
        return {
            "roi_percentage": roi_percentage,
            "net_value": net_value,
            "category": category,
            "cost": cost,
            "value_generated": value_generated,
            "time_period": time_period,
            "calculated_at": datetime.utcnow().isoformat()
        }
