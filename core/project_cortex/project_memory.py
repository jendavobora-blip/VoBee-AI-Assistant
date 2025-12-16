"""
Project Memory - Isolated memory management per project.

Stores project-specific context, history, and learned patterns.
Ensures deterministic retrieval and logging.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class ProjectMemory:
    """
    Manages isolated memory for a specific project.
    
    Features:
    - Context storage and retrieval
    - Conversation history
    - Learned patterns and preferences
    - Deterministic memory access
    """
    
    def __init__(self, project_id: str, storage_path: str = "data/projects/memory"):
        """
        Initialize project memory.
        
        Args:
            project_id: Unique project identifier
            storage_path: Base directory for memory storage
        """
        self.project_id = project_id
        self.storage_path = Path(storage_path) / project_id
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.context: Dict[str, Any] = {}
        self.history: List[Dict] = []
        self.patterns: Dict[str, Any] = {}
        
        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.{project_id}")
        self.logger.setLevel(logging.INFO)
        
        # Load existing memory
        self._load_memory()
        
        self.logger.info(f"ProjectMemory initialized for project: {project_id}")
    
    def store_context(self, key: str, value: Any, metadata: Optional[Dict] = None):
        """
        Store a context value with optional metadata.
        
        Args:
            key: Context key
            value: Context value
            metadata: Optional metadata about the context
        """
        self.context[key] = {
            "value": value,
            "metadata": metadata or {},
            "updated_at": datetime.utcnow().isoformat()
        }
        
        self._save_context()
        
        self.logger.debug(f"Stored context: {key}")
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a context value.
        
        Args:
            key: Context key
            default: Default value if key not found
            
        Returns:
            Context value or default
        """
        if key in self.context:
            return self.context[key]["value"]
        return default
    
    def add_to_history(
        self,
        event_type: str,
        data: Dict,
        importance: str = "normal"
    ):
        """
        Add an event to project history.
        
        Args:
            event_type: Type of event (e.g., 'task', 'decision', 'action')
            data: Event data
            importance: 'low', 'normal', 'high', 'critical'
        """
        event = {
            "type": event_type,
            "data": data,
            "importance": importance,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.history.append(event)
        self._save_history()
        
        self.logger.info(f"Added to history: {event_type} ({importance})")
    
    def get_history(
        self,
        event_type: Optional[str] = None,
        limit: Optional[int] = None,
        min_importance: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve history with optional filters.
        
        Args:
            event_type: Filter by event type
            limit: Maximum number of events to return
            min_importance: Minimum importance level
            
        Returns:
            List of history events
        """
        filtered_history = self.history
        
        # Filter by event type
        if event_type:
            filtered_history = [e for e in filtered_history if e["type"] == event_type]
        
        # Filter by importance
        if min_importance:
            importance_levels = {"low": 0, "normal": 1, "high": 2, "critical": 3}
            min_level = importance_levels.get(min_importance, 0)
            filtered_history = [
                e for e in filtered_history
                if importance_levels.get(e["importance"], 0) >= min_level
            ]
        
        # Apply limit
        if limit:
            filtered_history = filtered_history[-limit:]
        
        return filtered_history
    
    def store_pattern(self, pattern_type: str, pattern_data: Dict):
        """
        Store a learned pattern or preference.
        
        Args:
            pattern_type: Type of pattern
            pattern_data: Pattern data
        """
        if pattern_type not in self.patterns:
            self.patterns[pattern_type] = []
        
        pattern = {
            "data": pattern_data,
            "learned_at": datetime.utcnow().isoformat()
        }
        
        self.patterns[pattern_type].append(pattern)
        self._save_patterns()
        
        self.logger.debug(f"Stored pattern: {pattern_type}")
    
    def get_patterns(self, pattern_type: str) -> List[Dict]:
        """Get all patterns of a specific type."""
        return self.patterns.get(pattern_type, [])
    
    def clear_memory(self, confirm: bool = False):
        """
        Clear all memory for this project.
        
        Args:
            confirm: Must be True to actually clear
        """
        if not confirm:
            raise ValueError("Must confirm memory clear operation")
        
        self.context = {}
        self.history = []
        self.patterns = {}
        
        self._save_context()
        self._save_history()
        self._save_patterns()
        
        self.logger.warning(f"Cleared all memory for project: {self.project_id}")
    
    def _save_context(self):
        """Save context to disk."""
        context_file = self.storage_path / "context.json"
        with open(context_file, 'w') as f:
            json.dump(self.context, f, indent=2)
    
    def _save_history(self):
        """Save history to disk."""
        history_file = self.storage_path / "history.json"
        with open(history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def _save_patterns(self):
        """Save patterns to disk."""
        patterns_file = self.storage_path / "patterns.json"
        with open(patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)
    
    def _load_memory(self):
        """Load all memory components from disk."""
        # Load context
        context_file = self.storage_path / "context.json"
        if context_file.exists():
            with open(context_file, 'r') as f:
                self.context = json.load(f)
        
        # Load history
        history_file = self.storage_path / "history.json"
        if history_file.exists():
            with open(history_file, 'r') as f:
                self.history = json.load(f)
        
        # Load patterns
        patterns_file = self.storage_path / "patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                self.patterns = json.load(f)
