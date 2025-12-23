"""
Project Orchestrator Core Implementation

Main orchestrator class for coordinating project-level workflows
across multiple factories and services.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Enumeration of workflow status states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProjectOrchestrator:
    """
    Core Project Orchestrator for managing cross-factory workflows.
    
    This orchestrator coordinates activities across Application, Media,
    and Research Factories, supporting modular and parallel workstreams.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Project Orchestrator.
        
        Args:
            config: Optional configuration dictionary for orchestrator settings
        """
        self.config = config or {}
        self.factories = {}
        self.active_workflows = []
        self.workflow_history = []
        self.initialized = False
        
        logger.info("Initializing Project Orchestrator")
        self._setup_components()
    
    def _setup_components(self):
        """Initialize orchestration components."""
        from .workflow_manager import WorkflowManager
        from .factory_coordinator import FactoryCoordinator
        
        self.workflow_manager = WorkflowManager(self.config.get('workflow', {}))
        self.factory_coordinator = FactoryCoordinator(self.config.get('coordinator', {}))
        
        self.initialized = True
        logger.info("Project Orchestrator components initialized")
    
    def register_factory(self, factory_name: str, factory_instance: Any):
        """
        Register a factory with the orchestrator.
        
        Args:
            factory_name: Name of the factory (e.g., 'media', 'research', 'application')
            factory_instance: Instance of the factory
        """
        self.factories[factory_name] = factory_instance
        logger.info(f"Registered factory: {factory_name}")
    
    def create_workflow(
        self,
        workflow_name: str,
        workflow_config: Dict[str, Any]
    ) -> str:
        """
        Create a new cross-factory workflow.
        
        Args:
            workflow_name: Name of the workflow
            workflow_config: Configuration and steps for the workflow
        
        Returns:
            Workflow ID
        """
        workflow_id = self.workflow_manager.create_workflow(
            workflow_name,
            workflow_config
        )
        
        workflow = {
            'id': workflow_id,
            'name': workflow_name,
            'config': workflow_config,
            'status': WorkflowStatus.PENDING,
            'created_at': datetime.utcnow().isoformat(),
            'factories_involved': workflow_config.get('factories', [])
        }
        
        self.active_workflows.append(workflow)
        logger.info(f"Created workflow: {workflow_name} (ID: {workflow_id})")
        
        return workflow_id
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Execute a workflow across multiple factories.
        
        Args:
            workflow_id: ID of the workflow to execute
        
        Returns:
            Dictionary containing execution results
        """
        logger.info(f"Executing workflow: {workflow_id}")
        
        # Find the workflow
        workflow = next(
            (w for w in self.active_workflows if w['id'] == workflow_id),
            None
        )
        
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")
        
        # Update status
        workflow['status'] = WorkflowStatus.RUNNING
        workflow['started_at'] = datetime.utcnow().isoformat()
        
        # Coordinate execution across factories
        result = self.factory_coordinator.coordinate(
            workflow_id,
            workflow['config'],
            self.factories
        )
        
        # Update workflow status
        workflow['status'] = WorkflowStatus.COMPLETED if result.get('success') else WorkflowStatus.FAILED
        workflow['completed_at'] = datetime.utcnow().isoformat()
        workflow['result'] = result
        
        # Move to history
        self.workflow_history.append(workflow)
        self.active_workflows = [w for w in self.active_workflows if w['id'] != workflow_id]
        
        logger.info(f"Workflow {workflow_id} completed with status: {workflow['status'].value}")
        
        return {
            'workflow_id': workflow_id,
            'status': workflow['status'].value,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get the status of a workflow.
        
        Args:
            workflow_id: ID of the workflow
        
        Returns:
            Dictionary containing workflow status
        """
        # Check active workflows
        workflow = next(
            (w for w in self.active_workflows if w['id'] == workflow_id),
            None
        )
        
        # Check history if not active
        if not workflow:
            workflow = next(
                (w for w in self.workflow_history if w['id'] == workflow_id),
                None
            )
        
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")
        
        return {
            'workflow_id': workflow_id,
            'name': workflow['name'],
            'status': workflow['status'].value if isinstance(workflow['status'], WorkflowStatus) else workflow['status'],
            'created_at': workflow['created_at'],
            'factories_involved': workflow.get('factories_involved', [])
        }
    
    def get_active_workflows(self) -> List[Dict[str, Any]]:
        """
        Get list of active workflows.
        
        Returns:
            List of active workflow details
        """
        return [
            {
                'id': w['id'],
                'name': w['name'],
                'status': w['status'].value if isinstance(w['status'], WorkflowStatus) else w['status'],
                'factories_involved': w.get('factories_involved', [])
            }
            for w in self.active_workflows
        ]
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Project Orchestrator.
        
        Returns:
            Dictionary containing orchestrator status information
        """
        return {
            'initialized': self.initialized,
            'registered_factories': list(self.factories.keys()),
            'active_workflows': len(self.active_workflows),
            'completed_workflows': len(self.workflow_history),
            'timestamp': datetime.utcnow().isoformat()
        }
