"""
Worker Pool Service
Stateless, disposable workers for crawling, analysis, and benchmarking
"""

from flask import Flask, request, jsonify
import logging
from datetime import datetime, timedelta
import os
import json
import requests
import time
from typing import Dict, Any, List, Optional
from uuid import uuid4
from threading import Thread
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class Worker:
    """Base worker class for stateless task execution"""
    
    def __init__(self, worker_id: str, worker_type: str):
        self.worker_id = worker_id
        self.worker_type = worker_type
        self.status = 'idle'
        self.current_task = None
        self.tasks_completed = 0
        self.created_at = datetime.utcnow().isoformat()
        self.task_deadline = None
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def is_deadline_exceeded(self) -> bool:
        """Check if current task deadline is exceeded"""
        if not self.task_deadline:
            return False
        return datetime.utcnow() > self.task_deadline
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert worker to dictionary"""
        return {
            'worker_id': self.worker_id,
            'worker_type': self.worker_type,
            'status': self.status,
            'current_task': self.current_task,
            'tasks_completed': self.tasks_completed,
            'created_at': self.created_at,
            'task_deadline': self.task_deadline.isoformat() if self.task_deadline else None
        }

class CrawlerWorker(Worker):
    """Worker for web crawling and data collection"""
    
    def __init__(self, worker_id: str):
        super().__init__(worker_id, 'crawler')
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute crawling task"""
        self.status = 'working'
        self.current_task = task.get('task_id')
        
        # Set deadline if provided
        deadline_seconds = task.get('deadline')
        if deadline_seconds:
            self.task_deadline = datetime.utcnow() + timedelta(seconds=deadline_seconds)
            logger.info(f"Worker {self.worker_id} task deadline set to {self.task_deadline.isoformat()}")
        
        try:
            # Check deadline before starting
            if self.is_deadline_exceeded():
                logger.warning(f"Worker {self.worker_id} task deadline already exceeded before execution")
                self.status = 'idle'
                self.current_task = None
                self.task_deadline = None
                return {
                    'status': 'failed',
                    'worker_id': self.worker_id,
                    'error': 'Task deadline exceeded before execution'
                }
            
            target_url = task.get('url')
            crawl_depth = task.get('depth', 1)
            
            logger.info(f"Worker {self.worker_id} crawling {target_url}")
            
            # Simple crawling simulation
            result = self._crawl_url(target_url, crawl_depth)
            
            # Check deadline after execution
            if self.is_deadline_exceeded():
                logger.warning(f"Worker {self.worker_id} task deadline exceeded during execution")
                self.tasks_completed += 1
                self.status = 'idle'
                self.current_task = None
                self.task_deadline = None
                return {
                    'status': 'timeout',
                    'worker_id': self.worker_id,
                    'error': 'Task deadline exceeded during execution',
                    'partial_data': result
                }
            
            self.tasks_completed += 1
            self.status = 'idle'
            self.current_task = None
            self.task_deadline = None
            
            return {
                'status': 'success',
                'worker_id': self.worker_id,
                'data': result
            }
        
        except Exception as e:
            logger.error(f"Worker {self.worker_id} crawl failed: {e}")
            self.status = 'idle'
            self.current_task = None
            self.task_deadline = None
            return {
                'status': 'failed',
                'worker_id': self.worker_id,
                'error': str(e)
            }
    
    def _crawl_url(self, url: str, depth: int) -> Dict[str, Any]:
        """Perform actual crawling"""
        try:
            headers = {
                'User-Agent': 'VoBee-AI-Assistant-Worker/1.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            response = requests.get(url, timeout=10, headers=headers, verify=True)
            return {
                'url': url,
                'status_code': response.status_code,
                'content_length': len(response.content),
                'headers': dict(response.headers),
                'crawled_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'crawled_at': datetime.utcnow().isoformat()
            }

class AnalysisWorker(Worker):
    """Worker for data analysis tasks"""
    
    def __init__(self, worker_id: str):
        super().__init__(worker_id, 'analysis')
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis task"""
        self.status = 'working'
        self.current_task = task.get('task_id')
        
        # Set deadline if provided
        deadline_seconds = task.get('deadline')
        if deadline_seconds:
            self.task_deadline = datetime.utcnow() + timedelta(seconds=deadline_seconds)
            logger.info(f"Worker {self.worker_id} task deadline set to {self.task_deadline.isoformat()}")
        
        try:
            # Check deadline before starting
            if self.is_deadline_exceeded():
                logger.warning(f"Worker {self.worker_id} task deadline already exceeded before execution")
                self.status = 'idle'
                self.current_task = None
                self.task_deadline = None
                return {
                    'status': 'failed',
                    'worker_id': self.worker_id,
                    'error': 'Task deadline exceeded before execution'
                }
            
            analysis_type = task.get('analysis_type', 'general')
            data = task.get('data', {})
            
            logger.info(f"Worker {self.worker_id} analyzing data ({analysis_type})")
            
            # Perform analysis
            result = self._analyze_data(data, analysis_type)
            
            # Check deadline after execution
            if self.is_deadline_exceeded():
                logger.warning(f"Worker {self.worker_id} task deadline exceeded during execution")
                self.tasks_completed += 1
                self.status = 'idle'
                self.current_task = None
                self.task_deadline = None
                return {
                    'status': 'timeout',
                    'worker_id': self.worker_id,
                    'error': 'Task deadline exceeded during execution',
                    'partial_analysis': result
                }
            
            self.tasks_completed += 1
            self.status = 'idle'
            self.current_task = None
            self.task_deadline = None
            
            return {
                'status': 'success',
                'worker_id': self.worker_id,
                'analysis': result
            }
        
        except Exception as e:
            logger.error(f"Worker {self.worker_id} analysis failed: {e}")
            self.status = 'idle'
            self.current_task = None
            self.task_deadline = None
            return {
                'status': 'failed',
                'worker_id': self.worker_id,
                'error': str(e)
            }
    
    def _analyze_data(self, data: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """Perform data analysis"""
        # Simplified analysis
        result = {
            'analysis_type': analysis_type,
            'data_points': len(data),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if analysis_type == 'sentiment':
            # Sentiment analysis simulation
            result['sentiment'] = 'positive'
            result['confidence'] = 0.75
        elif analysis_type == 'statistics':
            # Statistical analysis simulation
            result['mean'] = 0.5
            result['median'] = 0.5
            result['std_dev'] = 0.1
        
        return result

class BenchmarkWorker(Worker):
    """Worker for performance benchmarking"""
    
    def __init__(self, worker_id: str):
        super().__init__(worker_id, 'benchmark')
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute benchmarking task"""
        self.status = 'working'
        self.current_task = task.get('task_id')
        
        # Set deadline if provided
        deadline_seconds = task.get('deadline')
        if deadline_seconds:
            self.task_deadline = datetime.utcnow() + timedelta(seconds=deadline_seconds)
            logger.info(f"Worker {self.worker_id} task deadline set to {self.task_deadline.isoformat()}")
        
        try:
            # Check deadline before starting
            if self.is_deadline_exceeded():
                logger.warning(f"Worker {self.worker_id} task deadline already exceeded before execution")
                self.status = 'idle'
                self.current_task = None
                self.task_deadline = None
                return {
                    'status': 'failed',
                    'worker_id': self.worker_id,
                    'error': 'Task deadline exceeded before execution'
                }
            
            benchmark_type = task.get('benchmark_type', 'cpu')
            iterations = task.get('iterations', 100)
            
            logger.info(f"Worker {self.worker_id} running {benchmark_type} benchmark")
            
            # Perform benchmark
            result = self._run_benchmark(benchmark_type, iterations)
            
            # Check deadline after execution
            if self.is_deadline_exceeded():
                logger.warning(f"Worker {self.worker_id} task deadline exceeded during execution")
                self.tasks_completed += 1
                self.status = 'idle'
                self.current_task = None
                self.task_deadline = None
                return {
                    'status': 'timeout',
                    'worker_id': self.worker_id,
                    'error': 'Task deadline exceeded during execution',
                    'partial_benchmark': result
                }
            
            self.tasks_completed += 1
            self.status = 'idle'
            self.current_task = None
            self.task_deadline = None
            
            return {
                'status': 'success',
                'worker_id': self.worker_id,
                'benchmark': result
            }
        
        except Exception as e:
            logger.error(f"Worker {self.worker_id} benchmark failed: {e}")
            self.status = 'idle'
            self.current_task = None
            self.task_deadline = None
            return {
                'status': 'failed',
                'worker_id': self.worker_id,
                'error': str(e)
            }
    
    def _run_benchmark(self, benchmark_type: str, iterations: int) -> Dict[str, Any]:
        """Run benchmark test"""
        start_time = time.time()
        
        # Simulate benchmark workload
        if benchmark_type == 'cpu':
            for _ in range(iterations):
                _ = sum(range(1000))
        elif benchmark_type == 'memory':
            data = [0] * iterations * 1000
        
        duration = time.time() - start_time
        
        return {
            'benchmark_type': benchmark_type,
            'iterations': iterations,
            'duration': duration,
            'throughput': iterations / duration if duration > 0 else 0,
            'timestamp': datetime.utcnow().isoformat()
        }

class WorkerPool:
    """Manages a pool of disposable workers"""
    
    def __init__(self):
        self.workers: Dict[str, Worker] = {}
        self.task_queue = queue.Queue()
        self.max_workers = int(os.getenv('MAX_WORKERS', 10))
        self.worker_types = {
            'crawler': CrawlerWorker,
            'analysis': AnalysisWorker,
            'benchmark': BenchmarkWorker
        }
        logger.info(f"Worker Pool initialized (max workers: {self.max_workers})")
    
    def create_worker(self, worker_type: str) -> Optional[Worker]:
        """Create a new worker of specified type"""
        if len(self.workers) >= self.max_workers:
            logger.warning("Worker pool at capacity")
            return None
        
        if worker_type not in self.worker_types:
            logger.error(f"Unknown worker type: {worker_type}")
            return None
        
        worker_id = str(uuid4())
        worker_class = self.worker_types[worker_type]
        worker = worker_class(worker_id)
        
        self.workers[worker_id] = worker
        logger.info(f"Created {worker_type} worker: {worker_id}")
        
        return worker
    
    def get_worker(self, worker_id: str) -> Optional[Worker]:
        """Get worker by ID"""
        return self.workers.get(worker_id)
    
    def dispose_worker(self, worker_id: str) -> bool:
        """Dispose of a worker"""
        if worker_id in self.workers:
            del self.workers[worker_id]
            logger.info(f"Disposed worker: {worker_id}")
            return True
        return False
    
    def get_idle_worker(self, worker_type: Optional[str] = None) -> Optional[Worker]:
        """Get an idle worker of specified type"""
        for worker in self.workers.values():
            if worker.status == 'idle':
                if worker_type is None or worker.worker_type == worker_type:
                    return worker
        return None
    
    def assign_task(self, worker_type: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Assign task to a worker"""
        # Try to find idle worker of the requested type
        worker = self.get_idle_worker(worker_type)
        
        # If no idle worker, create a new one
        if worker is None:
            worker = self.create_worker(worker_type)
        
        if worker is None:
            return {
                'status': 'queued',
                'message': 'No available workers, task queued'
            }
        
        # Execute task
        result = worker.execute(task)
        
        # Auto-dispose worker after task (stateless)
        self.dispose_worker(worker.worker_id)
        
        return result
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Get status of worker pool"""
        status = {
            'total_workers': len(self.workers),
            'max_workers': self.max_workers,
            'idle_workers': sum(1 for w in self.workers.values() if w.status == 'idle'),
            'working_workers': sum(1 for w in self.workers.values() if w.status == 'working'),
            'workers_by_type': {},
            'timestamp': datetime.utcnow().isoformat()
        }
        
        for worker_type in self.worker_types.keys():
            count = sum(1 for w in self.workers.values() if w.worker_type == worker_type)
            status['workers_by_type'][worker_type] = count
        
        return status

# Initialize worker pool
worker_pool = WorkerPool()

# API Endpoints

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "worker-pool",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/pool/status', methods=['GET'])
def get_pool_status():
    """Get worker pool status"""
    return jsonify(worker_pool.get_pool_status())

@app.route('/worker/create', methods=['POST'])
def create_worker():
    """Create a new worker"""
    data = request.get_json()
    worker_type = data.get('worker_type', 'crawler')
    
    worker = worker_pool.create_worker(worker_type)
    
    if worker:
        return jsonify(worker.to_dict()), 201
    else:
        return jsonify({"error": "Failed to create worker"}), 500

@app.route('/worker/<worker_id>', methods=['GET'])
def get_worker(worker_id: str):
    """Get worker details"""
    worker = worker_pool.get_worker(worker_id)
    
    if worker:
        return jsonify(worker.to_dict())
    else:
        return jsonify({"error": "Worker not found"}), 404

@app.route('/worker/<worker_id>', methods=['DELETE'])
def dispose_worker(worker_id: str):
    """Dispose of a worker"""
    success = worker_pool.dispose_worker(worker_id)
    
    if success:
        return jsonify({"message": "Worker disposed"}), 200
    else:
        return jsonify({"error": "Worker not found"}), 404

@app.route('/task/execute', methods=['POST'])
def execute_task():
    """Execute a task with an available worker"""
    data = request.get_json()
    
    worker_type = data.get('worker_type', 'crawler')
    task = data.get('task', {})
    task['task_id'] = str(uuid4())
    
    result = worker_pool.assign_task(worker_type, task)
    
    return jsonify(result)

@app.route('/workers', methods=['GET'])
def list_workers():
    """List all workers"""
    workers = [worker.to_dict() for worker in worker_pool.workers.values()]
    return jsonify({
        'workers': workers,
        'count': len(workers)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=False)
