"""
Architecture Scaffolding Module
Generates high-level project architecture and structure templates.
Includes interfaces for different architecture patterns and tech stacks.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json


class ArchitecturePattern(Enum):
    """Supported architecture patterns"""
    MONOLITH = "monolith"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    EVENT_DRIVEN = "event_driven"
    MVC = "mvc"
    CLEAN_ARCHITECTURE = "clean_architecture"


class TechStack(Enum):
    """Predefined technology stacks"""
    PYTHON_FASTAPI = "python_fastapi"
    PYTHON_FLASK = "python_flask"
    NODE_EXPRESS = "node_express"
    JAVA_SPRING = "java_spring"
    DOTNET_CORE = "dotnet_core"
    GO_GIN = "go_gin"
    REACT_SPA = "react_spa"
    VUE_SPA = "vue_spa"


class ArchitectureTemplate:
    """Base architecture templates for different patterns"""
    
    @staticmethod
    def get_monolith_template() -> Dict[str, Any]:
        """Monolithic architecture template"""
        return {
            'pattern': 'monolith',
            'structure': {
                'layers': [
                    {
                        'name': 'presentation',
                        'description': 'UI and API layer',
                        'components': ['controllers', 'routes', 'views'],
                    },
                    {
                        'name': 'business_logic',
                        'description': 'Core business logic and services',
                        'components': ['services', 'domain_models', 'validators'],
                    },
                    {
                        'name': 'data_access',
                        'description': 'Database and external API access',
                        'components': ['repositories', 'models', 'migrations'],
                    },
                ],
            },
            'directories': [
                'src/controllers',
                'src/services',
                'src/models',
                'src/repositories',
                'src/utils',
                'tests/unit',
                'tests/integration',
                'config',
                'docs',
            ],
            'interfaces': {
                'external': ['REST API', 'Web UI'],
                'internal': ['Service Layer', 'Data Layer'],
            },
        }
    
    @staticmethod
    def get_microservices_template() -> Dict[str, Any]:
        """Microservices architecture template"""
        return {
            'pattern': 'microservices',
            'structure': {
                'services': [
                    {
                        'name': 'api_gateway',
                        'type': 'gateway',
                        'description': 'Entry point for all client requests',
                        'responsibilities': ['routing', 'authentication', 'rate_limiting'],
                    },
                    {
                        'name': 'user_service',
                        'type': 'business',
                        'description': 'User management and authentication',
                        'responsibilities': ['user_crud', 'auth', 'profiles'],
                    },
                    {
                        'name': 'data_service',
                        'type': 'business',
                        'description': 'Core data processing',
                        'responsibilities': ['data_processing', 'analytics'],
                    },
                ],
                'infrastructure': [
                    {
                        'name': 'message_broker',
                        'type': 'messaging',
                        'technology': 'rabbitmq',
                    },
                    {
                        'name': 'service_discovery',
                        'type': 'discovery',
                        'technology': 'consul',
                    },
                ],
            },
            'directories': [
                'services/api-gateway',
                'services/user-service',
                'services/data-service',
                'infrastructure/docker',
                'infrastructure/kubernetes',
                'shared/models',
                'shared/utils',
                'docs',
            ],
            'interfaces': {
                'external': ['API Gateway'],
                'inter_service': ['REST', 'gRPC', 'Message Queue'],
            },
            'communication': {
                'sync': ['REST', 'gRPC'],
                'async': ['Message Queue', 'Event Bus'],
            },
        }
    
    @staticmethod
    def get_serverless_template() -> Dict[str, Any]:
        """Serverless architecture template"""
        return {
            'pattern': 'serverless',
            'structure': {
                'functions': [
                    {
                        'name': 'api_handler',
                        'trigger': 'http',
                        'description': 'Handles HTTP API requests',
                    },
                    {
                        'name': 'data_processor',
                        'trigger': 'queue',
                        'description': 'Processes background tasks',
                    },
                    {
                        'name': 'scheduled_job',
                        'trigger': 'cron',
                        'description': 'Periodic maintenance tasks',
                    },
                ],
                'resources': [
                    {
                        'type': 'storage',
                        'name': 'object_storage',
                        'service': 's3',
                    },
                    {
                        'type': 'database',
                        'name': 'dynamodb',
                        'service': 'dynamodb',
                    },
                ],
            },
            'directories': [
                'functions/api',
                'functions/processors',
                'functions/jobs',
                'shared/layers',
                'infrastructure/terraform',
                'tests',
                'docs',
            ],
            'interfaces': {
                'external': ['HTTP API', 'Event Triggers'],
                'internal': ['Shared Layers'],
            },
        }
    
    @staticmethod
    def get_layered_template() -> Dict[str, Any]:
        """Layered (N-tier) architecture template"""
        return {
            'pattern': 'layered',
            'structure': {
                'layers': [
                    {
                        'name': 'presentation',
                        'level': 1,
                        'dependencies': ['application'],
                    },
                    {
                        'name': 'application',
                        'level': 2,
                        'dependencies': ['domain', 'infrastructure'],
                    },
                    {
                        'name': 'domain',
                        'level': 3,
                        'dependencies': [],
                    },
                    {
                        'name': 'infrastructure',
                        'level': 4,
                        'dependencies': ['domain'],
                    },
                ],
            },
            'directories': [
                'src/presentation/controllers',
                'src/presentation/views',
                'src/application/services',
                'src/application/dto',
                'src/domain/entities',
                'src/domain/interfaces',
                'src/infrastructure/persistence',
                'src/infrastructure/external',
                'tests',
                'docs',
            ],
            'interfaces': {
                'external': ['Controllers', 'API Endpoints'],
                'internal': ['Service Interfaces', 'Repository Interfaces'],
            },
        }


class ArchitectureScaffolder:
    """
    Main architecture scaffolding engine.
    Generates high-level project structure based on specifications.
    """
    
    def __init__(self):
        self.templates = {
            ArchitecturePattern.MONOLITH: ArchitectureTemplate.get_monolith_template,
            ArchitecturePattern.MICROSERVICES: ArchitectureTemplate.get_microservices_template,
            ArchitecturePattern.SERVERLESS: ArchitectureTemplate.get_serverless_template,
            ArchitecturePattern.LAYERED: ArchitectureTemplate.get_layered_template,
        }
    
    def generate_architecture(
        self,
        specification: Dict[str, Any],
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate architecture scaffold from specification
        
        Args:
            specification: Generated specification from SpecificationGenerator
            preferences: Optional preferences for architecture generation
            
        Returns:
            Architecture scaffold with structure and interfaces
        """
        preferences = preferences or {}
        
        # Determine architecture pattern
        arch_type = specification.get('architecture', {}).get('type', 'monolith')
        pattern = self._determine_pattern(arch_type)
        
        # Get base template
        template_func = self.templates.get(
            pattern,
            self.templates[ArchitecturePattern.MONOLITH]
        )
        architecture = template_func()
        
        # Enrich with specification details
        architecture = self._enrich_architecture(architecture, specification, preferences)
        
        # Generate interface contracts
        architecture['interface_contracts'] = self._generate_interface_contracts(
            architecture, specification
        )
        
        # Add metadata
        architecture['metadata'] = {
            'generated_at': datetime.utcnow().isoformat(),
            'specification_version': specification.get('metadata', {}).get('version', '1.0'),
            'pattern': pattern.value,
            'ready_for_implementation': False,  # Deferred for later
        }
        
        return architecture
    
    def _determine_pattern(self, arch_type: str) -> ArchitecturePattern:
        """Determine architecture pattern from type"""
        pattern_mapping = {
            'monolith': ArchitecturePattern.MONOLITH,
            'web_application': ArchitecturePattern.LAYERED,
            'microservices': ArchitecturePattern.MICROSERVICES,
            'serverless': ArchitecturePattern.SERVERLESS,
            'layered': ArchitecturePattern.LAYERED,
            'component': ArchitecturePattern.LAYERED,
            'feature_addition': ArchitecturePattern.LAYERED,
        }
        
        return pattern_mapping.get(arch_type, ArchitecturePattern.MONOLITH)
    
    def _enrich_architecture(
        self,
        architecture: Dict[str, Any],
        specification: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enrich base architecture with specification details"""
        
        # Add technology stack
        architecture['technology_stack'] = specification.get('technology_stack', {})
        
        # Add components from specification
        spec_components = specification.get('components', {})
        if 'services' in spec_components and spec_components['services']:
            # Merge with template services
            if 'structure' in architecture and 'services' in architecture['structure']:
                # For microservices, extend services
                existing_services = {s['name']: s for s in architecture['structure']['services']}
                for service in spec_components['services']:
                    service_name = service.get('name', 'unknown')
                    if service_name not in existing_services:
                        architecture['structure']['services'].append(service)
        
        # Add database configuration
        if 'databases' in spec_components:
            architecture['databases'] = spec_components['databases']
        
        # Add security configuration
        architecture['security'] = specification.get('security', {})
        
        # Add deployment configuration
        architecture['deployment'] = specification.get('deployment', {})
        
        return architecture
    
    def _generate_interface_contracts(
        self,
        architecture: Dict[str, Any],
        specification: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate interface contracts between components"""
        contracts = []
        
        pattern = architecture.get('pattern', 'monolith')
        
        if pattern == 'microservices':
            # Generate contracts for inter-service communication
            services = architecture.get('structure', {}).get('services', [])
            
            for service in services:
                if service.get('type') == 'business':
                    contract = {
                        'service': service['name'],
                        'type': 'rest_api',
                        'endpoints': [
                            {
                                'path': f'/api/{service["name"]}/health',
                                'method': 'GET',
                                'description': 'Health check endpoint',
                            },
                            {
                                'path': f'/api/{service["name"]}/resource',
                                'method': 'POST',
                                'description': 'Create resource',
                                'request_schema': {},
                                'response_schema': {},
                            },
                        ],
                        'dependencies': [],
                    }
                    contracts.append(contract)
        
        elif pattern in ['monolith', 'layered']:
            # Generate contracts for layer interfaces
            layers = architecture.get('structure', {}).get('layers', [])
            
            for i, layer in enumerate(layers):
                if i < len(layers) - 1:
                    contract = {
                        'from_layer': layer['name'],
                        'to_layer': layers[i + 1]['name'],
                        'type': 'interface',
                        'methods': [
                            {
                                'name': f'process_data',
                                'parameters': [],
                                'returns': 'result',
                                'description': 'Process data through layer',
                            }
                        ],
                    }
                    contracts.append(contract)
        
        return contracts
    
    def generate_directory_structure(
        self,
        architecture: Dict[str, Any]
    ) -> List[str]:
        """
        Generate complete directory structure for the architecture
        
        Returns:
            List of directory paths to create
        """
        directories = architecture.get('directories', [])
        
        # Add common directories
        common_dirs = [
            'tests/unit',
            'tests/integration',
            'tests/e2e',
            'docs/api',
            'docs/architecture',
            'docs/deployment',
            'scripts',
            'config',
        ]
        
        all_directories = list(set(directories + common_dirs))
        all_directories.sort()
        
        return all_directories
    
    def generate_file_structure(
        self,
        architecture: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate file structure with placeholder content
        
        Returns:
            Dict mapping file paths to placeholder content
        """
        files = {}
        
        pattern = architecture.get('pattern', 'monolith')
        
        # Common files
        files['README.md'] = '# Project Name\n\nGenerated project structure.\n'
        files['.gitignore'] = '*.pyc\n__pycache__/\n.env\nnode_modules/\n'
        files['docs/ARCHITECTURE.md'] = f'# Architecture\n\nPattern: {pattern}\n'
        
        # Pattern-specific files
        if pattern == 'microservices':
            files['docker-compose.yml'] = '# Docker Compose configuration\nversion: "3.8"\n'
            services = architecture.get('structure', {}).get('services', [])
            for service in services:
                service_name = service['name']
                files[f'services/{service_name}/main.py'] = f'# {service_name} service\n'
                files[f'services/{service_name}/requirements.txt'] = ''
                files[f'services/{service_name}/Dockerfile'] = f'FROM python:3.11\n'
        
        elif pattern in ['monolith', 'layered']:
            files['src/main.py'] = '# Application entry point\n'
            files['requirements.txt'] = ''
            files['Dockerfile'] = 'FROM python:3.11\n'
        
        elif pattern == 'serverless':
            files['serverless.yml'] = '# Serverless configuration\n'
            functions = architecture.get('structure', {}).get('functions', [])
            for func in functions:
                func_name = func['name']
                files[f'functions/{func_name}/handler.py'] = f'# {func_name} handler\n'
        
        return files
    
    def export_architecture(
        self,
        architecture: Dict[str, Any],
        format: str = 'json'
    ) -> str:
        """
        Export architecture to specified format
        
        Args:
            architecture: Architecture scaffold
            format: Output format ('json', 'yaml', 'markdown')
            
        Returns:
            Formatted architecture string
        """
        if format == 'json':
            return json.dumps(architecture, indent=2)
        elif format == 'markdown':
            return self._to_markdown(architecture)
        else:
            return json.dumps(architecture, indent=2)
    
    def _to_markdown(self, architecture: Dict[str, Any]) -> str:
        """Convert architecture to markdown documentation"""
        md = f"# Architecture: {architecture.get('pattern', 'Unknown').upper()}\n\n"
        md += f"Generated: {architecture.get('metadata', {}).get('generated_at', 'N/A')}\n\n"
        
        md += "## Structure\n\n"
        if 'structure' in architecture:
            md += "```json\n"
            md += json.dumps(architecture['structure'], indent=2)
            md += "\n```\n\n"
        
        md += "## Directories\n\n"
        for directory in architecture.get('directories', []):
            md += f"- `{directory}`\n"
        
        md += "\n## Interfaces\n\n"
        for interface_type, interfaces in architecture.get('interfaces', {}).items():
            md += f"### {interface_type}\n\n"
            for interface in interfaces:
                md += f"- {interface}\n"
            md += "\n"
        
        return md
