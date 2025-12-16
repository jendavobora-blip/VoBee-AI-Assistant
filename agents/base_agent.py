"""
Base Agent - Foundation for all logical agent roles.

Provides common functionality and enforces guardrails.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from pathlib import Path


class AgentGuardrails:
    """
    Guardrails to prevent autonomous actions.
    
    All agents must operate within these constraints:
    - No direct code commits
    - No automatic deployments
    - No main branch modifications
    - Output artifacts only
    - Human approval required for critical actions
    """
    
    ALLOWED_ACTIONS = [
        "analyze",
        "research",
        "generate_artifact",
        "recommend",
        "review",
        "validate"
    ]
    
    FORBIDDEN_ACTIONS = [
        "commit",
        "push",
        "merge_to_main",
        "deploy",
        "delete_data",
        "modify_production"
    ]
    
    @staticmethod
    def validate_action(action: str) -> bool:
        """
        Validate if an action is allowed.
        
        Args:
            action: Action to validate
            
        Returns:
            True if allowed, False otherwise
        """
        if action in AgentGuardrails.FORBIDDEN_ACTIONS:
            return False
        
        return action in AgentGuardrails.ALLOWED_ACTIONS
    
    @staticmethod
    def requires_approval(action: str) -> bool:
        """
        Check if an action requires human approval.
        
        All agent actions require human approval as agents only produce
        artifacts and recommendations - never autonomous execution.
        
        Args:
            action: Action to check
            
        Returns:
            True (all actions require approval)
        """
        # All agent outputs are suggestions/artifacts only
        # No actions are auto-approved - human review always required
        return True


class BaseAgent(ABC):
    """
    Base class for all AI agents.
    
    Provides:
    - Common logging infrastructure
    - Artifact generation
    - Guardrail enforcement
    - Audit trail
    """
    
    # Must be overridden by subclasses
    ROLE_ID: str = "base"
    ROLE_NAME: str = "Base Agent"
    ROLE_DESCRIPTION: str = "Base agent class"
    CAPABILITIES: List[str] = []
    
    def __init__(self, output_dir: str = "data/agents/artifacts"):
        """
        Initialize the agent.
        
        Args:
            output_dir: Directory for agent artifacts
        """
        self.output_dir = Path(output_dir) / self.ROLE_ID
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.guardrails = AgentGuardrails()
        
        # Setup logging
        self.logger = logging.getLogger(f"agent.{self.ROLE_ID}")
        self.logger.setLevel(logging.INFO)
        
        # Track agent activity
        self.activity_log: List[Dict] = []
        
        self.logger.info(f"Agent initialized: {self.ROLE_NAME} ({self.ROLE_ID})")
    
    @abstractmethod
    def execute_task(self, task: Dict) -> Dict:
        """
        Execute a task assigned to this agent.
        
        Args:
            task: Task definition
            
        Returns:
            Task result with artifacts
        """
        pass
    
    def generate_artifact(
        self,
        artifact_type: str,
        content: Any,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Generate an output artifact.
        
        Args:
            artifact_type: Type of artifact (e.g., 'report', 'code', 'diagram')
            content: Artifact content
            metadata: Optional metadata
            
        Returns:
            Path to generated artifact
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{artifact_type}_{timestamp}"
        
        # Determine file extension based on type
        if artifact_type in ["code", "script"]:
            extension = ".py"
        elif artifact_type in ["report", "analysis"]:
            extension = ".md"
        elif artifact_type in ["data", "config"]:
            extension = ".json"
        else:
            extension = ".txt"
        
        filepath = self.output_dir / f"{filename}{extension}"
        
        # Create artifact wrapper
        artifact = {
            "type": artifact_type,
            "agent": self.ROLE_ID,
            "created_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "content": content
        }
        
        # Save artifact
        if extension == ".json":
            with open(filepath, 'w') as f:
                json.dump(artifact, f, indent=2)
        else:
            with open(filepath, 'w') as f:
                f.write(f"# Artifact: {artifact_type}\n")
                f.write(f"# Agent: {self.ROLE_NAME}\n")
                f.write(f"# Created: {artifact['created_at']}\n")
                f.write(f"\n{content}\n")
        
        self.logger.info(f"Generated artifact: {filepath}")
        
        # Log activity
        self._log_activity("generate_artifact", {
            "artifact_type": artifact_type,
            "filepath": str(filepath)
        })
        
        return str(filepath)
    
    def validate_action(self, action: str) -> bool:
        """
        Validate if an action can be performed.
        
        Args:
            action: Action to validate
            
        Returns:
            True if allowed, raises exception otherwise
        """
        if not self.guardrails.validate_action(action):
            raise PermissionError(
                f"Agent '{self.ROLE_ID}' is not allowed to perform action: {action}. "
                f"Forbidden actions: {', '.join(AgentGuardrails.FORBIDDEN_ACTIONS)}"
            )
        
        return True
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return self.CAPABILITIES
    
    def get_info(self) -> Dict:
        """Get agent information."""
        return {
            "role_id": self.ROLE_ID,
            "role_name": self.ROLE_NAME,
            "description": self.ROLE_DESCRIPTION,
            "capabilities": self.CAPABILITIES,
            "activity_count": len(self.activity_log)
        }
    
    def _log_activity(self, action: str, details: Dict):
        """Log agent activity for audit trail."""
        activity = {
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.activity_log.append(activity)
        
        # Persist activity log
        log_file = self.output_dir / "activity_log.json"
        with open(log_file, 'w') as f:
            json.dump(self.activity_log, f, indent=2)
