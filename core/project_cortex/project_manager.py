"""
Project Manager - Orchestrates multiple projects with isolated contexts.

Handles project lifecycle:
- Creation and initialization
- State management (active/paused)
- Project switching
- Resource allocation per project
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from pathlib import Path


class ProjectState(Enum):
    """Project operational states."""
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"
    INITIALIZING = "initializing"


class ProjectManager:
    """
    Manages multiple projects with isolated memory and budgets.
    
    Features:
    - Isolated project memory and context
    - Per-project budget tracking
    - Active/paused state management
    - Deterministic project switching
    """
    
    def __init__(self, storage_path: str = "data/projects"):
        """
        Initialize the Project Manager.
        
        Args:
            storage_path: Directory for storing project data
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.projects: Dict[str, dict] = {}
        self.active_project_id: Optional[str] = None
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Load existing projects
        self._load_projects()
        
        self.logger.info(f"ProjectManager initialized with {len(self.projects)} projects")
    
    def create_project(
        self,
        project_id: str,
        name: str,
        description: str = "",
        budget_limit: Optional[float] = None,
        quality_preference: str = "balanced"
    ) -> dict:
        """
        Create a new project with isolated context.
        
        Args:
            project_id: Unique identifier for the project
            name: Human-readable project name
            description: Project description
            budget_limit: Optional budget limit in dollars
            quality_preference: 'speed', 'balanced', or 'quality'
        
        Returns:
            dict: Project configuration
        """
        if project_id in self.projects:
            raise ValueError(f"Project '{project_id}' already exists")
        
        # TODO: Add validation for budget_limit range
        # TODO: Add validation for quality_preference options
        
        project = {
            "id": project_id,
            "name": name,
            "description": description,
            "state": ProjectState.INITIALIZING.value,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "budget_limit": budget_limit,
            "budget_used": 0.0,
            "quality_preference": quality_preference,
            "metadata": {}
        }
        
        self.projects[project_id] = project
        self._save_project(project_id)
        
        self.logger.info(f"Created project: {project_id} - {name}")
        
        return project
    
    def activate_project(self, project_id: str) -> dict:
        """
        Activate a project (make it the current working project).
        
        Args:
            project_id: Project to activate
            
        Returns:
            dict: Activated project
        """
        if project_id not in self.projects:
            raise ValueError(f"Project '{project_id}' not found")
        
        project = self.projects[project_id]
        
        if project["state"] == ProjectState.ARCHIVED.value:
            raise ValueError(f"Cannot activate archived project '{project_id}'")
        
        # Pause current active project if exists
        if self.active_project_id and self.active_project_id != project_id:
            self.pause_project(self.active_project_id)
        
        project["state"] = ProjectState.ACTIVE.value
        project["updated_at"] = datetime.utcnow().isoformat()
        self.active_project_id = project_id
        
        self._save_project(project_id)
        
        self.logger.info(f"Activated project: {project_id}")
        
        return project
    
    def pause_project(self, project_id: str) -> dict:
        """
        Pause a project (suspend operations without losing state).
        
        Args:
            project_id: Project to pause
            
        Returns:
            dict: Paused project
        """
        if project_id not in self.projects:
            raise ValueError(f"Project '{project_id}' not found")
        
        project = self.projects[project_id]
        project["state"] = ProjectState.PAUSED.value
        project["updated_at"] = datetime.utcnow().isoformat()
        
        if self.active_project_id == project_id:
            self.active_project_id = None
        
        self._save_project(project_id)
        
        self.logger.info(f"Paused project: {project_id}")
        
        return project
    
    def get_project(self, project_id: str) -> Optional[dict]:
        """Get project by ID."""
        return self.projects.get(project_id)
    
    def get_active_project(self) -> Optional[dict]:
        """Get currently active project."""
        if self.active_project_id:
            return self.projects.get(self.active_project_id)
        return None
    
    def list_projects(self, state_filter: Optional[str] = None) -> List[dict]:
        """
        List all projects, optionally filtered by state.
        
        Args:
            state_filter: Optional state to filter by
            
        Returns:
            List of projects
        """
        projects = list(self.projects.values())
        
        if state_filter:
            projects = [p for p in projects if p["state"] == state_filter]
        
        return sorted(projects, key=lambda p: p["created_at"], reverse=True)
    
    def update_budget_usage(self, project_id: str, cost: float) -> dict:
        """
        Update budget usage for a project.
        
        Args:
            project_id: Project ID
            cost: Cost to add to budget usage
            
        Returns:
            Updated project
        """
        if project_id not in self.projects:
            raise ValueError(f"Project '{project_id}' not found")
        
        project = self.projects[project_id]
        project["budget_used"] += cost
        project["updated_at"] = datetime.utcnow().isoformat()
        
        # Check budget limit
        if project["budget_limit"] and project["budget_used"] > project["budget_limit"]:
            self.logger.warning(
                f"Project '{project_id}' exceeded budget limit: "
                f"${project['budget_used']:.2f} > ${project['budget_limit']:.2f}"
            )
        
        self._save_project(project_id)
        
        return project
    
    def _save_project(self, project_id: str):
        """Save project to disk."""
        project = self.projects[project_id]
        project_file = self.storage_path / f"{project_id}.json"
        
        with open(project_file, 'w') as f:
            json.dump(project, f, indent=2)
        
        self.logger.debug(f"Saved project: {project_id}")
    
    def _load_projects(self):
        """Load all projects from disk."""
        if not self.storage_path.exists():
            return
        
        for project_file in self.storage_path.glob("*.json"):
            try:
                with open(project_file, 'r') as f:
                    project = json.load(f)
                    self.projects[project["id"]] = project
                    
                    # Restore active project
                    if project["state"] == ProjectState.ACTIVE.value:
                        self.active_project_id = project["id"]
            except Exception as e:
                self.logger.error(f"Failed to load project from {project_file}: {e}")
