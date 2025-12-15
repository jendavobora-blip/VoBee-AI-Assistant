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
    "compression": os.getenv("COMPRESSION_SERVICE_URL", "http://compression:5006"),
    "marketing": os.getenv("MARKETING_SERVICE_URL", "http://marketing-intelligence:5007"),
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

# Compression Service endpoints
@app.post("/api/v1/compress")
async def compress_data(data: Dict[str, Any]):
    """Compress data using advanced algorithms"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['compression']}/compress",
                json=data,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Compression failed: {e}")
        raise HTTPException(status_code=500, detail="Compression service error")

@app.post("/api/v1/decompress")
async def decompress_data(data: Dict[str, Any]):
    """Decompress data"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['compression']}/decompress",
                json=data,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Decompression failed: {e}")
        raise HTTPException(status_code=500, detail="Decompression service error")

@app.get("/api/v1/compression/stats")
async def get_compression_stats():
    """Get compression statistics"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['compression']}/stats",
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Failed to get compression stats: {e}")
        raise HTTPException(status_code=500, detail="Compression service error")

# Bot Orchestration endpoints
@app.post("/api/v1/bots")
async def create_bot(bot_config: Dict[str, Any]):
    """Create a new bot instance"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/bots",
                json=bot_config,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Bot creation failed: {e}")
        raise HTTPException(status_code=500, detail="Bot orchestration service error")

@app.post("/api/v1/swarms")
async def create_swarm(swarm_config: Dict[str, Any]):
    """Create a bot swarm for mass-action orchestration"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['orchestrator']}/swarms",
                json=swarm_config,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Swarm creation failed: {e}")
        raise HTTPException(status_code=500, detail="Bot orchestration service error")

@app.get("/api/v1/bots/stats")
async def get_bot_stats():
    """Get bot orchestration statistics"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['orchestrator']}/bots/stats",
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Failed to get bot stats: {e}")
        raise HTTPException(status_code=500, detail="Bot orchestration service error")

# Marketing Intelligence endpoints
@app.post("/api/v1/marketing/products")
async def create_product(product_data: Dict[str, Any]):
    """Create a new product"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['marketing']}/products",
                json=product_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Product creation failed: {e}")
        raise HTTPException(status_code=500, detail="Marketing service error")

@app.post("/api/v1/marketing/promotions")
async def create_promotion(promotion_data: Dict[str, Any]):
    """Create a new promotion"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['marketing']}/promotions",
                json=promotion_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Promotion creation failed: {e}")
        raise HTTPException(status_code=500, detail="Marketing service error")

@app.post("/api/v1/marketing/bundles")
async def create_bundle(bundle_data: Dict[str, Any]):
    """Create a product bundle for L20 orchestration"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['marketing']}/bundles",
                json=bundle_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Bundle creation failed: {e}")
        raise HTTPException(status_code=500, detail="Marketing service error")

@app.get("/api/v1/marketing/analytics")
async def get_marketing_analytics():
    """Get marketing analytics"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['marketing']}/analytics",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Failed to get analytics: {e}")
        raise HTTPException(status_code=500, detail="Marketing service error")

@app.post("/api/v1/marketing/dashboard/change-request")
async def request_dashboard_change(change_data: Dict[str, Any]):
    """Request dashboard configuration change"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['marketing']}/dashboard/change-request",
                json=change_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Dashboard change request failed: {e}")
        raise HTTPException(status_code=500, detail="Marketing service error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
