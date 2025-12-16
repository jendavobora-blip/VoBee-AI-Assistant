"""
Confirmation Workflow - Helper utilities for decision confirmation flows.

Provides reusable patterns for common confirmation workflows.
"""

import logging
from typing import Dict, List, Optional, Callable
from .decision_manager import DecisionManager, DecisionType


class ConfirmationWorkflow:
    """
    Helper class for managing common confirmation workflows.
    
    Features:
    - Pre-built confirmation patterns
    - Risk assessment helpers
    - Approval chain management
    """
    
    def __init__(self, decision_manager: DecisionManager):
        """
        Initialize confirmation workflow.
        
        Args:
            decision_manager: DecisionManager instance
        """
        self.decision_manager = decision_manager
        self.logger = logging.getLogger(__name__)
    
    def confirm_deployment(
        self,
        environment: str,
        services: List[str],
        version: str,
        rollback_plan: str
    ) -> str:
        """
        Request confirmation for a deployment.
        
        Args:
            environment: Target environment (dev, staging, production)
            services: List of services to deploy
            version: Version/tag to deploy
            rollback_plan: Description of rollback procedure
            
        Returns:
            Decision ID
        """
        # Assess risk based on environment
        risk_map = {
            "dev": "low",
            "staging": "medium",
            "production": "critical"
        }
        risk_level = risk_map.get(environment.lower(), "high")
        
        title = f"Deploy {', '.join(services)} to {environment}"
        description = f"""
Deployment Request:
- Environment: {environment}
- Services: {', '.join(services)}
- Version: {version}
- Rollback Plan: {rollback_plan}

This deployment requires explicit approval before execution.
"""
        
        proposed_action = {
            "action_type": "deployment",
            "environment": environment,
            "services": services,
            "version": version,
            "rollback_plan": rollback_plan
        }
        
        # Production deployments expire faster to encourage timely decisions
        expiry_hours = 2 if environment.lower() == "production" else 24
        
        decision_id = self.decision_manager.request_decision(
            decision_type=DecisionType.DEPLOYMENT,
            title=title,
            description=description,
            proposed_action=proposed_action,
            risk_level=risk_level,
            expiry_hours=expiry_hours
        )
        
        self.logger.info(
            f"Deployment confirmation requested: {decision_id} "
            f"({environment}, {len(services)} services)"
        )
        
        return decision_id
    
    def confirm_branch_merge(
        self,
        source_branch: str,
        target_branch: str,
        changes_summary: str,
        reviewer: str
    ) -> str:
        """
        Request confirmation for a branch merge.
        
        Args:
            source_branch: Source branch name
            target_branch: Target branch name (e.g., 'main')
            changes_summary: Summary of changes
            reviewer: Code reviewer identifier
            
        Returns:
            Decision ID
        """
        # Main/master branch merges are critical
        protected_branches = ["main", "master", "production"]
        risk_level = "critical" if target_branch in protected_branches else "medium"
        
        title = f"Merge {source_branch} → {target_branch}"
        description = f"""
Branch Merge Request:
- Source: {source_branch}
- Target: {target_branch}
- Reviewer: {reviewer}

Changes Summary:
{changes_summary}

⚠️ This merge requires explicit approval.
"""
        
        proposed_action = {
            "action_type": "branch_merge",
            "source_branch": source_branch,
            "target_branch": target_branch,
            "reviewer": reviewer
        }
        
        decision_id = self.decision_manager.request_decision(
            decision_type=DecisionType.BRANCH_MERGE,
            title=title,
            description=description,
            proposed_action=proposed_action,
            risk_level=risk_level,
            expiry_hours=12
        )
        
        self.logger.info(
            f"Branch merge confirmation requested: {decision_id} "
            f"({source_branch} → {target_branch})"
        )
        
        return decision_id
    
    def confirm_budget_change(
        self,
        project_id: str,
        current_budget: float,
        new_budget: float,
        justification: str
    ) -> str:
        """
        Request confirmation for budget change.
        
        Args:
            project_id: Project identifier
            current_budget: Current budget limit
            new_budget: Proposed new budget limit
            justification: Reason for change
            
        Returns:
            Decision ID
        """
        change_percent = ((new_budget - current_budget) / current_budget) * 100
        
        # Large budget increases are higher risk
        if abs(change_percent) > 50:
            risk_level = "high"
        elif abs(change_percent) > 25:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        title = f"Budget change for {project_id}: ${current_budget} → ${new_budget}"
        description = f"""
Budget Change Request:
- Project: {project_id}
- Current Budget: ${current_budget:.2f}
- Proposed Budget: ${new_budget:.2f}
- Change: {change_percent:+.1f}%

Justification:
{justification}
"""
        
        proposed_action = {
            "action_type": "budget_change",
            "project_id": project_id,
            "current_budget": current_budget,
            "new_budget": new_budget
        }
        
        decision_id = self.decision_manager.request_decision(
            decision_type=DecisionType.BUDGET_CHANGE,
            title=title,
            description=description,
            proposed_action=proposed_action,
            risk_level=risk_level,
            expiry_hours=48
        )
        
        self.logger.info(
            f"Budget change confirmation requested: {decision_id} "
            f"({change_percent:+.1f}%)"
        )
        
        return decision_id
    
    def confirm_data_deletion(
        self,
        data_type: str,
        scope: str,
        estimated_records: int,
        backup_available: bool
    ) -> str:
        """
        Request confirmation for data deletion.
        
        Args:
            data_type: Type of data to delete
            scope: Scope of deletion (e.g., "all", "project_xyz")
            estimated_records: Estimated number of records
            backup_available: Whether backup exists
            
        Returns:
            Decision ID
        """
        # Data deletion without backup is critical
        risk_level = "medium" if backup_available else "critical"
        
        title = f"Delete {data_type} data: {scope}"
        description = f"""
Data Deletion Request:
- Data Type: {data_type}
- Scope: {scope}
- Estimated Records: {estimated_records:,}
- Backup Available: {'Yes' if backup_available else '⚠️ NO'}

⚠️ This action cannot be undone without a backup.
"""
        
        proposed_action = {
            "action_type": "data_deletion",
            "data_type": data_type,
            "scope": scope,
            "estimated_records": estimated_records
        }
        
        metadata = {
            "backup_available": backup_available
        }
        
        decision_id = self.decision_manager.request_decision(
            decision_type=DecisionType.DATA_DELETION,
            title=title,
            description=description,
            proposed_action=proposed_action,
            risk_level=risk_level,
            expiry_hours=6,
            metadata=metadata
        )
        
        self.logger.info(
            f"Data deletion confirmation requested: {decision_id} "
            f"({estimated_records:,} records)"
        )
        
        return decision_id
    
    def get_pending_confirmations(self, high_priority_only: bool = False) -> List[dict]:
        """
        Get pending confirmations.
        
        Args:
            high_priority_only: If True, only return high/critical risk decisions
            
        Returns:
            List of pending decisions
        """
        if high_priority_only:
            pending = []
            for risk in ["high", "critical"]:
                pending.extend(self.decision_manager.list_pending_decisions(risk_level=risk))
            return pending
        
        return self.decision_manager.list_pending_decisions()
