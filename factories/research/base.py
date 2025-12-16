"""
Base classes and interfaces for research factory workflows.
Provides abstract foundation for research and analysis pipelines.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


class ResearchType(Enum):
    """Enumeration of supported research types"""
    MARKET_ANALYSIS = "market_analysis"
    RESEARCH_AGENT = "research_agent"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    TREND_ANALYSIS = "trend_analysis"


class ResearchStatus(Enum):
    """Status of research tasks"""
    PENDING = "pending"
    COLLECTING_DATA = "collecting_data"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ResearchPriority(Enum):
    """Priority levels for research tasks"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ResearchTask:
    """Represents a research task"""
    task_id: str
    research_type: ResearchType
    status: ResearchStatus
    priority: ResearchPriority
    parameters: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    progress: float = 0.0  # 0.0 to 1.0


@dataclass
class ResearchResult:
    """Structured research result"""
    task_id: str
    summary: str
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    confidence_score: float
    data_sources: List[str]
    timestamp: datetime
    metadata: Dict[str, Any]


class ResearchFactory(ABC):
    """
    Abstract base class for all research workflows.
    Defines the common interface that all research factories must implement.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the research factory with optional configuration.
        
        Args:
            config: Configuration dictionary for the factory
        """
        self.config = config or {}
        self._tasks: Dict[str, ResearchTask] = {}
        self._results: Dict[str, ResearchResult] = {}
        self._setup()
    
    @abstractmethod
    def _setup(self):
        """
        Setup method for factory-specific initialization.
        Override this to perform any required setup.
        """
        pass
    
    @abstractmethod
    def research(self, parameters: Dict[str, Any]) -> ResearchTask:
        """
        Execute research according to the provided parameters.
        
        Args:
            parameters: Dictionary containing research parameters
            
        Returns:
            ResearchTask object representing the research task
        """
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate the research parameters.
        
        Args:
            parameters: Dictionary containing parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        pass
    
    def get_task(self, task_id: str) -> Optional[ResearchTask]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: Unique identifier of the task
            
        Returns:
            ResearchTask if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def get_result(self, task_id: str) -> Optional[ResearchResult]:
        """
        Retrieve research result by task ID.
        
        Args:
            task_id: Unique identifier of the task
            
        Returns:
            ResearchResult if found, None otherwise
        """
        return self._results.get(task_id)
    
    def list_tasks(self, status: Optional[ResearchStatus] = None) -> List[ResearchTask]:
        """
        List all tasks, optionally filtered by status.
        
        Args:
            status: Optional status to filter by
            
        Returns:
            List of ResearchTask objects
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
        if task and task.status in [ResearchStatus.PENDING, ResearchStatus.COLLECTING_DATA, ResearchStatus.ANALYZING]:
            task.status = ResearchStatus.CANCELLED
            task.updated_at = datetime.now()
            return True
        return False
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of this research factory.
        
        Returns:
            Dictionary describing factory capabilities
        """
        return {
            "research_type": self.__class__.__name__,
            "data_sources": self._get_data_sources(),
            "features": self._get_features(),
            "analysis_types": self._get_analysis_types(),
        }
    
    @abstractmethod
    def _get_data_sources(self) -> List[str]:
        """Return list of supported data sources"""
        pass
    
    @abstractmethod
    def _get_features(self) -> List[str]:
        """Return list of supported features"""
        pass
    
    @abstractmethod
    def _get_analysis_types(self) -> List[str]:
        """Return list of supported analysis types"""
        pass
