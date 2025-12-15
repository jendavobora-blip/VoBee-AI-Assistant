"""
Orchestrator Service
Coordinates all AI services, manages task queues, and handles workflows
Enhanced with advanced bot swarm orchestration for up to 50,000 bots with L20 tier
"""

from flask import Flask, request, jsonify
import redis
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests
import os
from uuid import uuid4
from collections import defaultdict
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BotSwarmOrchestrator:
    """
    Advanced bot swarm orchestration system
    Supports up to 50,000 concurrent bots with L20 tier orchestration
    """
    
    def __init__(self):
        self.bots = {}  # Active bots registry
        self.bot_tasks = defaultdict(list)  # Tasks assigned to each bot
        self.swarm_groups = {}  # Bot swarm groups
        self.max_bots = 50000
        self.bot_stats = {
            'total_created': 0,
            'active_bots': 0,
            'tasks_executed': 0,
            'tier_distribution': defaultdict(int)
        }
        logger.info("Bot Swarm Orchestrator initialized - Max capacity: 50,000 bots")
    
    def create_bot(self, bot_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new bot instance
        
        Args:
            bot_config: Bot configuration including tier, capabilities, etc.
        """
        if len(self.bots) >= self.max_bots:
            raise ValueError(f"Maximum bot capacity ({self.max_bots}) reached")
        
        bot_id = str(uuid4())
        bot = {
            'id': bot_id,
            'name': bot_config.get('name', f'bot-{bot_id[:8]}'),
            'tier': bot_config.get('tier', 'standard'),  # standard, advanced, L20
            'capabilities': bot_config.get('capabilities', []),
            'status': 'active',
            'tasks_completed': 0,
            'created_at': datetime.utcnow().isoformat(),
            'last_active': datetime.utcnow().isoformat()
        }
        
        self.bots[bot_id] = bot
        self.bot_stats['total_created'] += 1
        self.bot_stats['active_bots'] += 1
        self.bot_stats['tier_distribution'][bot['tier']] += 1
        
        logger.info(f"Created bot {bot_id} - Tier: {bot['tier']}, Total active: {self.bot_stats['active_bots']}")
        return bot
    
    def create_bot_swarm(self, swarm_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a swarm of bots for mass-action orchestration
        
        Args:
            swarm_config: Swarm configuration including count, tier, etc.
        """
        swarm_id = str(uuid4())
        bot_count = min(swarm_config.get('count', 100), self.max_bots - len(self.bots))
        tier = swarm_config.get('tier', 'standard')
        
        if bot_count <= 0:
            raise ValueError("Cannot create swarm: bot capacity reached")
        
        swarm_bots = []
        for i in range(bot_count):
            bot_config = {
                'name': f"{swarm_config.get('name', 'swarm')}-bot-{i}",
                'tier': tier,
                'capabilities': swarm_config.get('capabilities', []),
                'swarm_id': swarm_id
            }
            bot = self.create_bot(bot_config)
            swarm_bots.append(bot['id'])
        
        swarm = {
            'id': swarm_id,
            'name': swarm_config.get('name', f'swarm-{swarm_id[:8]}'),
            'bot_count': bot_count,
            'tier': tier,
            'bot_ids': swarm_bots,
            'status': 'active',
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.swarm_groups[swarm_id] = swarm
        logger.info(f"Created bot swarm {swarm_id} with {bot_count} bots (Tier: {tier})")
        return swarm
    
    def assign_task_to_bot(self, bot_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Assign a task to a specific bot"""
        if bot_id not in self.bots:
            raise ValueError(f"Bot {bot_id} not found")
        
        bot = self.bots[bot_id]
        task_id = str(uuid4())
        
        task_assignment = {
            'task_id': task_id,
            'bot_id': bot_id,
            'task_type': task.get('type'),
            'task_data': task.get('data'),
            'status': 'assigned',
            'assigned_at': datetime.utcnow().isoformat()
        }
        
        self.bot_tasks[bot_id].append(task_assignment)
        bot['last_active'] = datetime.utcnow().isoformat()
        
        logger.info(f"Assigned task {task_id} to bot {bot_id}")
        return task_assignment
    
    def assign_task_to_swarm(self, swarm_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Distribute a task across all bots in a swarm
        Enables L20 orchestration for mass-action coordination
        """
        if swarm_id not in self.swarm_groups:
            raise ValueError(f"Swarm {swarm_id} not found")
        
        swarm = self.swarm_groups[swarm_id]
        assignments = []
        
        for bot_id in swarm['bot_ids']:
            assignment = self.assign_task_to_bot(bot_id, task)
            assignments.append(assignment)
        
        result = {
            'swarm_id': swarm_id,
            'task_type': task.get('type'),
            'assignments': len(assignments),
            'status': 'distributed',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Distributed task to {len(assignments)} bots in swarm {swarm_id}")
        return result
    
    def complete_bot_task(self, bot_id: str, task_id: str) -> Dict[str, Any]:
        """Mark a bot task as completed"""
        if bot_id not in self.bots:
            raise ValueError(f"Bot {bot_id} not found")
        
        bot = self.bots[bot_id]
        
        # Find and update task
        for task in self.bot_tasks[bot_id]:
            if task['task_id'] == task_id:
                task['status'] = 'completed'
                task['completed_at'] = datetime.utcnow().isoformat()
                bot['tasks_completed'] += 1
                bot['last_active'] = datetime.utcnow().isoformat()
                self.bot_stats['tasks_executed'] += 1
                logger.info(f"Bot {bot_id} completed task {task_id}")
                return task
        
        raise ValueError(f"Task {task_id} not found for bot {bot_id}")
    
    def get_bot_status(self, bot_id: str) -> Dict[str, Any]:
        """Get detailed status of a bot"""
        if bot_id not in self.bots:
            raise ValueError(f"Bot {bot_id} not found")
        
        bot = self.bots[bot_id]
        tasks = self.bot_tasks.get(bot_id, [])
        
        return {
            **bot,
            'total_tasks': len(tasks),
            'pending_tasks': len([t for t in tasks if t['status'] == 'assigned']),
            'completed_tasks': len([t for t in tasks if t['status'] == 'completed'])
        }
    
    def get_swarm_status(self, swarm_id: str) -> Dict[str, Any]:
        """Get detailed status of a bot swarm"""
        if swarm_id not in self.swarm_groups:
            raise ValueError(f"Swarm {swarm_id} not found")
        
        swarm = self.swarm_groups[swarm_id]
        
        total_tasks = 0
        active_bots = 0
        
        for bot_id in swarm['bot_ids']:
            if bot_id in self.bots and self.bots[bot_id]['status'] == 'active':
                active_bots += 1
                total_tasks += self.bots[bot_id]['tasks_completed']
        
        return {
            **swarm,
            'active_bots': active_bots,
            'total_tasks_completed': total_tasks,
            'average_tasks_per_bot': round(total_tasks / swarm['bot_count'], 2) if swarm['bot_count'] > 0 else 0
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get overall bot orchestration statistics"""
        return {
            **self.bot_stats,
            'swarm_count': len(self.swarm_groups),
            'capacity_remaining': self.max_bots - len(self.bots),
            'utilization_percent': round((len(self.bots) / self.max_bots) * 100, 2),
            'timestamp': datetime.utcnow().isoformat()
        }

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
            'compression': os.getenv('COMPRESSION_SERVICE_URL', 'http://compression-service:5006'),
            'marketing': os.getenv('MARKETING_SERVICE_URL', 'http://marketing-intelligence-service:5007'),
        }
        
        # Initialize bot swarm orchestrator
        self.bot_orchestrator = BotSwarmOrchestrator()
        
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

# Bot Orchestration Endpoints

@app.route('/bots', methods=['POST'])
def create_bot():
    """Create a new bot instance"""
    try:
        data = request.get_json()
        bot = orchestrator.bot_orchestrator.create_bot(data)
        return jsonify(bot), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating bot: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bots/<bot_id>', methods=['GET'])
def get_bot_status(bot_id: str):
    """Get bot status and statistics"""
    try:
        status = orchestrator.bot_orchestrator.get_bot_status(bot_id)
        return jsonify(status)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error getting bot status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bots/stats', methods=['GET'])
def get_bot_stats():
    """Get overall bot orchestration statistics"""
    stats = orchestrator.bot_orchestrator.get_stats()
    return jsonify(stats)

@app.route('/swarms', methods=['POST'])
def create_swarm():
    """Create a bot swarm for mass-action orchestration"""
    try:
        data = request.get_json()
        swarm = orchestrator.bot_orchestrator.create_bot_swarm(data)
        return jsonify(swarm), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating swarm: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/swarms/<swarm_id>', methods=['GET'])
def get_swarm_status(swarm_id: str):
    """Get swarm status and statistics"""
    try:
        status = orchestrator.bot_orchestrator.get_swarm_status(swarm_id)
        return jsonify(status)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error getting swarm status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bots/<bot_id>/tasks', methods=['POST'])
def assign_task_to_bot(bot_id: str):
    """Assign a task to a specific bot"""
    try:
        data = request.get_json()
        assignment = orchestrator.bot_orchestrator.assign_task_to_bot(bot_id, data)
        return jsonify(assignment), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error assigning task to bot: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/swarms/<swarm_id>/tasks', methods=['POST'])
def assign_task_to_swarm(swarm_id: str):
    """Distribute a task across all bots in a swarm"""
    try:
        data = request.get_json()
        result = orchestrator.bot_orchestrator.assign_task_to_swarm(swarm_id, data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error assigning task to swarm: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bots/<bot_id>/tasks/<task_id>/complete', methods=['POST'])
def complete_bot_task(bot_id: str, task_id: str):
    """Mark a bot task as completed"""
    try:
        result = orchestrator.bot_orchestrator.complete_bot_task(bot_id, task_id)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error completing bot task: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
