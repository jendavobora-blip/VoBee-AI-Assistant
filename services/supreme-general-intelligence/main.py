"""
Supreme General Intelligence (SGI) Service
Primary chat interface with intent understanding, action confirmation, and logging
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
import json
import os
import hashlib
from uuid import uuid4
import asyncpg
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL', 
    'postgresql://orchestrator:password@postgres:5432/orchestrator_db'
)

# Owner authentication
OWNER_SECRET = os.getenv('OWNER_SECRET')
if not OWNER_SECRET or OWNER_SECRET == 'your_secure_owner_secret_key':
    logger.error("OWNER_SECRET not configured! Set a secure value in environment variables.")
    raise ValueError("OWNER_SECRET must be set to a secure value. Please configure it in .env file.")

OWNER_SECRET_HASH = hashlib.sha256(OWNER_SECRET.encode()).hexdigest()

# Database connection pool
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    global db_pool
    # Startup
    try:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        logger.info("Database connection pool created")
        await init_database()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    yield
    
    # Shutdown
    if db_pool:
        await db_pool.close()
        logger.info("Database connection pool closed")

app = FastAPI(
    title="Supreme General Intelligence Interface",
    description="Primary chat interface with intent understanding and action confirmation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatMessage(BaseModel):
    message: str = Field(..., description="User message/command")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

class Intent(BaseModel):
    type: str = Field(..., description="Intent type (query, action, command)")
    action: Optional[str] = Field(None, description="Specific action to perform")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Action parameters")
    confidence: float = Field(..., description="Confidence score 0-1")

class ActionConfirmation(BaseModel):
    action_id: str = Field(..., description="Unique action identifier")
    confirmed: bool = Field(..., description="Whether action is confirmed")
    modifications: Optional[Dict[str, Any]] = Field(None, description="Any modifications to parameters")

class ActionSummary(BaseModel):
    action_id: str
    intent: Intent
    summary: str
    estimated_resources: Optional[Dict[str, Any]] = None
    risks: Optional[List[str]] = None
    requires_confirmation: bool = True

class ExecutionResult(BaseModel):
    action_id: str
    status: str  # success, failed, pending
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str
    logs: List[str] = []

class LogEntry(BaseModel):
    log_id: Optional[str] = None
    action_id: str
    level: str  # info, warning, error, debug
    message: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

# Authentication
async def verify_owner(x_owner_secret: str = Header(...)):
    """Verify owner-only access"""
    secret_hash = hashlib.sha256(x_owner_secret.encode()).hexdigest()
    if secret_hash != OWNER_SECRET_HASH:
        raise HTTPException(status_code=403, detail="Unauthorized: Owner access required")
    return True

# Database functions
async def init_database():
    """Initialize database tables"""
    if not db_pool:
        return
    
    async with db_pool.acquire() as conn:
        # Create actions table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS sgi_actions (
                action_id VARCHAR(255) PRIMARY KEY,
                intent JSONB NOT NULL,
                summary TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                confirmed BOOLEAN DEFAULT FALSE,
                result JSONB,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                executed_at TIMESTAMP
            )
        ''')
        
        # Create logs table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS sgi_logs (
                log_id VARCHAR(255) PRIMARY KEY,
                action_id VARCHAR(255) REFERENCES sgi_actions(action_id),
                level VARCHAR(20) NOT NULL,
                message TEXT NOT NULL,
                metadata JSONB,
                timestamp TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # Create conversations table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS sgi_conversations (
                conversation_id VARCHAR(255) PRIMARY KEY,
                messages JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        logger.info("Database tables initialized")

async def store_action(action_id: str, intent: Intent, summary: str):
    """Store action in database"""
    if not db_pool:
        return
    
    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO sgi_actions (action_id, intent, summary, status)
            VALUES ($1, $2, $3, 'pending')
        ''', action_id, json.dumps(intent.dict()), summary)

async def update_action_status(action_id: str, status: str, confirmed: bool = False, 
                               result: Optional[Dict] = None):
    """Update action status"""
    if not db_pool:
        return
    
    async with db_pool.acquire() as conn:
        await conn.execute('''
            UPDATE sgi_actions 
            SET status = $1, confirmed = $2, result = $3, updated_at = NOW()
            WHERE action_id = $4
        ''', status, confirmed, json.dumps(result) if result else None, action_id)

async def store_log(log_entry: LogEntry):
    """Store log entry in database"""
    if not db_pool:
        return
    
    log_id = log_entry.log_id or str(uuid4())
    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO sgi_logs (log_id, action_id, level, message, metadata)
            VALUES ($1, $2, $3, $4, $5)
        ''', log_id, log_entry.action_id, log_entry.level, log_entry.message, 
        json.dumps(log_entry.metadata) if log_entry.metadata else None)

async def get_action_logs(action_id: str) -> List[Dict]:
    """Retrieve logs for a specific action"""
    if not db_pool:
        return []
    
    async with db_pool.acquire() as conn:
        rows = await conn.fetch('''
            SELECT log_id, level, message, metadata, timestamp
            FROM sgi_logs
            WHERE action_id = $1
            ORDER BY timestamp ASC
        ''', action_id)
        
        return [dict(row) for row in rows]

# Intent understanding
def analyze_intent(message: str) -> Intent:
    """
    Analyze user message to understand intent
    Uses keyword matching and pattern recognition
    """
    message_lower = message.lower()
    
    # Action keywords
    action_keywords = {
        'generate': ['generate', 'create', 'make', 'produce'],
        'predict': ['predict', 'forecast', 'estimate'],
        'analyze': ['analyze', 'examine', 'inspect', 'check'],
        'scan': ['scan', 'search', 'find', 'discover', 'scout'],
        'deploy': ['deploy', 'launch', 'start', 'run'],
        'monitor': ['monitor', 'watch', 'track'],
        'repair': ['repair', 'fix', 'heal', 'restore']
    }
    
    # Entity keywords
    entity_keywords = {
        'image': ['image', 'picture', 'photo', 'visual'],
        'video': ['video', 'movie', 'clip', 'animation'],
        'crypto': ['crypto', 'bitcoin', 'ethereum', 'btc', 'eth', 'cryptocurrency'],
        'github': ['github', 'repository', 'repo', 'code'],
        'research': ['research', 'paper', 'arxiv', 'study'],
        'fraud': ['fraud', 'security', 'threat', 'anomaly']
    }
    
    detected_action = None
    detected_entity = None
    confidence = 0.5  # Base confidence
    
    # Detect action
    for action, keywords in action_keywords.items():
        if any(kw in message_lower for kw in keywords):
            detected_action = action
            confidence += 0.2
            break
    
    # Detect entity
    for entity, keywords in entity_keywords.items():
        if any(kw in message_lower for kw in keywords):
            detected_entity = entity
            confidence += 0.2
            break
    
    # Determine intent type
    if detected_action and detected_entity:
        intent_type = "action"
        action_str = f"{detected_action}_{detected_entity}"
        confidence = min(0.95, confidence)
    elif detected_action:
        intent_type = "command"
        action_str = detected_action
    elif '?' in message:
        intent_type = "query"
        action_str = None
    else:
        intent_type = "query"
        action_str = None
        confidence = 0.3
    
    # Extract parameters (simple extraction)
    parameters = {}
    if detected_entity == 'crypto':
        # Try to extract crypto symbol
        symbols = ['btc', 'eth', 'bitcoin', 'ethereum']
        for symbol in symbols:
            if symbol in message_lower:
                parameters['symbol'] = symbol.upper() if len(symbol) <= 3 else symbol.capitalize()
                break
    
    return Intent(
        type=intent_type,
        action=action_str,
        parameters=parameters,
        confidence=confidence
    )

def generate_action_summary(intent: Intent, message: str) -> str:
    """Generate human-readable action summary"""
    if intent.type == "query":
        return f"This appears to be a query: '{message}'. No action required."
    
    action_descriptions = {
        'generate_image': 'Generate an image based on your prompt',
        'generate_video': 'Generate a video based on your description',
        'predict_crypto': 'Predict cryptocurrency price movements',
        'analyze_fraud': 'Analyze data for fraud detection',
        'scan_github': 'Scan GitHub repositories for relevant projects',
        'scan_research': 'Search for relevant research papers',
        'deploy': 'Deploy a service or component',
        'monitor': 'Monitor system health and performance',
        'repair': 'Attempt to repair detected issues'
    }
    
    base_summary = action_descriptions.get(
        intent.action, 
        f"Execute action: {intent.action}"
    )
    
    if intent.parameters:
        params_str = ', '.join([f"{k}={v}" for k, v in intent.parameters.items()])
        return f"{base_summary} with parameters: {params_str}"
    
    return base_summary

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if db_pool else "disconnected"
    return {
        "status": "healthy",
        "service": "supreme-general-intelligence",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/chat", dependencies=[Depends(verify_owner)])
async def chat(message: ChatMessage) -> Dict[str, Any]:
    """
    Process user message and understand intent
    Returns intent analysis and action summary for confirmation
    """
    try:
        # Analyze intent
        intent = analyze_intent(message.message)
        
        # Generate action summary
        summary = generate_action_summary(intent, message.message)
        
        # Create action if it requires execution
        action_id = None
        requires_confirmation = intent.type in ["action", "command"]
        
        if requires_confirmation:
            action_id = str(uuid4())
            await store_action(action_id, intent, summary)
            
            # Log the action creation
            await store_log(LogEntry(
                action_id=action_id,
                level="info",
                message=f"Action created: {summary}",
                metadata={"intent": intent.dict()}
            ))
        
        response = {
            "message": "I understand your request.",
            "intent": intent.dict(),
            "summary": summary,
            "requires_confirmation": requires_confirmation
        }
        
        if action_id:
            response["action_id"] = action_id
            response["next_step"] = f"Please confirm this action using POST /confirm with action_id: {action_id}"
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/confirm", dependencies=[Depends(verify_owner)])
async def confirm_action(confirmation: ActionConfirmation) -> ExecutionResult:
    """
    Confirm and execute an action
    This is where the actual work happens after user confirmation
    """
    try:
        action_id = confirmation.action_id
        
        if not confirmation.confirmed:
            await update_action_status(action_id, "cancelled")
            await store_log(LogEntry(
                action_id=action_id,
                level="info",
                message="Action cancelled by user"
            ))
            return ExecutionResult(
                action_id=action_id,
                status="cancelled",
                timestamp=datetime.utcnow().isoformat(),
                logs=["Action cancelled"]
            )
        
        # Get action details from database
        if db_pool:
            async with db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    'SELECT intent, summary FROM sgi_actions WHERE action_id = $1',
                    action_id
                )
                if not row:
                    raise HTTPException(status_code=404, detail="Action not found")
                
                intent_data = json.loads(row['intent'])
                intent = Intent(**intent_data)
        else:
            raise HTTPException(status_code=503, detail="Database unavailable")
        
        # Update status to executing
        await update_action_status(action_id, "executing", confirmed=True)
        await store_log(LogEntry(
            action_id=action_id,
            level="info",
            message="Action execution started"
        ))
        
        # Execute action (delegate to appropriate service)
        result = await execute_action(action_id, intent, confirmation.modifications)
        
        # Update final status
        await update_action_status(action_id, "completed", confirmed=True, result=result)
        await store_log(LogEntry(
            action_id=action_id,
            level="info",
            message="Action completed successfully",
            metadata={"result": result}
        ))
        
        # Get all logs
        logs = await get_action_logs(action_id)
        log_messages = [log['message'] for log in logs]
        
        return ExecutionResult(
            action_id=action_id,
            status="success",
            result=result,
            timestamp=datetime.utcnow().isoformat(),
            logs=log_messages
        )
        
    except Exception as e:
        logger.error(f"Error executing action: {e}")
        
        # Log the error
        if 'action_id' in locals():
            await update_action_status(action_id, "failed")
            await store_log(LogEntry(
                action_id=action_id,
                level="error",
                message=f"Action failed: {str(e)}"
            ))
        
        raise HTTPException(status_code=500, detail=str(e))

async def execute_action(action_id: str, intent: Intent, 
                        modifications: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Execute the actual action by delegating to appropriate services
    """
    import httpx
    
    # Service URLs
    services = {
        'orchestrator': os.getenv('ORCHESTRATOR_URL', 'http://orchestrator:5003'),
        'spy_orchestration': os.getenv('SPY_ORCHESTRATION_URL', 'http://spy-orchestration:5006'),
    }
    
    # Apply modifications if provided
    parameters = intent.parameters.copy()
    if modifications:
        parameters.update(modifications)
    
    await store_log(LogEntry(
        action_id=action_id,
        level="debug",
        message=f"Executing action: {intent.action}",
        metadata={"parameters": parameters}
    ))
    
    # Route to appropriate service based on action
    if intent.action and intent.action.startswith('scan_'):
        # Route to spy-orchestration service
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{services['spy_orchestration']}/scan",
                json={
                    "scan_type": intent.action.replace('scan_', ''),
                    "parameters": parameters
                },
                timeout=300.0
            )
            return response.json()
    
    elif intent.action in ['generate_image', 'generate_video', 'predict_crypto']:
        # Route through orchestrator
        async with httpx.AsyncClient() as client:
            task_type = intent.action.replace('generate_', '').replace('predict_', '')
            response = await client.post(
                f"{services['orchestrator']}/orchestrate",
                json={
                    "tasks": [{
                        "type": f"{task_type}_generation" if 'generate' in intent.action else f"{task_type}_prediction",
                        "params": parameters
                    }],
                    "priority": "high"
                },
                timeout=600.0
            )
            return response.json()
    
    else:
        # Generic action execution
        return {
            "message": f"Action '{intent.action}' acknowledged",
            "parameters": parameters,
            "note": "Action execution simulated - integrate with actual services"
        }

@app.get("/logs/{action_id}", dependencies=[Depends(verify_owner)])
async def get_logs(action_id: str) -> List[Dict]:
    """Retrieve all logs for a specific action"""
    try:
        logs = await get_action_logs(action_id)
        return logs
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/actions", dependencies=[Depends(verify_owner)])
async def list_actions(limit: int = 50, status: Optional[str] = None) -> List[Dict]:
    """List all actions with optional status filter"""
    try:
        if not db_pool:
            raise HTTPException(status_code=503, detail="Database unavailable")
        
        async with db_pool.acquire() as conn:
            if status:
                rows = await conn.fetch('''
                    SELECT action_id, intent, summary, status, confirmed, created_at, updated_at
                    FROM sgi_actions
                    WHERE status = $1
                    ORDER BY created_at DESC
                    LIMIT $2
                ''', status, limit)
            else:
                rows = await conn.fetch('''
                    SELECT action_id, intent, summary, status, confirmed, created_at, updated_at
                    FROM sgi_actions
                    ORDER BY created_at DESC
                    LIMIT $1
                ''', limit)
            
            return [dict(row) for row in rows]
    
    except Exception as e:
        logger.error(f"Error listing actions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/action/{action_id}", dependencies=[Depends(verify_owner)])
async def get_action(action_id: str) -> Dict:
    """Get details of a specific action"""
    try:
        if not db_pool:
            raise HTTPException(status_code=503, detail="Database unavailable")
        
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow('''
                SELECT * FROM sgi_actions WHERE action_id = $1
            ''', action_id)
            
            if not row:
                raise HTTPException(status_code=404, detail="Action not found")
            
            return dict(row)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving action: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5010)
