"""
Predefined Agent Roles

This module defines common agent roles for the VoBee AI Operating System.
These are examples - the system supports 30-100+ custom roles.
"""

from .registry import AgentRegistry, AgentRole, AgentCapability


def initialize_default_roles(registry: AgentRegistry) -> None:
    """
    Initialize the registry with default agent roles.
    
    This demonstrates the role-based architecture with common roles.
    More roles can be added dynamically without code changes.
    """
    
    # Research & Analysis Roles
    registry.create_role(
        name="ResearchAnalyst",
        description="Conducts research, gathers data, and performs analysis",
        capabilities=[
            AgentCapability(
                name="web_research",
                description="Search and analyze web content",
                required_skills=["research", "analysis"]
            ),
            AgentCapability(
                name="data_analysis",
                description="Analyze datasets and extract insights",
                required_skills=["analysis", "statistics"]
            ),
        ],
        priority=3,
        max_concurrent_tasks=5
    )
    
    registry.create_role(
        name="DataScientist",
        description="Advanced data analysis and machine learning",
        capabilities=[
            AgentCapability(
                name="ml_modeling",
                description="Build and train machine learning models",
                required_skills=["ml", "python", "statistics"]
            ),
            AgentCapability(
                name="data_visualization",
                description="Create data visualizations",
                required_skills=["visualization", "analysis"]
            ),
        ],
        priority=4,
        max_concurrent_tasks=3
    )
    
    # Development Roles
    registry.create_role(
        name="SoftwareEngineer",
        description="Develops and maintains software systems",
        capabilities=[
            AgentCapability(
                name="code_development",
                description="Write, review, and refactor code",
                required_skills=["programming", "software-design"]
            ),
            AgentCapability(
                name="testing",
                description="Write and execute tests",
                required_skills=["testing", "programming"]
            ),
        ],
        priority=5,
        max_concurrent_tasks=3
    )
    
    registry.create_role(
        name="DevOpsEngineer",
        description="Manages infrastructure and deployment",
        capabilities=[
            AgentCapability(
                name="deployment",
                description="Deploy and manage applications",
                required_skills=["devops", "kubernetes", "docker"]
            ),
            AgentCapability(
                name="monitoring",
                description="Monitor system health and performance",
                required_skills=["monitoring", "devops"]
            ),
        ],
        priority=5,
        max_concurrent_tasks=5
    )
    
    # Creative Roles
    registry.create_role(
        name="ContentCreator",
        description="Creates written content and documentation",
        capabilities=[
            AgentCapability(
                name="content_writing",
                description="Write articles, documentation, and content",
                required_skills=["writing", "creativity"]
            ),
            AgentCapability(
                name="editing",
                description="Edit and improve existing content",
                required_skills=["writing", "editing"]
            ),
        ],
        priority=2,
        max_concurrent_tasks=10
    )
    
    registry.create_role(
        name="VisualDesigner",
        description="Creates visual assets and designs",
        capabilities=[
            AgentCapability(
                name="image_generation",
                description="Generate images and visual content",
                required_skills=["design", "image-generation"]
            ),
            AgentCapability(
                name="ui_design",
                description="Design user interfaces",
                required_skills=["design", "ui-ux"]
            ),
        ],
        priority=2,
        max_concurrent_tasks=5
    )
    
    # Coordination Roles
    registry.create_role(
        name="ProjectManager",
        description="Coordinates projects and manages tasks",
        capabilities=[
            AgentCapability(
                name="task_planning",
                description="Plan and organize tasks",
                required_skills=["planning", "coordination"]
            ),
            AgentCapability(
                name="resource_allocation",
                description="Allocate resources efficiently",
                required_skills=["planning", "resource-management"]
            ),
        ],
        priority=6,
        max_concurrent_tasks=3
    )
    
    registry.create_role(
        name="QualityAssurance",
        description="Ensures quality and reviews work",
        capabilities=[
            AgentCapability(
                name="quality_review",
                description="Review and validate work quality",
                required_skills=["review", "quality-assurance"]
            ),
            AgentCapability(
                name="testing",
                description="Test systems and identify issues",
                required_skills=["testing", "quality-assurance"]
            ),
        ],
        priority=4,
        max_concurrent_tasks=5
    )
    
    # Support Roles
    registry.create_role(
        name="CustomerSupport",
        description="Provides support and assistance",
        capabilities=[
            AgentCapability(
                name="user_assistance",
                description="Help users with questions and issues",
                required_skills=["communication", "support"]
            ),
            AgentCapability(
                name="documentation",
                description="Create and maintain documentation",
                required_skills=["writing", "documentation"]
            ),
        ],
        priority=3,
        max_concurrent_tasks=10
    )
    
    # Specialized Roles
    registry.create_role(
        name="SecurityAnalyst",
        description="Analyzes and improves security",
        capabilities=[
            AgentCapability(
                name="security_audit",
                description="Audit systems for security issues",
                required_skills=["security", "analysis"]
            ),
            AgentCapability(
                name="vulnerability_assessment",
                description="Identify and assess vulnerabilities",
                required_skills=["security", "testing"]
            ),
        ],
        priority=7,
        max_concurrent_tasks=2
    )
    
    registry.create_role(
        name="FinancialAnalyst",
        description="Analyzes financial data and budgets",
        capabilities=[
            AgentCapability(
                name="budget_analysis",
                description="Analyze budgets and spending",
                required_skills=["finance", "analysis"]
            ),
            AgentCapability(
                name="forecasting",
                description="Create financial forecasts",
                required_skills=["finance", "forecasting"]
            ),
        ],
        priority=4,
        max_concurrent_tasks=3
    )
    
    # AI-Specific Roles
    registry.create_role(
        name="ModelTrainer",
        description="Trains and fine-tunes AI models",
        capabilities=[
            AgentCapability(
                name="model_training",
                description="Train machine learning models",
                required_skills=["ml", "training", "gpu"]
            ),
            AgentCapability(
                name="hyperparameter_tuning",
                description="Optimize model parameters",
                required_skills=["ml", "optimization"]
            ),
        ],
        priority=5,
        max_concurrent_tasks=2
    )
    
    registry.create_role(
        name="DataCurator",
        description="Manages and prepares training data",
        capabilities=[
            AgentCapability(
                name="data_collection",
                description="Collect and organize data",
                required_skills=["data-management", "organization"]
            ),
            AgentCapability(
                name="data_cleaning",
                description="Clean and prepare datasets",
                required_skills=["data-management", "preprocessing"]
            ),
        ],
        priority=3,
        max_concurrent_tasks=5
    )
    
    # Automation Roles
    registry.create_role(
        name="AutomationSpecialist",
        description="Creates and manages automation workflows",
        capabilities=[
            AgentCapability(
                name="workflow_automation",
                description="Automate repetitive workflows",
                required_skills=["automation", "scripting"]
            ),
            AgentCapability(
                name="process_optimization",
                description="Optimize processes for efficiency",
                required_skills=["automation", "optimization"]
            ),
        ],
        priority=4,
        max_concurrent_tasks=5
    )
    
    # Monitoring & Maintenance Roles
    registry.create_role(
        name="SystemMonitor",
        description="Monitors system health and performance",
        capabilities=[
            AgentCapability(
                name="health_monitoring",
                description="Monitor system health",
                required_skills=["monitoring", "analysis"]
            ),
            AgentCapability(
                name="alerting",
                description="Generate and manage alerts",
                required_skills=["monitoring", "alerting"]
            ),
        ],
        priority=6,
        max_concurrent_tasks=10
    )


def get_role_catalog() -> dict:
    """
    Return a catalog of all available role types.
    
    This can be extended to 100+ roles without modifying core code.
    """
    return {
        "research": ["ResearchAnalyst", "DataScientist"],
        "development": ["SoftwareEngineer", "DevOpsEngineer"],
        "creative": ["ContentCreator", "VisualDesigner"],
        "coordination": ["ProjectManager", "QualityAssurance"],
        "support": ["CustomerSupport"],
        "security": ["SecurityAnalyst"],
        "finance": ["FinancialAnalyst"],
        "ai": ["ModelTrainer", "DataCurator"],
        "automation": ["AutomationSpecialist"],
        "monitoring": ["SystemMonitor"]
    }
