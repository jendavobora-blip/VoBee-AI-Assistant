"""
Task Decomposer - Breaks complex goals into 2000+ parallel micro-tasks.

This module decomposes high-level user goals into fine-grained tasks
that can be executed in parallel by the agent ecosystem.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MicroTask:
    """Represents a single micro-task."""
    
    def __init__(
        self,
        task_id: str,
        parent_id: Optional[str],
        task_type: str,
        description: str,
        parameters: Dict[str, Any],
        priority: TaskPriority,
        dependencies: List[str] = None,
        estimated_duration: int = 5
    ):
        self.task_id = task_id
        self.parent_id = parent_id
        self.task_type = task_type
        self.description = description
        self.parameters = parameters
        self.priority = priority
        self.dependencies = dependencies or []
        self.estimated_duration = estimated_duration
        self.status = TaskStatus.PENDING
        self.created_at = datetime.utcnow()
        self.assigned_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Optional[Any] = None
        self.assigned_agent: Optional[str] = None


class TaskDecomposer:
    """
    Decomposes complex goals into parallel micro-tasks.
    
    Features:
    - Intelligent task breakdown (up to 2000+ tasks)
    - Dependency graph construction
    - Priority assignment
    - Resource estimation
    - Parallel execution planning
    """
    
    def __init__(self):
        self.decomposition_rules = {
            "data_analysis": self._decompose_data_analysis,
            "content_generation": self._decompose_content_generation,
            "tech_scouting": self._decompose_tech_scouting,
            "learning": self._decompose_learning,
            "simulation": self._decompose_simulation,
            "media_creation": self._decompose_media_creation,
        }
    
    def decompose(
        self,
        goal: str,
        context: Dict[str, Any],
        max_tasks: int = 2000
    ) -> List[MicroTask]:
        """
        Decompose a high-level goal into micro-tasks.
        
        Args:
            goal: High-level goal description
            context: Additional context and parameters
            max_tasks: Maximum number of tasks to generate
            
        Returns:
            List of micro-tasks ready for parallel execution
        """
        # Identify goal type
        goal_type = self._identify_goal_type(goal, context)
        
        # Get appropriate decomposition strategy
        decomposer = self.decomposition_rules.get(
            goal_type,
            self._decompose_generic
        )
        
        # Generate micro-tasks
        tasks = decomposer(goal, context, max_tasks)
        
        # Build dependency graph
        tasks = self._build_dependencies(tasks)
        
        # Assign priorities
        tasks = self._assign_priorities(tasks)
        
        logger.info(f"Decomposed goal into {len(tasks)} micro-tasks")
        
        return tasks
    
    def _identify_goal_type(self, goal: str, context: Dict[str, Any]) -> str:
        """Identify the type of goal."""
        goal_lower = goal.lower()
        
        if any(word in goal_lower for word in ["analyze", "data", "statistics"]):
            return "data_analysis"
        elif any(word in goal_lower for word in ["generate", "create", "write"]):
            return "content_generation"
        elif any(word in goal_lower for word in ["scout", "discover", "find"]):
            return "tech_scouting"
        elif any(word in goal_lower for word in ["learn", "study", "research"]):
            return "learning"
        elif any(word in goal_lower for word in ["simulate", "test", "experiment"]):
            return "simulation"
        elif any(word in goal_lower for word in ["image", "video", "media"]):
            return "media_creation"
        else:
            return "generic"
    
    def _decompose_data_analysis(
        self,
        goal: str,
        context: Dict[str, Any],
        max_tasks: int
    ) -> List[MicroTask]:
        """Decompose data analysis goal."""
        tasks = []
        parent_id = str(uuid.uuid4())
        
        # Data collection tasks
        data_sources = context.get("data_sources", ["default"])
        for i, source in enumerate(data_sources):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="data_collection",
                description=f"Collect data from {source}",
                parameters={"source": source},
                priority=TaskPriority.HIGH,
                estimated_duration=10
            ))
        
        # Data processing tasks (parallel processing chunks)
        num_chunks = min(100, max_tasks - len(tasks) - 10)
        for i in range(num_chunks):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="data_processing",
                description=f"Process data chunk {i+1}/{num_chunks}",
                parameters={"chunk_id": i, "total_chunks": num_chunks},
                priority=TaskPriority.MEDIUM,
                estimated_duration=5
            ))
        
        # Analysis tasks
        analysis_types = ["statistical", "correlation", "trend", "anomaly"]
        for analysis in analysis_types:
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="data_analysis",
                description=f"Perform {analysis} analysis",
                parameters={"analysis_type": analysis},
                priority=TaskPriority.MEDIUM,
                estimated_duration=15
            ))
        
        # Synthesis task
        tasks.append(MicroTask(
            task_id=str(uuid.uuid4()),
            parent_id=parent_id,
            task_type="synthesis",
            description="Synthesize analysis results",
            parameters={"goal": goal},
            priority=TaskPriority.HIGH,
            estimated_duration=10
        ))
        
        return tasks
    
    def _decompose_content_generation(
        self,
        goal: str,
        context: Dict[str, Any],
        max_tasks: int
    ) -> List[MicroTask]:
        """Decompose content generation goal."""
        tasks = []
        parent_id = str(uuid.uuid4())
        
        content_type = context.get("content_type", "text")
        quantity = context.get("quantity", 10)
        
        # Research tasks
        tasks.append(MicroTask(
            task_id=str(uuid.uuid4()),
            parent_id=parent_id,
            task_type="research",
            description="Research topic and gather references",
            parameters={"goal": goal},
            priority=TaskPriority.HIGH,
            estimated_duration=20
        ))
        
        # Outline creation
        tasks.append(MicroTask(
            task_id=str(uuid.uuid4()),
            parent_id=parent_id,
            task_type="outline",
            description="Create content outline",
            parameters={"content_type": content_type},
            priority=TaskPriority.MEDIUM,
            estimated_duration=10
        ))
        
        # Parallel content generation
        num_pieces = min(quantity, max_tasks - len(tasks) - 5)
        for i in range(num_pieces):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="content_creation",
                description=f"Generate content piece {i+1}/{num_pieces}",
                parameters={
                    "piece_id": i,
                    "content_type": content_type
                },
                priority=TaskPriority.MEDIUM,
                estimated_duration=15
            ))
        
        # Review and polish
        tasks.append(MicroTask(
            task_id=str(uuid.uuid4()),
            parent_id=parent_id,
            task_type="review",
            description="Review and polish content",
            parameters={"content_type": content_type},
            priority=TaskPriority.MEDIUM,
            estimated_duration=20
        ))
        
        return tasks
    
    def _decompose_tech_scouting(
        self,
        goal: str,
        context: Dict[str, Any],
        max_tasks: int
    ) -> List[MicroTask]:
        """Decompose tech scouting goal."""
        tasks = []
        parent_id = str(uuid.uuid4())
        
        # Parallel scanning tasks
        sources = ["github", "arxiv", "hackernews", "producthunt"]
        for source in sources:
            # Create multiple parallel scanners per source
            scanners_per_source = min(50, max_tasks // len(sources) // 2)
            for i in range(scanners_per_source):
                tasks.append(MicroTask(
                    task_id=str(uuid.uuid4()),
                    parent_id=parent_id,
                    task_type="tech_scan",
                    description=f"Scan {source} (worker {i+1})",
                    parameters={
                        "source": source,
                        "worker_id": i,
                        "query": context.get("query", "AI")
                    },
                    priority=TaskPriority.MEDIUM,
                    estimated_duration=10
                ))
        
        # Evaluation tasks
        num_evaluators = min(200, max_tasks - len(tasks) - 10)
        for i in range(num_evaluators):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="tech_evaluation",
                description=f"Evaluate discovered tech {i+1}",
                parameters={"evaluator_id": i},
                priority=TaskPriority.LOW,
                estimated_duration=5
            ))
        
        return tasks
    
    def _decompose_learning(
        self,
        goal: str,
        context: Dict[str, Any],
        max_tasks: int
    ) -> List[MicroTask]:
        """Decompose learning goal."""
        tasks = []
        parent_id = str(uuid.uuid4())
        
        # Parallel data ingestion
        num_ingestors = min(1000, max_tasks // 2)
        for i in range(num_ingestors):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="data_ingest",
                description=f"Ingest data chunk {i+1}",
                parameters={"chunk_id": i},
                priority=TaskPriority.MEDIUM,
                estimated_duration=5
            ))
        
        # Parallel compression
        num_compressors = min(500, max_tasks - num_ingestors - 10)
        for i in range(num_compressors):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="knowledge_compression",
                description=f"Compress knowledge {i+1}",
                parameters={"compressor_id": i},
                priority=TaskPriority.MEDIUM,
                estimated_duration=3
            ))
        
        return tasks
    
    def _decompose_simulation(
        self,
        goal: str,
        context: Dict[str, Any],
        max_tasks: int
    ) -> List[MicroTask]:
        """Decompose simulation goal."""
        tasks = []
        parent_id = str(uuid.uuid4())
        
        num_scenarios = context.get("num_scenarios", 1000)
        num_scenarios = min(num_scenarios, max_tasks - 10)
        
        # Parallel simulations
        for i in range(num_scenarios):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="simulation",
                description=f"Run simulation scenario {i+1}",
                parameters={"scenario_id": i},
                priority=TaskPriority.MEDIUM,
                estimated_duration=10
            ))
        
        # Analysis task
        tasks.append(MicroTask(
            task_id=str(uuid.uuid4()),
            parent_id=parent_id,
            task_type="simulation_analysis",
            description="Analyze simulation results",
            parameters={"total_scenarios": num_scenarios},
            priority=TaskPriority.HIGH,
            estimated_duration=30
        ))
        
        return tasks
    
    def _decompose_media_creation(
        self,
        goal: str,
        context: Dict[str, Any],
        max_tasks: int
    ) -> List[MicroTask]:
        """Decompose media creation goal."""
        tasks = []
        parent_id = str(uuid.uuid4())
        
        media_type = context.get("media_type", "image")
        quantity = context.get("quantity", 10)
        
        # Style research
        tasks.append(MicroTask(
            task_id=str(uuid.uuid4()),
            parent_id=parent_id,
            task_type="style_research",
            description="Research visual style",
            parameters={"media_type": media_type},
            priority=TaskPriority.HIGH,
            estimated_duration=10
        ))
        
        # Parallel media generation
        num_pieces = min(quantity, max_tasks - 5)
        for i in range(num_pieces):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="media_generation",
                description=f"Generate {media_type} {i+1}/{num_pieces}",
                parameters={
                    "media_type": media_type,
                    "piece_id": i
                },
                priority=TaskPriority.MEDIUM,
                estimated_duration=20 if media_type == "video" else 5
            ))
        
        return tasks
    
    def _decompose_generic(
        self,
        goal: str,
        context: Dict[str, Any],
        max_tasks: int
    ) -> List[MicroTask]:
        """Generic decomposition for unknown goal types."""
        tasks = []
        parent_id = str(uuid.uuid4())
        
        # Create a reasonable number of generic tasks
        num_tasks = min(100, max_tasks)
        for i in range(num_tasks):
            tasks.append(MicroTask(
                task_id=str(uuid.uuid4()),
                parent_id=parent_id,
                task_type="generic_task",
                description=f"Execute sub-task {i+1}/{num_tasks}",
                parameters={"task_id": i, "goal": goal},
                priority=TaskPriority.MEDIUM,
                estimated_duration=5
            ))
        
        return tasks
    
    def _build_dependencies(self, tasks: List[MicroTask]) -> List[MicroTask]:
        """Build dependency graph between tasks."""
        # Group tasks by type
        task_groups = {}
        for task in tasks:
            if task.task_type not in task_groups:
                task_groups[task.task_type] = []
            task_groups[task.task_type].append(task)
        
        # Add dependencies based on logical flow
        dependency_rules = {
            "data_processing": ["data_collection"],
            "data_analysis": ["data_processing"],
            "synthesis": ["data_analysis"],
            "content_creation": ["outline", "research"],
            "review": ["content_creation"],
            "tech_evaluation": ["tech_scan"],
            "knowledge_compression": ["data_ingest"],
            "simulation_analysis": ["simulation"],
        }
        
        for task in tasks:
            required_types = dependency_rules.get(task.task_type, [])
            for req_type in required_types:
                if req_type in task_groups:
                    # Depend on all tasks of required type
                    task.dependencies.extend([
                        t.task_id for t in task_groups[req_type]
                    ])
        
        return tasks
    
    def _assign_priorities(self, tasks: List[MicroTask]) -> List[MicroTask]:
        """Assign priorities based on dependencies and type."""
        # Tasks with no dependencies get higher priority
        for task in tasks:
            if not task.dependencies:
                if task.priority == TaskPriority.MEDIUM:
                    task.priority = TaskPriority.HIGH
        
        # Final synthesis tasks get critical priority
        synthesis_types = ["synthesis", "review", "simulation_analysis"]
        for task in tasks:
            if task.task_type in synthesis_types:
                task.priority = TaskPriority.CRITICAL
        
        return tasks
    
    def get_parallelizable_tasks(self, tasks: List[MicroTask]) -> List[MicroTask]:
        """Get tasks that can be executed in parallel (no dependencies)."""
        return [t for t in tasks if not t.dependencies and t.status == TaskStatus.PENDING]
    
    def get_task_stats(self, tasks: List[MicroTask]) -> Dict[str, Any]:
        """Get statistics about task decomposition."""
        return {
            "total_tasks": len(tasks),
            "pending": sum(1 for t in tasks if t.status == TaskStatus.PENDING),
            "running": sum(1 for t in tasks if t.status == TaskStatus.RUNNING),
            "completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in tasks if t.status == TaskStatus.FAILED),
            "parallelizable": len(self.get_parallelizable_tasks(tasks)),
            "total_estimated_duration": sum(t.estimated_duration for t in tasks),
            "task_types": len(set(t.task_type for t in tasks)),
        }
