"""
Agent Ecosystem - Distributed AI Agent Swarm (Port 5011)

Main FastAPI service for managing and orchestrating 2000+ AI agents.
Integrates Ray for distributed computing and Redis for state management.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import os
import uvicorn

from registry import AgentRegistry, AgentCapability, AgentStatus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agent Ecosystem - AI Agent Swarm",
    description="Distributed AI agent management system supporting 2000+ parallel agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent registry
registry = AgentRegistry(
    min_agents=10,
    max_agents=2000,
    scale_up_threshold=50,
    scale_down_threshold=10
)

# Pydantic models
class TaskRequest(BaseModel):
    task_type: str = Field(..., description="Type of task")
    capability: str = Field(..., description="Required agent capability")
    parameters: Dict[str, Any] = Field(default={}, description="Task parameters")
    priority: int = Field(default=2, description="Task priority (1-4)")


class TaskResponse(BaseModel):
    task_id: str
    agent_id: Optional[str]
    status: str
    message: str


class TaskCompletionRequest(BaseModel):
    task_id: str
    agent_id: str
    success: bool
    processing_time: float
    result: Optional[Dict[str, Any]] = None


class SpawnAgentRequest(BaseModel):
    agent_type: str
    capabilities: List[str]
    max_concurrent_tasks: int = Field(default=1, ge=1, le=10)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    stats = registry.get_stats()
    return {
        "status": "healthy",
        "service": "agent-ecosystem",
        "timestamp": datetime.utcnow().isoformat(),
        "agent_stats": stats
    }


@app.get("/")
async def root():
    """Root endpoint with service information."""
    stats = registry.get_stats()
    return {
        "service": "Agent Ecosystem",
        "description": "Distributed AI agent swarm supporting 2000+ parallel agents",
        "capabilities": [
            "Dynamic agent spawning/termination",
            "Auto-scaling (10 to 2000+ agents)",
            "Capability-based task matching",
            "Performance tracking",
            "Load balancing"
        ],
        "current_stats": stats,
        "endpoints": [
            "POST /task/assign - Assign task to agent",
            "POST /task/complete - Mark task as complete",
            "POST /agent/spawn - Manually spawn agent",
            "DELETE /agent/{agent_id} - Terminate agent",
            "GET /agents - List all agents",
            "GET /agents/capability/{capability} - Get agents by capability",
            "POST /scale - Trigger auto-scaling",
            "GET /stats - Get detailed statistics"
        ]
    }


@app.post("/task/assign", response_model=TaskResponse)
async def assign_task(request: TaskRequest):
    """
    Assign a task to an available agent.
    
    Auto-spawns new agents if needed and capacity allows.
    """
    try:
        # Generate task ID
        import uuid
        task_id = str(uuid.uuid4())
        
        # Map string capability to enum
        capability_map = {
            "data_ingestion": AgentCapability.DATA_INGESTION,
            "tech_scouting": AgentCapability.TECH_SCOUTING,
            "code_analysis": AgentCapability.CODE_ANALYSIS,
            "content_generation": AgentCapability.CONTENT_GENERATION,
            "cost_optimization": AgentCapability.COST_OPTIMIZATION,
            "business_analysis": AgentCapability.BUSINESS_ANALYSIS,
            "experimentation": AgentCapability.EXPERIMENTATION,
            "feedback_analysis": AgentCapability.FEEDBACK_ANALYSIS,
            "strategy_evolution": AgentCapability.STRATEGY_EVOLUTION,
            "integration_testing": AgentCapability.INTEGRATION_TESTING,
        }
        
        capability = capability_map.get(
            request.capability.lower(),
            AgentCapability.DATA_INGESTION
        )
        
        # Assign task
        agent_id = registry.assign_task(task_id, capability)
        
        if not agent_id:
            return TaskResponse(
                task_id=task_id,
                agent_id=None,
                status="queued",
                message="No agents available - task queued for processing"
            )
        
        logger.info(f"Task {task_id} assigned to agent {agent_id}")
        
        return TaskResponse(
            task_id=task_id,
            agent_id=agent_id,
            status="assigned",
            message=f"Task assigned to agent {agent_id}"
        )
    
    except Exception as e:
        logger.error(f"Task assignment error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/task/complete")
async def complete_task(request: TaskCompletionRequest):
    """
    Mark a task as completed.
    
    Updates agent performance metrics and triggers auto-scaling if needed.
    """
    try:
        registry.complete_task(
            agent_id=request.agent_id,
            task_id=request.task_id,
            success=request.success,
            processing_time=request.processing_time
        )
        
        # Trigger auto-scaling check
        stats = registry.get_stats()
        registry.auto_scale(stats.get("queue_depth", 0))
        
        return {
            "success": True,
            "message": "Task completion recorded",
            "task_id": request.task_id,
            "result": request.result
        }
    
    except Exception as e:
        logger.error(f"Task completion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/spawn")
async def spawn_agent(request: SpawnAgentRequest):
    """Manually spawn a new agent."""
    try:
        # Map string capabilities to enums
        capability_map = {
            "data_ingestion": AgentCapability.DATA_INGESTION,
            "tech_scouting": AgentCapability.TECH_SCOUTING,
            "code_analysis": AgentCapability.CODE_ANALYSIS,
            "content_generation": AgentCapability.CONTENT_GENERATION,
            "cost_optimization": AgentCapability.COST_OPTIMIZATION,
            "business_analysis": AgentCapability.BUSINESS_ANALYSIS,
            "experimentation": AgentCapability.EXPERIMENTATION,
            "feedback_analysis": AgentCapability.FEEDBACK_ANALYSIS,
            "strategy_evolution": AgentCapability.STRATEGY_EVOLUTION,
            "integration_testing": AgentCapability.INTEGRATION_TESTING,
        }
        
        capabilities = {
            capability_map.get(cap.lower(), AgentCapability.DATA_INGESTION)
            for cap in request.capabilities
        }
        
        agent = registry.spawn_agent(
            agent_type=request.agent_type,
            capabilities=capabilities,
            max_concurrent_tasks=request.max_concurrent_tasks
        )
        
        if not agent:
            raise HTTPException(
                status_code=400,
                detail="Failed to spawn agent - max capacity reached"
            )
        
        return {
            "success": True,
            "agent_id": agent.agent_id,
            "agent_type": agent.agent_type,
            "capabilities": [c.value for c in agent.capabilities],
            "message": f"Agent {agent.agent_id} spawned successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent spawn error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/agent/{agent_id}")
async def terminate_agent(agent_id: str):
    """Terminate a specific agent."""
    try:
        success = registry.terminate_agent(agent_id)
        
        if not success:
            raise HTTPException(
                status_code=400,
                detail="Failed to terminate agent - may be busy or not found"
            )
        
        return {
            "success": True,
            "message": f"Agent {agent_id} terminated successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent termination error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List all agents with their status."""
    try:
        agents = [
            {
                "agent_id": agent.agent_id,
                "agent_type": agent.agent_type,
                "status": agent.status.value,
                "capabilities": [c.value for c in agent.capabilities],
                "current_tasks": len(agent.current_tasks),
                "tasks_completed": agent.tasks_completed,
                "tasks_failed": agent.tasks_failed,
                "performance_score": round(agent.performance_score, 3),
                "last_active": agent.last_active.isoformat()
            }
            for agent in registry.agents.values()
        ]
        
        return {
            "success": True,
            "total_agents": len(agents),
            "agents": agents
        }
    
    except Exception as e:
        logger.error(f"List agents error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents/capability/{capability}")
async def get_agents_by_capability(capability: str):
    """Get all agents with a specific capability."""
    try:
        capability_map = {
            "data_ingestion": AgentCapability.DATA_INGESTION,
            "tech_scouting": AgentCapability.TECH_SCOUTING,
            "code_analysis": AgentCapability.CODE_ANALYSIS,
            "content_generation": AgentCapability.CONTENT_GENERATION,
            "cost_optimization": AgentCapability.COST_OPTIMIZATION,
            "business_analysis": AgentCapability.BUSINESS_ANALYSIS,
            "experimentation": AgentCapability.EXPERIMENTATION,
            "feedback_analysis": AgentCapability.FEEDBACK_ANALYSIS,
            "strategy_evolution": AgentCapability.STRATEGY_EVOLUTION,
            "integration_testing": AgentCapability.INTEGRATION_TESTING,
        }
        
        cap = capability_map.get(capability.lower())
        if not cap:
            raise HTTPException(status_code=400, detail=f"Unknown capability: {capability}")
        
        agents = registry.get_agents_by_capability(cap)
        
        return {
            "success": True,
            "capability": capability,
            "count": len(agents),
            "agents": [
                {
                    "agent_id": agent.agent_id,
                    "agent_type": agent.agent_type,
                    "status": agent.status.value,
                    "performance_score": round(agent.performance_score, 3)
                }
                for agent in agents
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get agents by capability error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scale")
async def trigger_auto_scale(queue_depth: int = 0):
    """Manually trigger auto-scaling based on queue depth."""
    try:
        registry.auto_scale(queue_depth)
        
        stats = registry.get_stats()
        
        return {
            "success": True,
            "message": "Auto-scaling triggered",
            "stats": stats
        }
    
    except Exception as e:
        logger.error(f"Auto-scale error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_detailed_stats():
    """Get detailed agent ecosystem statistics."""
    try:
        stats = registry.get_stats()
        
        # Add capability breakdown
        capability_stats = {}
        for cap in AgentCapability:
            agents = registry.get_agents_by_capability(cap)
            capability_stats[cap.value] = {
                "total_agents": len(agents),
                "idle_agents": sum(1 for a in agents if a.status == AgentStatus.IDLE),
                "busy_agents": sum(1 for a in agents if a.status == AgentStatus.BUSY),
            }
        
        stats["capabilities"] = capability_stats
        
        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "stats": stats
        }
    
    except Exception as e:
        logger.error(f"Get stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5011"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
