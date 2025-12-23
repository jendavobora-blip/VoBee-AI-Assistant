"""
Project Manager - Orchestrates multiple parallel projects
Manages 1-50 parallel projects with resource allocation
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from uuid import uuid4

from .project import Project, ProjectStatus

logger = logging.getLogger(__name__)


class ProjectManager:
    """
    Central project management brain capable of handling 1-50 parallel projects
    Provides isolation, resource management, and orchestration capabilities
    """
    
    MAX_ACTIVE_PROJECTS = 50
    MAX_TOTAL_PROJECTS = 100
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self.created_at = datetime.utcnow().isoformat()
        logger.info("ProjectManager initialized")
    
    def create_project(
        self,
        name: str,
        description: str = "",
        budget: Optional[Dict[str, Any]] = None,
        goals: Optional[List[str]] = None,
        auto_activate: bool = True
    ) -> Project:
        """
        Create a new project
        
        Args:
            name: Project name
            description: Project description
            budget: Budget allocation
            goals: List of project goals
            auto_activate: Automatically activate project
            
        Returns:
            Created Project instance
            
        Raises:
            ValueError: If project limit reached
        """
        # Check active project limit
        active_count = self.get_active_project_count()
        if active_count >= self.MAX_ACTIVE_PROJECTS and auto_activate:
            raise ValueError(
                f"Maximum active projects ({self.MAX_ACTIVE_PROJECTS}) reached. "
                "Please sleep or archive some projects first."
            )
        
        # Check total project limit
        if len(self.projects) >= self.MAX_TOTAL_PROJECTS:
            raise ValueError(
                f"Maximum total projects ({self.MAX_TOTAL_PROJECTS}) reached. "
                "Please archive some projects first."
            )
        
        project_id = str(uuid4())
        project = Project(
            project_id=project_id,
            name=name,
            description=description,
            budget=budget,
            goals=goals
        )
        
        self.projects[project_id] = project
        logger.info(f"Created project '{name}' with ID {project_id}")
        
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get project by ID"""
        return self.projects.get(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """Get all projects"""
        return list(self.projects.values())
    
    def get_active_projects(self) -> List[Project]:
        """Get all active projects"""
        return [p for p in self.projects.values() if p.is_active()]
    
    def get_sleeping_projects(self) -> List[Project]:
        """Get all sleeping projects"""
        return [p for p in self.projects.values() if p.is_sleeping()]
    
    def get_active_project_count(self) -> int:
        """Get count of active projects"""
        return len(self.get_active_projects())
    
    def sleep_project(self, project_id: str) -> bool:
        """
        Put a project to sleep to free resources
        
        Args:
            project_id: ID of project to sleep
            
        Returns:
            True if successful, False otherwise
        """
        project = self.get_project(project_id)
        if project:
            result = project.sleep()
            if result:
                logger.info(f"Project {project_id} ({project.name}) put to sleep")
            return result
        return False
    
    def wake_project(self, project_id: str) -> bool:
        """
        Wake a project from sleep
        
        Args:
            project_id: ID of project to wake
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            ValueError: If active project limit reached
        """
        project = self.get_project(project_id)
        if not project:
            return False
        
        # Check if we can wake (active limit)
        if self.get_active_project_count() >= self.MAX_ACTIVE_PROJECTS:
            raise ValueError(
                f"Cannot wake project: Maximum active projects "
                f"({self.MAX_ACTIVE_PROJECTS}) reached"
            )
        
        result = project.wake()
        if result:
            logger.info(f"Project {project_id} ({project.name}) woken up")
        return result
    
    def archive_project(self, project_id: str) -> bool:
        """Archive a project (set to archived status)"""
        project = self.get_project(project_id)
        if project:
            project.status = ProjectStatus.ARCHIVED
            logger.info(f"Project {project_id} ({project.name}) archived")
            return True
        return False
    
    def delete_project(self, project_id: str) -> bool:
        """Permanently delete a project"""
        if project_id in self.projects:
            project = self.projects.pop(project_id)
            logger.info(f"Project {project_id} ({project.name}) deleted")
            return True
        return False
    
    def get_project_summary(self) -> Dict[str, Any]:
        """Get summary of all projects and their states"""
        total = len(self.projects)
        active = len(self.get_active_projects())
        sleeping = len(self.get_sleeping_projects())
        
        statuses = {}
        for status in ProjectStatus:
            count = len([p for p in self.projects.values() if p.status == status])
            statuses[status.value] = count
        
        return {
            'total_projects': total,
            'active_projects': active,
            'sleeping_projects': sleeping,
            'max_active': self.MAX_ACTIVE_PROJECTS,
            'max_total': self.MAX_TOTAL_PROJECTS,
            'capacity_utilization': f"{(active/self.MAX_ACTIVE_PROJECTS)*100:.1f}%",
            'status_breakdown': statuses,
            'created_at': self.created_at,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def auto_sleep_idle_projects(self, idle_threshold_minutes: int = 30) -> List[str]:
        """
        Automatically sleep projects that have been idle
        
        Args:
            idle_threshold_minutes: Minutes of inactivity before auto-sleep
            
        Returns:
            List of project IDs that were put to sleep
        """
        from datetime import timedelta
        
        slept_projects = []
        now = datetime.utcnow()
        threshold = timedelta(minutes=idle_threshold_minutes)
        
        for project in self.get_active_projects():
            last_active = datetime.fromisoformat(project.last_active_at)
            if now - last_active > threshold:
                if self.sleep_project(project.project_id):
                    slept_projects.append(project.project_id)
                    logger.info(
                        f"Auto-slept idle project {project.project_id} "
                        f"({project.name})"
                    )
        
        return slept_projects
    
    def to_dict(self) -> Dict[str, Any]:
        """Export all projects to dictionary"""
        return {
            'projects': {
                pid: project.to_dict() 
                for pid, project in self.projects.items()
            },
            'summary': self.get_project_summary()
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Import projects from dictionary"""
        if 'projects' in data:
            for project_id, project_data in data['projects'].items():
                self.projects[project_id] = Project.from_dict(project_data)
            logger.info(f"Loaded {len(self.projects)} projects from data")
