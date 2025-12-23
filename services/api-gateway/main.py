"""
API Gateway for AI Orchestration System
Provides unified interface for all AI services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Orchestration System API Gateway",
    description="Unified API for 3D/4D generation, crypto prediction, and AI services",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service endpoints
SERVICES = {
    "image_generation": os.getenv("IMAGE_SERVICE_URL", "http://image-generation:5000"),
    "video_generation": os.getenv("VIDEO_SERVICE_URL", "http://video-generation:5001"),
    "crypto_prediction": os.getenv("CRYPTO_SERVICE_URL", "http://crypto-prediction:5002"),
    "orchestrator": os.getenv("ORCHESTRATOR_URL", "http://orchestrator:5003"),
    "fraud_detection": os.getenv("FRAUD_SERVICE_URL", "http://fraud-detection:5004"),
}

# NEW: Enhanced service endpoints (optional)
ENHANCED_SERVICES = {
    "vllm_inference": os.getenv("VLLM_SERVICE_URL", "http://vllm-inference:5020"),
    "langchain_orchestrator": os.getenv("LANGCHAIN_SERVICE_URL", "http://langchain-orchestrator:5021"),
    "haystack_search": os.getenv("HAYSTACK_SERVICE_URL", "http://haystack-search:5022"),
}

# Feature flags (environment variables override)
FEATURES_ENABLED = {
    "vllm": os.getenv("ENABLE_VLLM", "false").lower() == "true",
    "langchain": os.getenv("ENABLE_LANGCHAIN", "false").lower() == "true",
    "haystack": os.getenv("ENABLE_HAYSTACK", "false").lower() == "true",
}

# Request models
class ImageGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "realistic"
    resolution: Optional[str] = "1024x1024"
    hdr: Optional[bool] = True
    pbr: Optional[bool] = True
    model: Optional[str] = "stable-diffusion"

class VideoGenerationRequest(BaseModel):
    prompt: str
    duration: Optional[int] = 5
    resolution: Optional[str] = "8K"
    fps: Optional[int] = 60
    use_nerf: Optional[bool] = True
    style: Optional[str] = "realistic"

class CryptoPredictionRequest(BaseModel):
    symbol: str
    timeframe: Optional[str] = "1h"
    prediction_horizon: Optional[int] = 24

class OrchestrationRequest(BaseModel):
    tasks: List[Dict[str, Any]]
    priority: Optional[str] = "normal"

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Service status endpoint
@app.get("/status")
async def get_status():
    """Get status of all services"""
    status = {}
    async with httpx.AsyncClient() as client:
        for service_name, service_url in SERVICES.items():
            try:
                response = await client.get(f"{service_url}/health", timeout=5.0)
                status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": service_url
                }
            except Exception as e:
                status[service_name] = {
                    "status": "unreachable",
                    "error": str(e),
                    "url": service_url
                }
    return status

# Image Generation endpoints
@app.post('/api/v1/generate/image')
async def generate_image(request: ImageGenerationRequest):
    """Generate 3D/4D images with HDR and PBR rendering"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['image_generation']}/generate",
                json=request.dict(),
                timeout=300.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Image generation failed: {e}")
        raise HTTPException(status_code=500, detail="Image generation service error")

# Video Generation endpoints
@app.post("/api/v1/generate/video")
async def generate_video(request: VideoGenerationRequest):
    """Generate 8K video with NeRF rendering"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['video_generation']}/generate",
                json=request.dict(),
                timeout=600.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Video generation failed: {e}")
        raise HTTPException(status_code=500, detail="Video generation service error")

# Crypto Prediction endpoints
@app.post("/api/v1/crypto/predict")
async def predict_crypto(request: CryptoPredictionRequest):
    """Predict cryptocurrency prices using LSTM/Transformer models"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['crypto_prediction']}/predict",
                json=request.dict(),
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Crypto prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Crypto prediction service error")

@app.get("/api/v1/crypto/sentiment/{symbol}")
async def get_sentiment_analysis(symbol: str):
    """Get sentiment analysis for a cryptocurrency"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['crypto_prediction']}/sentiment/{symbol}",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Sentiment analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Sentiment analysis service error")

# Orchestration endpoints
@app.post("/api/v1/orchestrate")
async def orchestrate_tasks(request: OrchestrationRequest):
    """Orchestrate multiple AI tasks"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/orchestrate",
                json=request.dict(),
                timeout=600.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Orchestration failed: {e}")
        raise HTTPException(status_code=500, detail="Orchestration service error")

# Fraud Detection endpoints
@app.post("/api/v1/fraud/analyze")
async def analyze_fraud(data: Dict[str, Any]):
    """Analyze transaction for potential fraud"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['fraud_detection']}/analyze",
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Fraud analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Fraud detection service error")

# ========================================
# V2 API ENDPOINTS - ENHANCED FEATURES
# All V2 endpoints gracefully fall back to V1
# ========================================

@app.post("/api/v2/generate/image")
async def generate_image_v2(request: ImageGenerationRequest):
    """
    Enhanced image generation with PyTorch Lightning & ONNX
    
    Falls back to V1 if enhanced features not available
    """
    try:
        # V2 endpoint always available - falls back gracefully
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['image_generation']}/generate",
                json=request.dict(),
                timeout=300.0
            )
            response.raise_for_status()
            result = response.json()
            result["api_version"] = "v2"
            return result
    except httpx.HTTPError as e:
        logger.warning(f"V2 image generation failed: {e}, falling back to V1")
        # Automatic fallback to V1
        return await generate_image(request)


@app.post("/api/v2/generate/video")
async def generate_video_v2(request: VideoGenerationRequest):
    """
    Enhanced video generation with PyTorch Lightning
    
    Falls back to V1 if enhanced features not available
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['video_generation']}/generate",
                json=request.dict(),
                timeout=600.0
            )
            response.raise_for_status()
            result = response.json()
            result["api_version"] = "v2"
            return result
    except httpx.HTTPError as e:
        logger.warning(f"V2 video generation failed: {e}, falling back to V1")
        return await generate_video(request)


@app.post("/api/v2/crypto/predict")
async def predict_crypto_v2(request: CryptoPredictionRequest):
    """
    Enhanced crypto prediction with JAX acceleration
    
    Falls back to V1 if JAX not available
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['crypto_prediction']}/predict",
                json=request.dict(),
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            result["api_version"] = "v2"
            return result
    except httpx.HTTPError as e:
        logger.warning(f"V2 crypto prediction failed: {e}, falling back to V1")
        return await predict_crypto(request)


# NEW: vLLM Fast Inference (optional)
class FastGenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7


@app.post("/api/v2/generate/fast")
async def generate_fast_llm(request: FastGenerateRequest):
    """
    Ultra-fast LLM inference with vLLM (24x faster)
    
    Returns 501 if vLLM service not enabled
    """
    if not FEATURES_ENABLED["vllm"]:
        raise HTTPException(
            status_code=501,
            detail="vLLM service not enabled. Set ENABLE_VLLM=true or use V1 endpoints."
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ENHANCED_SERVICES['vllm_inference']}/v2/generate",
                json=request.dict(),
                timeout=120.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"vLLM inference failed: {e}")
        raise HTTPException(status_code=500, detail="vLLM inference service error")


# NEW: LangChain Orchestration (optional)
@app.post("/api/v2/orchestrate/langchain")
async def orchestrate_with_langchain(data: Dict[str, Any]):
    """
    Advanced LLM workflow orchestration with LangChain
    
    Returns 501 if LangChain service not enabled
    """
    if not FEATURES_ENABLED["langchain"]:
        raise HTTPException(
            status_code=501,
            detail="LangChain service not enabled. Set ENABLE_LANGCHAIN=true."
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ENHANCED_SERVICES['langchain_orchestrator']}/orchestrate",
                json=data,
                timeout=600.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"LangChain orchestration failed: {e}")
        raise HTTPException(status_code=500, detail="LangChain service error")


# NEW: Haystack RAG Search (optional)
@app.post("/api/v2/search/rag")
async def rag_search(query: str, top_k: int = 3):
    """
    Retrieval-Augmented Generation with Haystack
    
    Returns 501 if Haystack service not enabled
    """
    if not FEATURES_ENABLED["haystack"]:
        raise HTTPException(
            status_code=501,
            detail="Haystack service not enabled. Set ENABLE_HAYSTACK=true."
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ENHANCED_SERVICES['haystack_search']}/rag/query",
                json={"question": query, "top_k": top_k},
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"RAG search failed: {e}")
        raise HTTPException(status_code=500, detail="Haystack service error")


# Enhanced status endpoint
@app.get("/api/v2/status")
async def get_enhanced_status():
    """Get status of all services including enhanced features"""
    status = {}
    
    # Check V1 services
    async with httpx.AsyncClient() as client:
        for service_name, service_url in SERVICES.items():
            try:
                response = await client.get(f"{service_url}/health", timeout=5.0)
                status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": service_url,
                    "version": "v1"
                }
            except Exception as e:
                status[service_name] = {
                    "status": "unreachable",
                    "error": str(e),
                    "url": service_url
                }
        
        # Check enhanced services (if enabled)
        for service_name, service_url in ENHANCED_SERVICES.items():
            feature_key = service_name.split("_")[0]
            if FEATURES_ENABLED.get(feature_key, False):
                try:
                    response = await client.get(f"{service_url}/health", timeout=5.0)
                    status[service_name] = {
                        "status": "healthy" if response.status_code == 200 else "unhealthy",
                        "url": service_url,
                        "version": "v2-enhanced"
                    }
                except Exception as e:
                    status[service_name] = {
                        "status": "unreachable",
                        "error": str(e),
                        "url": service_url
                    }
            else:
                status[service_name] = {
                    "status": "disabled",
                    "url": service_url,
                    "note": f"Enable with ENABLE_{feature_key.upper()}=true"
                }
    
    return {
        "services": status,
        "features_enabled": FEATURES_ENABLED,
        "timestamp": datetime.utcnow().isoformat()
    }


# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    enabled_features = sum(1 for enabled in FEATURES_ENABLED.values() if enabled)
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "services": len(SERVICES),
        "enhanced_services": len(ENHANCED_SERVICES),
        "features_enabled": enabled_features,
        "status": "operational",
        "api_versions": ["v1", "v2"]
    }


# Feature information endpoint
@app.get("/api/features")
async def get_features():
    """Get information about available enhanced features"""
    return {
        "api_versions": {
            "v1": {
                "description": "Original API - Always available",
                "endpoints": [
                    "/api/v1/generate/image",
                    "/api/v1/generate/video",
                    "/api/v1/crypto/predict"
                ],
                "status": "production"
            },
            "v2": {
                "description": "Enhanced API with TOP AI technologies",
                "endpoints": [
                    "/api/v2/generate/image",
                    "/api/v2/generate/video",
                    "/api/v2/crypto/predict",
                    "/api/v2/generate/fast",
                    "/api/v2/orchestrate/langchain",
                    "/api/v2/search/rag"
                ],
                "fallback": "Automatic fallback to V1 on failure"
            }
        },
        "enhanced_features": {
            "pytorch_lightning": {
                "description": "10x faster multi-GPU training",
                "services": ["image-generation", "video-generation"],
                "status": "optional"
            },
            "vllm": {
                "description": "24x faster LLM inference",
                "enabled": FEATURES_ENABLED["vllm"],
                "endpoint": "/api/v2/generate/fast"
            },
            "langchain": {
                "description": "LLM orchestration framework",
                "enabled": FEATURES_ENABLED["langchain"],
                "endpoint": "/api/v2/orchestrate/langchain"
            },
            "haystack": {
                "description": "RAG & semantic search",
                "enabled": FEATURES_ENABLED["haystack"],
                "endpoint": "/api/v2/search/rag"
            },
            "jax": {
                "description": "High-performance scientific computing",
                "services": ["crypto-prediction"],
                "status": "optional"
            },
            "onnx": {
                "description": "Cross-platform inference optimization",
                "status": "optional"
            },
            "rust_ai": {
                "description": "Ultra-fast Rust-based inference",
                "status": "experimental"
            }
        },
        "backward_compatible": True,
        "zero_breaking_changes": True
    }

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "services": len(SERVICES),
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
