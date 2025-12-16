"""
Orchestrator Service
Coordinates all AI services, manages task queues, and handles workflows
"""

from flask import Flask, request, jsonify
import redis
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import requests
import os
from uuid import uuid4

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class TaskOrchestrator:
    """Main orchestration engine for managing AI tasks"""
    
    def __init__(self):
        self.redis_host = os.getenv('REDIS_HOST', 'redis-service')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_client = None
        self.connect_redis()
        
        # Service endpoints
        self.services = {
            'image_generation': os.getenv('IMAGE_SERVICE_URL', 'http://image-generation-service:5000'),
            'video_generation': os.getenv('VIDEO_SERVICE_URL', 'http://video-generation-service:5001'),
            'crypto_prediction': os.getenv('CRYPTO_SERVICE_URL', 'http://crypto-prediction-service:5002'),
            'fraud_detection': os.getenv('FRAUD_SERVICE_URL', 'http://fraud-detection-service:5004'),
        }
        
        logger.info("Task Orchestrator initialized successfully")
    
    def connect_redis(self):
        """Connect to Redis for task queue management"""
        try:
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info(f"Connected to Redis at {self.redis_host}:{self.redis_port}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def create_task(self, task_type: str, task_data: Dict[str, Any]):
        """
        Create a new task in the queue
        
        Args:
            task_type: Type of task (image_gen, video_gen, crypto_pred)
            task_data: Task parameters
        """
        task_id = str(uuid4())
        task = {
            'id': task_id,
            'type': task_type,
            'data': task_data,
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        if self.redis_client:
            try:
                # Store task in Redis
                self.redis_client.setex(
                    f"task:{task_id}",
                    3600,  # 1 hour TTL
                    json.dumps(task)
                )
                # Add to queue
                self.redis_client.rpush(f"queue:{task_type}", task_id)
                logger.info(f"Created task {task_id} of type {task_type}")
            except Exception as e:
                logger.error(f"Error creating task: {e}")
        
        return task
    
    def orchestrate_workflow(self, tasks: List[Dict[str, Any]], priority: str = "normal"):
        """
        Orchestrate multiple tasks in a workflow with priority management
        and task decomposition
        
        Args:
            tasks: List of tasks to execute
            priority: Workflow priority (low, normal, high, critical)
        """
        try:
            workflow_id = str(uuid4())
            logger.info(f"Orchestrating workflow {workflow_id} with {len(tasks)} tasks, priority: {priority}")
            
            # Decompose and prioritize tasks
            decomposed_tasks = self._decompose_tasks(tasks)
            prioritized_tasks = self._prioritize_tasks(decomposed_tasks, priority)
            
            # Allocate resources based on priority
            resource_allocation = self._allocate_resources(prioritized_tasks, priority)
            
            results = []
            
            for task in prioritized_tasks:
                task_type = task.get('type')
                task_params = task.get('params', {})
                task_priority = task.get('priority', priority)
                
                logger.info(f"Executing task {task_type} with priority {task_priority}")
                
                # Create and execute task
                if task_type == 'image_generation':
                    result = self.execute_image_generation(task_params)
                elif task_type == 'video_generation':
                    result = self.execute_video_generation(task_params)
                elif task_type == 'crypto_prediction':
                    result = self.execute_crypto_prediction(task_params)
                elif task_type == 'fraud_detection':
                    result = self.execute_fraud_detection(task_params)
                else:
                    result = {'error': f'Unknown task type: {task_type}'}
                
                results.append({
                    'task_type': task_type,
                    'priority': task_priority,
                    'result': result
                })
            
            workflow_result = {
                'workflow_id': workflow_id,
                'status': 'completed',
                'priority': priority,
                'tasks_executed': len(prioritized_tasks),
                'resource_allocation': resource_allocation,
                'results': results,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Store workflow result
            if self.redis_client:
                try:
                    self.redis_client.setex(
                        f"workflow:{workflow_id}",
                        7200,  # 2 hours TTL
                        json.dumps(workflow_result)
                    )
                except Exception as e:
                    logger.error(f"Error storing workflow result: {e}")
            
            return workflow_result
            
        except Exception as e:
            logger.error(f"Workflow orchestration failed: {e}")
            raise
    
    def _decompose_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Decompose complex tasks into simpler subtasks
        L19 layer task decomposition
        """
        decomposed = []
        
        for task in tasks:
            task_type = task.get('type')
            
            # Check if task needs decomposition
            if task_type == 'complex_generation':
                # Decompose into image + video generation
                decomposed.append({
                    'type': 'image_generation',
                    'params': task.get('params', {}),
                    'parent_task': task_type
                })
                decomposed.append({
                    'type': 'video_generation',
                    'params': task.get('params', {}),
                    'parent_task': task_type
                })
            elif task_type == 'market_analysis':
                # Decompose into prediction + fraud detection
                decomposed.append({
                    'type': 'crypto_prediction',
                    'params': task.get('params', {}),
                    'parent_task': task_type
                })
                decomposed.append({
                    'type': 'fraud_detection',
                    'params': task.get('params', {}),
                    'parent_task': task_type
                })
            else:
                # No decomposition needed
                decomposed.append(task)
        
        logger.info(f"Task decomposition: {len(tasks)} → {len(decomposed)} tasks")
        return decomposed
    
    def _prioritize_tasks(self, tasks: List[Dict[str, Any]], workflow_priority: str) -> List[Dict[str, Any]]:
        """
        Prioritize tasks based on type and workflow priority
        Priority levels: critical > high > normal > low
        """
        priority_mapping = {
            'critical': 4,
            'high': 3,
            'normal': 2,
            'low': 1
        }
        
        # Task type priority multipliers
        type_priority = {
            'fraud_detection': 1.5,  # Security tasks get higher priority
            'crypto_prediction': 1.2,  # Time-sensitive
            'image_generation': 1.0,
            'video_generation': 0.8  # Resource-intensive, lower priority
        }
        
        base_priority = priority_mapping.get(workflow_priority, 2)
        
        for task in tasks:
            task_type = task.get('type')
            type_mult = type_priority.get(task_type, 1.0)
            task['priority_score'] = base_priority * type_mult
            task['priority'] = workflow_priority
        
        # Sort by priority score (highest first)
        prioritized = sorted(tasks, key=lambda x: x.get('priority_score', 0), reverse=True)
        
        task_list = [f"{t['type']}({t['priority_score']:.1f})" for t in prioritized]
        logger.info(f"Tasks prioritized: {task_list}")
        return prioritized
    
    def _allocate_resources(self, tasks: List[Dict[str, Any]], priority: str) -> Dict[str, Any]:
        """
        Allocate resources based on task requirements and priority
        Returns resource allocation plan
        """
        allocation = {
            'cpu': 0,
            'memory': 0,
            'gpu': 0,
            'estimated_duration': 0
        }
        
        # Resource requirements per task type (simplified)
        resource_requirements = {
            'image_generation': {'cpu': 2, 'memory': 4096, 'gpu': 1, 'duration': 30},
            'video_generation': {'cpu': 4, 'memory': 8192, 'gpu': 1, 'duration': 120},
            'crypto_prediction': {'cpu': 1, 'memory': 2048, 'gpu': 0, 'duration': 10},
            'fraud_detection': {'cpu': 1, 'memory': 1024, 'gpu': 0, 'duration': 5}
        }
        
        for task in tasks:
            task_type = task.get('type')
            requirements = resource_requirements.get(task_type, {})
            
            allocation['cpu'] = max(allocation['cpu'], requirements.get('cpu', 0))
            allocation['memory'] += requirements.get('memory', 0)
            allocation['gpu'] = max(allocation['gpu'], requirements.get('gpu', 0))
            allocation['estimated_duration'] += requirements.get('duration', 0)
        
        # Apply priority modifiers
        if priority == 'critical':
            allocation['cpu'] = int(allocation['cpu'] * 1.5)
            allocation['memory'] = int(allocation['memory'] * 1.5)
        elif priority == 'high':
            allocation['cpu'] = int(allocation['cpu'] * 1.2)
            allocation['memory'] = int(allocation['memory'] * 1.2)
        
        logger.info(f"Resource allocation: CPU={allocation['cpu']}, Memory={allocation['memory']}MB, GPU={allocation['gpu']}")
        return allocation
    
    def execute_image_generation(self, params: Dict[str, Any]):
        """Execute image generation task"""
        try:
            response = requests.post(
                f"{self.services['image_generation']}/generate",
                json=params,
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Image generation task failed: {e}")
            return {'error': str(e)}
    
    def execute_video_generation(self, params: Dict[str, Any]):
        """Execute video generation task"""
        try:
            response = requests.post(
                f"{self.services['video_generation']}/generate",
                json=params,
                timeout=600
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Video generation task failed: {e}")
            return {'error': str(e)}
    
    def execute_crypto_prediction(self, params: Dict[str, Any]):
        """Execute crypto prediction task"""
        try:
            response = requests.post(
                f"{self.services['crypto_prediction']}/predict",
                json=params,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Crypto prediction task failed: {e}")
            return {'error': str(e)}
    
    def execute_fraud_detection(self, params: Dict[str, Any]):
        """Execute fraud detection task"""
        try:
            response = requests.post(
                f"{self.services['fraud_detection']}/analyze",
                json=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Fraud detection task failed: {e}")
            return {'error': str(e)}
    
    def get_task_status(self, task_id: str):
        """Get status of a specific task"""
        if self.redis_client:
            try:
                task_data = self.redis_client.get(f"task:{task_id}")
                if task_data:
                    return json.loads(task_data)
            except Exception as e:
                logger.error(f"Error retrieving task status: {e}")
        return None

# Initialize orchestrator
orchestrator = TaskOrchestrator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    redis_status = "connected" if orchestrator.redis_client else "disconnected"
    return jsonify({
        "status": "healthy",
        "service": "orchestrator",
        "redis": redis_status,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    """Orchestrate multiple AI tasks"""
    try:
        data = request.get_json()
        
        if 'tasks' not in data:
            return jsonify({"error": "Tasks list is required"}), 400
        
        result = orchestrator.orchestrate_workflow(
            tasks=data['tasks'],
            priority=data.get('priority', 'normal')
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in orchestrate endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id: str):
    """Get task status by ID"""
    try:
        task = orchestrator.get_task_status(task_id)
        if task:
            return jsonify(task), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving task: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/services', methods=['GET'])
def list_services():
    """List all available services"""
    return jsonify({
        "services": orchestrator.services
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
