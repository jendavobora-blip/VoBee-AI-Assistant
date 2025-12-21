"""Helper utilities for Vobio AI Studio backend"""

import hashlib
import time
from typing import Any, Dict
from datetime import datetime


def generate_operation_id(prefix: str, data: str) -> str:
    """Generate a unique operation ID"""
    timestamp = str(time.time())
    combined = f"{data}_{timestamp}"
    hash_value = hashlib.md5(combined.encode()).hexdigest()[:8]
    return f"{prefix}_{hash_value}"


def validate_prompt(prompt: str, max_length: int = 1000) -> tuple[bool, str]:
    """Validate user prompt"""
    if not prompt or not prompt.strip():
        return False, "Prompt cannot be empty"
    
    if len(prompt) > max_length:
        return False, f"Prompt exceeds maximum length of {max_length} characters"
    
    return True, "Valid"


def validate_resolution(resolution: str) -> tuple[bool, str]:
    """Validate resolution parameter"""
    valid_resolutions = [
        "512x512", "768x768", "1024x1024",
        "1080p", "4K", "8K"
    ]
    
    if resolution not in valid_resolutions:
        return False, f"Invalid resolution. Must be one of: {', '.join(valid_resolutions)}"
    
    return True, "Valid"


def format_timestamp(dt: datetime = None) -> str:
    """Format timestamp in ISO format"""
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat() + "Z"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system operations"""
    import re
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    return filename


def calculate_video_size(duration: int, fps: int, resolution: str) -> Dict[str, Any]:
    """Calculate estimated video file size and metadata"""
    resolution_multipliers = {
        "1080p": 1.0,
        "4K": 4.0,
        "8K": 16.0
    }
    
    multiplier = resolution_multipliers.get(resolution, 1.0)
    base_size_mb = 10  # MB per second for 1080p
    
    estimated_size_mb = duration * base_size_mb * multiplier
    total_frames = duration * fps
    
    return {
        "estimated_size_mb": round(estimated_size_mb, 2),
        "total_frames": total_frames,
        "duration": duration,
        "fps": fps,
        "resolution": resolution
    }
