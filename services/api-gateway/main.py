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
    "waitlist": os.getenv("WAITLIST_URL", "http://waitlist:5000"),
    "invites": os.getenv("INVITES_URL", "http://invites:5000"),
    "referrals": os.getenv("REFERRALS_URL", "http://referrals:5000"),
    "quality_gates": os.getenv("QUALITY_GATES_URL", "http://quality-gates:5000"),
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

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "services": len(SERVICES),
        "status": "operational"
    }

# Proxy helper function
async def proxy_to_service(service_name: str, path: str, method: str = "GET", json_data: Dict = None):
    """Proxy request to a service"""
    try:
        service_url = SERVICES.get(service_name)
        if not service_url:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        
        async with httpx.AsyncClient() as client:
            url = f"{service_url}/api/{service_name}/{path}"
            
            if method == "GET":
                response = await client.get(url, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, json=json_data, timeout=30.0)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Proxy error for {service_name}/{path}: {e}")
        raise HTTPException(status_code=500, detail=f"{service_name} service error")

# Waitlist endpoints
@app.post("/api/waitlist/join")
async def proxy_waitlist_join(data: Dict[str, Any]):
    """Join waitlist"""
    return await proxy_to_service("waitlist", "join", "POST", data)

@app.get("/api/waitlist/stats")
async def proxy_waitlist_stats():
    """Get waitlist stats"""
    return await proxy_to_service("waitlist", "stats", "GET")

# Invite code endpoints
@app.post("/api/invites/generate")
async def proxy_invites_generate(data: Dict[str, Any]):
    """Generate invite codes"""
    return await proxy_to_service("invites", "generate", "POST", data)

@app.post("/api/invites/redeem")
async def proxy_invites_redeem(data: Dict[str, Any]):
    """Redeem invite code"""
    return await proxy_to_service("invites", "redeem", "POST", data)

@app.get("/api/invites/{code}/status")
async def proxy_invites_status(code: str):
    """Get invite code status"""
    return await proxy_to_service("invites", f"{code}/status", "GET")

# Referral endpoints
@app.post("/api/referrals/earn")
async def proxy_referrals_earn(data: Dict[str, Any]):
    """Check earned codes"""
    return await proxy_to_service("referrals", "earn", "POST", data)

@app.post("/api/referrals/share")
async def proxy_referrals_share(data: Dict[str, Any]):
    """Share referral"""
    return await proxy_to_service("referrals", "share", "POST", data)

@app.get("/api/referrals/{email}/quality")
async def proxy_referrals_quality(email: str):
    """Get referral quality"""
    return await proxy_to_service("referrals", f"{email}/quality", "GET")

# Quality gates endpoints
@app.get("/api/quality/trust-score")
async def proxy_quality_trust_score():
    """Get trust score"""
    return await proxy_to_service("quality_gates", "trust-score", "GET")

@app.post("/api/quality/evaluate-gate")
async def proxy_quality_evaluate():
    """Evaluate quality gate"""
    return await proxy_to_service("quality_gates", "evaluate-gate", "POST", {})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
