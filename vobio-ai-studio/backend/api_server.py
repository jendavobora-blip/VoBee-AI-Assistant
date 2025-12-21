from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import uvicorn
from ai_engine import AIEngine, AIConfig

app = FastAPI(title="Vobio AI Studio API")

# CORS for Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize AI Engine
engine = AIEngine(AIConfig(mock_mode=True))

# Progress tracking
progress_store: Dict[str, Dict] = {}


class ImageRequest(BaseModel):
    prompt: str
    style: str = "realistic"
    resolution: str = "1024x1024"
    hdr: bool = True
    pbr: bool = True


class VideoRequest(BaseModel):
    prompt: str
    duration: int = 5
    resolution: str = "4K"
    fps: int = 30
    use_nerf: bool = False


def progress_callback(operation_id: str):
    def callback(progress: int, stage: str):
        progress_store[operation_id] = {
            "progress": progress,
            "stage": stage
        }
    return callback


@app.get("/health")
async def health():
    return {"status": "healthy", "engine": "online"}


@app.get("/gpu-info")
async def gpu_info():
    return engine.get_gpu_info()


@app.post("/generate/image")
async def generate_image(request: ImageRequest, background_tasks: BackgroundTasks):
    operation_id = f"img_{asyncio.get_event_loop().time()}"
    
    # Run in background
    result = await engine.generate_image(
        prompt=request.prompt,
        style=request.style,
        resolution=request.resolution,
        hdr=request.hdr,
        pbr=request.pbr,
        progress_callback=progress_callback(operation_id),
        operation_id=operation_id
    )
    
    return result


@app.post("/generate/video")
async def generate_video(request: VideoRequest):
    operation_id = f"vid_{asyncio.get_event_loop().time()}"
    
    result = await engine.generate_video(
        prompt=request.prompt,
        duration=request.duration,
        resolution=request.resolution,
        fps=request.fps,
        use_nerf=request.use_nerf,
        progress_callback=progress_callback(operation_id),
        operation_id=operation_id
    )
    
    return result


@app.get("/progress/{operation_id}")
async def get_progress(operation_id: str):
    if operation_id in progress_store:
        return progress_store[operation_id]
    raise HTTPException(status_code=404, detail="Operation not found")


@app.post("/cancel/{operation_id}")
async def cancel_operation(operation_id: str):
    success = engine.cancel_operation(operation_id)
    if success:
        return {"status": "cancelled", "operation_id": operation_id}
    raise HTTPException(status_code=404, detail="Operation not found")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
