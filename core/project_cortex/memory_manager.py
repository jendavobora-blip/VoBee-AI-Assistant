"""
Memory Manager - Handles isolated memory for each project
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Manages isolated memory storage for projects
    Supports different memory types: short-term, long-term, context
    """
    
    def __init__(self):
        self.project_memories: Dict[str, Dict[str, Any]] = {}
        logger.info("MemoryManager initialized")
    
    def create_project_memory(self, project_id: str):
        """Initialize memory storage for a new project"""
        if project_id not in self.project_memories:
            self.project_memories[project_id] = {
                'short_term': {},  # Temporary memory (session-based)
                'long_term': {},   # Persistent memory
                'context': {},     # Current context/state
                'metadata': {
                    'created_at': datetime.utcnow().isoformat(),
                    'total_entries': 0,
                    'last_accessed': datetime.utcnow().isoformat()
                }
            }
            logger.info(f"Created memory storage for project {project_id}")
    
    def store(
        self,
        project_id: str,
        key: str,
        value: Any,
        memory_type: str = "long_term"
    ):
        """
        Store data in project memory
        
        Args:
            project_id: Project identifier
            key: Memory key
            value: Value to store
            memory_type: Type of memory (short_term, long_term, context)
        """
        if project_id not in self.project_memories:
            self.create_project_memory(project_id)
        
        if memory_type not in ['short_term', 'long_term', 'context']:
            memory_type = 'long_term'
        
        self.project_memories[project_id][memory_type][key] = {
            'value': value,
            'stored_at': datetime.utcnow().isoformat(),
            'type': type(value).__name__
        }
        
        # Update metadata
        self.project_memories[project_id]['metadata']['total_entries'] += 1
        self.project_memories[project_id]['metadata']['last_accessed'] = \
            datetime.utcnow().isoformat()
    
    def retrieve(
        self,
        project_id: str,
        key: str,
        memory_type: str = "long_term"
    ) -> Optional[Any]:
        """
        Retrieve data from project memory
        
        Args:
            project_id: Project identifier
            key: Memory key
            memory_type: Type of memory to retrieve from
            
        Returns:
            Stored value or None if not found
        """
        if project_id not in self.project_memories:
            return None
        
        if memory_type not in ['short_term', 'long_term', 'context']:
            memory_type = 'long_term'
        
        memory_store = self.project_memories[project_id].get(memory_type, {})
        
        if key in memory_store:
            # Update last accessed
            self.project_memories[project_id]['metadata']['last_accessed'] = \
                datetime.utcnow().isoformat()
            return memory_store[key]['value']
        
        return None
    
    def delete(
        self,
        project_id: str,
        key: str,
        memory_type: str = "long_term"
    ) -> bool:
        """Delete a memory entry"""
        if project_id not in self.project_memories:
            return False
        
        memory_store = self.project_memories[project_id].get(memory_type, {})
        
        if key in memory_store:
            del memory_store[key]
            # Decrement total entries counter
            self.project_memories[project_id]['metadata']['total_entries'] -= 1
            return True
        
        return False
    
    def clear_short_term(self, project_id: str):
        """Clear short-term memory for a project"""
        if project_id in self.project_memories:
            self.project_memories[project_id]['short_term'] = {}
            logger.info(f"Cleared short-term memory for project {project_id}")
    
    def clear_all(self, project_id: str):
        """Clear all memory for a project"""
        if project_id in self.project_memories:
            del self.project_memories[project_id]
            logger.info(f"Cleared all memory for project {project_id}")
    
    def get_memory_stats(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get memory statistics for a project"""
        if project_id not in self.project_memories:
            return None
        
        memory = self.project_memories[project_id]
        
        return {
            'project_id': project_id,
            'short_term_count': len(memory.get('short_term', {})),
            'long_term_count': len(memory.get('long_term', {})),
            'context_count': len(memory.get('context', {})),
            'total_entries': memory['metadata']['total_entries'],
            'created_at': memory['metadata']['created_at'],
            'last_accessed': memory['metadata']['last_accessed']
        }
    
    def search_memory(
        self,
        project_id: str,
        search_term: str,
        memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search through project memory
        
        Args:
            project_id: Project identifier
            search_term: Term to search for in keys
            memory_type: Optional memory type filter
            
        Returns:
            List of matching memory entries
        """
        if project_id not in self.project_memories:
            return []
        
        results = []
        memory = self.project_memories[project_id]
        
        memory_types = [memory_type] if memory_type else ['short_term', 'long_term', 'context']
        
        for mtype in memory_types:
            if mtype not in memory:
                continue
            
            for key, entry in memory[mtype].items():
                if search_term.lower() in key.lower():
                    results.append({
                        'key': key,
                        'value': entry['value'],
                        'memory_type': mtype,
                        'stored_at': entry['stored_at']
                    })
        
        return results
