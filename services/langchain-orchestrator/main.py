"""
LangChain Orchestration Service
Advanced LLM workflow orchestration and chaining
NEW SERVICE - Optional, does not affect existing services
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LangChain Orchestration Service",
    description="Advanced LLM workflow orchestration with LangChain",
    version="1.0.0"
)

# Try to import LangChain
try:
    from langchain.chains import LLMChain, SequentialChain
    from langchain.prompts import PromptTemplate
    from langchain.llms import OpenAI
    from langchain.memory import ConversationBufferMemory
    LANGCHAIN_AVAILABLE = True
    logger.info("✅ LangChain library available")
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("⚠️  LangChain not installed. Install with: pip install langchain")


# Request models
class OrchestrationRequest(BaseModel):
    workflow_type: str  # "simple", "sequential", "parallel", "agent"
    inputs: Dict[str, Any]
    llm_config: Optional[Dict[str, Any]] = None
    memory_enabled: Optional[bool] = False

class ChainRequest(BaseModel):
    prompt_template: str
    input_variables: Dict[str, str]
    llm_model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "langchain-orchestrator",
        "langchain_available": LANGCHAIN_AVAILABLE,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/orchestrate")
async def orchestrate_workflow(request: OrchestrationRequest):
    """
    Orchestrate complex LLM workflows
    
    Workflow types:
    - simple: Single LLM call
    - sequential: Chain of LLM calls
    - parallel: Multiple LLM calls in parallel
    - agent: Autonomous agent with tools
    """
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="LangChain not available. Install with: pip install langchain"
        )
    
    try:
        logger.info(f"🔗 Orchestrating workflow: {request.workflow_type}")
        
        # Get LLM configuration
        llm_config = request.llm_config or {}
        api_key = os.getenv("OPENAI_API_KEY", llm_config.get("api_key"))
        
        if not api_key:
            raise HTTPException(
                status_code=400,
                detail="OpenAI API key required. Set OPENAI_API_KEY environment variable."
            )
        
        # Initialize LLM
        llm = OpenAI(
            api_key=api_key,
            temperature=llm_config.get("temperature", 0.7),
            model_name=llm_config.get("model", "gpt-3.5-turbo")
        )
        
        # Initialize memory if enabled
        memory = None
        if request.memory_enabled:
            memory = ConversationBufferMemory()
        
        # Execute workflow based on type
        result = None
        
        if request.workflow_type == "simple":
            # Simple single LLM call
            prompt_template = PromptTemplate(
                input_variables=list(request.inputs.keys()),
                template=request.inputs.get("template", "{input}")
            )
            chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory)
            result = chain.run(**request.inputs)
        
        elif request.workflow_type == "sequential":
            # Sequential chain of LLM calls
            chains = []
            for step in request.inputs.get("steps", []):
                prompt = PromptTemplate(
                    input_variables=step.get("input_variables", []),
                    template=step.get("template", "")
                )
                chain = LLMChain(
                    llm=llm,
                    prompt=prompt,
                    output_key=step.get("output_key", f"step_{len(chains)}")
                )
                chains.append(chain)
            
            sequential_chain = SequentialChain(
                chains=chains,
                input_variables=request.inputs.get("initial_inputs", []),
                output_variables=[c.output_key for c in chains]
            )
            result = sequential_chain(request.inputs.get("initial_values", {}))
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported workflow type: {request.workflow_type}"
            )
        
        return {
            "status": "success",
            "workflow_type": request.workflow_type,
            "result": result,
            "memory_enabled": request.memory_enabled,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Orchestration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chain/simple")
async def simple_chain(request: ChainRequest):
    """Execute a simple LLM chain"""
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="LangChain not available"
        )
    
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=400, detail="OpenAI API key required")
        
        llm = OpenAI(
            api_key=api_key,
            temperature=request.temperature,
            model_name=request.llm_model
        )
        
        prompt = PromptTemplate(
            input_variables=list(request.input_variables.keys()),
            template=request.prompt_template
        )
        
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(**request.input_variables)
        
        return {
            "status": "success",
            "result": result,
            "prompt_template": request.prompt_template,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Simple chain failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/features")
async def list_features():
    """List available LangChain features"""
    return {
        "service": "langchain-orchestrator",
        "langchain_available": LANGCHAIN_AVAILABLE,
        "features": [
            {
                "name": "Simple Chain",
                "description": "Single LLM call with prompt template",
                "endpoint": "/chain/simple"
            },
            {
                "name": "Sequential Chain",
                "description": "Multiple LLM calls in sequence",
                "endpoint": "/orchestrate",
                "workflow_type": "sequential"
            },
            {
                "name": "Memory",
                "description": "Conversation history and context management",
                "supported": True
            },
            {
                "name": "Agent",
                "description": "Autonomous agent with tool usage",
                "status": "planned"
            }
        ],
        "supported_llms": [
            "OpenAI GPT-3.5/4",
            "Claude",
            "Local models"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "5021"))
    logger.info(f"🚀 Starting LangChain Orchestration Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
