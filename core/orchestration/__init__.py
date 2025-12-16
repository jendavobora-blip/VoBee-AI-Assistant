"""
Core Orchestration Module
Provides workflow coordination and factory integration for the VoBee AI system.
Manages task routing, factory connectivity, and multi-factory workflows.
"""

from typing import Dict, Any, Optional
from .workflow import WorkflowCoordinator, WorkflowTemplate, WorkflowStep
from .factory_connector import FactoryConnector, FactoryType
from .router import TaskRouter, RoutingStrategy

__all__ = [
    "WorkflowCoordinator",
    "WorkflowTemplate",
    "WorkflowStep",
    "FactoryConnector",
    "FactoryType",
    "TaskRouter",
    "RoutingStrategy",
    "OrchestrationEngine",
]


class OrchestrationEngine:
    """
    Main orchestration engine coordinating all factories and workflows.
    Provides a unified interface for complex multi-factory operations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the orchestration engine.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.workflow_coordinator = WorkflowCoordinator(self.config.get("workflow", {}))
        self.factory_connector = FactoryConnector(self.config.get("factories", {}))
        self.task_router = TaskRouter(self.config.get("routing", {}))
        
    def execute_workflow(self, workflow_template: WorkflowTemplate) -> Dict[str, Any]:
        """
        Execute a multi-factory workflow.
        
        Args:
            workflow_template: Template defining the workflow
            
        Returns:
            Dictionary containing workflow execution results
        """
        return self.workflow_coordinator.execute(workflow_template)
    
    def route_task(self, task: Dict[str, Any]) -> str:
        """
        Route a task to the appropriate factory.
        
        Args:
            task: Task definition
            
        Returns:
            Factory identifier for the task
        """
        return self.task_router.route(task)
    
    def get_factory_status(self) -> Dict[str, Any]:
        """
        Get status of all connected factories.
        
        Returns:
            Dictionary with factory status information
        """
        return self.factory_connector.get_all_status()
