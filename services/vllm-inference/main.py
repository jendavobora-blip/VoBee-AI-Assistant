"""
vLLM Ultra-Fast LLM Inference Service
Provides 24x faster inference than traditional methods
NEW SERVICE - Optional, does not affect existing services
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="vLLM Fast Inference Service",
    description="Ultra-fast large language model inference with PagedAttention",
    version="1.0.0"
)

# Try to import vLLM
try:
    from vllm import LLM, SamplingParams
    VLLM_AVAILABLE = True
    logger.info("✅ vLLM library available")
except ImportError:
    VLLM_AVAILABLE = False
    logger.warning("⚠️  vLLM not installed. Install with: pip install vllm")
    # Mock classes for when vLLM is not available
    class LLM:
        def __init__(self, *args, **kwargs):
            pass
        def generate(self, *args, **kwargs):
            return []
    class SamplingParams:
        def __init__(self, *args, **kwargs):
            pass


# Configuration
MODEL_NAME = os.getenv("VLLM_MODEL", "meta-llama/Llama-3-8b")
MAX_MODEL_LEN = int(os.getenv("VLLM_MAX_MODEL_LEN", "4096"))
TENSOR_PARALLEL_SIZE = int(os.getenv("VLLM_TENSOR_PARALLEL", "1"))

# Request models
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = 50
    stop: Optional[List[str]] = None

class BatchGenerateRequest(BaseModel):
    prompts: List[str]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = 50


# Initialize vLLM model (lazy loading)
llm_model = None

def get_model():
    """Lazy load vLLM model"""
    global llm_model
    
    if llm_model is None:
        if not VLLM_AVAILABLE:
            raise RuntimeError(
                "vLLM not available. Install with: pip install vllm\n"
                "Or use legacy inference endpoints."
            )
        
        logger.info("=" * 60)
        logger.info(f"🚀 Loading vLLM model: {MODEL_NAME}")
        logger.info(f"   Max model length: {MAX_MODEL_LEN}")
        logger.info(f"   Tensor parallel size: {TENSOR_PARALLEL_SIZE}")
        logger.info("=" * 60)
        
        try:
            llm_model = LLM(
                model=MODEL_NAME,
                max_model_len=MAX_MODEL_LEN,
                tensor_parallel_size=TENSOR_PARALLEL_SIZE,
                trust_remote_code=True
            )
            logger.info("✅ vLLM model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load vLLM model: {e}")
            raise
    
    return llm_model


@app.on_event("startup")
async def startup_event():
    """Initialize model on startup (optional)"""
    if VLLM_AVAILABLE and os.getenv("PRELOAD_MODEL", "false").lower() == "true":
        try:
            get_model()
        except Exception as e:
            logger.warning(f"Model preload failed: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "vllm-inference",
        "vllm_available": VLLM_AVAILABLE,
        "model": MODEL_NAME,
        "model_loaded": llm_model is not None,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/v2/generate")
async def generate_fast(request: GenerateRequest):
    """
    Ultra-fast text generation endpoint
    
    Features:
    - 24x faster than traditional inference
    - PagedAttention for efficient memory use
    - Continuous batching
    
    Fallback: Returns 501 if vLLM not available
    """
    if not VLLM_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="vLLM not available. Use V1 API endpoint or install vLLM."
        )
    
    try:
        # Get model
        llm = get_model()
        
        # Configure sampling parameters
        sampling_params = SamplingParams(
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            max_tokens=request.max_tokens,
            stop=request.stop
        )
        
        # Generate
        start_time = datetime.utcnow()
        outputs = llm.generate([request.prompt], sampling_params)
        end_time = datetime.utcnow()
        
        # Extract result
        generated_text = outputs[0].outputs[0].text
        
        # Calculate metrics
        generation_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            "status": "success",
            "generated_text": generated_text,
            "prompt": request.prompt,
            "model": MODEL_NAME,
            "generation_time_ms": generation_time_ms,
            "tokens_generated": len(outputs[0].outputs[0].token_ids),
            "metadata": {
                "temperature": request.temperature,
                "top_p": request.top_p,
                "top_k": request.top_k,
                "vllm_optimized": True
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v2/generate/batch")
async def generate_batch(request: BatchGenerateRequest):
    """
    Batch generation for multiple prompts
    
    Benefits:
    - Process multiple prompts in parallel
    - Continuous batching optimization
    - Significant speedup for batch workloads
    """
    if not VLLM_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="vLLM not available. Use V1 API endpoint or install vLLM."
        )
    
    try:
        llm = get_model()
        
        sampling_params = SamplingParams(
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            max_tokens=request.max_tokens
        )
        
        start_time = datetime.utcnow()
        outputs = llm.generate(request.prompts, sampling_params)
        end_time = datetime.utcnow()
        
        # Extract results
        results = []
        for i, output in enumerate(outputs):
            results.append({
                "prompt": request.prompts[i],
                "generated_text": output.outputs[0].text,
                "tokens_generated": len(output.outputs[0].token_ids)
            })
        
        generation_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            "status": "success",
            "results": results,
            "batch_size": len(request.prompts),
            "total_generation_time_ms": generation_time_ms,
            "avg_time_per_prompt_ms": generation_time_ms / len(request.prompts),
            "model": MODEL_NAME,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Batch generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model/info")
async def model_info():
    """Get information about the loaded model"""
    return {
        "model_name": MODEL_NAME,
        "max_model_len": MAX_MODEL_LEN,
        "tensor_parallel_size": TENSOR_PARALLEL_SIZE,
        "model_loaded": llm_model is not None,
        "vllm_available": VLLM_AVAILABLE,
        "features": [
            "PagedAttention",
            "Continuous Batching",
            "Tensor Parallelism",
            "24x faster inference"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "5020"))
    logger.info(f"🚀 Starting vLLM Inference Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
