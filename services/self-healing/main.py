"""
Self-Healing Architecture Service
Health monitoring, failure detection, and auto-repair
"""

from flask import Flask, request, jsonify
import logging
from datetime import datetime, timedelta
import requests
import os
import json
from typing import Dict, Any, List, Optional
import time
from threading import Thread
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class SelfHealingMonitor:
    """Health monitoring and auto-repair system"""
    
    def __init__(self):
        self.services = {
            'api-gateway': {'url': 'http://api-gateway:8000', 'port': 8000},
            'image-generation': {'url': 'http://image-generation:5000', 'port': 5000},
            'video-generation': {'url': 'http://video-generation:5001', 'port': 5001},
            'crypto-prediction': {'url': 'http://crypto-prediction:5002', 'port': 5002},
            'orchestrator': {'url': 'http://orchestrator:5003', 'port': 5003},
            'fraud-detection': {'url': 'http://fraud-detection:5004', 'port': 5004},
            'auto-scaler': {'url': 'http://auto-scaler:5005', 'port': 5005},
            'spy-orchestration': {'url': 'http://spy-orchestration:5006', 'port': 5006},
            'self-healing': {'url': 'http://self-healing:5007', 'port': 5007},
            'worker-pool': {'url': 'http://worker-pool:5008', 'port': 5008},
            'supreme-general-intelligence': {'url': 'http://supreme-general-intelligence:5010', 'port': 5010},
        }
        
        self.health_checks = {}
        self.failure_counts = {}
        self.repair_history = []
        self.monitoring_enabled = True
        
        # Configuration
        self.check_interval = int(os.getenv('HEALTH_CHECK_INTERVAL', 30))  # seconds
        self.failure_threshold = int(os.getenv('FAILURE_THRESHOLD', 3))
        self.repair_timeout = int(os.getenv('REPAIR_TIMEOUT', 300))  # seconds
        
        # Start monitoring thread
        self.monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info("Self-Healing Monitor initialized")
    
    def _monitor_loop(self):
        """Continuous monitoring loop"""
        while self.monitoring_enabled:
            try:
                self.check_all_services()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.check_interval)
    
    def check_service_health(self, service_name: str, service_config: Dict) -> Dict[str, Any]:
        """Check health of a single service"""
        health_status = {
            'service': service_name,
            'status': 'unknown',
            'response_time': None,
            'error': None,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            start_time = time.time()
            response = requests.get(
                f"{service_config['url']}/health",
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                health_status['status'] = 'healthy'
                health_status['response_time'] = response_time
                
                # Reset failure count on success
                self.failure_counts[service_name] = 0
            else:
                health_status['status'] = 'unhealthy'
                health_status['error'] = f"HTTP {response.status_code}"
                self._increment_failure(service_name)
        
        except requests.exceptions.ConnectionError:
            health_status['status'] = 'unreachable'
            health_status['error'] = 'Connection failed'
            self._increment_failure(service_name)
        
        except requests.exceptions.Timeout:
            health_status['status'] = 'timeout'
            health_status['error'] = 'Request timeout'
            self._increment_failure(service_name)
        
        except Exception as e:
            health_status['status'] = 'error'
            health_status['error'] = str(e)
            self._increment_failure(service_name)
        
        self.health_checks[service_name] = health_status
        return health_status
    
    def _increment_failure(self, service_name: str):
        """Increment failure count and trigger repair if threshold exceeded"""
        if service_name not in self.failure_counts:
            self.failure_counts[service_name] = 0
        
        self.failure_counts[service_name] += 1
        
        if self.failure_counts[service_name] >= self.failure_threshold:
            logger.warning(
                f"Service {service_name} has failed {self.failure_counts[service_name]} times. "
                f"Triggering auto-repair..."
            )
            self.attempt_repair(service_name)
    
    def check_all_services(self) -> Dict[str, Dict]:
        """Check health of all services"""
        results = {}
        for service_name, service_config in self.services.items():
            results[service_name] = self.check_service_health(service_name, service_config)
        return results
    
    def attempt_repair(self, service_name: str) -> Dict[str, Any]:
        """
        Attempt to repair a failed service
        """
        repair_result = {
            'service': service_name,
            'timestamp': datetime.utcnow().isoformat(),
            'actions_taken': [],
            'success': False,
            'error': None
        }
        
        try:
            logger.info(f"Starting repair for service: {service_name}")
            
            # Step 1: Try to restart the service (Docker container)
            restart_success = self._restart_service_container(service_name)
            repair_result['actions_taken'].append({
                'action': 'restart_container',
                'success': restart_success
            })
            
            if restart_success:
                # Wait for service to come up
                time.sleep(10)
                
                # Step 2: Verify service is healthy
                health_check = self.check_service_health(
                    service_name, 
                    self.services[service_name]
                )
                
                if health_check['status'] == 'healthy':
                    repair_result['success'] = True
                    repair_result['actions_taken'].append({
                        'action': 'health_verified',
                        'success': True
                    })
                    logger.info(f"Service {service_name} successfully repaired")
                else:
                    # Step 3: If still unhealthy, try rollback (if applicable)
                    logger.warning(f"Service {service_name} still unhealthy after restart")
                    repair_result['error'] = 'Service unhealthy after restart'
            else:
                repair_result['error'] = 'Failed to restart container'
        
        except Exception as e:
            logger.error(f"Error during repair of {service_name}: {e}")
            repair_result['error'] = str(e)
        
        # Store repair history
        self.repair_history.append(repair_result)
        
        # Keep only last 100 repair attempts
        if len(self.repair_history) > 100:
            self.repair_history = self.repair_history[-100:]
        
        return repair_result
    
    def _restart_service_container(self, service_name: str) -> bool:
        """
        Restart a Docker container for a service
        """
        try:
            # Check if Docker socket is available
            docker_socket = '/var/run/docker.sock'
            if not os.path.exists(docker_socket):
                logger.warning("Docker socket not available, skipping container restart")
                return False
            
            # Use docker-compose to restart the service
            result = subprocess.run(
                ['docker', 'restart', service_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info(f"Successfully restarted container: {service_name}")
                return True
            else:
                logger.error(f"Failed to restart container {service_name}: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout while restarting container: {service_name}")
            return False
        
        except Exception as e:
            logger.error(f"Error restarting container {service_name}: {e}")
            return False
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get overall system health summary"""
        total_services = len(self.services)
        healthy_services = sum(
            1 for status in self.health_checks.values() 
            if status.get('status') == 'healthy'
        )
        
        return {
            'total_services': total_services,
            'healthy_services': healthy_services,
            'unhealthy_services': total_services - healthy_services,
            'overall_health': 'healthy' if healthy_services == total_services else 'degraded',
            'timestamp': datetime.utcnow().isoformat(),
            'services': self.health_checks
        }
    
    def propose_fixes(self, service_name: str) -> List[Dict[str, Any]]:
        """
        Propose potential fixes for a failed service
        """
        fixes = []
        
        health_status = self.health_checks.get(service_name, {})
        status = health_status.get('status', 'unknown')
        
        if status == 'unreachable':
            fixes.append({
                'issue': 'Service unreachable',
                'fix': 'Restart the service container',
                'command': f'docker restart {service_name}',
                'risk': 'low'
            })
            fixes.append({
                'issue': 'Network connectivity',
                'fix': 'Check Docker network configuration',
                'command': 'docker network inspect ai-network',
                'risk': 'low'
            })
        
        elif status == 'timeout':
            fixes.append({
                'issue': 'Service timeout',
                'fix': 'Increase resource allocation',
                'command': 'Edit docker-compose.yml to increase CPU/memory limits',
                'risk': 'low'
            })
            fixes.append({
                'issue': 'Heavy load',
                'fix': 'Scale the service horizontally',
                'command': f'docker-compose up -d --scale {service_name}=2',
                'risk': 'medium'
            })
        
        elif status == 'unhealthy':
            fixes.append({
                'issue': 'Application error',
                'fix': 'Check service logs for errors',
                'command': f'docker logs {service_name}',
                'risk': 'low'
            })
            fixes.append({
                'issue': 'Configuration issue',
                'fix': 'Verify environment variables and configuration',
                'command': f'docker inspect {service_name}',
                'risk': 'low'
            })
        
        return fixes

# Initialize monitor
monitor = SelfHealingMonitor()

# API Endpoints

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "self-healing",
        "monitoring_enabled": monitor.monitoring_enabled,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/system/health', methods=['GET'])
def get_system_health():
    """Get overall system health"""
    return jsonify(monitor.get_system_health_summary())

@app.route('/service/<service_name>/health', methods=['GET'])
def get_service_health(service_name: str):
    """Get health status of a specific service"""
    if service_name not in monitor.services:
        return jsonify({"error": "Service not found"}), 404
    
    health_status = monitor.check_service_health(
        service_name, 
        monitor.services[service_name]
    )
    return jsonify(health_status)

@app.route('/service/<service_name>/repair', methods=['POST'])
def repair_service(service_name: str):
    """Manually trigger repair for a service"""
    if service_name not in monitor.services:
        return jsonify({"error": "Service not found"}), 404
    
    result = monitor.attempt_repair(service_name)
    return jsonify(result)

@app.route('/service/<service_name>/fixes', methods=['GET'])
def get_proposed_fixes(service_name: str):
    """Get proposed fixes for a service"""
    if service_name not in monitor.services:
        return jsonify({"error": "Service not found"}), 404
    
    fixes = monitor.propose_fixes(service_name)
    return jsonify({
        'service': service_name,
        'proposed_fixes': fixes
    })

@app.route('/repairs/history', methods=['GET'])
def get_repair_history():
    """Get repair history"""
    limit = request.args.get('limit', 50, type=int)
    return jsonify({
        'repairs': monitor.repair_history[-limit:],
        'total': len(monitor.repair_history)
    })

@app.route('/monitoring/toggle', methods=['POST'])
def toggle_monitoring():
    """Enable or disable monitoring"""
    data = request.get_json()
    enabled = data.get('enabled', True)
    monitor.monitoring_enabled = enabled
    
    return jsonify({
        'monitoring_enabled': monitor.monitoring_enabled,
        'message': f"Monitoring {'enabled' if enabled else 'disabled'}"
    })

@app.route('/services', methods=['GET'])
def list_services():
    """List all monitored services"""
    return jsonify({
        'services': list(monitor.services.keys()),
        'count': len(monitor.services)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)
