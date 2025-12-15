"""
L20 Supreme Brain Orchestration System
Provides mega-scale orchestration for cross-domain AI coordination
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import json

logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    """Task priority levels for intelligent scheduling"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5

class IntelligenceType(Enum):
    """Types of Master Intelligences (L18 subsystems)"""
    PRODUCT_CONTENT = "product_content_generation"
    MARKETING = "cross_industry_marketing"
    WEB_APP_BUILDER = "autonomous_web_app_builder"
    ADVANCED_MEDIA = "advanced_media_generation"
    CRYPTO_ANALYTICS = "crypto_analytics"
    FRAUD_PREVENTION = "fraud_prevention"

class SupremeBrain:
    """
    L20 Supreme Brain - Highest level orchestration intelligence
    Handles project-wide strategizing, task prioritization, and cross-domain coordination
    """
    
    def __init__(self, orchestrator):
        """
        Initialize Supreme Brain with reference to base orchestrator
        
        Args:
            orchestrator: Base TaskOrchestrator instance
        """
        self.orchestrator = orchestrator
        self.active_strategies = {}
        self.intelligence_modules = {}
        self.task_history = []
        self.performance_metrics = {
            'tasks_completed': 0,
            'total_execution_time': 0,
            'success_rate': 0.0,
            'active_intelligences': 0
        }
        
        logger.info("L20 Supreme Brain initialized")
    
    def strategize(self, objective: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        High-level strategic planning for complex objectives
        
        Args:
            objective: Primary objective to achieve
            constraints: Resource and operational constraints
            
        Returns:
            Strategic plan with task breakdown and priorities
        """
        logger.info(f"Strategizing for objective: {objective}")
        
        strategy = {
            'strategy_id': self._generate_id(),
            'objective': objective,
            'constraints': constraints,
            'created_at': datetime.utcnow().isoformat(),
            'phases': [],
            'estimated_complexity': self._estimate_complexity(objective),
            'recommended_intelligences': []
        }
        
        # Analyze objective and decompose into phases
        phases = self._decompose_objective(objective, constraints)
        strategy['phases'] = phases
        
        # Determine which intelligences to engage
        intelligences = self._select_intelligences(objective, phases)
        strategy['recommended_intelligences'] = intelligences
        
        # Store strategy
        self.active_strategies[strategy['strategy_id']] = strategy
        
        return strategy
    
    def prioritize_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Intelligent task prioritization using multi-factor analysis
        
        Args:
            tasks: List of tasks to prioritize
            
        Returns:
            Prioritized task list
        """
        logger.info(f"Prioritizing {len(tasks)} tasks")
        
        for task in tasks:
            # Calculate priority score based on multiple factors
            score = self._calculate_priority_score(task)
            task['priority_score'] = score
            task['priority_level'] = self._get_priority_level(score)
        
        # Sort by priority score (higher = more important)
        prioritized = sorted(tasks, key=lambda x: x['priority_score'], reverse=True)
        
        return prioritized
    
    def coordinate_cross_domain(self, domains: List[str], task_specs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate tasks across multiple domains (image, video, crypto, etc.)
        
        Args:
            domains: List of domains to coordinate
            task_specs: Specifications for cross-domain tasks
            
        Returns:
            Coordination plan and execution results
        """
        logger.info(f"Coordinating across domains: {', '.join(domains)}")
        
        coordination_plan = {
            'coordination_id': self._generate_id(),
            'domains': domains,
            'task_specs': task_specs,
            'execution_order': [],
            'dependencies': {},
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Analyze dependencies between domains
        dependencies = self._analyze_dependencies(domains, task_specs)
        coordination_plan['dependencies'] = dependencies
        
        # Determine optimal execution order
        execution_order = self._optimize_execution_order(domains, dependencies)
        coordination_plan['execution_order'] = execution_order
        
        # Execute coordinated tasks
        results = []
        for domain in execution_order:
            if domain in task_specs:
                result = self._execute_domain_task(domain, task_specs[domain])
                results.append(result)
        
        coordination_plan['results'] = results
        coordination_plan['status'] = 'completed'
        
        return coordination_plan
    
    def optimize_resource_allocation(self, available_resources: Dict[str, Any], 
                                    pending_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Optimize allocation of resources across pending tasks
        
        Args:
            available_resources: Available compute, memory, GPU resources
            pending_tasks: Tasks waiting for execution
            
        Returns:
            Optimized resource allocation plan
        """
        logger.info("Optimizing resource allocation")
        
        allocation_plan = {
            'timestamp': datetime.utcnow().isoformat(),
            'available_resources': available_resources,
            'task_count': len(pending_tasks),
            'allocations': []
        }
        
        # Sort tasks by priority
        prioritized_tasks = self.prioritize_tasks(pending_tasks)
        
        # Allocate resources based on task requirements and priority
        for task in prioritized_tasks:
            allocation = self._allocate_resources(task, available_resources)
            if allocation:
                allocation_plan['allocations'].append(allocation)
                # Update available resources
                available_resources = self._update_available_resources(
                    available_resources, allocation
                )
        
        return allocation_plan
    
    def _generate_id(self) -> str:
        """Generate unique identifier"""
        from uuid import uuid4
        return f"l20_{str(uuid4())[:8]}"
    
    def _estimate_complexity(self, objective: str) -> str:
        """Estimate complexity level of objective"""
        # Simple heuristic based on keywords and length
        complexity_keywords = ['multiple', 'complex', 'advanced', 'scale', 'optimize']
        keyword_count = sum(1 for kw in complexity_keywords if kw in objective.lower())
        
        if keyword_count >= 3 or len(objective) > 200:
            return 'very_high'
        elif keyword_count >= 2 or len(objective) > 100:
            return 'high'
        elif keyword_count >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _decompose_objective(self, objective: str, constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose objective into executable phases"""
        phases = []
        
        # Analyze objective for different task types
        keywords_map = {
            'image': 'image_generation',
            'video': 'video_generation',
            'predict': 'crypto_prediction',
            'analyze': 'fraud_detection',
            'marketing': 'marketing_intelligence',
            'content': 'content_generation',
            'build': 'web_app_builder'
        }
        
        for keyword, task_type in keywords_map.items():
            if keyword in objective.lower():
                phases.append({
                    'phase_id': self._generate_id(),
                    'type': task_type,
                    'description': f"{task_type} phase for {objective[:50]}",
                    'estimated_duration': self._estimate_duration(task_type),
                    'dependencies': []
                })
        
        # If no specific keywords found, create general planning phase
        if not phases:
            phases.append({
                'phase_id': self._generate_id(),
                'type': 'general_orchestration',
                'description': objective,
                'estimated_duration': 60,
                'dependencies': []
            })
        
        return phases
    
    def _select_intelligences(self, objective: str, phases: List[Dict[str, Any]]) -> List[str]:
        """Select appropriate Master Intelligences for the objective"""
        intelligences = set()
        
        intelligence_keywords = {
            IntelligenceType.PRODUCT_CONTENT.value: ['product', 'content', 'description', 'catalog'],
            IntelligenceType.MARKETING.value: ['marketing', 'campaign', 'promotion', 'advertising'],
            IntelligenceType.WEB_APP_BUILDER.value: ['build', 'app', 'website', 'web', 'interface'],
            IntelligenceType.ADVANCED_MEDIA.value: ['image', 'video', '8k', '4k', 'media', 'render'],
            IntelligenceType.CRYPTO_ANALYTICS.value: ['crypto', 'bitcoin', 'predict', 'trading'],
            IntelligenceType.FRAUD_PREVENTION.value: ['fraud', 'security', 'detect', 'anomaly']
        }
        
        objective_lower = objective.lower()
        for intelligence_type, keywords in intelligence_keywords.items():
            if any(kw in objective_lower for kw in keywords):
                intelligences.add(intelligence_type)
        
        # Also check phases
        for phase in phases:
            phase_type = phase.get('type', '')
            if 'image' in phase_type or 'video' in phase_type:
                intelligences.add(IntelligenceType.ADVANCED_MEDIA.value)
            elif 'crypto' in phase_type:
                intelligences.add(IntelligenceType.CRYPTO_ANALYTICS.value)
            elif 'marketing' in phase_type:
                intelligences.add(IntelligenceType.MARKETING.value)
        
        return list(intelligences)
    
    def _calculate_priority_score(self, task: Dict[str, Any]) -> float:
        """Calculate priority score for a task"""
        score = 50.0  # Base score
        
        # Factor 1: Explicit priority level
        priority_map = {
            'critical': 100,
            'high': 75,
            'normal': 50,
            'low': 25,
            'background': 10
        }
        explicit_priority = task.get('priority', 'normal')
        score = priority_map.get(explicit_priority, 50)
        
        # Factor 2: Resource requirements (higher requirements = higher priority for batch processing)
        if task.get('requires_gpu', False):
            score += 15
        
        # Factor 3: Estimated duration (balance between quick wins and important long tasks)
        duration = task.get('estimated_duration', 60)
        if duration < 30:
            score += 10  # Quick tasks get boost
        
        # Factor 4: Dependencies (tasks with dependents get higher priority)
        dependents = task.get('dependents', [])
        score += len(dependents) * 5
        
        return score
    
    def _get_priority_level(self, score: float) -> str:
        """Convert numeric score to priority level"""
        if score >= 90:
            return TaskPriority.CRITICAL.name
        elif score >= 70:
            return TaskPriority.HIGH.name
        elif score >= 40:
            return TaskPriority.NORMAL.name
        elif score >= 20:
            return TaskPriority.LOW.name
        else:
            return TaskPriority.BACKGROUND.name
    
    def _analyze_dependencies(self, domains: List[str], task_specs: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analyze dependencies between domain tasks"""
        dependencies = {domain: [] for domain in domains}
        
        # Simple dependency analysis based on task types
        # Video generation might depend on image generation
        if 'video_generation' in domains and 'image_generation' in domains:
            if task_specs.get('video_generation', {}).get('use_generated_images', False):
                dependencies['video_generation'].append('image_generation')
        
        # Marketing might depend on content generation
        if 'marketing' in domains and 'content_generation' in domains:
            dependencies['marketing'].append('content_generation')
        
        return dependencies
    
    def _optimize_execution_order(self, domains: List[str], dependencies: Dict[str, List[str]]) -> List[str]:
        """Determine optimal execution order based on dependencies"""
        executed = set()
        order = []
        
        # Simple topological sort
        while len(order) < len(domains):
            for domain in domains:
                if domain not in executed:
                    # Check if all dependencies are satisfied
                    deps = dependencies.get(domain, [])
                    if all(dep in executed for dep in deps):
                        order.append(domain)
                        executed.add(domain)
        
        return order
    
    def _execute_domain_task(self, domain: str, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task for a specific domain"""
        logger.info(f"Executing {domain} task")
        
        # Map domain to orchestrator service
        domain_mapping = {
            'image_generation': 'image_generation',
            'video_generation': 'video_generation',
            'crypto_prediction': 'crypto_prediction',
            'fraud_detection': 'fraud_detection'
        }
        
        try:
            service_type = domain_mapping.get(domain)
            if service_type == 'image_generation':
                result = self.orchestrator.execute_image_generation(task_spec)
            elif service_type == 'video_generation':
                result = self.orchestrator.execute_video_generation(task_spec)
            elif service_type == 'crypto_prediction':
                result = self.orchestrator.execute_crypto_prediction(task_spec)
            elif service_type == 'fraud_detection':
                result = self.orchestrator.execute_fraud_detection(task_spec)
            else:
                result = {'status': 'skipped', 'reason': 'Domain not mapped to service'}
            
            return {
                'domain': domain,
                'status': 'completed',
                'result': result
            }
        except Exception as e:
            logger.error(f"Error executing {domain} task: {e}")
            return {
                'domain': domain,
                'status': 'failed',
                'error': str(e)
            }
    
    def _estimate_duration(self, task_type: str) -> int:
        """Estimate task duration in seconds"""
        duration_map = {
            'image_generation': 120,
            'video_generation': 300,
            'crypto_prediction': 30,
            'fraud_detection': 15,
            'marketing_intelligence': 60,
            'content_generation': 45,
            'web_app_builder': 180
        }
        return duration_map.get(task_type, 60)
    
    def _allocate_resources(self, task: Dict[str, Any], available: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Allocate resources for a task"""
        required_cpu = task.get('cpu_required', 1)
        required_memory = task.get('memory_required', 1024)  # MB
        required_gpu = task.get('gpu_required', 0)
        
        available_cpu = available.get('cpu', 0)
        available_memory = available.get('memory', 0)
        available_gpu = available.get('gpu', 0)
        
        # Check if resources are available
        if (available_cpu >= required_cpu and 
            available_memory >= required_memory and
            available_gpu >= required_gpu):
            
            return {
                'task_id': task.get('id', 'unknown'),
                'allocated_cpu': required_cpu,
                'allocated_memory': required_memory,
                'allocated_gpu': required_gpu,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        return None
    
    def _update_available_resources(self, available: Dict[str, Any], 
                                   allocation: Dict[str, Any]) -> Dict[str, Any]:
        """Update available resources after allocation"""
        return {
            'cpu': available.get('cpu', 0) - allocation.get('allocated_cpu', 0),
            'memory': available.get('memory', 0) - allocation.get('allocated_memory', 0),
            'gpu': available.get('gpu', 0) - allocation.get('allocated_gpu', 0)
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get Supreme Brain performance metrics"""
        return {
            'performance_metrics': self.performance_metrics,
            'active_strategies': len(self.active_strategies),
            'active_intelligences': len(self.intelligence_modules),
            'task_history_size': len(self.task_history),
            'timestamp': datetime.utcnow().isoformat()
        }
