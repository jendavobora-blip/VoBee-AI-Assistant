"""
Vobio AI Studio - Integrated API Server
Complete production-ready implementation with all runtime contracts
"""

import os
import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn

# Import all modules
from telemetry import setup_telemetry, get_tracer
from feature_gates import get_feature_gates
from identity import get_identity_manager
from memory_service import get_memory_service
from cost_tracker import get_cost_tracker
from safety_system import get_safety_system
from human_approval import get_approval_queue, ApprovalStatus
from ai_orchestrator import get_orchestrator
from lifesync_module import get_lifesync_module

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Vobio AI Studio API",
    description="Production-ready AI orchestration with safety, observability, and human approval",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
tracer = None
feature_gates = None
identity_manager = None
memory_service = None
cost_tracker = None
safety_system = None
approval_queue = None
orchestrator = None
lifesync_module = None


@app.on_event("startup")
async def startup_event():
    """Initialize all services on startup"""
    global tracer, feature_gates, identity_manager, memory_service
    global cost_tracker, safety_system, approval_queue, orchestrator, lifesync_module
    
    logger.info("Starting Vobio AI Studio API...")
    
    # Setup telemetry
    tracer, _ = setup_telemetry(app)
    
    # Initialize services
    feature_gates = get_feature_gates()
    identity_manager = get_identity_manager()
    memory_service = get_memory_service()
    cost_tracker = get_cost_tracker()
    safety_system = get_safety_system()
    approval_queue = get_approval_queue()
    orchestrator = get_orchestrator()
    lifesync_module = get_lifesync_module()
    
    logger.info("All services initialized successfully")
    logger.info(f"Feature flags: {feature_gates.get_features_status()}")


# Request/Response Models
class LoginRequest(BaseModel):
    username: str
    credential_data: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    message: str


class ImageGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "realistic"


class VideoGenerationRequest(BaseModel):
    prompt: str
    duration: Optional[int] = 5


class LifeSyncRequest(BaseModel):
    scenario: str
    options: List[str]
    user_context: Optional[Dict[str, Any]] = None


class ApprovalReviewRequest(BaseModel):
    action: str  # "approve" or "reject"
    comment: Optional[str] = None


class CodeValidationRequest(BaseModel):
    code: str


# Dependency for user authentication
async def get_current_user(x_user_id: Optional[str] = Header(None)) -> str:
    """Extract user_id from header"""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing X-User-ID header")
    return x_user_id


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "vobio-api",
        "features": feature_gates.get_features_status() if feature_gates else {}
    }


# Authentication endpoints
@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """Mock passkey login"""
    try:
        credential_data = request.credential_data or {}
        credential_data["username"] = request.username
        
        result = identity_manager.authenticate_passkey(credential_data)
        
        return {
            "status": "success",
            "user": result["user"],
            "token": result["token"],
            "expires_in": result["expires_in"]
        }
    
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/logout")
async def logout(user_id: str = Depends(get_current_user)):
    """Logout user"""
    # In a real system, would invalidate token
    return {"status": "success", "message": "Logged out"}


# AI Operations
@app.post("/api/chat")
async def chat(request: ChatRequest, user_id: str = Depends(get_current_user)):
    """Chat with AI assistant"""
    
    # Check cost limits
    limit_check = cost_tracker.check_limits(user_id)
    if not limit_check["allowed"]:
        raise HTTPException(status_code=429, detail=limit_check["reason"])
    
    # Execute through orchestrator
    result = await orchestrator.execute(
        operation="chat",
        user_id=user_id,
        input_data={"message": request.message}
    )
    
    # Track cost
    cost = result.get("cost", 0.005)
    cost_tracker.track_request(user_id, "chat", cost, {"message_length": len(request.message)})
    
    # Store in memory
    memory_service.store_memory(user_id, f"User asked: {request.message}")
    
    return result


@app.post("/api/generate/image")
async def generate_image(request: ImageGenerationRequest, user_id: str = Depends(get_current_user)):
    """Generate image"""
    
    if not feature_gates.is_enabled("enable_image_generation"):
        raise HTTPException(status_code=403, detail="Image generation is disabled")
    
    # Check cost limits
    limit_check = cost_tracker.check_limits(user_id)
    if not limit_check["allowed"]:
        raise HTTPException(status_code=429, detail=limit_check["reason"])
    
    # Safety check
    safety_check = safety_system.validate_api_call("/api/generate/image", "POST", request.dict())
    if not safety_check["allowed"]:
        raise HTTPException(status_code=400, detail=f"Safety check failed: {safety_check['issues']}")
    
    # Execute
    result = await orchestrator.execute(
        operation="generate_image",
        user_id=user_id,
        input_data=request.dict()
    )
    
    # Track cost
    cost = result.get("cost", 0.02)
    cost_tracker.track_request(user_id, "generate_image", cost, {"prompt": request.prompt})
    
    return result


@app.post("/api/generate/video")
async def generate_video(request: VideoGenerationRequest, user_id: str = Depends(get_current_user)):
    """Generate video"""
    
    if not feature_gates.is_enabled("enable_video_generation"):
        raise HTTPException(status_code=403, detail="Video generation is disabled")
    
    # Check cost limits
    limit_check = cost_tracker.check_limits(user_id)
    if not limit_check["allowed"]:
        raise HTTPException(status_code=429, detail=limit_check["reason"])
    
    # Execute
    result = await orchestrator.execute(
        operation="generate_video",
        user_id=user_id,
        input_data=request.dict()
    )
    
    # Track cost
    cost = result.get("cost", 0.10)
    cost_tracker.track_request(user_id, "generate_video", cost, {"prompt": request.prompt})
    
    return result


@app.post("/api/lifesync/decision")
async def lifesync_decision(request: LifeSyncRequest, user_id: str = Depends(get_current_user)):
    """LifeSync decision assistant"""
    
    if not feature_gates.is_enabled("enable_lifesync"):
        raise HTTPException(status_code=403, detail="LifeSync is disabled")
    
    # Check cost limits
    limit_check = cost_tracker.check_limits(user_id)
    if not limit_check["allowed"]:
        raise HTTPException(status_code=429, detail=limit_check["reason"])
    
    # Analyze decision
    result = lifesync_module.analyze_decision(
        scenario=request.scenario,
        options=request.options,
        user_context=request.user_context
    )
    
    # Track cost
    cost = 0.01
    cost_tracker.track_request(user_id, "lifesync_decision", cost, {"scenario": request.scenario})
    
    return result


# Code validation endpoint
@app.post("/api/safety/validate-code")
async def validate_code(request: CodeValidationRequest, user_id: str = Depends(get_current_user)):
    """Validate code for safety"""
    
    validation = safety_system.validate_code(request.code)
    
    # If requires approval, create request
    if validation.get("requires_approval") and feature_gates.is_enabled("enable_human_approval"):
        approval_request = approval_queue.create_request(
            user_id=user_id,
            operation_type="code_execution",
            operation_data={"code": request.code},
            risk_level=validation["risk_level"],
            reason=f"Code validation issues: {', '.join(validation['issues'])}"
        )
        
        validation["approval_request_id"] = approval_request.request_id
    
    return validation


# Human approval endpoints
@app.get("/api/approvals/pending")
async def get_pending_approvals(user_id: str = Depends(get_current_user)):
    """Get pending approval requests"""
    
    pending = approval_queue.get_pending_requests(user_id)
    
    return {
        "status": "success",
        "count": len(pending),
        "requests": [req.to_dict() for req in pending]
    }


@app.post("/api/approvals/{request_id}")
async def review_approval(
    request_id: str, 
    review: ApprovalReviewRequest,
    user_id: str = Depends(get_current_user)
):
    """Approve or reject a request"""
    
    if review.action == "approve":
        success = approval_queue.approve_request(request_id, user_id, review.comment)
    elif review.action == "reject":
        success = approval_queue.reject_request(request_id, user_id, review.comment)
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    if not success:
        raise HTTPException(status_code=404, detail="Request not found or already processed")
    
    return {"status": "success", "action": review.action}


# Cost tracking endpoints
@app.get("/api/costs/usage")
async def get_usage(user_id: str = Depends(get_current_user)):
    """Get user cost usage"""
    
    usage = cost_tracker.get_user_usage(user_id)
    return usage


@app.get("/api/costs/limits")
async def get_limits(user_id: str = Depends(get_current_user)):
    """Check cost limits"""
    
    limits = cost_tracker.check_limits(user_id)
    return limits


# Memory endpoints
@app.get("/api/memory/context")
async def get_context(user_id: str = Depends(get_current_user)):
    """Get user context from memory"""
    
    context = memory_service.get_user_context(user_id)
    return {"status": "success", "context": context}


@app.post("/api/memory/store")
async def store_memory(
    memory: Dict[str, Any],
    user_id: str = Depends(get_current_user)
):
    """Store a memory"""
    
    success = memory_service.store_memory(
        user_id=user_id,
        memory=memory.get("content", ""),
        metadata=memory.get("metadata")
    )
    
    return {"status": "success" if success else "error"}


# Feature flags endpoint
@app.get("/api/features")
async def get_features():
    """Get feature flag status"""
    return {
        "status": "success",
        "features": feature_gates.get_features_status()
    }


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global error handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": "Internal server error"}
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "api_server_integrated:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
