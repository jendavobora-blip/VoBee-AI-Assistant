"""Configuration management for Vobio AI Studio backend"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ServerConfig:
    """Server configuration"""
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False
    log_level: str = "info"


@dataclass
class AIConfig:
    """AI Engine configuration"""
    max_resolution: str = "4K"
    enable_gpu: bool = True
    mock_mode: bool = True
    log_level: str = "INFO"
    max_concurrent_operations: int = 3


def load_config_from_env() -> tuple[ServerConfig, AIConfig]:
    """Load configuration from environment variables"""
    
    server_config = ServerConfig(
        host=os.getenv("SERVER_HOST", "127.0.0.1"),
        port=int(os.getenv("SERVER_PORT", "8000")),
        reload=os.getenv("SERVER_RELOAD", "false").lower() == "true",
        log_level=os.getenv("SERVER_LOG_LEVEL", "info")
    )
    
    ai_config = AIConfig(
        max_resolution=os.getenv("AI_MAX_RESOLUTION", "4K"),
        enable_gpu=os.getenv("AI_ENABLE_GPU", "true").lower() == "true",
        mock_mode=os.getenv("AI_MOCK_MODE", "true").lower() == "true",
        log_level=os.getenv("AI_LOG_LEVEL", "INFO"),
        max_concurrent_operations=int(os.getenv("AI_MAX_CONCURRENT_OPS", "3"))
    )
    
    return server_config, ai_config
