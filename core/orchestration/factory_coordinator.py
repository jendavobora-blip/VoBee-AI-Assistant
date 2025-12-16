"""
Factory Coordinator Module

Coordinates communication and workflow execution across multiple factories.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class FactoryCoordinator:
    """
    Coordinator for inter-factory communication and parallel execution.
    
    Manages workflow execution across Application, Media, and Research
    Factories with support for parallel and sequential execution patterns.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Factory Coordinator.
        
        Args:
            config: Optional configuration for factory coordination
        """
        self.config = config or {}
        self.max_workers = self.config.get('max_workers', 4)
        self.execution_history = []
        
        logger.info("Factory Coordinator initialized")
    
    def coordinate(
        self,
        workflow_id: str,
        workflow_config: Dict[str, Any],
        factories: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Coordinate workflow execution across factories.
        
        Args:
            workflow_id: ID of the workflow being executed
            workflow_config: Workflow configuration and steps
            factories: Dictionary of available factory instances
        
        Returns:
            Dictionary containing coordination results
        """
        logger.info(f"Coordinating workflow {workflow_id} across factories")
        
        steps = workflow_config.get('steps', [])
        parallel = workflow_config.get('parallel', False)
        
        if parallel:
            result = self._execute_parallel(workflow_id, steps, factories)
        else:
            result = self._execute_sequential(workflow_id, steps, factories)
        
        # Store execution history
        self.execution_history.append({
            'workflow_id': workflow_id,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return result
    
    def _execute_sequential(
        self,
        workflow_id: str,
        steps: List[Dict[str, Any]],
        factories: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute workflow steps sequentially.
        
        Args:
            workflow_id: Workflow ID
            steps: List of workflow steps
            factories: Available factories
        
        Returns:
            Execution results
        """
        logger.info(f"Executing {len(steps)} steps sequentially")
        
        results = []
        context = {}
        
        for step_idx, step in enumerate(steps):
            factory_name = step.get('factory')
            action = step.get('action')
            params = step.get('params', {})
            
            # Merge context from previous steps
            params = {**params, 'context': context}
            
            result = self._execute_step(
                workflow_id,
                step_idx,
                factory_name,
                action,
                params,
                factories
            )
            
            results.append(result)
            
            # Update context for next step
            if result.get('success'):
                context[f'step_{step_idx}'] = result.get('data')
            else:
                # Stop on failure
                return {
                    'success': False,
                    'message': f'Step {step_idx} failed',
                    'results': results
                }
        
        return {
            'success': True,
            'message': 'All steps completed successfully',
            'results': results
        }
    
    def _execute_parallel(
        self,
        workflow_id: str,
        steps: List[Dict[str, Any]],
        factories: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute workflow steps in parallel.
        
        Args:
            workflow_id: Workflow ID
            steps: List of workflow steps
            factories: Available factories
        
        Returns:
            Execution results
        """
        logger.info(f"Executing {len(steps)} steps in parallel")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_step = {
                executor.submit(
                    self._execute_step,
                    workflow_id,
                    step_idx,
                    step.get('factory'),
                    step.get('action'),
                    step.get('params', {}),
                    factories
                ): step_idx
                for step_idx, step in enumerate(steps)
            }
            
            for future in as_completed(future_to_step):
                step_idx = future_to_step[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    logger.error(f"Step {step_idx} generated an exception: {exc}")
                    results.append({
                        'success': False,
                        'step': step_idx,
                        'error': str(exc)
                    })
        
        # Check if all succeeded
        all_success = all(r.get('success', False) for r in results)
        
        return {
            'success': all_success,
            'message': 'All steps completed' if all_success else 'Some steps failed',
            'results': results
        }
    
    def _execute_step(
        self,
        workflow_id: str,
        step_idx: int,
        factory_name: str,
        action: str,
        params: Dict[str, Any],
        factories: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single workflow step.
        
        Args:
            workflow_id: Workflow ID
            step_idx: Step index
            factory_name: Name of the factory to use
            action: Action to perform
            params: Action parameters
            factories: Available factories
        
        Returns:
            Step execution result
        """
        logger.info(f"Executing step {step_idx} on factory {factory_name}: {action}")
        
        # Placeholder for actual factory method invocation
        # This will be extended to call actual factory methods
        
        if factory_name not in factories:
            return {
                'success': False,
                'step': step_idx,
                'error': f'Factory not found: {factory_name}'
            }
        
        # Simulate factory call
        result = {
            'success': True,
            'step': step_idx,
            'factory': factory_name,
            'action': action,
            'data': {
                'message': f'Step {step_idx} executed on {factory_name}',
                'params': params
            }
        }
        
        return result
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent execution history.
        
        Args:
            limit: Maximum number of historical records to return
        
        Returns:
            List of execution history records
        """
        return self.execution_history[-limit:]
