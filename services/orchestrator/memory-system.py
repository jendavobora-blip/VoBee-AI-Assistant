"""
Memory System - Learning and Context Management
Part of the VoBee AI Orchestration System

Stores task results, learns patterns, improves over time, and manages context.

⚠️ DOES NOT MODIFY EXISTING main.py - This is a NEW extension module
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemorySystem:
    """
    Memory system for storing task results, learning patterns,
    and improving orchestrator performance over time
    """
    
    def __init__(self):
        self.short_term_memory = []  # Recent tasks
        self.long_term_memory = {}   # Patterns and learnings
        self.context_store = {}      # Active contexts
        self.pattern_library = {}    # Learned patterns
        self.max_short_term = 100    # Keep last 100 tasks
        logger.info("Memory System initialized")
    
    def store_task_result(self, task_id: str, task_data: Dict[str, Any], result: Dict[str, Any]):
        """
        Store task result in memory
        
        Args:
            task_id: Unique task identifier
            task_data: Task input data
            result: Task execution result
        """
        memory_entry = {
            'task_id': task_id,
            'task_type': task_data.get('type'),
            'input': task_data,
            'result': result,
            'success': result.get('success', False),
            'execution_time': result.get('execution_time', 0),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Add to short-term memory
        self.short_term_memory.append(memory_entry)
        
        # Maintain max size
        if len(self.short_term_memory) > self.max_short_term:
            self.short_term_memory.pop(0)
        
        # Extract patterns for long-term memory
        self._extract_patterns(memory_entry)
        
        logger.info(f"Stored task result: {task_id}")
    
    def _extract_patterns(self, memory_entry: Dict[str, Any]):
        """Extract patterns from task execution for learning"""
        task_type = memory_entry.get('task_type')
        success = memory_entry.get('success')
        execution_time = memory_entry.get('execution_time')
        
        if task_type not in self.long_term_memory:
            self.long_term_memory[task_type] = {
                'total_executions': 0,
                'successful_executions': 0,
                'failed_executions': 0,
                'total_time': 0,
                'avg_execution_time': 0,
                'success_rate': 0,
                'common_patterns': [],
                'error_patterns': []
            }
        
        ltm = self.long_term_memory[task_type]
        ltm['total_executions'] += 1
        
        if success:
            ltm['successful_executions'] += 1
        else:
            ltm['failed_executions'] += 1
            # Store error pattern
            error = memory_entry.get('result', {}).get('error')
            if error:
                ltm['error_patterns'].append(error)
        
        ltm['total_time'] += execution_time
        ltm['avg_execution_time'] = ltm['total_time'] / ltm['total_executions']
        ltm['success_rate'] = ltm['successful_executions'] / ltm['total_executions']
        
        logger.debug(f"Updated long-term memory for {task_type}: success_rate={ltm['success_rate']:.2f}")
    
    def learn_pattern(self, pattern_name: str, pattern_data: Dict[str, Any]):
        """
        Learn a new pattern
        
        Args:
            pattern_name: Name of the pattern
            pattern_data: Pattern details
        """
        self.pattern_library[pattern_name] = {
            'data': pattern_data,
            'learned_at': datetime.utcnow().isoformat(),
            'usage_count': 0
        }
        logger.info(f"Learned new pattern: {pattern_name}")
    
    def get_pattern(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a learned pattern"""
        pattern = self.pattern_library.get(pattern_name)
        if pattern:
            pattern['usage_count'] += 1
            return pattern['data']
        return None
    
    def create_context(self, context_id: str, context_data: Dict[str, Any]):
        """
        Create a new context for task execution
        
        Args:
            context_id: Unique context identifier
            context_data: Context data
        """
        self.context_store[context_id] = {
            'data': context_data,
            'created_at': datetime.utcnow().isoformat(),
            'last_accessed': datetime.utcnow().isoformat(),
            'access_count': 0
        }
        logger.info(f"Created context: {context_id}")
    
    def get_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve context data"""
        context = self.context_store.get(context_id)
        if context:
            context['last_accessed'] = datetime.utcnow().isoformat()
            context['access_count'] += 1
            return context['data']
        return None
    
    def update_context(self, context_id: str, updates: Dict[str, Any]):
        """Update existing context"""
        if context_id in self.context_store:
            self.context_store[context_id]['data'].update(updates)
            self.context_store[context_id]['last_accessed'] = datetime.utcnow().isoformat()
            logger.info(f"Updated context: {context_id}")
    
    def get_relevant_memories(self, task_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get relevant memories for a task type
        
        Args:
            task_type: Type of task
            limit: Maximum number of memories to return
            
        Returns:
            List of relevant memory entries
        """
        relevant = [
            mem for mem in self.short_term_memory
            if mem.get('task_type') == task_type
        ]
        
        # Return most recent ones
        return relevant[-limit:] if relevant else []
    
    def get_success_patterns(self, task_type: str) -> Dict[str, Any]:
        """Get success patterns for a task type"""
        ltm = self.long_term_memory.get(task_type, {})
        
        if not ltm:
            return {
                'success_rate': 0,
                'recommendations': ['No historical data available'],
                'confidence': 'low'
            }
        
        success_rate = ltm.get('success_rate', 0)
        avg_time = ltm.get('avg_execution_time', 0)
        
        # Generate recommendations
        recommendations = []
        if success_rate < 0.7:
            recommendations.append('Success rate is low - consider alternative approaches')
        if avg_time > 60:
            recommendations.append('Execution time is high - consider optimization')
        if not recommendations:
            recommendations.append('Task type has good historical performance')
        
        confidence = 'high' if ltm['total_executions'] > 10 else 'medium' if ltm['total_executions'] > 3 else 'low'
        
        return {
            'success_rate': success_rate,
            'avg_execution_time': avg_time,
            'total_executions': ltm['total_executions'],
            'recommendations': recommendations,
            'confidence': confidence
        }
    
    def get_failure_insights(self, task_type: str) -> Dict[str, Any]:
        """Get insights about failures for a task type"""
        ltm = self.long_term_memory.get(task_type, {})
        
        if not ltm:
            return {'failures': 0, 'patterns': [], 'suggestions': []}
        
        failures = ltm.get('failed_executions', 0)
        error_patterns = ltm.get('error_patterns', [])
        
        # Analyze error patterns
        common_errors = {}
        for error in error_patterns[-20:]:  # Last 20 errors
            error_str = str(error)
            common_errors[error_str] = common_errors.get(error_str, 0) + 1
        
        top_errors = sorted(common_errors.items(), key=lambda x: x[1], reverse=True)[:3]
        
        suggestions = []
        if failures > 5:
            suggestions.append('High failure rate detected - review service configuration')
        if top_errors:
            suggestions.append(f'Most common error: {top_errors[0][0]}')
        
        return {
            'failures': failures,
            'failure_rate': ltm.get('failed_executions', 0) / max(ltm.get('total_executions', 1), 1),
            'common_errors': top_errors,
            'suggestions': suggestions
        }
    
    def improve_from_feedback(self, task_type: str, feedback: Dict[str, Any]):
        """
        Improve system based on feedback
        
        Args:
            task_type: Type of task
            feedback: Feedback data
        """
        if task_type not in self.long_term_memory:
            self.long_term_memory[task_type] = {
                'feedback': [],
                'improvements': []
            }
        
        ltm = self.long_term_memory[task_type]
        if 'feedback' not in ltm:
            ltm['feedback'] = []
        
        ltm['feedback'].append({
            'data': feedback,
            'received_at': datetime.utcnow().isoformat()
        })
        
        logger.info(f"Recorded feedback for {task_type}")
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of memory system state"""
        return {
            'short_term_count': len(self.short_term_memory),
            'long_term_types': len(self.long_term_memory),
            'patterns_learned': len(self.pattern_library),
            'active_contexts': len(self.context_store),
            'task_types': list(self.long_term_memory.keys()),
            'memory_utilization': {
                'short_term': f"{len(self.short_term_memory)}/{self.max_short_term}",
                'long_term': len(self.long_term_memory)
            }
        }


# Global instance
memory_system = MemorySystem()

if __name__ == '__main__':
    # Test the memory system
    print("Testing Memory System...")
    
    # Store a task result
    task_data = {'type': 'email_campaign', 'subject': 'Test'}
    result = {'success': True, 'execution_time': 5.2}
    
    memory_system.store_task_result('task_123', task_data, result)
    
    # Get success patterns
    patterns = memory_system.get_success_patterns('email_campaign')
    print(f"\nSuccess patterns: {json.dumps(patterns, indent=2)}")
    
    # Get memory summary
    summary = memory_system.get_memory_summary()
    print(f"\nMemory summary: {json.dumps(summary, indent=2)}")
