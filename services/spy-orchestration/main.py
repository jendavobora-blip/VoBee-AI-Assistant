"""
Spy-Orchestration Pipeline Service
Automated scouting for AI models, open-source tech, and research papers
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime, timedelta
import httpx
import hashlib
import json
import os
import asyncpg
from uuid import uuid4
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL', 
    'postgresql://orchestrator:password@postgres:5432/orchestrator_db'
)

# API Keys
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

# Database connection pool
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    global db_pool
    # Startup
    try:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        logger.info("Database connection pool created")
        await init_database()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    yield
    
    # Shutdown
    if db_pool:
        await db_pool.close()
        logger.info("Database connection pool closed")

app = FastAPI(
    title="Spy-Orchestration Pipeline",
    description="Automated scouting for AI models, research, and technologies",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ScanRequest(BaseModel):
    scan_type: str = Field(..., description="Type of scan: github, research, blog")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)

class DiscoveryResult(BaseModel):
    result_id: str
    scan_type: str
    title: str
    description: str
    url: str
    relevance_score: float
    metadata: Dict[str, Any]
    discovered_at: str

class ScanStatus(BaseModel):
    scan_id: str
    status: str  # pending, running, completed, failed
    scan_type: str
    started_at: str
    completed_at: Optional[str] = None
    results_count: int = 0
    error: Optional[str] = None

# Database initialization
async def init_database():
    """Initialize database tables"""
    if not db_pool:
        return
    
    async with db_pool.acquire() as conn:
        # Create scan results table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS spy_discoveries (
                result_id VARCHAR(255) PRIMARY KEY,
                scan_id VARCHAR(255),
                scan_type VARCHAR(50) NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                url TEXT NOT NULL,
                content_hash VARCHAR(64) UNIQUE,
                relevance_score FLOAT DEFAULT 0.5,
                metadata JSONB,
                discovered_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # Create scan jobs table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS spy_scans (
                scan_id VARCHAR(255) PRIMARY KEY,
                scan_type VARCHAR(50) NOT NULL,
                parameters JSONB,
                status VARCHAR(50) DEFAULT 'pending',
                started_at TIMESTAMP DEFAULT NOW(),
                completed_at TIMESTAMP,
                results_count INTEGER DEFAULT 0,
                error TEXT
            )
        ''')
        
        # Create index for deduplication
        await conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_content_hash ON spy_discoveries(content_hash)
        ''')
        
        logger.info("Spy-orchestration database tables initialized")

async def store_discovery(discovery: DiscoveryResult, scan_id: str) -> bool:
    """
    Store discovery with deduplication
    Returns True if stored (new), False if duplicate
    """
    if not db_pool:
        return False
    
    # Generate content hash for deduplication
    content = f"{discovery.title}|{discovery.url}".encode()
    content_hash = hashlib.sha256(content).hexdigest()
    
    try:
        async with db_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO spy_discoveries 
                (result_id, scan_id, scan_type, title, description, url, content_hash, 
                 relevance_score, metadata, discovered_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (content_hash) DO NOTHING
            ''', discovery.result_id, scan_id, discovery.scan_type, discovery.title,
            discovery.description, discovery.url, content_hash, discovery.relevance_score,
            json.dumps(discovery.metadata), discovery.discovered_at)
            
            # Check if actually inserted
            result = await conn.fetchval(
                'SELECT COUNT(*) FROM spy_discoveries WHERE content_hash = $1',
                content_hash
            )
            return result == 1
    
    except Exception as e:
        logger.error(f"Error storing discovery: {e}")
        return False

async def update_scan_status(scan_id: str, status: str, results_count: int = 0, 
                             error: Optional[str] = None):
    """Update scan job status"""
    if not db_pool:
        return
    
    async with db_pool.acquire() as conn:
        if status == 'completed' or status == 'failed':
            await conn.execute('''
                UPDATE spy_scans 
                SET status = $1, results_count = $2, error = $3, completed_at = NOW()
                WHERE scan_id = $4
            ''', status, results_count, error, scan_id)
        else:
            await conn.execute('''
                UPDATE spy_scans 
                SET status = $1, results_count = $2
                WHERE scan_id = $3
            ''', status, results_count, scan_id)

# GitHub scanning
async def scan_github(scan_id: str, parameters: Dict[str, Any]) -> List[DiscoveryResult]:
    """
    Scan GitHub for relevant repositories
    """
    logger.info(f"Starting GitHub scan: {scan_id}")
    
    query = parameters.get('query', 'AI machine learning stars:>100')
    max_results = parameters.get('max_results', 50)
    
    discoveries = []
    
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    try:
        async with httpx.AsyncClient() as client:
            # Search repositories
            response = await client.get(
                'https://api.github.com/search/repositories',
                params={
                    'q': query,
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': min(max_results, 100)
                },
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            for repo in data.get('items', []):
                # Calculate relevance score
                relevance_score = calculate_repo_relevance(repo, parameters)
                
                # Filter by minimum relevance
                min_relevance = parameters.get('min_relevance', 0.3)
                if relevance_score < min_relevance:
                    continue
                
                discovery = DiscoveryResult(
                    result_id=str(uuid4()),
                    scan_type='github',
                    title=repo['full_name'],
                    description=repo.get('description', ''),
                    url=repo['html_url'],
                    relevance_score=relevance_score,
                    metadata={
                        'stars': repo['stargazers_count'],
                        'forks': repo['forks_count'],
                        'language': repo.get('language'),
                        'topics': repo.get('topics', []),
                        'updated_at': repo['updated_at'],
                        'license': repo.get('license', {}).get('name') if repo.get('license') else None
                    },
                    discovered_at=datetime.utcnow().isoformat()
                )
                
                discoveries.append(discovery)
                
                # Store in database
                is_new = await store_discovery(discovery, scan_id)
                if is_new:
                    logger.info(f"New repository discovered: {repo['full_name']}")
                else:
                    logger.debug(f"Duplicate repository skipped: {repo['full_name']}")
    
    except Exception as e:
        logger.error(f"Error scanning GitHub: {e}")
        raise
    
    return discoveries

def calculate_repo_relevance(repo: Dict, parameters: Dict) -> float:
    """
    Calculate relevance score for a GitHub repository
    Based on stars, recency, topics, and keywords
    """
    score = 0.0
    
    # Stars contribution (0-0.3)
    stars = repo['stargazers_count']
    if stars > 10000:
        score += 0.3
    elif stars > 1000:
        score += 0.2
    elif stars > 100:
        score += 0.1
    
    # Recency contribution (0-0.2)
    try:
        updated_at = datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))
        days_since_update = (datetime.utcnow().replace(tzinfo=updated_at.tzinfo) - updated_at).days
        if days_since_update < 30:
            score += 0.2
        elif days_since_update < 180:
            score += 0.1
    except:
        pass
    
    # Topics contribution (0-0.3)
    topics = repo.get('topics', [])
    ai_topics = ['machine-learning', 'deep-learning', 'artificial-intelligence', 
                 'neural-networks', 'llm', 'gpt', 'transformer', 'ai']
    matching_topics = sum(1 for topic in topics if topic in ai_topics)
    score += min(0.3, matching_topics * 0.1)
    
    # Keywords in description (0-0.2)
    description = (repo.get('description') or '').lower()
    keywords = parameters.get('keywords', ['ai', 'ml', 'machine learning'])
    if any(kw.lower() in description for kw in keywords):
        score += 0.2
    
    return min(1.0, score)

# Research paper scanning
async def scan_research(scan_id: str, parameters: Dict[str, Any]) -> List[DiscoveryResult]:
    """
    Scan arXiv and other sources for research papers
    """
    logger.info(f"Starting research scan: {scan_id}")
    
    query = parameters.get('query', 'artificial intelligence')
    max_results = parameters.get('max_results', 50)
    category = parameters.get('category', 'cs.AI')  # Computer Science - AI
    
    discoveries = []
    
    try:
        async with httpx.AsyncClient() as client:
            # Query arXiv API
            response = await client.get(
                'http://export.arxiv.org/api/query',
                params={
                    'search_query': f'cat:{category} AND all:{query}',
                    'start': 0,
                    'max_results': max_results,
                    'sortBy': 'submittedDate',
                    'sortOrder': 'descending'
                },
                timeout=60.0
            )
            response.raise_for_status()
            
            # Parse XML response (simple parsing)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.text)
            
            # Namespace for arXiv
            ns = {'atom': 'http://www.w3.org/2005/Atom', 
                  'arxiv': 'http://arxiv.org/schemas/atom'}
            
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                id_elem = entry.find('atom:id', ns)
                published_elem = entry.find('atom:published', ns)
                
                if title_elem is None or id_elem is None:
                    continue
                
                title = title_elem.text.strip()
                summary = summary_elem.text.strip() if summary_elem is not None else ''
                url = id_elem.text.strip()
                published = published_elem.text if published_elem is not None else ''
                
                # Get authors
                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None:
                        authors.append(name_elem.text)
                
                # Calculate relevance
                relevance_score = calculate_paper_relevance(title, summary, parameters)
                
                # Filter by minimum relevance
                min_relevance = parameters.get('min_relevance', 0.3)
                if relevance_score < min_relevance:
                    continue
                
                discovery = DiscoveryResult(
                    result_id=str(uuid4()),
                    scan_type='research',
                    title=title,
                    description=summary[:500],  # Truncate summary
                    url=url,
                    relevance_score=relevance_score,
                    metadata={
                        'authors': authors,
                        'published': published,
                        'category': category
                    },
                    discovered_at=datetime.utcnow().isoformat()
                )
                
                discoveries.append(discovery)
                
                # Store in database
                is_new = await store_discovery(discovery, scan_id)
                if is_new:
                    logger.info(f"New paper discovered: {title[:50]}...")
    
    except Exception as e:
        logger.error(f"Error scanning research papers: {e}")
        raise
    
    return discoveries

def calculate_paper_relevance(title: str, summary: str, parameters: Dict) -> float:
    """Calculate relevance score for a research paper"""
    score = 0.0
    
    combined_text = f"{title} {summary}".lower()
    
    # Keywords matching (0-0.5)
    keywords = parameters.get('keywords', ['neural', 'learning', 'ai', 'model'])
    matches = sum(1 for kw in keywords if kw.lower() in combined_text)
    score += min(0.5, matches * 0.15)
    
    # Title relevance (0-0.3)
    if any(kw.lower() in title.lower() for kw in keywords):
        score += 0.3
    
    # Base relevance (0.2)
    score += 0.2
    
    return min(1.0, score)

# Technology blog scanning
async def scan_blogs(scan_id: str, parameters: Dict[str, Any]) -> List[DiscoveryResult]:
    """
    Scan technology blogs and news sources
    Simulated implementation - can be extended to scrape actual blogs
    """
    logger.info(f"Starting blog scan: {scan_id}")
    
    # This is a simplified implementation
    # In production, integrate with RSS feeds, APIs, or web scraping
    
    discoveries = []
    
    # Example: Known AI/ML blog sources
    blog_sources = [
        {
            'name': 'OpenAI Blog',
            'url': 'https://openai.com/blog',
            'topics': ['GPT', 'DALL-E', 'ChatGPT', 'AI Safety']
        },
        {
            'name': 'Google AI Blog',
            'url': 'https://ai.googleblog.com',
            'topics': ['TensorFlow', 'BERT', 'Neural Networks']
        },
        {
            'name': 'DeepMind Blog',
            'url': 'https://deepmind.com/blog',
            'topics': ['AlphaGo', 'Reinforcement Learning', 'Protein Folding']
        }
    ]
    
    for source in blog_sources:
        discovery = DiscoveryResult(
            result_id=str(uuid4()),
            scan_type='blog',
            title=source['name'],
            description=f"Technology blog covering: {', '.join(source['topics'])}",
            url=source['url'],
            relevance_score=0.7,
            metadata={
                'topics': source['topics'],
                'source_type': 'blog'
            },
            discovered_at=datetime.utcnow().isoformat()
        )
        
        discoveries.append(discovery)
        await store_discovery(discovery, scan_id)
    
    return discoveries

# Background task for scanning
async def perform_scan(scan_id: str, scan_type: str, parameters: Dict[str, Any]):
    """Perform scan in background"""
    try:
        await update_scan_status(scan_id, 'running')
        
        if scan_type == 'github':
            results = await scan_github(scan_id, parameters)
        elif scan_type == 'research':
            results = await scan_research(scan_id, parameters)
        elif scan_type == 'blog':
            results = await scan_blogs(scan_id, parameters)
        else:
            raise ValueError(f"Unknown scan type: {scan_type}")
        
        await update_scan_status(scan_id, 'completed', results_count=len(results))
        logger.info(f"Scan {scan_id} completed with {len(results)} results")
        
    except Exception as e:
        logger.error(f"Scan {scan_id} failed: {e}")
        await update_scan_status(scan_id, 'failed', error=str(e))

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if db_pool else "disconnected"
    return {
        "status": "healthy",
        "service": "spy-orchestration",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/scan")
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks) -> ScanStatus:
    """Start a new scanning job"""
    try:
        scan_id = str(uuid4())
        
        # Store scan job
        if db_pool:
            async with db_pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO spy_scans (scan_id, scan_type, parameters, status)
                    VALUES ($1, $2, $3, 'pending')
                ''', scan_id, request.scan_type, json.dumps(request.parameters))
        
        # Start scan in background
        background_tasks.add_task(perform_scan, scan_id, request.scan_type, request.parameters)
        
        return ScanStatus(
            scan_id=scan_id,
            status='pending',
            scan_type=request.scan_type,
            started_at=datetime.utcnow().isoformat(),
            results_count=0
        )
    
    except Exception as e:
        logger.error(f"Error starting scan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scan/{scan_id}")
async def get_scan_status(scan_id: str) -> ScanStatus:
    """Get status of a scan job"""
    try:
        if not db_pool:
            raise HTTPException(status_code=503, detail="Database unavailable")
        
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow('''
                SELECT * FROM spy_scans WHERE scan_id = $1
            ''', scan_id)
            
            if not row:
                raise HTTPException(status_code=404, detail="Scan not found")
            
            return ScanStatus(
                scan_id=row['scan_id'],
                status=row['status'],
                scan_type=row['scan_type'],
                started_at=row['started_at'].isoformat(),
                completed_at=row['completed_at'].isoformat() if row['completed_at'] else None,
                results_count=row['results_count'],
                error=row['error']
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting scan status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/discoveries")
async def list_discoveries(scan_type: Optional[str] = None, 
                          min_relevance: float = 0.5,
                          limit: int = 100) -> List[DiscoveryResult]:
    """List all discoveries with optional filtering"""
    try:
        if not db_pool:
            raise HTTPException(status_code=503, detail="Database unavailable")
        
        async with db_pool.acquire() as conn:
            if scan_type:
                rows = await conn.fetch('''
                    SELECT * FROM spy_discoveries
                    WHERE scan_type = $1 AND relevance_score >= $2
                    ORDER BY relevance_score DESC, discovered_at DESC
                    LIMIT $3
                ''', scan_type, min_relevance, limit)
            else:
                rows = await conn.fetch('''
                    SELECT * FROM spy_discoveries
                    WHERE relevance_score >= $1
                    ORDER BY relevance_score DESC, discovered_at DESC
                    LIMIT $2
                ''', min_relevance, limit)
            
            results = []
            for row in rows:
                results.append(DiscoveryResult(
                    result_id=row['result_id'],
                    scan_type=row['scan_type'],
                    title=row['title'],
                    description=row['description'] or '',
                    url=row['url'],
                    relevance_score=row['relevance_score'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    discovered_at=row['discovered_at'].isoformat()
                ))
            
            return results
    
    except Exception as e:
        logger.error(f"Error listing discoveries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats() -> Dict[str, Any]:
    """Get statistics about discoveries"""
    try:
        if not db_pool:
            raise HTTPException(status_code=503, detail="Database unavailable")
        
        async with db_pool.acquire() as conn:
            total = await conn.fetchval('SELECT COUNT(*) FROM spy_discoveries')
            
            by_type = await conn.fetch('''
                SELECT scan_type, COUNT(*) as count
                FROM spy_discoveries
                GROUP BY scan_type
            ''')
            
            recent = await conn.fetchval('''
                SELECT COUNT(*) FROM spy_discoveries
                WHERE discovered_at > NOW() - INTERVAL '7 days'
            ''')
            
            return {
                'total_discoveries': total,
                'discoveries_by_type': {row['scan_type']: row['count'] for row in by_type},
                'discoveries_last_7_days': recent,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5006)
