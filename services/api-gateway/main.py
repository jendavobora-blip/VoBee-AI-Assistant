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

# L20 Supreme Brain endpoints

@app.post("/api/v1/l20/strategize")
async def l20_strategize(objective: str, constraints: Optional[Dict[str, Any]] = None):
    """High-level strategic planning using L20 Supreme Brain"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/l20/strategize",
                json={"objective": objective, "constraints": constraints or {}},
                timeout=120.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"L20 strategize failed: {e}")
        raise HTTPException(status_code=500, detail="L20 strategize service error")

@app.post("/api/v1/l20/prioritize")
async def l20_prioritize(tasks: List[Dict[str, Any]]):
    """Intelligent task prioritization using L20 Supreme Brain"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/l20/prioritize",
                json={"tasks": tasks},
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"L20 prioritize failed: {e}")
        raise HTTPException(status_code=500, detail="L20 prioritize service error")

@app.post("/api/v1/l20/coordinate")
async def l20_coordinate(domains: List[str], task_specs: Dict[str, Any]):
    """Cross-domain coordination using L20 Supreme Brain"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/l20/coordinate",
                json={"domains": domains, "task_specs": task_specs},
                timeout=600.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"L20 coordinate failed: {e}")
        raise HTTPException(status_code=500, detail="L20 coordinate service error")

@app.post("/api/v1/l20/optimize-resources")
async def l20_optimize_resources(available_resources: Dict[str, Any], pending_tasks: List[Dict[str, Any]]):
    """Optimize resource allocation using L20 Supreme Brain"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/l20/optimize-resources",
                json={"available_resources": available_resources, "pending_tasks": pending_tasks},
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"L20 optimize-resources failed: {e}")
        raise HTTPException(status_code=500, detail="L20 optimize-resources service error")

@app.get("/api/v1/l20/metrics")
async def l20_metrics():
    """Get L20 Supreme Brain metrics"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['orchestrator']}/l20/metrics",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"L20 metrics failed: {e}")
        raise HTTPException(status_code=500, detail="L20 metrics service error")

# Master Intelligence endpoints

@app.post("/api/v1/intelligence/{intelligence_type}/execute")
async def execute_intelligence(intelligence_type: str, task: Dict[str, Any]):
    """Execute specific Master Intelligence task"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/intelligence/{intelligence_type}/execute",
                json=task,
                timeout=300.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Intelligence execution failed: {e}")
        raise HTTPException(status_code=500, detail="Intelligence execution service error")

@app.get("/api/v1/intelligence/{intelligence_type}/metrics")
async def get_intelligence_metrics(intelligence_type: str):
    """Get metrics for specific Master Intelligence"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['orchestrator']}/intelligence/{intelligence_type}/metrics",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Intelligence metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Intelligence metrics service error")

@app.get("/api/v1/intelligence/list")
async def list_intelligences():
    """List all available Master Intelligences"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['orchestrator']}/intelligence/list",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"List intelligences failed: {e}")
        raise HTTPException(status_code=500, detail="List intelligences service error")

# AI Swarm endpoints

@app.post("/api/v1/swarm/dispatch")
async def swarm_dispatch(tasks: List[Dict[str, Any]]):
    """Dispatch micro-tasks to AI swarm"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/swarm/dispatch",
                json={"tasks": tasks},
                timeout=300.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Swarm dispatch failed: {e}")
        raise HTTPException(status_code=500, detail="Swarm dispatch service error")

@app.get("/api/v1/swarm/status")
async def swarm_status():
    """Get AI swarm status"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['orchestrator']}/swarm/status",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Swarm status failed: {e}")
        raise HTTPException(status_code=500, detail="Swarm status service error")

@app.get("/api/v1/swarm/metrics")
async def swarm_metrics():
    """Get AI swarm performance metrics"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['orchestrator']}/swarm/metrics",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Swarm metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Swarm metrics service error")

@app.post("/api/v1/swarm/scale")
async def swarm_scale(target_size: int):
    """Scale AI swarm to target size"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/swarm/scale",
                json={"target_size": target_size},
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Swarm scale failed: {e}")
        raise HTTPException(status_code=500, detail="Swarm scale service error")

@app.post("/api/v1/swarm/optimize")
async def swarm_optimize():
    """Optimize swarm configuration"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/swarm/optimize",
                json={},
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Swarm optimize failed: {e}")
        raise HTTPException(status_code=500, detail="Swarm optimize service error")

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
