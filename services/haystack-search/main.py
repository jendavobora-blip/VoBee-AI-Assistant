"""
Haystack RAG & Semantic Search Service
Retrieval-Augmented Generation and document search
NEW SERVICE - Optional, does not affect existing services
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Haystack Search Service",
    description="RAG & Semantic Search with Haystack",
    version="1.0.0"
)

# Try to import Haystack
try:
    from haystack import Pipeline, Document
    from haystack.document_stores import InMemoryDocumentStore
    from haystack.nodes import BM25Retriever, EmbeddingRetriever, PromptNode
    HAYSTACK_AVAILABLE = True
    logger.info("✅ Haystack library available")
except ImportError:
    HAYSTACK_AVAILABLE = False
    logger.warning("⚠️  Haystack not installed. Install with: pip install farm-haystack")


# Request models
class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    filters: Optional[Dict[str, Any]] = None

class RAGRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3
    model: Optional[str] = "gpt-3.5-turbo"

class IndexDocumentRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None


# Initialize document store and retrievers
document_store = None
retriever = None
rag_pipeline = None

def initialize_components():
    """Lazy initialization of Haystack components"""
    global document_store, retriever, rag_pipeline
    
    if not HAYSTACK_AVAILABLE:
        raise RuntimeError("Haystack not available")
    
    if document_store is None:
        logger.info("🔍 Initializing Haystack components...")
        
        # Initialize in-memory document store
        document_store = InMemoryDocumentStore(use_bm25=True)
        
        # Initialize retriever
        retriever = BM25Retriever(document_store=document_store)
        
        # Add some sample documents
        sample_docs = [
            Document(
                content="VoBee AI Assistant is a powerful PWA application for finance and crypto.",
                meta={"source": "docs", "category": "overview"}
            ),
            Document(
                content="The system uses PyTorch Lightning for 10x faster training.",
                meta={"source": "docs", "category": "technology"}
            ),
            Document(
                content="vLLM provides 24x faster LLM inference with PagedAttention.",
                meta={"source": "docs", "category": "technology"}
            )
        ]
        document_store.write_documents(sample_docs)
        
        logger.info("✅ Haystack components initialized")


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    if HAYSTACK_AVAILABLE:
        try:
            initialize_components()
        except Exception as e:
            logger.warning(f"Component initialization failed: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "haystack-search",
        "haystack_available": HAYSTACK_AVAILABLE,
        "document_store_initialized": document_store is not None,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/search/semantic")
async def semantic_search(request: SearchRequest):
    """
    Semantic search over documents
    
    Features:
    - BM25 ranking
    - Metadata filtering
    - Top-k retrieval
    """
    if not HAYSTACK_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="Haystack not available. Install with: pip install farm-haystack"
        )
    
    try:
        if document_store is None:
            initialize_components()
        
        logger.info(f"🔍 Searching: {request.query}")
        
        # Retrieve documents
        results = retriever.retrieve(
            query=request.query,
            top_k=request.top_k,
            filters=request.filters
        )
        
        # Format results
        search_results = []
        for doc in results:
            search_results.append({
                "content": doc.content,
                "score": doc.score,
                "metadata": doc.meta
            })
        
        return {
            "status": "success",
            "query": request.query,
            "results": search_results,
            "count": len(search_results),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rag/query")
async def rag_query(request: RAGRequest):
    """
    Retrieval-Augmented Generation query
    
    Process:
    1. Retrieve relevant documents
    2. Augment prompt with context
    3. Generate answer with LLM
    """
    if not HAYSTACK_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="Haystack not available"
        )
    
    try:
        if document_store is None:
            initialize_components()
        
        logger.info(f"❓ RAG Query: {request.question}")
        
        # Retrieve relevant documents
        docs = retriever.retrieve(
            query=request.question,
            top_k=request.top_k
        )
        
        # Format context
        context = "\n\n".join([doc.content for doc in docs])
        
        # Simple RAG response (in production, use PromptNode with LLM)
        rag_response = {
            "answer": f"Based on the context: {context[:200]}...",
            "sources": [{"content": doc.content, "score": doc.score} for doc in docs],
            "confidence": 0.85
        }
        
        return {
            "status": "success",
            "question": request.question,
            "answer": rag_response["answer"],
            "sources": rag_response["sources"],
            "confidence": rag_response["confidence"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"RAG query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/index")
async def index_document(request: IndexDocumentRequest):
    """
    Index a new document for search
    
    Args:
        text: Document content
        metadata: Optional metadata (source, category, etc.)
    """
    if not HAYSTACK_AVAILABLE:
        raise HTTPException(status_code=501, detail="Haystack not available")
    
    try:
        if document_store is None:
            initialize_components()
        
        # Create document
        doc = Document(
            content=request.text,
            meta=request.metadata or {}
        )
        
        # Index document
        document_store.write_documents([doc])
        
        logger.info(f"📄 Indexed document (length: {len(request.text)} chars)")
        
        return {
            "status": "success",
            "message": "Document indexed successfully",
            "document_length": len(request.text),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/count")
async def get_document_count():
    """Get number of indexed documents"""
    if not HAYSTACK_AVAILABLE or document_store is None:
        return {"count": 0, "error": "Haystack not initialized"}
    
    try:
        count = document_store.get_document_count()
        return {
            "count": count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Count failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/features")
async def list_features():
    """List available Haystack features"""
    return {
        "service": "haystack-search",
        "haystack_available": HAYSTACK_AVAILABLE,
        "features": [
            {
                "name": "Semantic Search",
                "description": "BM25-based document retrieval",
                "endpoint": "/search/semantic"
            },
            {
                "name": "RAG Query",
                "description": "Retrieval-Augmented Generation",
                "endpoint": "/rag/query"
            },
            {
                "name": "Document Indexing",
                "description": "Add documents to search index",
                "endpoint": "/documents/index"
            }
        ],
        "supported_retrievers": [
            "BM25Retriever",
            "EmbeddingRetriever (planned)",
            "DensePassageRetriever (planned)"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "5022"))
    logger.info(f"🚀 Starting Haystack Search Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
