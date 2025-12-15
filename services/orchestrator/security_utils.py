"""
Security utilities for L20 orchestration system
Provides input validation, sanitization, and security best practices
"""

import re
import logging
from typing import Any, Dict, List, Optional
from functools import wraps
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)

class SecurityValidator:
    """Security validation and sanitization utilities"""
    
    # Maximum allowed sizes
    MAX_STRING_LENGTH = 10000
    MAX_LIST_SIZE = 1000
    MAX_DICT_SIZE = 1000
    MAX_TASK_COUNT = 10000
    
    # Allowed patterns
    # Note: This list must be kept in sync with intelligences defined in orchestrator
    # TODO: Consider dynamically loading this from orchestrator configuration
    ALLOWED_INTELLIGENCE_TYPES = [
        'product_content',
        'marketing',
        'web_app_builder',
        'advanced_media'
    ]
    
    ALLOWED_TASK_TYPES = [
        'image_generation',
        'video_generation',
        'crypto_prediction',
        'fraud_detection',
        'data_processing',
        'image_processing',
        'text_processing',
        'api_calls',
        'validation',
        'ml_inference'
    ]
    
    ALLOWED_PRIORITIES = ['critical', 'high', 'normal', 'low', 'background']
    
    @staticmethod
    def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input
        
        Args:
            value: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Limit length
        max_len = max_length or SecurityValidator.MAX_STRING_LENGTH
        if len(value) > max_len:
            logger.warning(f"String truncated from {len(value)} to {max_len} characters")
            value = value[:max_len]
        
        return value.strip()
    
    @staticmethod
    def validate_intelligence_type(intelligence_type: str) -> bool:
        """Validate intelligence type"""
        sanitized = SecurityValidator.sanitize_string(intelligence_type, 50)
        return sanitized in SecurityValidator.ALLOWED_INTELLIGENCE_TYPES
    
    @staticmethod
    def validate_task_type(task_type: str) -> bool:
        """Validate task type"""
        sanitized = SecurityValidator.sanitize_string(task_type, 50)
        return sanitized in SecurityValidator.ALLOWED_TASK_TYPES
    
    @staticmethod
    def validate_priority(priority: str) -> bool:
        """Validate priority level"""
        sanitized = SecurityValidator.sanitize_string(priority, 20).lower()
        return sanitized in SecurityValidator.ALLOWED_PRIORITIES
    
    @staticmethod
    def validate_list_size(items: List[Any], max_size: Optional[int] = None) -> bool:
        """Validate list size"""
        max_sz = max_size or SecurityValidator.MAX_LIST_SIZE
        if len(items) > max_sz:
            raise ValueError(f"List size {len(items)} exceeds maximum {max_sz}")
        return True
    
    @staticmethod
    def validate_dict_size(data: Dict[str, Any], max_size: Optional[int] = None) -> bool:
        """Validate dictionary size"""
        max_sz = max_size or SecurityValidator.MAX_DICT_SIZE
        if len(data) > max_sz:
            raise ValueError(f"Dictionary size {len(data)} exceeds maximum {max_sz}")
        return True
    
    @staticmethod
    def sanitize_task(task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize task data
        
        Args:
            task: Task dictionary to sanitize
            
        Returns:
            Sanitized task dictionary
        """
        sanitized = {}
        
        # Validate task structure
        if 'type' in task:
            task_type = SecurityValidator.sanitize_string(task['type'], 50)
            if not SecurityValidator.validate_task_type(task_type):
                raise ValueError(f"Invalid task type: {task_type}")
            sanitized['type'] = task_type
        
        # Sanitize priority
        if 'priority' in task:
            priority = SecurityValidator.sanitize_string(task['priority'], 20).lower()
            if not SecurityValidator.validate_priority(priority):
                logger.warning(f"Invalid priority '{priority}', defaulting to 'normal'")
                priority = 'normal'
            sanitized['priority'] = priority
        
        # Sanitize data field
        if 'data' in task:
            if isinstance(task['data'], dict):
                SecurityValidator.validate_dict_size(task['data'], 100)
                sanitized['data'] = task['data']
            else:
                sanitized['data'] = {}
        
        # Sanitize params field
        if 'params' in task:
            if isinstance(task['params'], dict):
                SecurityValidator.validate_dict_size(task['params'], 100)
                sanitized['params'] = task['params']
            else:
                sanitized['params'] = {}
        
        # Copy safe fields
        safe_fields = ['id', 'task_id', 'estimated_duration', 'cpu_required', 
                      'memory_required', 'gpu_required', 'requires_gpu']
        for field in safe_fields:
            if field in task:
                sanitized[field] = task[field]
        
        return sanitized
    
    @staticmethod
    def sanitize_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sanitize list of tasks
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            List of sanitized tasks
        """
        if not isinstance(tasks, list):
            raise ValueError("Tasks must be a list")
        
        SecurityValidator.validate_list_size(tasks, SecurityValidator.MAX_TASK_COUNT)
        
        return [SecurityValidator.sanitize_task(task) for task in tasks]
    
    @staticmethod
    def validate_resource_values(resources: Dict[str, Any]) -> bool:
        """
        Validate resource values are within reasonable limits
        
        Args:
            resources: Resource dictionary
            
        Returns:
            True if valid
        """
        if not isinstance(resources, dict):
            raise ValueError("Resources must be a dictionary")
        
        # Validate CPU
        if 'cpu' in resources:
            cpu = resources['cpu']
            if not isinstance(cpu, (int, float)) or cpu < 0 or cpu > 1024:
                raise ValueError(f"Invalid CPU value: {cpu}")
        
        # Validate memory (in MB)
        if 'memory' in resources:
            memory = resources['memory']
            if not isinstance(memory, (int, float)) or memory < 0 or memory > 1024000:
                raise ValueError(f"Invalid memory value: {memory}")
        
        # Validate GPU
        if 'gpu' in resources:
            gpu = resources['gpu']
            if not isinstance(gpu, (int, float)) or gpu < 0 or gpu > 64:
                raise ValueError(f"Invalid GPU value: {gpu}")
        
        return True


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = {}  # {client_id: [timestamp1, timestamp2, ...]}
        self.limits = {
            'default': (100, 60),  # 100 requests per 60 seconds
            'l20_strategize': (10, 60),  # 10 requests per minute
            'l20_coordinate': (20, 60),  # 20 requests per minute
            'swarm_dispatch': (50, 60),  # 50 requests per minute
            'intelligence_execute': (30, 60),  # 30 requests per minute
        }
    
    def check_rate_limit(self, client_id: str, endpoint: str = 'default') -> bool:
        """
        Check if client is within rate limit
        
        Args:
            client_id: Client identifier (IP, API key, etc.)
            endpoint: Endpoint identifier for specific limits
            
        Returns:
            True if within limit, False otherwise
        """
        now = datetime.utcnow()
        limit, window = self.limits.get(endpoint, self.limits['default'])
        
        # Initialize client if not exists
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Clean old requests outside window
        cutoff = now - timedelta(seconds=window)
        self.requests[client_id] = [
            ts for ts in self.requests[client_id] if ts > cutoff
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= limit:
            logger.warning(f"Rate limit exceeded for client {client_id} on {endpoint}")
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining_requests(self, client_id: str, endpoint: str = 'default') -> int:
        """Get remaining requests for client"""
        limit, window = self.limits.get(endpoint, self.limits['default'])
        
        if client_id not in self.requests:
            return limit
        
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=window)
        recent_requests = [ts for ts in self.requests[client_id] if ts > cutoff]
        
        return max(0, limit - len(recent_requests))


def require_rate_limit(endpoint: str = 'default'):
    """
    Decorator to enforce rate limiting on endpoints
    
    Args:
        endpoint: Endpoint identifier for specific limits
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, extract client_id from request
            # For now, use a placeholder
            client_id = "default_client"
            
            rate_limiter = getattr(wrapper, 'rate_limiter', None)
            if rate_limiter is None:
                rate_limiter = RateLimiter()
                wrapper.rate_limiter = rate_limiter
            
            if not rate_limiter.check_rate_limit(client_id, endpoint):
                raise ValueError("Rate limit exceeded. Please try again later.")
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def sanitize_user_input(data: Dict[str, Any], depth: int = 0, max_depth: int = 10) -> Dict[str, Any]:
    """
    Sanitize all user input data with circular reference protection
    
    Args:
        data: Input data dictionary
        depth: Current recursion depth
        max_depth: Maximum allowed recursion depth
        
    Returns:
        Sanitized data dictionary
    """
    if depth >= max_depth:
        logger.warning(f"Maximum recursion depth {max_depth} reached during sanitization")
        return {}
    
    sanitized = {}
    
    for key, value in data.items():
        # Sanitize key
        safe_key = SecurityValidator.sanitize_string(str(key), 100)
        
        # Sanitize value based on type
        if isinstance(value, str):
            sanitized[safe_key] = SecurityValidator.sanitize_string(value)
        elif isinstance(value, (int, float, bool)):
            sanitized[safe_key] = value
        elif isinstance(value, list):
            SecurityValidator.validate_list_size(value)
            sanitized[safe_key] = [
                sanitize_user_input(item, depth + 1, max_depth) if isinstance(item, dict) else item
                for item in value
            ]
        elif isinstance(value, dict):
            SecurityValidator.validate_dict_size(value)
            sanitized[safe_key] = sanitize_user_input(value, depth + 1, max_depth)
        elif value is None:
            sanitized[safe_key] = None
        else:
            # Convert unknown types to string and sanitize
            sanitized[safe_key] = SecurityValidator.sanitize_string(str(value))
    
    return sanitized


def generate_secure_id(prefix: str = "") -> str:
    """
    Generate a secure unique identifier
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        Secure unique identifier
    """
    timestamp = datetime.utcnow().isoformat()
    random_data = f"{timestamp}{id(object())}"
    hash_obj = hashlib.sha256(random_data.encode())
    hash_value = hash_obj.hexdigest()[:16]
    
    if prefix:
        return f"{prefix}_{hash_value}"
    return hash_value


# Global rate limiter instance
rate_limiter = RateLimiter()
