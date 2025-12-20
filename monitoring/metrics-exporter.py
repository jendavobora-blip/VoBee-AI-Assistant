"""
Metrics Exporter for VoBee AI Orchestration
Exports metrics from all modules to Prometheus
"""

from prometheus_client import start_http_server, Counter, Gauge, Histogram
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define metrics
tasks_completed = Counter('tasks_completed_total', 'Total completed tasks', ['module'])
tasks_failed = Counter('tasks_failed_total', 'Total failed tasks', ['module'])
active_tasks = Gauge('active_tasks', 'Number of active tasks', ['module'])
request_duration = Histogram('request_duration_seconds', 'Request duration', ['module'])
module_health = Gauge('module_health_status', 'Module health status', ['module', 'status'])
service_up = Gauge('up', 'Service up status', ['job', 'instance'])

class MetricsExporter:
    """Export metrics from AI modules"""
    
    def __init__(self):
        self.modules = [
            'email-ai', 'facebook-ai', 'marketing-ai', 'seo-ai', 'content-ai', 'analytics-ai',
            'finance-ai', 'invoice-ai', 'budget-ai', 'tax-ai', 'cashflow-ai',
            'research-ai', 'web-scraper-ai', 'data-mining-ai', 'sentiment-ai', 'trend-ai',
            'email-response-ai', 'chat-support-ai', 'translation-ai', 'voice-ai', 'meeting-ai',
            'music-ai', 'design-ai', 'animation-ai', 'presentation-ai', 'podcast-ai',
            'code-review-ai', 'documentation-ai', 'testing-ai', 'deployment-ai'
        ]
        logger.info("Metrics Exporter initialized")
    
    def collect_metrics(self):
        """Collect metrics from all modules"""
        for module in self.modules:
            try:
                # Try to get health status
                response = requests.get(f'http://{module}:5000/health', timeout=5)
                
                if response.status_code == 200:
                    service_up.labels(job='ai-services', instance=module).set(1)
                    module_health.labels(module=module, status='healthy').set(1)
                else:
                    service_up.labels(job='ai-services', instance=module).set(0)
                    module_health.labels(module=module, status='unhealthy').set(1)
                    
            except Exception as e:
                logger.error(f"Error collecting metrics from {module}: {e}")
                service_up.labels(job='ai-services', instance=module).set(0)
                module_health.labels(module=module, status='unknown').set(1)
    
    def run(self, interval=30):
        """Run metrics collection loop"""
        logger.info(f"Starting metrics collection (interval: {interval}s)")
        
        while True:
            try:
                self.collect_metrics()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                time.sleep(interval)

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(9090)
    logger.info("Metrics server started on port 9090")
    
    # Start metrics collection
    exporter = MetricsExporter()
    exporter.run()
