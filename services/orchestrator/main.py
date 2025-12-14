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
        self.redis_host = os.getenv('REDIS_HOST', 'redis')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_client = None
        self.connect_redis()
        
        # Service endpoints
        self.services = {
            'image_generation': os.getenv('IMAGE_SERVICE_URL', 'http://image-generation:5000'),
            'video_generation': os.getenv('VIDEO_SERVICE_URL', 'http://video-generation:5001'),
            'crypto_prediction': os.getenv('CRYPTO_SERVICE_URL', 'http://crypto-prediction:5002'),
            'fraud_detection': os.getenv('FRAUD_SERVICE_URL', 'http://fraud-detection:5004'),
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
        Orchestrate multiple tasks in a workflow
        
        Args:
            tasks: List of tasks to execute
            priority: Workflow priority (low, normal, high)
        """
        try:
            workflow_id = str(uuid4())
            logger.info(f"Orchestrating workflow {workflow_id} with {len(tasks)} tasks")
            
            results = []
            
            for task in tasks:
                task_type = task.get('type')
                task_params = task.get('params', {})
                
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
                    'result': result
                })
            
            workflow_result = {
                'workflow_id': workflow_id,
                'status': 'completed',
                'priority': priority,
                'tasks_executed': len(tasks),
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
