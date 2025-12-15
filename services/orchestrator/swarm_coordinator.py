"""
AI Swarm Coordinator
Handles millions of micro-tasks through intelligent bot orchestration
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque
import threading
from enum import Enum

logger = logging.getLogger(__name__)

class SwarmBotStatus(Enum):
    """Status of individual swarm bots"""
    IDLE = "idle"
    WORKING = "working"
    FAILED = "failed"
    MAINTENANCE = "maintenance"

class MicroTaskPriority(Enum):
    """Priority levels for micro-tasks"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

class SwarmBot:
    """Individual bot in the swarm"""
    
    def __init__(self, bot_id: str, capabilities: List[str]):
        self.bot_id = bot_id
        self.capabilities = capabilities
        self.status = SwarmBotStatus.IDLE
        self.current_task = None
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_execution_time = 0
        self.created_at = datetime.utcnow()
    
    def can_handle(self, task_type: str) -> bool:
        """Check if bot can handle a specific task type"""
        return task_type in self.capabilities or 'general' in self.capabilities
    
    def assign_task(self, task: Dict[str, Any]) -> bool:
        """Assign a task to this bot"""
        if self.status != SwarmBotStatus.IDLE:
            return False
        
        self.current_task = task
        self.status = SwarmBotStatus.WORKING
        return True
    
    def complete_task(self, success: bool, execution_time: float):
        """Mark task as completed"""
        if success:
            self.tasks_completed += 1
        else:
            self.tasks_failed += 1
        
        self.total_execution_time += execution_time
        self.current_task = None
        self.status = SwarmBotStatus.IDLE
    
    def get_performance_score(self) -> float:
        """Calculate bot performance score"""
        total_tasks = self.tasks_completed + self.tasks_failed
        if total_tasks == 0:
            return 1.0
        
        success_rate = self.tasks_completed / total_tasks
        avg_time = self.total_execution_time / total_tasks if total_tasks > 0 else 0
        
        # Lower time is better, higher success rate is better
        return (success_rate * 0.7) + (0.3 if avg_time < 10 else 0.15)


class SwarmCoordinator:
    """
    AI Swarm Coordinator for mega-scale micro-task orchestration
    Manages millions of micro-tasks across distributed bot network
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.bots: Dict[str, SwarmBot] = {}
        self.task_queues: Dict[int, deque] = {
            MicroTaskPriority.CRITICAL.value: deque(),
            MicroTaskPriority.HIGH.value: deque(),
            MicroTaskPriority.NORMAL.value: deque(),
            MicroTaskPriority.LOW.value: deque()
        }
        self.completed_tasks = []
        self.failed_tasks = []
        self.metrics = {
            'total_tasks_processed': 0,
            'active_bots': 0,
            'idle_bots': 0,
            'queue_length': 0,
            'throughput': 0.0  # tasks per second
        }
        self.lock = threading.Lock()
        
        # Initialize swarm
        self._initialize_swarm()
        
        logger.info("AI Swarm Coordinator initialized")
    
    def _initialize_swarm(self, bot_count: int = 100):
        """Initialize the bot swarm"""
        logger.info(f"Initializing swarm with {bot_count} bots")
        
        # Create bots with different capabilities
        capability_sets = [
            ['general', 'data_processing'],
            ['general', 'image_processing'],
            ['general', 'text_processing'],
            ['general', 'api_calls'],
            ['general', 'validation'],
            ['specialized', 'ml_inference'],
            ['specialized', 'data_transformation']
        ]
        
        # Get current bot count to avoid ID collisions
        current_count = len(self.bots)
        
        for i in range(bot_count):
            bot_id = f"bot_{current_count + i:06d}"
            capabilities = capability_sets[i % len(capability_sets)]
            self.bots[bot_id] = SwarmBot(bot_id, capabilities)
        
        self.metrics['idle_bots'] += bot_count
        logger.info(f"Swarm initialized with {bot_count} new bots (total: {len(self.bots)})")
    
    def scale_swarm(self, target_size: int):
        """
        Scale the swarm to target size
        
        Args:
            target_size: Desired number of bots
        """
        current_size = len(self.bots)
        
        if target_size > current_size:
            # Add more bots
            bots_to_add = target_size - current_size
            logger.info(f"Scaling up swarm by {bots_to_add} bots")
            self._initialize_swarm(bots_to_add)
        elif target_size < current_size:
            # Remove idle bots
            logger.info(f"Scaling down swarm to {target_size} bots")
            idle_bots = [bot_id for bot_id, bot in self.bots.items() 
                        if bot.status == SwarmBotStatus.IDLE]
            
            to_remove = current_size - target_size
            for bot_id in idle_bots[:to_remove]:
                del self.bots[bot_id]
        
        self._update_metrics()
    
    def dispatch_micro_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Dispatch micro-tasks to the swarm
        
        Args:
            tasks: List of micro-tasks to execute
            
        Returns:
            Dispatch results and task IDs
        """
        logger.info(f"Dispatching {len(tasks)} micro-tasks to swarm")
        
        dispatch_result = {
            'dispatch_id': self._generate_dispatch_id(),
            'total_tasks': len(tasks),
            'queued_tasks': 0,
            'immediate_assignments': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        with self.lock:
            for task in tasks:
                # Enrich task with metadata
                task['task_id'] = self._generate_task_id()
                task['queued_at'] = datetime.utcnow().isoformat()
                task['attempts'] = 0
                
                # Determine priority
                priority = task.get('priority', 'normal')
                priority_value = self._get_priority_value(priority)
                
                # Try immediate assignment to idle bot
                assigned = self._try_immediate_assignment(task)
                
                if assigned:
                    dispatch_result['immediate_assignments'] += 1
                else:
                    # Queue task
                    self.task_queues[priority_value].append(task)
                    dispatch_result['queued_tasks'] += 1
        
        # Start processing queue
        self._process_queue()
        
        self._update_metrics()
        
        return dispatch_result
    
    def _try_immediate_assignment(self, task: Dict[str, Any]) -> bool:
        """Try to immediately assign task to an idle bot"""
        task_type = task.get('type', 'general')
        
        for bot_id, bot in self.bots.items():
            if bot.status == SwarmBotStatus.IDLE and bot.can_handle(task_type):
                if bot.assign_task(task):
                    # Execute task in background
                    self._execute_task_async(bot_id, task)
                    return True
        
        return False
    
    def _process_queue(self):
        """Process queued tasks"""
        # Process queues in priority order
        for priority in sorted(self.task_queues.keys()):
            queue = self.task_queues[priority]
            
            while queue:
                task = queue[0]  # Peek at first task
                
                # Find suitable idle bot
                bot_id = self._find_suitable_bot(task)
                
                if bot_id:
                    # Remove from queue and assign
                    task = queue.popleft()
                    bot = self.bots[bot_id]
                    bot.assign_task(task)
                    self._execute_task_async(bot_id, task)
                else:
                    # No available bot, stop processing this queue
                    break
    
    def _find_suitable_bot(self, task: Dict[str, Any]) -> Optional[str]:
        """Find the best bot for a task"""
        task_type = task.get('type', 'general')
        suitable_bots = []
        
        for bot_id, bot in self.bots.items():
            if bot.status == SwarmBotStatus.IDLE and bot.can_handle(task_type):
                suitable_bots.append((bot_id, bot.get_performance_score()))
        
        if not suitable_bots:
            return None
        
        # Return bot with highest performance score
        suitable_bots.sort(key=lambda x: x[1], reverse=True)
        return suitable_bots[0][0]
    
    def _execute_task_async(self, bot_id: str, task: Dict[str, Any]):
        """Execute task asynchronously"""
        # In a real implementation, this would use threading or async/await
        # For now, we'll simulate execution
        
        def execute():
            start_time = datetime.utcnow()
            try:
                result = self._execute_micro_task(task)
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                
                # Mark task as completed
                bot = self.bots[bot_id]
                bot.complete_task(success=True, execution_time=execution_time)
                
                task['result'] = result
                task['status'] = 'completed'
                task['completed_at'] = datetime.utcnow().isoformat()
                
                with self.lock:
                    self.completed_tasks.append(task)
                    self.metrics['total_tasks_processed'] += 1
                
            except Exception as e:
                logger.error(f"Task execution failed: {e}")
                
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                bot = self.bots[bot_id]
                bot.complete_task(success=False, execution_time=execution_time)
                
                task['error'] = str(e)
                task['status'] = 'failed'
                
                with self.lock:
                    self.failed_tasks.append(task)
            
            # Process next queued task
            self._process_queue()
        
        # Execute in separate thread (simplified for demo)
        thread = threading.Thread(target=execute)
        thread.daemon = True
        thread.start()
    
    def _execute_micro_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single micro-task"""
        task_type = task.get('type')
        task_data = task.get('data', {})
        
        # Simulate task execution based on type
        if task_type == 'data_processing':
            return {'processed': True, 'records': task_data.get('record_count', 0)}
        elif task_type == 'image_processing':
            return {'processed_image': 'image_url', 'filters_applied': task_data.get('filters', [])}
        elif task_type == 'text_processing':
            return {'processed_text': 'result', 'word_count': 100}
        elif task_type == 'api_calls':
            return {'api_response': 'success', 'data': {}}
        elif task_type == 'validation':
            return {'valid': True, 'errors': []}
        elif task_type == 'ml_inference':
            return {'predictions': [], 'confidence': 0.95}
        else:
            return {'status': 'completed', 'type': task_type}
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Get current swarm status"""
        self._update_metrics()
        
        bot_status_counts = {
            'idle': 0,
            'working': 0,
            'failed': 0,
            'maintenance': 0
        }
        
        for bot in self.bots.values():
            bot_status_counts[bot.status.value] += 1
        
        queue_lengths = {
            f'priority_{p}': len(q) for p, q in self.task_queues.items()
        }
        
        return {
            'total_bots': len(self.bots),
            'bot_status': bot_status_counts,
            'queue_lengths': queue_lengths,
            'total_queue_length': sum(len(q) for q in self.task_queues.values()),
            'completed_tasks': len(self.completed_tasks),
            'failed_tasks': len(self.failed_tasks),
            'metrics': self.metrics,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics"""
        total_bots = len(self.bots)
        active_bots = sum(1 for bot in self.bots.values() if bot.status == SwarmBotStatus.WORKING)
        
        bot_performances = [bot.get_performance_score() for bot in self.bots.values()]
        avg_performance = sum(bot_performances) / len(bot_performances) if bot_performances else 0
        
        total_completed = sum(bot.tasks_completed for bot in self.bots.values())
        total_failed = sum(bot.tasks_failed for bot in self.bots.values())
        
        return {
            'total_bots': total_bots,
            'active_bots': active_bots,
            'idle_bots': total_bots - active_bots,
            'avg_bot_performance': avg_performance,
            'total_tasks_completed': total_completed,
            'total_tasks_failed': total_failed,
            'success_rate': total_completed / (total_completed + total_failed) if (total_completed + total_failed) > 0 else 0,
            'queue_status': {
                f'priority_{p}': len(q) for p, q in self.task_queues.items()
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _update_metrics(self):
        """Update swarm metrics"""
        with self.lock:
            self.metrics['active_bots'] = sum(
                1 for bot in self.bots.values() if bot.status == SwarmBotStatus.WORKING
            )
            self.metrics['idle_bots'] = sum(
                1 for bot in self.bots.values() if bot.status == SwarmBotStatus.IDLE
            )
            self.metrics['queue_length'] = sum(len(q) for q in self.task_queues.values())
    
    def _generate_dispatch_id(self) -> str:
        """Generate unique dispatch ID"""
        from uuid import uuid4
        return f"dispatch_{str(uuid4())[:8]}"
    
    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        from uuid import uuid4
        return f"task_{str(uuid4())[:12]}"
    
    def _get_priority_value(self, priority: str) -> int:
        """Convert priority string to value"""
        priority_map = {
            'critical': MicroTaskPriority.CRITICAL.value,
            'high': MicroTaskPriority.HIGH.value,
            'normal': MicroTaskPriority.NORMAL.value,
            'low': MicroTaskPriority.LOW.value
        }
        return priority_map.get(priority.lower(), MicroTaskPriority.NORMAL.value)
    
    def optimize_swarm(self) -> Dict[str, Any]:
        """
        Optimize swarm configuration based on current load
        
        Returns:
            Optimization results and recommendations
        """
        logger.info("Optimizing swarm configuration")
        
        metrics = self.get_performance_metrics()
        queue_length = sum(len(q) for q in self.task_queues.values())
        active_bots = metrics['active_bots']
        idle_bots = metrics['idle_bots']
        
        recommendations = []
        
        # Check if we need to scale up
        if queue_length > len(self.bots) * 2:
            recommended_bots = len(self.bots) + (queue_length // 10)
            recommendations.append({
                'action': 'scale_up',
                'current_bots': len(self.bots),
                'recommended_bots': recommended_bots,
                'reason': 'High queue length detected'
            })
        
        # Check if we can scale down
        elif idle_bots > len(self.bots) * 0.7 and queue_length < 10:
            recommended_bots = max(active_bots + 20, 50)  # Keep minimum of 50 bots
            recommendations.append({
                'action': 'scale_down',
                'current_bots': len(self.bots),
                'recommended_bots': recommended_bots,
                'reason': 'Too many idle bots with low queue'
            })
        
        # Check for underperforming bots
        low_performers = [
            bot_id for bot_id, bot in self.bots.items()
            if bot.get_performance_score() < 0.5 and bot.tasks_completed > 10
        ]
        
        if low_performers:
            recommendations.append({
                'action': 'replace_bots',
                'bot_ids': low_performers[:10],  # Limit to 10 at a time
                'reason': 'Low performance detected'
            })
        
        return {
            'current_state': metrics,
            'recommendations': recommendations,
            'timestamp': datetime.utcnow().isoformat()
        }
