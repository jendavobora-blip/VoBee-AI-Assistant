"""
Specification Generation Module
Converts extracted intent into detailed functional specifications.
Includes validation framework for ensuring specifications meet constraints.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json


class SpecificationType(Enum):
    """Types of specifications that can be generated"""
    FUNCTIONAL = "functional"
    TECHNICAL = "technical"
    API = "api"
    DATABASE = "database"
    UI_UX = "ui_ux"
    DEPLOYMENT = "deployment"
    SECURITY = "security"


class ConstraintValidator:
    """Validates specifications against predefined constraints"""
    
    def __init__(self):
        self.constraints = {
            'max_complexity': 10,  # Scale of 1-10
            'min_scalability': 5,   # Scale of 1-10
            'required_security_level': 'medium',  # low, medium, high
            'max_services': 20,
            'min_test_coverage': 70,  # percentage
        }
    
    def validate(self, specification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate specification against constraints
        
        Returns:
            Dict with validation results and issues
        """
        validation_result = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'score': 100,
        }
        
        # Check complexity
        complexity = specification.get('metadata', {}).get('complexity', 5)
        if complexity > self.constraints['max_complexity']:
            validation_result['issues'].append(
                f"Complexity {complexity} exceeds maximum {self.constraints['max_complexity']}"
            )
            validation_result['valid'] = False
            validation_result['score'] -= 20
        
        # Check service count for microservices architecture
        if specification.get('architecture', {}).get('type') == 'microservices':
            service_count = len(specification.get('components', {}).get('services', []))
            if service_count > self.constraints['max_services']:
                validation_result['warnings'].append(
                    f"Service count {service_count} is high, consider consolidation"
                )
                validation_result['score'] -= 10
        
        # Check security requirements
        security_level = specification.get('security', {}).get('level', 'medium')
        if self._compare_security_level(security_level, self.constraints['required_security_level']) < 0:
            validation_result['issues'].append(
                f"Security level '{security_level}' below required '{self.constraints['required_security_level']}'"
            )
            validation_result['valid'] = False
            validation_result['score'] -= 30
        
        return validation_result
    
    def _compare_security_level(self, level1: str, level2: str) -> int:
        """Compare security levels (-1: less, 0: equal, 1: greater)"""
        levels = ['low', 'medium', 'high', 'critical']
        idx1 = levels.index(level1.lower()) if level1.lower() in levels else 1
        idx2 = levels.index(level2.lower()) if level2.lower() in levels else 1
        return idx1 - idx2


class SpecificationTemplate:
    """Base template for generating specifications"""
    
    @staticmethod
    def get_base_template() -> Dict[str, Any]:
        """Returns base specification template"""
        return {
            'metadata': {
                'version': '1.0',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'status': 'draft',
                'complexity': 5,
            },
            'intent': {},
            'requirements': {
                'functional': [],
                'non_functional': [],
            },
            'architecture': {
                'type': 'monolith',
                'style': 'layered',
            },
            'components': {
                'services': [],
                'databases': [],
                'external_apis': [],
            },
            'technology_stack': {
                'backend': [],
                'frontend': [],
                'database': [],
                'infrastructure': [],
            },
            'security': {
                'level': 'medium',
                'authentication': [],
                'authorization': [],
                'data_protection': [],
            },
            'deployment': {
                'target': 'cloud',
                'strategy': 'rolling',
                'scaling': 'horizontal',
            },
            'testing': {
                'required_coverage': 80,
                'types': ['unit', 'integration'],
            },
            'documentation': {
                'required': True,
                'formats': ['api_docs', 'readme', 'architecture_docs'],
            },
        }


class SpecificationGenerator:
    """
    Main specification generator.
    Converts intent into detailed functional and technical specifications.
    """
    
    def __init__(self):
        self.validator = ConstraintValidator()
        self.template = SpecificationTemplate()
    
    def generate_specification(
        self, 
        intent: Dict[str, Any],
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate specification from extracted intent
        
        Args:
            intent: Extracted intent from IntentExtractor
            preferences: Optional user preferences for spec generation
            
        Returns:
            Complete specification with validation results
        """
        preferences = preferences or {}
        
        # Start with base template
        spec = self.template.get_base_template()
        
        # Populate from intent
        spec['intent'] = intent
        spec['metadata']['intent_type'] = intent.get('intent_type', 'unknown')
        
        # Generate specification based on intent type
        intent_type = intent.get('intent_type')
        
        if intent_type == 'create_application':
            spec = self._generate_application_spec(intent, spec, preferences)
        elif intent_type == 'add_feature':
            spec = self._generate_feature_spec(intent, spec, preferences)
        elif intent_type == 'generate_component':
            spec = self._generate_component_spec(intent, spec, preferences)
        else:
            spec = self._generate_generic_spec(intent, spec, preferences)
        
        # Validate specification
        validation_result = self.validator.validate(spec)
        spec['validation'] = validation_result
        
        return spec
    
    def _generate_application_spec(
        self,
        intent: Dict[str, Any],
        spec: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate specification for new application"""
        
        # Extract application details from intent
        entities = intent.get('entities', {})
        technologies = intent.get('technologies', [])
        
        # Determine application type
        app_types = entities.get('app_types', [])
        if 'web' in app_types or 'frontend' in technologies:
            spec['architecture']['type'] = 'web_application'
            spec['components']['services'].append({
                'name': 'frontend',
                'type': 'web_ui',
                'framework': 'react',  # Default, can be customized
            })
        
        if 'api' in app_types or 'backend' in technologies:
            spec['components']['services'].append({
                'name': 'backend',
                'type': 'rest_api',
                'framework': 'fastapi',  # Default
            })
        
        # Set technology stack based on detected technologies
        if 'python' in technologies:
            spec['technology_stack']['backend'].append('python')
            spec['technology_stack']['backend'].append('fastapi')
        
        if 'javascript' in technologies or 'react' in technologies:
            spec['technology_stack']['frontend'].append('javascript')
            spec['technology_stack']['frontend'].append('react')
        
        if 'docker' in technologies:
            spec['technology_stack']['infrastructure'].append('docker')
        
        if 'kubernetes' in technologies:
            spec['technology_stack']['infrastructure'].append('kubernetes')
            spec['deployment']['target'] = 'kubernetes'
        
        # Add default functional requirements
        spec['requirements']['functional'] = [
            'User authentication and authorization',
            'Data persistence and retrieval',
            'Error handling and logging',
            'API endpoints for core functionality',
        ]
        
        # Add non-functional requirements
        spec['requirements']['non_functional'] = [
            'Response time < 200ms for 95% of requests',
            'Support for 1000 concurrent users',
            'Minimum 99.9% uptime SLA',
            'Automated backup and recovery',
        ]
        
        # Set appropriate complexity
        num_services = len(spec['components']['services'])
        spec['metadata']['complexity'] = min(10, 3 + num_services)
        
        return spec
    
    def _generate_feature_spec(
        self,
        intent: Dict[str, Any],
        spec: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate specification for adding a feature"""
        
        # Simplify spec for feature addition
        spec['architecture']['type'] = 'feature_addition'
        
        # Add feature-specific requirements
        spec['requirements']['functional'] = [
            'Integrate with existing application architecture',
            'Maintain backward compatibility',
            'Add necessary API endpoints or UI components',
            'Update documentation',
        ]
        
        spec['requirements']['non_functional'] = [
            'No degradation in existing performance',
            'Minimal impact on deployment process',
            'Maintain existing test coverage',
        ]
        
        spec['metadata']['complexity'] = 3
        
        return spec
    
    def _generate_component_spec(
        self,
        intent: Dict[str, Any],
        spec: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate specification for a single component"""
        
        spec['architecture']['type'] = 'component'
        
        # Component-specific spec
        spec['components']['services'] = [
            {
                'name': 'new_component',
                'type': 'service',
                'responsibilities': [],
                'interfaces': {
                    'input': [],
                    'output': [],
                },
                'dependencies': [],
            }
        ]
        
        spec['requirements']['functional'] = [
            'Well-defined interface contracts',
            'Proper error handling',
            'Logging and monitoring',
        ]
        
        spec['metadata']['complexity'] = 2
        
        return spec
    
    def _generate_generic_spec(
        self,
        intent: Dict[str, Any],
        spec: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate generic specification for unrecognized intents"""
        
        spec['metadata']['complexity'] = 5
        spec['requirements']['functional'] = [
            'Define clear objectives and requirements',
            'Identify stakeholders and users',
            'Specify acceptance criteria',
        ]
        
        return spec
    
    def validate_specification(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an existing specification"""
        return self.validator.validate(spec)
    
    def update_specification(
        self,
        spec: Dict[str, Any],
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing specification with new information
        
        Args:
            spec: Existing specification
            updates: Dictionary of updates to apply
            
        Returns:
            Updated specification
        """
        # Deep merge updates into spec
        spec = self._deep_merge(spec, updates)
        spec['metadata']['updated_at'] = datetime.utcnow().isoformat()
        
        # Re-validate
        validation_result = self.validator.validate(spec)
        spec['validation'] = validation_result
        
        return spec
    
    def _deep_merge(self, base: Dict, updates: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
