"""
Media Factory Module
Provides interfaces and implementations for media-related workflows including
image, video, and voice processing.
"""

from typing import Dict, Any, Optional
from .base import MediaFactory, MediaType
from .image import ImageWorkflow
from .video import VideoWorkflow
from .voice import VoiceWorkflow

__all__ = [
    "MediaFactory",
    "MediaType",
    "ImageWorkflow",
    "VideoWorkflow",
    "VoiceWorkflow",
]


class MediaFactoryRegistry:
    """Central registry for media workflow factories"""
    
    _workflows = {
        MediaType.IMAGE: ImageWorkflow,
        MediaType.VIDEO: VideoWorkflow,
        MediaType.VOICE: VoiceWorkflow,
    }
    
    @classmethod
    def get_workflow(cls, media_type: MediaType, config: Optional[Dict[str, Any]] = None):
        """
        Get a workflow instance for the specified media type.
        
        Args:
            media_type: Type of media workflow to create
            config: Optional configuration dictionary
            
        Returns:
            Instance of the requested workflow
            
        Raises:
            ValueError: If media_type is not supported
        """
        if media_type not in cls._workflows:
            raise ValueError(f"Unsupported media type: {media_type}")
        
        workflow_class = cls._workflows[media_type]
        return workflow_class(config or {})
    
    @classmethod
    def list_available_workflows(cls):
        """List all available media workflow types"""
        return list(cls._workflows.keys())
