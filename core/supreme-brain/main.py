"""
Supreme Brain - Core Consciousness (Port 5010)

Main FastAPI service that orchestrates the self-evolving AI organism.
Integrates identity keeper, decision engine, output composer, and task decomposer.
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import os
import uvicorn

from identity_keeper import IdentityKeeper
from decision_engine import DecisionEngine, ActionCriticality
from output_composer import OutputComposer, AgentOutput
from task_decomposer import TaskDecomposer, TaskPriority

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Supreme Brain - VOBee Core Consciousness",
    description="Central orchestration service for self-evolving AI organism",
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

# Initialize components
identity_keeper = IdentityKeeper()
decision_engine = DecisionEngine()
output_composer = OutputComposer()
task_decomposer = TaskDecomposer()

# Pydantic models
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Additional context")


class ChatResponse(BaseModel):
    response: str
    action_id: Optional[str] = None
    requires_approval: bool = False
    estimated_cost: float = 0.0
    estimated_duration: int = 0


class ApprovalRequest(BaseModel):
    action_id: str = Field(..., description="Action ID to approve")
    approved: bool = Field(..., description="Approval decision")


class TaskDecompositionRequest(BaseModel):
    goal: str = Field(..., description="High-level goal to decompose")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Context")
    max_tasks: int = Field(default=2000, description="Maximum tasks to generate")


class AgentOutputRequest(BaseModel):
    outputs: List[Dict[str, Any]] = Field(..., description="Agent outputs to compose")
    strategy: str = Field(default="comprehensive", description="Composition strategy")


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "supreme-brain",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "identity_keeper": "active",
            "decision_engine": "active",
            "output_composer": "active",
            "task_decomposer": "active"
        }
    }


@app.get("/")
async def root():
    """Root endpoint with introduction."""
    return {
        "service": "Supreme Brain",
        "introduction": identity_keeper.get_introduction(),
        "capabilities": [
            "Intent understanding",
            "Task decomposition (up to 2000+ parallel tasks)",
            "Human-in-the-loop approval",
            "Multi-agent output composition",
            "Unified personality maintenance"
        ],
        "endpoints": [
            "POST /chat - Chat with VOBee",
            "POST /approve - Approve pending actions",
            "POST /decompose - Decompose complex goals",
            "POST /compose - Compose agent outputs",
            "GET /decisions - Get pending decisions",
            "GET /stats - Get system statistics"
        ]
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for interacting with VOBee.
    
    Processes user message, determines intent, and either:
    - Returns direct response for simple queries
    - Returns action plan requiring approval for complex operations
    """
    try:
        logger.info(f"Chat request: {request.message[:100]}")
        
        # Parse intent (simplified - in production would use LLM)
        intent = _parse_intent(request.message, request.context)
        
        # Determine if action is needed
        if intent["requires_action"]:
            # Decompose into tasks
            tasks = task_decomposer.decompose(
                goal=request.message,
                context=request.context,
                max_tasks=100  # Limit for chat context
            )
            
            # Create proposed actions from tasks
            proposed_actions = [
                {
                    "type": task.task_type,
                    "description": task.description,
                    "parameters": task.parameters
                }
                for task in tasks[:10]  # Show top 10 for approval
            ]
            
            # Create decision
            decision = decision_engine.analyze_request(
                user_input=request.message,
                intent=intent,
                proposed_actions=proposed_actions
            )
            
            # Format response with personality
            summary = f"""I understand you want to: {request.message}

Here's my proposed action plan:

{decision.description}

💰 Estimated cost: ${decision.estimated_cost:.4f}
⏱️ Estimated time: {decision.estimated_duration}s
🔧 Tasks to execute: {len(tasks)}
"""
            
            # Apply personality
            response = identity_keeper.apply_personality(
                raw_response=summary,
                context={"requires_approval": decision.status == "pending_approval"}
            )
            
            return ChatResponse(
                response=response,
                action_id=decision.action_id,
                requires_approval=(decision.status == "pending_approval"),
                estimated_cost=decision.estimated_cost,
                estimated_duration=decision.estimated_duration
            )
        
        else:
            # Simple informational response
            response = _generate_simple_response(intent, request.message)
            
            # Apply personality
            response = identity_keeper.apply_personality(
                raw_response=response,
                context={"requires_approval": False}
            )
            
            return ChatResponse(
                response=response,
                requires_approval=False
            )
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/approve")
async def approve_action(request: ApprovalRequest):
    """
    Approve or reject a pending action.
    """
    try:
        # Approve decision
        approved = decision_engine.approve_decision(
            action_id=request.action_id,
            user_confirmation=request.approved
        )
        
        if not approved:
            return {
                "success": False,
                "message": "Action rejected or not found"
            }
        
        # Execute if approved
        if request.approved:
            result = decision_engine.execute_decision(request.action_id)
            
            response = f"""✅ Action approved and executing!

{result.get('message', 'Execution started')}

You can track progress through the agent ecosystem."""
            
            # Apply personality
            response = identity_keeper.apply_personality(
                raw_response=response,
                context={"execution_started": True}
            )
            
            return {
                "success": True,
                "message": response,
                "execution_result": result
            }
        else:
            return {
                "success": True,
                "message": "Action rejected successfully"
            }
    
    except Exception as e:
        logger.error(f"Approval error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/decompose")
async def decompose_goal(request: TaskDecompositionRequest):
    """
    Decompose a complex goal into micro-tasks.
    """
    try:
        tasks = task_decomposer.decompose(
            goal=request.goal,
            context=request.context,
            max_tasks=request.max_tasks
        )
        
        stats = task_decomposer.get_task_stats(tasks)
        
        return {
            "success": True,
            "goal": request.goal,
            "total_tasks": len(tasks),
            "stats": stats,
            "parallelizable_tasks": stats["parallelizable"],
            "task_preview": [
                {
                    "id": t.task_id,
                    "type": t.task_type,
                    "description": t.description,
                    "priority": t.priority.value,
                    "dependencies": len(t.dependencies)
                }
                for t in tasks[:20]  # Show first 20
            ]
        }
    
    except Exception as e:
        logger.error(f"Decomposition error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compose")
async def compose_outputs(request: AgentOutputRequest):
    """
    Compose multiple agent outputs into unified response.
    """
    try:
        # Convert dict outputs to AgentOutput objects
        agent_outputs = [
            AgentOutput(
                agent_id=o.get("agent_id", "unknown"),
                agent_type=o.get("agent_type", "generic"),
                output=o.get("output"),
                confidence=o.get("confidence", 0.5),
                processing_time=o.get("processing_time", 0.0)
            )
            for o in request.outputs
        ]
        
        # Compose outputs
        composed = output_composer.compose(agent_outputs, request.strategy)
        
        # Validate
        is_valid = output_composer.validate_output(composed)
        
        # Format for user
        formatted = output_composer.format_for_user(composed)
        
        return {
            "success": composed.get("success", False),
            "composed_output": composed,
            "formatted_response": formatted,
            "is_valid": is_valid,
            "metadata": composed.get("meta", {})
        }
    
    except Exception as e:
        logger.error(f"Composition error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/decisions")
async def get_pending_decisions():
    """
    Get all pending decisions requiring approval.
    """
    try:
        pending = decision_engine.get_pending_decisions()
        return {
            "success": True,
            "count": len(pending),
            "decisions": pending
        }
    except Exception as e:
        logger.error(f"Get decisions error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_statistics():
    """
    Get Supreme Brain statistics.
    """
    try:
        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "identity": identity_keeper.get_personality_stats(),
            "decisions": decision_engine.get_decision_stats(),
            "service_info": {
                "name": "Supreme Brain",
                "version": "1.0.0",
                "port": 5010
            }
        }
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions
def _parse_intent(message: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse user intent from message.
    In production, this would use GPT-4/Claude for understanding.
    """
    message_lower = message.lower()
    
    # Action keywords
    action_keywords = [
        "generate", "create", "build", "scan", "find", "search",
        "analyze", "process", "learn", "train", "optimize"
    ]
    
    requires_action = any(keyword in message_lower for keyword in action_keywords)
    
    # Determine intent type
    if any(word in message_lower for word in ["image", "picture", "photo"]):
        intent_type = "image_generation"
    elif any(word in message_lower for word in ["video", "animation"]):
        intent_type = "video_generation"
    elif any(word in message_lower for word in ["scan", "scout", "discover"]):
        intent_type = "tech_scouting"
    elif any(word in message_lower for word in ["learn", "study", "research"]):
        intent_type = "learning"
    elif any(word in message_lower for word in ["analyze", "data"]):
        intent_type = "data_analysis"
    else:
        intent_type = "general"
    
    return {
        "type": intent_type,
        "requires_action": requires_action,
        "original_message": message,
        "context": context
    }


def _generate_simple_response(intent: Dict[str, Any], message: str) -> str:
    """Generate simple response for non-action intents."""
    responses = {
        "greeting": "Hello! I'm VOBee, ready to help with complex AI tasks.",
        "status": "All systems operational. I can decompose goals, scout tech, generate media, and more.",
        "capabilities": "I can break down complex goals into 2000+ parallel tasks, scout new technologies, generate media, optimize costs, and continuously learn.",
        "default": f"I understand you're asking about: {message}\n\nI'm here to help with complex AI orchestration tasks. What would you like me to do?"
    }
    
    message_lower = message.lower()
    if any(word in message_lower for word in ["hello", "hi", "hey"]):
        return responses["greeting"]
    elif any(word in message_lower for word in ["status", "health"]):
        return responses["status"]
    elif any(word in message_lower for word in ["what can you", "capabilities", "help"]):
        return responses["capabilities"]
    else:
        return responses["default"]


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5010"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
