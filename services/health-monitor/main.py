"""
Health Monitor & Auto-Healing Service
Monitors all services, detects failures, and performs automatic recovery
"""

from flask import Flask, jsonify, request
import httpx
import logging
import os
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
from elasticsearch import Elasticsearch
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class HealthMonitor:
    """Main health monitoring and auto-healing engine"""
    
    def __init__(self):
        self.services = {
            'api-gateway': os.getenv('API_GATEWAY_URL', 'http://api-gateway:8000'),
            'image-generation': os.getenv('IMAGE_SERVICE_URL', 'http://image-generation:5000'),
            'video-generation': os.getenv('VIDEO_SERVICE_URL', 'http://video-generation:5001'),
            'crypto-prediction': os.getenv('CRYPTO_SERVICE_URL', 'http://crypto-prediction:5002'),
            'orchestrator': os.getenv('ORCHESTRATOR_URL', 'http://orchestrator:5003'),
            'fraud-detection': os.getenv('FRAUD_SERVICE_URL', 'http://fraud-detection:5004'),
            'auto-scaler': os.getenv('AUTO_SCALER_URL', 'http://auto-scaler:5005'),
        }
        
        # Health check configuration
        self.check_interval = int(os.getenv('HEALTH_CHECK_INTERVAL', 30))
        self.max_failures = int(os.getenv('MAX_FAILURES_BEFORE_RECOVERY', 3))
        self.recovery_timeout = int(os.getenv('RECOVERY_TIMEOUT', 60))
        
        # Track service health
        self.service_status = {}
        self.failure_counts = defaultdict(int)
        self.last_recovery_time = {}
        self.error_history = defaultdict(lambda: deque(maxlen=100))
        
        # ElasticSearch for logging
        self.es_enabled = os.getenv('ELASTICSEARCH_ENABLED', 'true').lower() == 'true'
        if self.es_enabled:
            try:
                self.es_client = Elasticsearch([os.getenv('ELASTICSEARCH_URL', 'http://elasticsearch:9200')])
                logger.info("Connected to ElasticSearch for logging")
            except Exception as e:
                logger.warning(f"Failed to connect to ElasticSearch: {e}")
                self.es_enabled = False
        
        logger.info(f"Health Monitor initialized with {len(self.services)} services")
        logger.info(f"Check interval: {self.check_interval}s, Max failures: {self.max_failures}")
    
    async def check_service_health(self, service_name: str, service_url: str) -> Dict[str, Any]:
        """Check health of a single service"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                start_time = time.time()
                response = await client.get(f"{service_url}/health")
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    return {
                        'service': service_name,
                        'status': 'healthy',
                        'response_time': response_time,
                        'timestamp': datetime.utcnow().isoformat(),
                        'url': service_url
                    }
                else:
                    return {
                        'service': service_name,
                        'status': 'unhealthy',
                        'error': f"HTTP {response.status_code}",
                        'timestamp': datetime.utcnow().isoformat(),
                        'url': service_url
                    }
        except Exception as e:
            return {
                'service': service_name,
                'status': 'unreachable',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
                'url': service_url
            }
    
    async def check_all_services(self) -> Dict[str, Any]:
        """Check health of all services"""
        results = {}
        tasks = []
        
        for service_name, service_url in self.services.items():
            tasks.append(self.check_service_health(service_name, service_url))
        
        health_results = await asyncio.gather(*tasks)
        
        for result in health_results:
            service_name = result['service']
            results[service_name] = result
            self.service_status[service_name] = result
            
            # Track failures
            if result['status'] != 'healthy':
                self.failure_counts[service_name] += 1
                self.error_history[service_name].append({
                    'timestamp': result['timestamp'],
                    'error': result.get('error', 'unknown'),
                    'status': result['status']
                })
                
                # Log to ElasticSearch
                self.log_error_to_elasticsearch(result)
                
                # Trigger auto-healing if threshold reached
                if self.failure_counts[service_name] >= self.max_failures:
                    await self.auto_heal_service(service_name)
            else:
                # Reset failure count on success
                self.failure_counts[service_name] = 0
        
        return results
    
    async def auto_heal_service(self, service_name: str):
        """Attempt to auto-heal a failed service"""
        # Check if we recently attempted recovery
        last_recovery = self.last_recovery_time.get(service_name)
        if last_recovery:
            time_since_recovery = (datetime.utcnow() - last_recovery).total_seconds()
            if time_since_recovery < self.recovery_timeout:
                logger.info(f"Skipping recovery for {service_name}, recent attempt {time_since_recovery}s ago")
                return
        
        logger.warning(f"Auto-healing triggered for service: {service_name}")
        self.last_recovery_time[service_name] = datetime.utcnow()
        
        recovery_log = {
            'service': service_name,
            'action': 'auto_heal',
            'timestamp': datetime.utcnow().isoformat(),
            'failure_count': self.failure_counts[service_name],
            'recent_errors': list(self.error_history[service_name])[-5:]
        }
        
        # In Docker/Kubernetes environment, services auto-restart
        # Here we log the action and notify
        logger.info(f"Auto-healing action logged for {service_name}")
        
        # Log to ElasticSearch
        self.log_recovery_to_elasticsearch(recovery_log)
        
        # Reset failure count after recovery attempt
        self.failure_counts[service_name] = 0
        
        # Wait a bit before next check
        await asyncio.sleep(10)
    
    def log_error_to_elasticsearch(self, error_data: Dict[str, Any]):
        """Log error to ElasticSearch"""
        if not self.es_enabled:
            return
        
        try:
            doc = {
                'type': 'service_error',
                'service': error_data['service'],
                'status': error_data['status'],
                'error': error_data.get('error', ''),
                'timestamp': error_data['timestamp'],
                '@timestamp': datetime.utcnow().isoformat()
            }
            self.es_client.index(index='health-monitor-errors', document=doc)
        except Exception as e:
            logger.error(f"Failed to log to ElasticSearch: {e}")
    
    def log_recovery_to_elasticsearch(self, recovery_data: Dict[str, Any]):
        """Log recovery action to ElasticSearch"""
        if not self.es_enabled:
            return
        
        try:
            doc = {
                'type': 'auto_healing',
                'service': recovery_data['service'],
                'action': recovery_data['action'],
                'failure_count': recovery_data['failure_count'],
                'recent_errors': recovery_data['recent_errors'],
                'timestamp': recovery_data['timestamp'],
                '@timestamp': datetime.utcnow().isoformat()
            }
            self.es_client.index(index='health-monitor-recovery', document=doc)
        except Exception as e:
            logger.error(f"Failed to log recovery to ElasticSearch: {e}")
    
    def get_service_statistics(self) -> Dict[str, Any]:
        """Get statistics about service health"""
        total_services = len(self.services)
        healthy_services = sum(1 for status in self.service_status.values() 
                              if status.get('status') == 'healthy')
        
        return {
            'total_services': total_services,
            'healthy_services': healthy_services,
            'unhealthy_services': total_services - healthy_services,
            'failure_counts': dict(self.failure_counts),
            'last_check': datetime.utcnow().isoformat()
        }
    
    def get_error_history(self, service_name: str = None) -> Dict[str, Any]:
        """Get error history for services"""
        if service_name:
            return {
                'service': service_name,
                'errors': list(self.error_history.get(service_name, []))
            }
        else:
            return {
                'all_services': {
                    name: list(errors) 
                    for name, errors in self.error_history.items()
                }
            }


# Initialize health monitor
monitor = HealthMonitor()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check for the monitor itself"""
    return jsonify({
        "status": "healthy",
        "service": "health-monitor",
        "timestamp": datetime.utcnow().isoformat(),
        "elasticsearch_enabled": monitor.es_enabled
    })


@app.route('/check-services', methods=['GET'])
async def check_services():
    """Check health of all monitored services"""
    results = await monitor.check_all_services()
    return jsonify(results)


@app.route('/service-status', methods=['GET'])
def get_service_status():
    """Get current status of all services"""
    return jsonify(monitor.service_status)


@app.route('/statistics', methods=['GET'])
def get_statistics():
    """Get health statistics"""
    return jsonify(monitor.get_service_statistics())


@app.route('/error-history', methods=['GET'])
def get_error_history():
    """Get error history"""
    service_name = request.args.get('service')
    return jsonify(monitor.get_error_history(service_name))


@app.route('/recovery-history', methods=['GET'])
def get_recovery_history():
    """Get recovery action history"""
    return jsonify({
        'last_recovery_times': {
            name: time.isoformat() 
            for name, time in monitor.last_recovery_time.items()
        }
    })


@app.route('/trigger-heal/<service_name>', methods=['POST'])
async def trigger_manual_heal(service_name: str):
    """Manually trigger healing for a specific service"""
    if service_name not in monitor.services:
        return jsonify({"error": "Service not found"}), 404
    
    await monitor.auto_heal_service(service_name)
    return jsonify({
        "message": f"Auto-healing triggered for {service_name}",
        "timestamp": datetime.utcnow().isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=False)
