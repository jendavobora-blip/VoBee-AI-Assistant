"""
Orchestrator Service
Coordinates all AI services, manages task queues, and handles workflows
Includes L20 Supreme Brain orchestration system
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

# Import L20 components
from supreme_brain import SupremeBrain
from master_intelligences import (
    ProductContentIntelligence,
    MarketingIntelligence,
    WebAppBuilderIntelligence,
    AdvancedMediaIntelligence
)
from swarm_coordinator import SwarmCoordinator
from security_utils import (
    SecurityValidator,
    sanitize_user_input,
    rate_limiter
)

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
        
        # Initialize L20 Supreme Brain and components
        self.supreme_brain = SupremeBrain(self)
        
        # Initialize Master Intelligences (L18 subsystems)
        self.intelligences = {
            'product_content': ProductContentIntelligence(self),
            'marketing': MarketingIntelligence(self),
            'web_app_builder': WebAppBuilderIntelligence(self),
            'advanced_media': AdvancedMediaIntelligence(self)
        }
        
        # Initialize AI Swarm Coordinator
        self.swarm_coordinator = SwarmCoordinator(self)
        
        logger.info("Task Orchestrator with L20 Supreme Brain initialized successfully")
    
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

# L20 Supreme Brain endpoints

@app.route('/l20/strategize', methods=['POST'])
def l20_strategize():
    """High-level strategic planning endpoint"""
    try:
        # Rate limiting
        client_id = request.remote_addr
        if not rate_limiter.check_rate_limit(client_id, 'l20_strategize'):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        data = request.get_json()
        
        # Input validation
        if not data or 'objective' not in data:
            return jsonify({"error": "Objective is required"}), 400
        
        # Sanitize input
        sanitized_data = sanitize_user_input(data)
        
        objective = SecurityValidator.sanitize_string(sanitized_data['objective'], 1000)
        constraints = sanitized_data.get('constraints', {})
        
        # Validate constraints
        if constraints:
            SecurityValidator.validate_dict_size(constraints, 50)
        
        strategy = orchestrator.supreme_brain.strategize(objective, constraints)
        
        return jsonify(strategy), 200
        
    except ValueError as e:
        logger.error(f"Validation error in strategize: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in strategize endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/l20/prioritize', methods=['POST'])
def l20_prioritize():
    """Intelligent task prioritization endpoint"""
    try:
        # Rate limiting
        client_id = request.remote_addr
        if not rate_limiter.check_rate_limit(client_id, 'default'):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        data = request.get_json()
        
        if not data or 'tasks' not in data:
            return jsonify({"error": "Tasks list is required"}), 400
        
        # Sanitize and validate tasks
        sanitized_tasks = SecurityValidator.sanitize_tasks(data['tasks'])
        
        prioritized_tasks = orchestrator.supreme_brain.prioritize_tasks(sanitized_tasks)
        
        return jsonify({
            "prioritized_tasks": prioritized_tasks,
            "total_tasks": len(prioritized_tasks)
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error in prioritize: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in prioritize endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/l20/coordinate', methods=['POST'])
def l20_coordinate():
    """Cross-domain coordination endpoint"""
    try:
        # Rate limiting
        client_id = request.remote_addr
        if not rate_limiter.check_rate_limit(client_id, 'l20_coordinate'):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        data = request.get_json()
        
        if not data or 'domains' not in data:
            return jsonify({"error": "Domains list is required"}), 400
        
        # Sanitize input
        sanitized_data = sanitize_user_input(data)
        
        domains = sanitized_data['domains']
        task_specs = sanitized_data.get('task_specs', {})
        
        # Validate domains
        if not isinstance(domains, list):
            return jsonify({"error": "Domains must be a list"}), 400
        
        SecurityValidator.validate_list_size(domains, 20)
        
        coordination_plan = orchestrator.supreme_brain.coordinate_cross_domain(domains, task_specs)
        
        return jsonify(coordination_plan), 200
        
    except ValueError as e:
        logger.error(f"Validation error in coordinate: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in coordinate endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/l20/optimize-resources', methods=['POST'])
def l20_optimize_resources():
    """Resource optimization endpoint"""
    try:
        # Rate limiting
        client_id = request.remote_addr
        if not rate_limiter.check_rate_limit(client_id, 'default'):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        data = request.get_json()
        
        # Sanitize input
        sanitized_data = sanitize_user_input(data)
        
        available_resources = sanitized_data.get('available_resources', {
            'cpu': 64,
            'memory': 256000,
            'gpu': 4
        })
        pending_tasks = sanitized_data.get('pending_tasks', [])
        
        # Validate resources
        SecurityValidator.validate_resource_values(available_resources)
        
        # Validate tasks
        if pending_tasks:
            pending_tasks = SecurityValidator.sanitize_tasks(pending_tasks)
        
        allocation_plan = orchestrator.supreme_brain.optimize_resource_allocation(
            available_resources, pending_tasks
        )
        
        return jsonify(allocation_plan), 200
        
    except ValueError as e:
        logger.error(f"Validation error in optimize-resources: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in optimize-resources endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/l20/metrics', methods=['GET'])
def l20_metrics():
    """Get L20 Supreme Brain metrics"""
    try:
        metrics = orchestrator.supreme_brain.get_metrics()
        return jsonify(metrics), 200
    except Exception as e:
        logger.error(f"Error in metrics endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# Master Intelligence endpoints

@app.route('/intelligence/<intelligence_type>/execute', methods=['POST'])
def execute_intelligence(intelligence_type: str):
    """Execute specific Master Intelligence task"""
    try:
        # Rate limiting
        client_id = request.remote_addr
        if not rate_limiter.check_rate_limit(client_id, 'intelligence_execute'):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        # Validate intelligence type
        if not SecurityValidator.validate_intelligence_type(intelligence_type):
            return jsonify({
                "error": f"Unknown intelligence type: {intelligence_type}",
                "available": list(orchestrator.intelligences.keys())
            }), 400
        
        data = request.get_json()
        
        # Sanitize input
        sanitized_data = sanitize_user_input(data)
        
        intelligence = orchestrator.intelligences[intelligence_type]
        result = intelligence.execute(sanitized_data)
        
        return jsonify(result), 200
        
    except ValueError as e:
        logger.error(f"Validation error executing {intelligence_type} intelligence: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error executing {intelligence_type} intelligence: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/intelligence/<intelligence_type>/metrics', methods=['GET'])
def get_intelligence_metrics(intelligence_type: str):
    """Get metrics for specific Master Intelligence"""
    try:
        if intelligence_type not in orchestrator.intelligences:
            return jsonify({
                "error": f"Unknown intelligence type: {intelligence_type}"
            }), 400
        
        intelligence = orchestrator.intelligences[intelligence_type]
        metrics = intelligence.get_metrics()
        
        return jsonify(metrics), 200
        
    except Exception as e:
        logger.error(f"Error getting {intelligence_type} metrics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/intelligence/list', methods=['GET'])
def list_intelligences():
    """List all available Master Intelligences"""
    intelligences = {}
    for name, intelligence in orchestrator.intelligences.items():
        intelligences[name] = {
            'name': intelligence.name,
            'metrics': intelligence.get_metrics()
        }
    
    return jsonify({
        "intelligences": intelligences,
        "count": len(intelligences)
    })

# AI Swarm endpoints

@app.route('/swarm/dispatch', methods=['POST'])
def swarm_dispatch():
    """Dispatch micro-tasks to AI swarm"""
    try:
        # Rate limiting
        client_id = request.remote_addr
        if not rate_limiter.check_rate_limit(client_id, 'swarm_dispatch'):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        data = request.get_json()
        
        if not data or 'tasks' not in data:
            return jsonify({"error": "Tasks list is required"}), 400
        
        # Sanitize and validate tasks
        sanitized_tasks = SecurityValidator.sanitize_tasks(data['tasks'])
        
        result = orchestrator.swarm_coordinator.dispatch_micro_tasks(sanitized_tasks)
        
        return jsonify(result), 200
        
    except ValueError as e:
        logger.error(f"Validation error in swarm dispatch: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in swarm dispatch: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/swarm/status', methods=['GET'])
def swarm_status():
    """Get AI swarm status"""
    try:
        status = orchestrator.swarm_coordinator.get_swarm_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting swarm status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/swarm/metrics', methods=['GET'])
def swarm_metrics():
    """Get AI swarm performance metrics"""
    try:
        metrics = orchestrator.swarm_coordinator.get_performance_metrics()
        return jsonify(metrics), 200
    except Exception as e:
        logger.error(f"Error getting swarm metrics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/swarm/scale', methods=['POST'])
def swarm_scale():
    """Scale AI swarm to target size"""
    try:
        # Rate limiting
        client_id = request.remote_addr
        if not rate_limiter.check_rate_limit(client_id, 'default'):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        data = request.get_json()
        
        if not data or 'target_size' not in data:
            return jsonify({"error": "Target size is required"}), 400
        
        target_size = data['target_size']
        
        # Validate target size
        if not isinstance(target_size, int) or target_size < 10 or target_size > 1000000:
            return jsonify({"error": "Target size must be between 10 and 1,000,000"}), 400
        
        orchestrator.swarm_coordinator.scale_swarm(target_size)
        
        return jsonify({
            "status": "success",
            "message": f"Swarm scaled to {target_size} bots",
            "current_status": orchestrator.swarm_coordinator.get_swarm_status()
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error scaling swarm: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error scaling swarm: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/swarm/optimize', methods=['POST'])
def swarm_optimize():
    """Optimize swarm configuration"""
    try:
        result = orchestrator.swarm_coordinator.optimize_swarm()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error optimizing swarm: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
