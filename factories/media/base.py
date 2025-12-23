"""
Base classes and interfaces for media factory workflows.
Provides abstract foundation for media processing pipelines.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


class MediaType(Enum):
    """Enumeration of supported media types"""
    IMAGE = "image"
    VIDEO = "video"
    VOICE = "voice"


class ProcessingStatus(Enum):
    """Status of media processing tasks"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class MediaTask:
    """Represents a media processing task"""
    task_id: str
    media_type: MediaType
    status: ProcessingStatus
    parameters: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MediaFactory(ABC):
    """
    Abstract base class for all media workflows.
    Defines the common interface that all media factories must implement.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the media factory with optional configuration.
        
        Args:
            config: Configuration dictionary for the factory
        """
        self.config = config or {}
        self._tasks: Dict[str, MediaTask] = {}
        self._setup()
    
    @abstractmethod
    def _setup(self):
        """
        Setup method for factory-specific initialization.
        Override this to perform any required setup.
        """
        pass
    
    @abstractmethod
    def process(self, parameters: Dict[str, Any]) -> MediaTask:
        """
        Process media according to the provided parameters.
        
        Args:
            parameters: Dictionary containing processing parameters
            
        Returns:
            MediaTask object representing the processing task
        """
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate the processing parameters.
        
        Args:
            parameters: Dictionary containing parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        pass
    
    def get_task(self, task_id: str) -> Optional[MediaTask]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: Unique identifier of the task
            
        Returns:
            MediaTask if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def list_tasks(self, status: Optional[ProcessingStatus] = None) -> List[MediaTask]:
        """
        List all tasks, optionally filtered by status.
        
        Args:
            status: Optional status to filter by
            
        Returns:
            List of MediaTask objects
        """
        if status is None:
            return list(self._tasks.values())
        return [task for task in self._tasks.values() if task.status == status]
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a task by its ID.
        
        Args:
            task_id: Unique identifier of the task to cancel
            
        Returns:
            True if task was cancelled, False otherwise
        """
        task = self._tasks.get(task_id)
        if task and task.status in [ProcessingStatus.PENDING, ProcessingStatus.PROCESSING]:
            task.status = ProcessingStatus.CANCELLED
            task.updated_at = datetime.now()
            return True
        return False
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of this media factory.
        
        Returns:
            Dictionary describing factory capabilities
        """
        return {
            "media_type": self.__class__.__name__,
            "supported_formats": self._get_supported_formats(),
            "features": self._get_features(),
        }
    
    @abstractmethod
    def _get_supported_formats(self) -> List[str]:
        """Return list of supported media formats"""
        pass
    
    @abstractmethod
    def _get_features(self) -> List[str]:
        """Return list of supported features"""
        pass
