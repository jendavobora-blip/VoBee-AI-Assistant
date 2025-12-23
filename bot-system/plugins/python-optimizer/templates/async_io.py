"""
Async I/O Template for FastAPI Services

This template shows how to optimize I/O-bound operations with async/await.
"""

import asyncio
import aiohttp
import aiofiles
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AsyncHTTPClient:
    """
    Optimized async HTTP client with connection pooling and retry logic.
    """
    
    def __init__(
        self,
        timeout: int = 30,
        max_connections: int = 100,
        retry_attempts: int = 3,
    ):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_connections = max_connections
        self.retry_attempts = retry_attempts
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Create session on context manager entry"""
        connector = aiohttp.TCPConnector(limit=self.max_connections)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=self.timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session on context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """
        Perform async GET request with retry logic.
        """
        for attempt in range(self.retry_attempts):
            try:
                async with self.session.get(url, **kwargs) as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    logger.error(f"GET request failed after {self.retry_attempts} attempts: {e}")
                    raise
                logger.warning(f"GET request failed (attempt {attempt + 1}): {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def post(self, url: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform async POST request with retry logic.
        """
        for attempt in range(self.retry_attempts):
            try:
                async with self.session.post(url, json=data, **kwargs) as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    logger.error(f"POST request failed after {self.retry_attempts} attempts: {e}")
                    raise
                logger.warning(f"POST request failed (attempt {attempt + 1}): {e}")
                await asyncio.sleep(2 ** attempt)
    
    async def batch_get(self, urls: List[str], **kwargs) -> List[Dict[str, Any]]:
        """
        Perform multiple GET requests concurrently.
        
        Example:
            async with AsyncHTTPClient() as client:
                results = await client.batch_get([url1, url2, url3])
        """
        tasks = [self.get(url, **kwargs) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)


class AsyncFileOperations:
    """
    Async file I/O operations for better performance.
    """
    
    @staticmethod
    async def read_file(file_path: str, mode: str = 'r') -> str:
        """
        Read file asynchronously.
        
        Args:
            file_path: Path to file
            mode: File open mode ('r' for text, 'rb' for binary)
        
        Returns:
            File contents
        """
        async with aiofiles.open(file_path, mode) as f:
            return await f.read()
    
    @staticmethod
    async def write_file(file_path: str, content: str, mode: str = 'w'):
        """
        Write file asynchronously.
        
        Args:
            file_path: Path to file
            content: Content to write
            mode: File open mode ('w' for text, 'wb' for binary)
        """
        async with aiofiles.open(file_path, mode) as f:
            await f.write(content)
    
    @staticmethod
    async def read_multiple_files(file_paths: List[str]) -> List[str]:
        """
        Read multiple files concurrently.
        
        Example:
            contents = await AsyncFileOperations.read_multiple_files([
                'file1.txt', 'file2.txt', 'file3.txt'
            ])
        """
        tasks = [AsyncFileOperations.read_file(path) for path in file_paths]
        return await asyncio.gather(*tasks)


class AsyncTaskQueue:
    """
    Async task queue with worker pool for processing tasks concurrently.
    """
    
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.queue = asyncio.Queue()
        self.results = []
    
    async def add_task(self, coro):
        """Add a coroutine task to the queue"""
        await self.queue.put(coro)
    
    async def worker(self, worker_id: int):
        """Worker that processes tasks from the queue"""
        while True:
            try:
                task = await self.queue.get()
                if task is None:  # Sentinel value to stop worker
                    break
                
                logger.debug(f"Worker {worker_id} processing task")
                result = await task
                self.results.append(result)
                
                self.queue.task_done()
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                self.queue.task_done()
    
    async def process_all(self) -> List[Any]:
        """
        Process all tasks in the queue using worker pool.
        
        Returns:
            List of results from all tasks
        """
        self.results = []
        
        # Start workers
        workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.max_workers)
        ]
        
        # Wait for all tasks to complete
        await self.queue.join()
        
        # Stop workers
        for _ in range(self.max_workers):
            await self.queue.put(None)
        
        # Wait for workers to finish
        await asyncio.gather(*workers)
        
        return self.results


# Example: Optimized API endpoint with async operations
async def optimized_endpoint_example():
    """
    Example of an optimized FastAPI endpoint using async operations.
    
    Usage in FastAPI:
        @app.get("/data")
        async def get_data():
            return await optimized_endpoint_example()
    """
    # Parallel API calls
    async with AsyncHTTPClient() as client:
        results = await client.batch_get([
            "https://api.service1.com/data",
            "https://api.service2.com/data",
            "https://api.service3.com/data",
        ])
    
    # Parallel file operations
    files = await AsyncFileOperations.read_multiple_files([
        "data1.json",
        "data2.json",
        "data3.json",
    ])
    
    # Process results
    return {
        "api_results": results,
        "file_contents": files,
    }


# Example: Database queries with async
async def async_database_example(db_session):
    """
    Example of async database operations.
    
    Usage:
        from sqlalchemy import select
        from models import User
        
        async with db_pool.get_session() as session:
            users = await async_database_example(session)
    """
    from sqlalchemy import select
    
    # Async query execution
    # result = await db_session.execute(select(User).where(User.active == True))
    # users = result.scalars().all()
    
    # return users
    pass
