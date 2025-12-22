"""
Qdrant Memory Service
Provides user-specific memory and context storage
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"


class MemoryService:
    """Manages user memories in Qdrant vector database"""
    
    def __init__(self):
        self.client = None
        self.collection_name = "user_memories"
        self.vector_size = 384  # Mock embedding size
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Qdrant client"""
        try:
            self.client = QdrantClient(url=QDRANT_URL)
            
            # Create collection if it doesn't exist
            collections = self.client.get_collections().collections
            if not any(col.name == self.collection_name for col in collections):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            
            logger.info("Qdrant client initialized")
        
        except Exception as e:
            logger.warning(f"Failed to initialize Qdrant: {e}")
            if MOCK_MODE:
                logger.info("Running in mock mode without Qdrant")
                self.client = None
    
    def _generate_mock_embedding(self, text: str) -> List[float]:
        """Generate a mock embedding vector"""
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to vector
        vector = []
        for i in range(self.vector_size):
            byte_val = hash_bytes[i % len(hash_bytes)]
            vector.append((byte_val / 255.0) * 2 - 1)  # Normalize to [-1, 1]
        
        return vector
    
    def store_memory(self, user_id: str, memory: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Store a memory for a user"""
        
        if not self.client and not MOCK_MODE:
            return False
        
        try:
            # Generate embedding
            embedding = self._generate_mock_embedding(memory)
            
            # Create point
            point_id = hash(f"{user_id}-{memory}-{datetime.utcnow().isoformat()}")
            
            payload = {
                "user_id": user_id,
                "memory": memory,
                "timestamp": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
            
            if self.client:
                point = PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
                
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=[point]
                )
            
            logger.info(f"Memory stored for user {user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            return False
    
    def search_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search user memories"""
        
        if not self.client:
            # Return mock memories in mock mode
            return [
                {
                    "memory": "User prefers detailed explanations",
                    "score": 0.9,
                    "timestamp": datetime.utcnow().isoformat()
                }
            ]
        
        try:
            # Generate query embedding
            query_embedding = self._generate_mock_embedding(query)
            
            # Search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter={
                    "must": [
                        {"key": "user_id", "match": {"value": user_id}}
                    ]
                },
                limit=limit
            )
            
            memories = []
            for result in results:
                memories.append({
                    "memory": result.payload.get("memory"),
                    "score": result.score,
                    "timestamp": result.payload.get("timestamp"),
                    "metadata": {k: v for k, v in result.payload.items() 
                               if k not in ["user_id", "memory", "timestamp"]}
                })
            
            return memories
        
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            return []
    
    def get_user_context(self, user_id: str) -> str:
        """Get user context for AI interactions"""
        memories = self.search_memories(user_id, "context", limit=3)
        
        if not memories:
            return "No previous context available."
        
        context_parts = []
        for mem in memories:
            context_parts.append(f"- {mem['memory']}")
        
        return "User Context:\n" + "\n".join(context_parts)


# Global instance
_memory_service = None


def get_memory_service() -> MemoryService:
    """Get or create the global MemoryService instance"""
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService()
    return _memory_service
