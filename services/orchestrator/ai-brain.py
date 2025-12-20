"""
AI Brain - Central Decision-Making System
Part of the VoBee AI Orchestration System

This module extends the orchestrator with advanced decision-making,
task prioritization, resource allocation, and learning capabilities.

⚠️ DOES NOT MODIFY EXISTING main.py - This is a NEW extension module
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIBrain:
    """
    Central AI decision-making system for the orchestrator.
    Handles intelligent task prioritization, resource allocation,
    and learning from past results.
    """
    
    def __init__(self):
        self.decision_history = []
        self.performance_metrics = {}
        self.learning_data = {}
        logger.info("AI Brain initialized")
    
    def make_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make intelligent decision based on context
        
        Args:
            context: Current system state and task requirements
            
        Returns:
            Decision with reasoning and confidence score
        """
        task_type = context.get('task_type')
        available_resources = context.get('resources', {})
        priority = context.get('priority', 'normal')
        
        # Analyze past performance for this task type
        past_performance = self.learning_data.get(task_type, {})
        
        decision = {
            'task_type': task_type,
            'selected_service': self._select_best_service(task_type, past_performance),
            'resource_allocation': self._allocate_resources(task_type, available_resources),
            'priority_level': self._calculate_priority(priority, task_type),
            'confidence': self._calculate_confidence(task_type, past_performance),
            'reasoning': self._generate_reasoning(task_type, priority),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Store decision for learning
        self.decision_history.append(decision)
        
        logger.info(f"Decision made: {task_type} -> {decision['selected_service']} (confidence: {decision['confidence']:.2f})")
        
        return decision
    
    def _select_best_service(self, task_type: str, past_performance: Dict[str, Any]) -> str:
        """Select the best service based on task type and past performance"""
        # Service mapping based on task type
        service_mapping = {
            'email_campaign': 'email-ai',
            'social_media': 'facebook-ai',
            'seo': 'seo-ai',
            'content': 'content-ai',
            'analytics': 'analytics-ai',
            'finance': 'finance-ai',
            'invoice': 'invoice-ai',
            'research': 'research-ai',
            'translation': 'translation-ai',
            'code_review': 'code-review-ai',
        }
        
        return service_mapping.get(task_type, 'orchestrator')
    
    def _allocate_resources(self, task_type: str, available_resources: Dict[str, Any]) -> Dict[str, Any]:
        """Intelligently allocate resources based on task requirements"""
        # Resource requirements by task type
        requirements = {
            'email_campaign': {'cpu': 1, 'memory': 512, 'priority': 'normal'},
            'analytics': {'cpu': 2, 'memory': 2048, 'priority': 'high'},
            'content': {'cpu': 1, 'memory': 1024, 'priority': 'normal'},
            'code_review': {'cpu': 2, 'memory': 1024, 'priority': 'high'},
        }
        
        return requirements.get(task_type, {'cpu': 1, 'memory': 512, 'priority': 'normal'})
    
    def _calculate_priority(self, base_priority: str, task_type: str) -> int:
        """Calculate numerical priority score"""
        priority_map = {'low': 1, 'normal': 2, 'high': 3, 'critical': 4}
        base_score = priority_map.get(base_priority, 2)
        
        # Adjust based on task type
        if task_type in ['finance', 'code_review']:
            base_score += 1
        
        return min(base_score, 4)
    
    def _calculate_confidence(self, task_type: str, past_performance: Dict[str, Any]) -> float:
        """Calculate confidence score for decision"""
        if not past_performance:
            return 0.7  # Default confidence for new task types
        
        success_rate = past_performance.get('success_rate', 0.7)
        sample_size = past_performance.get('sample_size', 1)
        
        # Increase confidence with more samples
        confidence = success_rate * (1 - (1 / (sample_size + 1)))
        
        return min(confidence, 0.99)
    
    def _generate_reasoning(self, task_type: str, priority: str) -> str:
        """Generate human-readable reasoning for decision"""
        return f"Selected based on task type '{task_type}' with priority '{priority}' and historical performance data"
    
    def prioritize_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Intelligently prioritize a list of tasks
        
        Args:
            tasks: List of tasks to prioritize
            
        Returns:
            Prioritized task list with scores
        """
        scored_tasks = []
        
        for task in tasks:
            score = self._calculate_task_score(task)
            task['priority_score'] = score
            scored_tasks.append(task)
        
        # Sort by priority score (highest first)
        sorted_tasks = sorted(scored_tasks, key=lambda x: x['priority_score'], reverse=True)
        
        logger.info(f"Prioritized {len(sorted_tasks)} tasks")
        
        return sorted_tasks
    
    def _calculate_task_score(self, task: Dict[str, Any]) -> float:
        """Calculate priority score for a single task"""
        base_priority = task.get('priority', 'normal')
        task_type = task.get('type')
        deadline = task.get('deadline')
        
        # Base score from priority
        priority_scores = {'low': 1.0, 'normal': 2.0, 'high': 3.0, 'critical': 4.0}
        score = priority_scores.get(base_priority, 2.0)
        
        # Adjust for task type importance
        important_types = ['finance', 'security', 'fraud_detection']
        if task_type in important_types:
            score *= 1.5
        
        # Adjust for deadline urgency
        if deadline:
            # Placeholder for deadline calculation
            score *= 1.2
        
        return score
    
    def learn_from_result(self, task_result: Dict[str, Any]):
        """
        Learn from task execution results to improve future decisions
        
        Args:
            task_result: Result of task execution including success/failure
        """
        task_type = task_result.get('task_type')
        success = task_result.get('success', False)
        execution_time = task_result.get('execution_time', 0)
        
        if task_type not in self.learning_data:
            self.learning_data[task_type] = {
                'total_executions': 0,
                'successful_executions': 0,
                'total_time': 0,
                'success_rate': 0.0,
                'avg_execution_time': 0.0
            }
        
        data = self.learning_data[task_type]
        data['total_executions'] += 1
        if success:
            data['successful_executions'] += 1
        data['total_time'] += execution_time
        
        # Update metrics
        data['success_rate'] = data['successful_executions'] / data['total_executions']
        data['avg_execution_time'] = data['total_time'] / data['total_executions']
        data['sample_size'] = data['total_executions']
        
        logger.info(f"Learned from {task_type}: success_rate={data['success_rate']:.2f}, avg_time={data['avg_execution_time']:.2f}s")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of AI brain performance and learning"""
        return {
            'total_decisions': len(self.decision_history),
            'task_types_learned': len(self.learning_data),
            'learning_data': self.learning_data,
            'recent_decisions': self.decision_history[-10:] if self.decision_history else []
        }

# Global instance
ai_brain = AIBrain()

if __name__ == '__main__':
    # Test the AI Brain
    print("Testing AI Brain...")
    
    # Test decision making
    context = {
        'task_type': 'email_campaign',
        'priority': 'high',
        'resources': {'cpu': 4, 'memory': 8192}
    }
    
    decision = ai_brain.make_decision(context)
    print(f"\nDecision: {json.dumps(decision, indent=2)}")
    
    # Test task prioritization
    tasks = [
        {'type': 'email_campaign', 'priority': 'normal'},
        {'type': 'finance', 'priority': 'high'},
        {'type': 'content', 'priority': 'low'}
    ]
    
    prioritized = ai_brain.prioritize_tasks(tasks)
    print(f"\nPrioritized tasks: {json.dumps(prioritized, indent=2)}")
    
    # Test learning
    result = {
        'task_type': 'email_campaign',
        'success': True,
        'execution_time': 5.2
    }
    
    ai_brain.learn_from_result(result)
    print(f"\nPerformance summary: {json.dumps(ai_brain.get_performance_summary(), indent=2)}")
