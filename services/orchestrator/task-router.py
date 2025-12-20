"""
Task Router - Intelligent Task Routing System
Part of the VoBee AI Orchestration System

Routes tasks to appropriate AI modules with load balancing,
retry logic, and fallback strategies.

⚠️ DOES NOT MODIFY EXISTING main.py - This is a NEW extension module
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskRouter:
    """
    Intelligent task routing system with load balancing and fallback strategies
    """
    
    def __init__(self):
        self.service_endpoints = {}
        self.service_health = {}
        self.routing_history = []
        self.load_balancer = LoadBalancer()
        logger.info("Task Router initialized")
    
    def register_service(self, service_name: str, endpoint: str, capabilities: List[str]):
        """Register a new AI service"""
        self.service_endpoints[service_name] = {
            'endpoint': endpoint,
            'capabilities': capabilities,
            'registered_at': datetime.utcnow().isoformat()
        }
        self.service_health[service_name] = {
            'status': 'healthy',
            'last_check': datetime.utcnow().isoformat()
        }
        logger.info(f"Registered service: {service_name} with {len(capabilities)} capabilities")
    
    def route_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a task to the appropriate service
        
        Args:
            task: Task to route
            
        Returns:
            Routing decision with target service and fallback options
        """
        task_type = task.get('type')
        requirements = task.get('requirements', {})
        
        # Find capable services
        capable_services = self._find_capable_services(task_type)
        
        if not capable_services:
            logger.warning(f"No capable services found for task type: {task_type}")
            return {
                'status': 'no_service_found',
                'task_type': task_type,
                'fallback': 'orchestrator'
            }
        
        # Select best service using load balancer
        primary_service = self.load_balancer.select_service(capable_services, self.service_health)
        
        # Select fallback services
        fallback_services = [s for s in capable_services if s != primary_service][:2]
        
        routing_decision = {
            'task_id': task.get('id', 'unknown'),
            'task_type': task_type,
            'primary_service': primary_service,
            'fallback_services': fallback_services,
            'endpoint': self.service_endpoints[primary_service]['endpoint'],
            'retry_strategy': self._get_retry_strategy(task_type),
            'routed_at': datetime.utcnow().isoformat()
        }
        
        self.routing_history.append(routing_decision)
        logger.info(f"Routed task {task_type} to {primary_service}")
        
        return routing_decision
    
    def _find_capable_services(self, task_type: str) -> List[str]:
        """Find all services capable of handling a task type"""
        capable = []
        
        # Task type to capability mapping
        task_capability_map = {
            'email': ['email_campaign', 'email_automation'],
            'social_media': ['posting', 'engagement_analysis'],
            'finance': ['financial_analysis', 'reporting'],
            'content': ['content_generation', 'writing'],
            'analytics': ['data_analysis', 'insights'],
        }
        
        required_capabilities = task_capability_map.get(task_type, [task_type])
        
        for service_name, service_info in self.service_endpoints.items():
            service_capabilities = service_info.get('capabilities', [])
            
            # Check if service has any required capability
            if any(cap in service_capabilities for cap in required_capabilities):
                # Only include healthy services
                if self.service_health.get(service_name, {}).get('status') == 'healthy':
                    capable.append(service_name)
        
        return capable
    
    def _get_retry_strategy(self, task_type: str) -> Dict[str, Any]:
        """Get retry strategy for task type"""
        strategies = {
            'email': {'max_retries': 3, 'backoff': 'exponential', 'timeout': 30},
            'finance': {'max_retries': 2, 'backoff': 'linear', 'timeout': 60},
            'content': {'max_retries': 3, 'backoff': 'exponential', 'timeout': 120},
            'default': {'max_retries': 3, 'backoff': 'exponential', 'timeout': 60}
        }
        
        return strategies.get(task_type, strategies['default'])
    
    def handle_failure(self, routing_decision: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Handle task routing failure with fallback strategy
        
        Args:
            routing_decision: Original routing decision that failed
            
        Returns:
            New routing decision with fallback service, or None if no fallback available
        """
        fallback_services = routing_decision.get('fallback_services', [])
        
        if not fallback_services:
            logger.error(f"No fallback services available for task {routing_decision.get('task_id')}")
            return None
        
        # Use first fallback service
        fallback_service = fallback_services[0]
        remaining_fallbacks = fallback_services[1:]
        
        fallback_decision = {
            'task_id': routing_decision.get('task_id'),
            'task_type': routing_decision.get('task_type'),
            'primary_service': fallback_service,
            'fallback_services': remaining_fallbacks,
            'endpoint': self.service_endpoints[fallback_service]['endpoint'],
            'retry_strategy': routing_decision.get('retry_strategy'),
            'is_fallback': True,
            'original_service': routing_decision.get('primary_service'),
            'routed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Falling back to {fallback_service} for task {routing_decision.get('task_id')}")
        
        return fallback_decision
    
    def update_service_health(self, service_name: str, health_status: str):
        """Update health status of a service"""
        if service_name in self.service_health:
            self.service_health[service_name] = {
                'status': health_status,
                'last_check': datetime.utcnow().isoformat()
            }
            logger.info(f"Updated health status for {service_name}: {health_status}")
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics"""
        total_routes = len(self.routing_history)
        service_counts = {}
        
        for route in self.routing_history:
            service = route.get('primary_service')
            service_counts[service] = service_counts.get(service, 0) + 1
        
        return {
            'total_routes': total_routes,
            'service_distribution': service_counts,
            'registered_services': len(self.service_endpoints),
            'healthy_services': sum(1 for h in self.service_health.values() if h.get('status') == 'healthy')
        }


class LoadBalancer:
    """Load balancer for distributing tasks across services"""
    
    def __init__(self, strategy: str = 'round_robin'):
        self.strategy = strategy
        self.current_index = {}
        logger.info(f"Load Balancer initialized with strategy: {strategy}")
    
    def select_service(self, services: List[str], health_status: Dict[str, Any]) -> str:
        """Select a service based on load balancing strategy"""
        if not services:
            raise ValueError("No services available for load balancing")
        
        # Filter healthy services
        healthy_services = [s for s in services if health_status.get(s, {}).get('status') == 'healthy']
        
        if not healthy_services:
            logger.warning("No healthy services available, using any available service")
            healthy_services = services
        
        if self.strategy == 'round_robin':
            return self._round_robin(healthy_services)
        elif self.strategy == 'random':
            return random.choice(healthy_services)
        elif self.strategy == 'least_loaded':
            return self._least_loaded(healthy_services)
        else:
            return healthy_services[0]
    
    def _round_robin(self, services: List[str]) -> str:
        """Round-robin load balancing"""
        services_key = ','.join(sorted(services))
        
        if services_key not in self.current_index:
            self.current_index[services_key] = 0
        
        index = self.current_index[services_key]
        selected = services[index % len(services)]
        
        self.current_index[services_key] = (index + 1) % len(services)
        
        return selected
    
    def _least_loaded(self, services: List[str]) -> str:
        """Select least loaded service (placeholder - would need actual load metrics)"""
        # For now, just return first service
        # In production, would check actual service load
        return services[0]


# Global instance
task_router = TaskRouter()

# Register default services
task_router.register_service('email-ai', 'http://email-ai:5000', ['email_campaign', 'email_automation'])
task_router.register_service('facebook-ai', 'http://facebook-ai:5000', ['posting', 'engagement_analysis'])
task_router.register_service('finance-ai', 'http://finance-ai:5000', ['financial_analysis', 'reporting'])
task_router.register_service('content-ai', 'http://content-ai:5000', ['content_generation', 'writing'])

if __name__ == '__main__':
    # Test the task router
    print("Testing Task Router...")
    
    test_task = {
        'id': 'task_123',
        'type': 'email',
        'requirements': {}
    }
    
    decision = task_router.route_task(test_task)
    print(f"\nRouting decision: {decision}")
    
    print(f"\nRouting stats: {task_router.get_routing_stats()}")
