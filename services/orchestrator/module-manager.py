"""
Module Manager
Part of the VoBee AI Orchestration System

Enable/disable modules, health monitoring, version management, dependency tracking.

⚠️ DOES NOT MODIFY EXISTING main.py - This is a NEW extension module
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModuleManager:
    """
    Module manager for controlling AI service modules
    """
    
    def __init__(self):
        self.modules = {}
        self.health_status = {}
        self.dependencies = {}
        self.version_info = {}
        logger.info("Module Manager initialized")
        
        # Register default modules
        self._register_default_modules()
    
    def _register_default_modules(self):
        """Register all available AI modules"""
        modules_config = [
            # Business & Marketing
            {'name': 'email-ai', 'category': 'business', 'port': 5100, 'dependencies': []},
            {'name': 'facebook-ai', 'category': 'business', 'port': 5101, 'dependencies': []},
            {'name': 'marketing-ai', 'category': 'business', 'port': 5102, 'dependencies': []},
            {'name': 'seo-ai', 'category': 'business', 'port': 5103, 'dependencies': []},
            {'name': 'content-ai', 'category': 'business', 'port': 5104, 'dependencies': []},
            {'name': 'analytics-ai', 'category': 'business', 'port': 5105, 'dependencies': []},
            
            # Finance
            {'name': 'finance-ai', 'category': 'finance', 'port': 5110, 'dependencies': [], 'read_only': True},
            {'name': 'invoice-ai', 'category': 'finance', 'port': 5111, 'dependencies': []},
            {'name': 'budget-ai', 'category': 'finance', 'port': 5112, 'dependencies': []},
            {'name': 'tax-ai', 'category': 'finance', 'port': 5113, 'dependencies': []},
            {'name': 'cashflow-ai', 'category': 'finance', 'port': 5114, 'dependencies': []},
            
            # Research & Data
            {'name': 'research-ai', 'category': 'research', 'port': 5120, 'dependencies': []},
            {'name': 'web-scraper-ai', 'category': 'research', 'port': 5121, 'dependencies': []},
            {'name': 'data-mining-ai', 'category': 'research', 'port': 5122, 'dependencies': []},
            {'name': 'sentiment-ai', 'category': 'research', 'port': 5123, 'dependencies': []},
            {'name': 'trend-ai', 'category': 'research', 'port': 5124, 'dependencies': []},
            
            # Communication
            {'name': 'email-response-ai', 'category': 'communication', 'port': 5130, 'dependencies': []},
            {'name': 'chat-support-ai', 'category': 'communication', 'port': 5131, 'dependencies': []},
            {'name': 'translation-ai', 'category': 'communication', 'port': 5132, 'dependencies': []},
            {'name': 'voice-ai', 'category': 'communication', 'port': 5133, 'dependencies': []},
            {'name': 'meeting-ai', 'category': 'communication', 'port': 5134, 'dependencies': []},
            
            # Creative
            {'name': 'music-ai', 'category': 'creative', 'port': 5140, 'dependencies': []},
            {'name': 'design-ai', 'category': 'creative', 'port': 5141, 'dependencies': []},
            {'name': 'animation-ai', 'category': 'creative', 'port': 5142, 'dependencies': []},
            {'name': 'presentation-ai', 'category': 'creative', 'port': 5143, 'dependencies': []},
            {'name': 'podcast-ai', 'category': 'creative', 'port': 5144, 'dependencies': []},
            
            # Technical
            {'name': 'code-review-ai', 'category': 'technical', 'port': 5150, 'dependencies': []},
            {'name': 'documentation-ai', 'category': 'technical', 'port': 5151, 'dependencies': []},
            {'name': 'testing-ai', 'category': 'technical', 'port': 5152, 'dependencies': []},
            {'name': 'deployment-ai', 'category': 'technical', 'port': 5153, 'dependencies': []},
        ]
        
        for config in modules_config:
            self.register_module(
                name=config['name'],
                category=config['category'],
                port=config['port'],
                dependencies=config['dependencies'],
                read_only=config.get('read_only', False)
            )
    
    def register_module(self, name: str, category: str, port: int, 
                       dependencies: List[str] = None, read_only: bool = False):
        """Register a new module"""
        self.modules[name] = {
            'name': name,
            'category': category,
            'port': port,
            'endpoint': f'http://{name}:{port}',
            'enabled': True,  # Enabled by default
            'read_only': read_only,
            'registered_at': datetime.utcnow().isoformat()
        }
        
        self.health_status[name] = {
            'status': 'unknown',
            'last_check': None
        }
        
        self.dependencies[name] = dependencies or []
        
        self.version_info[name] = {
            'version': '1.0.0',
            'last_updated': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Registered module: {name} ({category})")
    
    def enable_module(self, module_name: str) -> Dict[str, Any]:
        """Enable a module"""
        if module_name not in self.modules:
            return {'error': f'Module {module_name} not found'}
        
        # Check dependencies
        deps = self.dependencies.get(module_name, [])
        for dep in deps:
            if not self.modules.get(dep, {}).get('enabled', False):
                return {
                    'error': f'Cannot enable {module_name}: dependency {dep} is disabled'
                }
        
        self.modules[module_name]['enabled'] = True
        logger.info(f"Enabled module: {module_name}")
        
        return {
            'success': True,
            'module': module_name,
            'status': 'enabled'
        }
    
    def disable_module(self, module_name: str) -> Dict[str, Any]:
        """Disable a module"""
        if module_name not in self.modules:
            return {'error': f'Module {module_name} not found'}
        
        # Check if other modules depend on this one
        dependents = [
            name for name, deps in self.dependencies.items()
            if module_name in deps and self.modules.get(name, {}).get('enabled', False)
        ]
        
        if dependents:
            return {
                'error': f'Cannot disable {module_name}: required by {", ".join(dependents)}',
                'dependents': dependents
            }
        
        self.modules[module_name]['enabled'] = False
        logger.info(f"Disabled module: {module_name}")
        
        return {
            'success': True,
            'module': module_name,
            'status': 'disabled'
        }
    
    def update_health_status(self, module_name: str, status: str, details: Dict[str, Any] = None):
        """Update module health status"""
        if module_name not in self.health_status:
            self.health_status[module_name] = {}
        
        self.health_status[module_name] = {
            'status': status,
            'last_check': datetime.utcnow().isoformat(),
            'details': details or {}
        }
    
    def get_module_status(self, module_name: str) -> Dict[str, Any]:
        """Get status of a specific module"""
        if module_name not in self.modules:
            return {'error': f'Module {module_name} not found'}
        
        module = self.modules[module_name]
        health = self.health_status.get(module_name, {})
        version = self.version_info.get(module_name, {})
        deps = self.dependencies.get(module_name, [])
        
        return {
            'name': module_name,
            'enabled': module.get('enabled', False),
            'category': module.get('category'),
            'endpoint': module.get('endpoint'),
            'health': health,
            'version': version.get('version'),
            'dependencies': deps,
            'read_only': module.get('read_only', False)
        }
    
    def get_all_modules(self, category: str = None, enabled_only: bool = False) -> List[Dict[str, Any]]:
        """Get list of all modules"""
        modules_list = []
        
        for name in self.modules:
            module = self.get_module_status(name)
            
            # Filter by category
            if category and module.get('category') != category:
                continue
            
            # Filter by enabled status
            if enabled_only and not module.get('enabled', False):
                continue
            
            modules_list.append(module)
        
        return modules_list
    
    def get_modules_by_category(self) -> Dict[str, List[str]]:
        """Get modules grouped by category"""
        by_category = {}
        
        for name, module in self.modules.items():
            category = module.get('category', 'other')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(name)
        
        return by_category
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get overall health summary"""
        total = len(self.modules)
        enabled = sum(1 for m in self.modules.values() if m.get('enabled', False))
        disabled = total - enabled
        
        health_counts = {
            'healthy': 0,
            'degraded': 0,
            'unhealthy': 0,
            'unknown': 0
        }
        
        for status_info in self.health_status.values():
            status = status_info.get('status', 'unknown')
            health_counts[status] = health_counts.get(status, 0) + 1
        
        return {
            'total_modules': total,
            'enabled': enabled,
            'disabled': disabled,
            'health_status': health_counts,
            'categories': len(set(m.get('category') for m in self.modules.values()))
        }


# Global instance
module_manager = ModuleManager()

if __name__ == '__main__':
    # Test the module manager
    print("Testing Module Manager...")
    
    # Get all modules
    all_modules = module_manager.get_all_modules()
    print(f"\nTotal modules: {len(all_modules)}")
    
    # Get by category
    by_category = module_manager.get_modules_by_category()
    print(f"\nModules by category:")
    for cat, mods in by_category.items():
        print(f"  {cat}: {len(mods)} modules")
    
    # Get health summary
    health = module_manager.get_health_summary()
    print(f"\nHealth summary: {json.dumps(health, indent=2)}")
    
    # Test enable/disable
    result = module_manager.disable_module('email-ai')
    print(f"\nDisable result: {result}")
    
    result = module_manager.enable_module('email-ai')
    print(f"Enable result: {result}")
