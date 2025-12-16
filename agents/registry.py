"""
Agent Registry Configuration

Defines all available agents and their roles in the system.
Supports scaling to 30-100 logical agent roles.
"""

# Import all agent classes to register them
from .architect_agent import ArchitectAgent
from .market_research_agent import MarketResearchAgent
from .compliance_agent import ComplianceAgent
from .media_generation_agent import MediaGenerationAgent

# Import base classes
from .base_agent import BaseAgent, AgentGuardrails

# Agent categories for organization
AGENT_CATEGORIES = {
    "architecture": [
        "architect",
        # Future: "cloud_architect", "data_architect", "security_architect"
    ],
    "research": [
        "market_research",
        # Future: "technical_research", "user_research", "competitive_intelligence"
    ],
    "compliance": [
        "compliance",
        # Future: "legal_review", "privacy_officer", "audit_specialist"
    ],
    "media": [
        "media_generation",
        # Future: "video_editor", "graphic_designer", "content_strategist"
    ],
    # Future categories:
    # "development": ["backend_dev", "frontend_dev", "devops", "qa_engineer"],
    # "operations": ["sre", "monitoring", "incident_response"],
    # "product": ["product_manager", "ux_designer", "business_analyst"],
    # "data": ["data_scientist", "ml_engineer", "data_engineer"],
}

# Guardrail configurations
GUARDRAIL_CONFIG = {
    "prevent_main_branch_merge": True,
    "prevent_direct_deployment": True,
    "prevent_autonomous_commits": True,
    "require_approval_for_critical_actions": True,
    "artifact_output_only": True,
    "audit_all_actions": True,
}

# Agent capability matrix
# Defines which actions each category can perform
CAPABILITY_MATRIX = {
    "architecture": {
        "allowed": ["analyze", "design", "review", "recommend"],
        "forbidden": ["deploy", "commit", "merge"]
    },
    "research": {
        "allowed": ["research", "analyze", "report"],
        "forbidden": ["deploy", "commit", "merge", "modify_code"]
    },
    "compliance": {
        "allowed": ["audit", "review", "assess", "report"],
        "forbidden": ["deploy", "commit", "merge", "auto_fix"]
    },
    "media": {
        "allowed": ["generate_spec", "recommend", "plan"],
        "forbidden": ["deploy", "commit", "auto_publish"]
    },
}


def get_agent_by_role(role_id: str) -> BaseAgent:
    """
    Get agent instance by role ID.
    
    Args:
        role_id: Agent role identifier
        
    Returns:
        Agent instance
    """
    from agents import get_agent
    
    agent_class = get_agent(role_id)
    if not agent_class:
        raise ValueError(f"Unknown agent role: {role_id}")
    
    return agent_class()


def list_available_agents() -> dict:
    """
    List all available agents organized by category.
    
    Returns:
        Dictionary of categories and their agents
    """
    from agents import AGENT_REGISTRY
    
    available = {}
    for category, role_ids in AGENT_CATEGORIES.items():
        available[category] = []
        for role_id in role_ids:
            if role_id in AGENT_REGISTRY:
                agent_class = AGENT_REGISTRY[role_id]
                available[category].append({
                    "role_id": agent_class.ROLE_ID,
                    "role_name": agent_class.ROLE_NAME,
                    "description": agent_class.ROLE_DESCRIPTION,
                    "capabilities": agent_class.CAPABILITIES
                })
    
    return available


def validate_agent_action(role_id: str, action: str) -> bool:
    """
    Validate if an agent can perform an action.
    
    Args:
        role_id: Agent role identifier
        action: Action to validate
        
    Returns:
        True if allowed, False otherwise
    """
    # Find agent category
    category = None
    for cat, role_ids in AGENT_CATEGORIES.items():
        if role_id in role_ids:
            category = cat
            break
    
    if not category:
        return False
    
    # Check capability matrix
    capabilities = CAPABILITY_MATRIX.get(category, {})
    
    if action in capabilities.get("forbidden", []):
        return False
    
    if action in capabilities.get("allowed", []):
        return True
    
    # Default deny for unlisted actions
    return False


# TODO: Expand agent roster to 30-100 roles
# Suggested future agents:
FUTURE_AGENTS = [
    # Development
    "backend_developer", "frontend_developer", "mobile_developer",
    "devops_engineer", "qa_engineer", "performance_engineer",
    
    # Architecture
    "cloud_architect", "data_architect", "security_architect",
    "integration_architect", "solutions_architect",
    
    # Research & Analysis
    "technical_researcher", "user_researcher", "data_analyst",
    "business_analyst", "competitive_intelligence",
    
    # Operations
    "sre", "monitoring_specialist", "incident_responder",
    "capacity_planner", "release_manager",
    
    # Product & Design
    "product_manager", "ux_designer", "ui_designer",
    "content_strategist", "technical_writer",
    
    # Data & ML
    "data_scientist", "ml_engineer", "data_engineer",
    "ml_ops", "feature_engineer",
    
    # Security & Compliance
    "security_engineer", "penetration_tester", "privacy_officer",
    "compliance_auditor", "legal_reviewer",
    
    # Media & Content
    "video_editor", "graphic_designer", "copywriter",
    "social_media_manager", "brand_strategist",
    
    # Support & Services
    "technical_support", "customer_success", "documentation_specialist",
    "training_coordinator", "community_manager",
]
