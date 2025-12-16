"""
Agent Roles - Defines 30-100 logical roles for the agent system
No hard-wired vendor dependencies, placeholder structure only
"""

from enum import Enum
from typing import List, Dict, Any


class RoleCategory(Enum):
    """High-level categories for agent roles"""
    OPERATIONS = "operations"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATA = "data"
    DEVOPS = "devops"
    SECURITY = "security"
    TESTING = "testing"
    DESIGN = "design"
    PRODUCT = "product"
    RESEARCH = "research"


class AgentRole:
    """
    Defines a logical agent role with capabilities and requirements
    This is a placeholder structure - no hard-wired vendor dependencies
    """
    
    # Operations Roles
    OPERATIONS_ARCHITECT = {
        'name': 'Operations Architect',
        'category': RoleCategory.OPERATIONS,
        'description': 'Designs and oversees operational infrastructure',
        'capabilities': [
            'system_architecture',
            'infrastructure_planning',
            'resource_optimization',
            'workflow_design'
        ],
        'required_skills': ['architecture', 'operations', 'strategy']
    }
    
    OPERATIONS_MANAGER = {
        'name': 'Operations Manager',
        'category': RoleCategory.OPERATIONS,
        'description': 'Manages day-to-day operations and coordination',
        'capabilities': [
            'task_coordination',
            'team_management',
            'process_optimization',
            'monitoring'
        ],
        'required_skills': ['management', 'coordination', 'monitoring']
    }
    
    # Frontend Roles
    FRONTEND_ARCHITECT = {
        'name': 'Frontend Architect',
        'category': RoleCategory.FRONTEND,
        'description': 'Designs frontend architecture and patterns',
        'capabilities': [
            'ui_architecture',
            'component_design',
            'performance_optimization',
            'framework_selection'
        ],
        'required_skills': ['frontend', 'architecture', 'javascript', 'react']
    }
    
    FRONTEND_DEVELOPER = {
        'name': 'Frontend Developer',
        'category': RoleCategory.FRONTEND,
        'description': 'Implements user interfaces and frontend features',
        'capabilities': [
            'ui_development',
            'component_implementation',
            'state_management',
            'responsive_design'
        ],
        'required_skills': ['html', 'css', 'javascript', 'react']
    }
    
    UI_UX_SPECIALIST = {
        'name': 'UI/UX Specialist',
        'category': RoleCategory.FRONTEND,
        'description': 'Focuses on user interface and user experience design',
        'capabilities': [
            'interface_design',
            'user_flow_design',
            'prototyping',
            'usability_testing'
        ],
        'required_skills': ['design', 'ux', 'prototyping', 'user_research']
    }
    
    # Backend Roles
    BACKEND_ARCHITECT = {
        'name': 'Backend Architect',
        'category': RoleCategory.BACKEND,
        'description': 'Designs backend systems and APIs',
        'capabilities': [
            'api_design',
            'database_architecture',
            'microservices_design',
            'scalability_planning'
        ],
        'required_skills': ['backend', 'architecture', 'databases', 'apis']
    }
    
    BACKEND_DEVELOPER = {
        'name': 'Backend Developer',
        'category': RoleCategory.BACKEND,
        'description': 'Implements backend services and APIs',
        'capabilities': [
            'api_implementation',
            'database_operations',
            'business_logic',
            'integration'
        ],
        'required_skills': ['python', 'nodejs', 'databases', 'apis']
    }
    
    API_SPECIALIST = {
        'name': 'API Specialist',
        'category': RoleCategory.BACKEND,
        'description': 'Specializes in API design and implementation',
        'capabilities': [
            'rest_api_design',
            'graphql_design',
            'api_documentation',
            'api_security'
        ],
        'required_skills': ['rest', 'graphql', 'openapi', 'api_design']
    }
    
    # Data Roles
    DATA_ARCHITECT = {
        'name': 'Data Architect',
        'category': RoleCategory.DATA,
        'description': 'Designs data infrastructure and pipelines',
        'capabilities': [
            'data_modeling',
            'pipeline_design',
            'data_warehouse_design',
            'etl_design'
        ],
        'required_skills': ['data_modeling', 'sql', 'data_warehousing', 'etl']
    }
    
    DATA_ENGINEER = {
        'name': 'Data Engineer',
        'category': RoleCategory.DATA,
        'description': 'Builds and maintains data pipelines',
        'capabilities': [
            'pipeline_implementation',
            'data_processing',
            'data_integration',
            'data_quality'
        ],
        'required_skills': ['python', 'spark', 'sql', 'data_pipelines']
    }
    
    DATA_SCIENTIST = {
        'name': 'Data Scientist',
        'category': RoleCategory.DATA,
        'description': 'Analyzes data and builds ML models',
        'capabilities': [
            'data_analysis',
            'ml_modeling',
            'statistical_analysis',
            'prediction'
        ],
        'required_skills': ['python', 'machine_learning', 'statistics', 'data_analysis']
    }
    
    ML_ENGINEER = {
        'name': 'ML Engineer',
        'category': RoleCategory.DATA,
        'description': 'Implements and deploys machine learning models',
        'capabilities': [
            'model_training',
            'model_deployment',
            'model_optimization',
            'mlops'
        ],
        'required_skills': ['python', 'pytorch', 'tensorflow', 'mlops']
    }
    
    # DevOps Roles
    DEVOPS_ARCHITECT = {
        'name': 'DevOps Architect',
        'category': RoleCategory.DEVOPS,
        'description': 'Designs CI/CD and infrastructure automation',
        'capabilities': [
            'cicd_design',
            'infrastructure_as_code',
            'automation_strategy',
            'cloud_architecture'
        ],
        'required_skills': ['devops', 'kubernetes', 'terraform', 'cloud']
    }
    
    DEVOPS_ENGINEER = {
        'name': 'DevOps Engineer',
        'category': RoleCategory.DEVOPS,
        'description': 'Implements and maintains DevOps infrastructure',
        'capabilities': [
            'cicd_implementation',
            'container_orchestration',
            'monitoring_setup',
            'automation'
        ],
        'required_skills': ['docker', 'kubernetes', 'jenkins', 'terraform']
    }
    
    SRE = {
        'name': 'Site Reliability Engineer',
        'category': RoleCategory.DEVOPS,
        'description': 'Ensures system reliability and performance',
        'capabilities': [
            'reliability_engineering',
            'incident_response',
            'performance_tuning',
            'monitoring'
        ],
        'required_skills': ['sre', 'monitoring', 'kubernetes', 'incident_management']
    }
    
    # Security Roles
    SECURITY_ARCHITECT = {
        'name': 'Security Architect',
        'category': RoleCategory.SECURITY,
        'description': 'Designs security systems and protocols',
        'capabilities': [
            'security_design',
            'threat_modeling',
            'security_architecture',
            'compliance_design'
        ],
        'required_skills': ['security', 'cryptography', 'compliance', 'threat_modeling']
    }
    
    SECURITY_ENGINEER = {
        'name': 'Security Engineer',
        'category': RoleCategory.SECURITY,
        'description': 'Implements security measures and monitoring',
        'capabilities': [
            'security_implementation',
            'vulnerability_scanning',
            'penetration_testing',
            'security_monitoring'
        ],
        'required_skills': ['security', 'penetration_testing', 'monitoring', 'compliance']
    }
    
    # Testing Roles
    QA_ARCHITECT = {
        'name': 'QA Architect',
        'category': RoleCategory.TESTING,
        'description': 'Designs testing strategy and frameworks',
        'capabilities': [
            'test_strategy',
            'framework_design',
            'quality_metrics',
            'automation_strategy'
        ],
        'required_skills': ['testing', 'automation', 'quality_assurance', 'strategy']
    }
    
    QA_ENGINEER = {
        'name': 'QA Engineer',
        'category': RoleCategory.TESTING,
        'description': 'Implements tests and ensures quality',
        'capabilities': [
            'test_implementation',
            'automated_testing',
            'manual_testing',
            'bug_tracking'
        ],
        'required_skills': ['testing', 'selenium', 'pytest', 'quality_assurance']
    }
    
    # Design Roles
    DESIGN_LEAD = {
        'name': 'Design Lead',
        'category': RoleCategory.DESIGN,
        'description': 'Leads design vision and strategy',
        'capabilities': [
            'design_strategy',
            'design_systems',
            'team_leadership',
            'brand_development'
        ],
        'required_skills': ['design', 'leadership', 'design_systems', 'branding']
    }
    
    VISUAL_DESIGNER = {
        'name': 'Visual Designer',
        'category': RoleCategory.DESIGN,
        'description': 'Creates visual assets and interfaces',
        'capabilities': [
            'visual_design',
            'graphics_creation',
            'icon_design',
            'illustration'
        ],
        'required_skills': ['design', 'figma', 'photoshop', 'illustration']
    }
    
    # Product Roles
    PRODUCT_MANAGER = {
        'name': 'Product Manager',
        'category': RoleCategory.PRODUCT,
        'description': 'Manages product strategy and roadmap',
        'capabilities': [
            'product_strategy',
            'roadmap_planning',
            'stakeholder_management',
            'requirements_gathering'
        ],
        'required_skills': ['product_management', 'strategy', 'roadmapping', 'agile']
    }
    
    PRODUCT_OWNER = {
        'name': 'Product Owner',
        'category': RoleCategory.PRODUCT,
        'description': 'Defines and prioritizes product backlog',
        'capabilities': [
            'backlog_management',
            'user_story_creation',
            'prioritization',
            'sprint_planning'
        ],
        'required_skills': ['agile', 'scrum', 'user_stories', 'prioritization']
    }
    
    # Research Roles
    RESEARCH_SCIENTIST = {
        'name': 'Research Scientist',
        'category': RoleCategory.RESEARCH,
        'description': 'Conducts research and develops new approaches',
        'capabilities': [
            'research_design',
            'experimentation',
            'paper_writing',
            'innovation'
        ],
        'required_skills': ['research', 'statistics', 'experimentation', 'writing']
    }
    
    AI_RESEARCHER = {
        'name': 'AI Researcher',
        'category': RoleCategory.RESEARCH,
        'description': 'Researches and develops AI technologies',
        'capabilities': [
            'ai_research',
            'model_development',
            'algorithm_design',
            'benchmarking'
        ],
        'required_skills': ['ai', 'machine_learning', 'deep_learning', 'research']
    }
    
    @classmethod
    def get_all_roles(cls) -> List[Dict[str, Any]]:
        """Get all defined agent roles"""
        roles = []
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, dict) and 'name' in attr and 'category' in attr:
                roles.append(attr)
        return roles
    
    @classmethod
    def get_roles_by_category(cls, category: RoleCategory) -> List[Dict[str, Any]]:
        """Get all roles in a specific category"""
        all_roles = cls.get_all_roles()
        return [role for role in all_roles if role['category'] == category]
    
    @classmethod
    def get_role_count(cls) -> int:
        """Get total number of defined roles"""
        return len(cls.get_all_roles())


# Additional roles can be easily added following this pattern
# The system is designed to support 30-100 logical roles
