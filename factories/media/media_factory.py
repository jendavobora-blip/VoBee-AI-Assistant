"""
Media Factory Core Implementation

Main factory class for coordinating media generation workflows.
Provides a modular, interface-driven approach for future extensions.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MediaFactory:
    """
    Core Media Factory class for managing media generation workflows.
    
    This factory coordinates image, video, and voice processing tasks,
    providing a unified interface for media generation operations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Media Factory.
        
        Args:
            config: Optional configuration dictionary for factory settings
        """
        self.config = config or {}
        self.handlers = {}
        self.task_queue = []
        self.initialized = False
        
        logger.info("Initializing Media Factory")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Initialize media handlers for different media types."""
        from .image_handler import ImageHandler
        from .video_handler import VideoHandler
        from .voice_handler import VoiceHandler
        
        self.handlers['image'] = ImageHandler(self.config.get('image', {}))
        self.handlers['video'] = VideoHandler(self.config.get('video', {}))
        self.handlers['voice'] = VoiceHandler(self.config.get('voice', {}))
        
        self.initialized = True
        logger.info("Media Factory handlers initialized")
    
    def create_media(self, media_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create media of the specified type.
        
        Args:
            media_type: Type of media to create ('image', 'video', 'voice')
            params: Parameters for media creation
        
        Returns:
            Dictionary containing the result of media creation
        """
        if media_type not in self.handlers:
            raise ValueError(f"Unsupported media type: {media_type}")
        
        logger.info(f"Creating {media_type} media with params: {params}")
        
        handler = self.handlers[media_type]
        result = handler.process(params)
        
        return {
            'status': 'success',
            'media_type': media_type,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_handler(self, media_type: str):
        """
        Get a specific media handler.
        
        Args:
            media_type: Type of handler to retrieve
        
        Returns:
            The requested handler instance
        """
        return self.handlers.get(media_type)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Media Factory.
        
        Returns:
            Dictionary containing factory status information
        """
        return {
            'initialized': self.initialized,
            'handlers': list(self.handlers.keys()),
            'task_queue_size': len(self.task_queue),
            'timestamp': datetime.utcnow().isoformat()
        }
