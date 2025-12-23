"""
API Gateway for AI Orchestration System
Provides unified interface for all AI services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx
import os
import logging
from datetime import datetime
import redis.asyncio as aioredis
import json
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis client for caching
redis_client = None

app = FastAPI(
    title="AI Orchestration System API Gateway",
    description="Unified API for 3D/4D generation, crypto prediction, and AI services",
    version="1.0.0",
    default_response_class=ORJSONResponse  # Faster JSON serialization
)

# Cache decorator for Redis
def cache_result(ttl: int = 300):
    """Cache decorator with Redis backend"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if redis_client is None:
                return await func(*args, **kwargs)
            
            # Generate cache key from function name and args
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            try:
                # Try to get from cache
                cached = await redis_client.get(cache_key)
                if cached:
                    logger.info(f"Cache hit for {cache_key}")
                    return json.loads(cached)
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
            
            # Execute function
            result = await func(*args, **kwargs)
            
            try:
                # Store in cache
                await redis_client.setex(cache_key, ttl, json.dumps(result))
            except Exception as e:
                logger.warning(f"Cache write error: {e}")
            
            return result
        return wrapper
    return decorator

@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup"""
    global redis_client
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    
    try:
        redis_client = await aioredis.from_url(
            f"redis://{redis_host}:{redis_port}",
            encoding="utf-8",
            decode_responses=True
        )
        logger.info("Redis connection established")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        redis_client = None

@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection on shutdown"""
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")

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
@cache_result(ttl=30)  # Cache for 30 seconds
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
    # Optimized Uvicorn configuration for production
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=4,  # Multi-worker for better performance
        loop="uvloop",  # Fastest event loop
        http="httptools",  # Faster HTTP parsing
        log_level="info"
    )
