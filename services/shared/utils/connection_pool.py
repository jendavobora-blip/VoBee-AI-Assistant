"""
Connection Pooling Utilities for Database and Cache Connections
"""
from typing import Optional
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)


class DatabasePool:
    """
    Optimized database connection pool using SQLAlchemy async.
    
    Features:
    - Connection pooling with configurable size
    - Pre-ping for connection health
    - Connection recycling
    - Async/await support
    """
    
    def __init__(
        self,
        database_url: str,
        pool_size: int = 20,
        max_overflow: int = 10,
        pool_pre_ping: bool = True,
        pool_recycle: int = 3600,
        echo: bool = False
    ):
        """
        Initialize database connection pool.
        
        Args:
            database_url: Database connection string
            pool_size: Number of connections to maintain
            max_overflow: Maximum overflow beyond pool_size
            pool_pre_ping: Check connection health before using
            pool_recycle: Recycle connections after N seconds
            echo: Log SQL statements
        """
        self.engine: Optional[AsyncEngine] = None
        self.async_session: Optional[sessionmaker] = None
        self.database_url = database_url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_pre_ping = pool_pre_ping
        self.pool_recycle = pool_recycle
        self.echo = echo
    
    async def initialize(self):
        """Initialize the connection pool"""
        try:
            self.engine = create_async_engine(
                self.database_url,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_pre_ping=self.pool_pre_ping,
                pool_recycle=self.pool_recycle,
                echo=self.echo,
            )
            
            self.async_session = sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            
            logger.info(
                f"Database pool initialized: pool_size={self.pool_size}, "
                f"max_overflow={self.max_overflow}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def close(self):
        """Close all connections in the pool"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database pool closed")
    
    def get_session(self) -> AsyncSession:
        """
        Get a database session from the pool.
        
        Usage:
            async with pool.get_session() as session:
                result = await session.execute(query)
        """
        if not self.async_session:
            raise RuntimeError("Database pool not initialized")
        return self.async_session()
    
    async def health_check(self) -> bool:
        """Check if the database connection is healthy"""
        try:
            async with self.get_session() as session:
                await session.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


class RedisPool:
    """
    Optimized Redis connection pool.
    
    Features:
    - Connection pooling
    - Automatic reconnection
    - Health checking
    """
    
    def __init__(
        self,
        host: str = "redis",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_connections: int = 50,
        decode_responses: bool = True
    ):
        """
        Initialize Redis connection pool.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password (optional)
            max_connections: Maximum number of connections
            decode_responses: Automatically decode responses to strings
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.max_connections = max_connections
        self.decode_responses = decode_responses
        self.client: Optional[aioredis.Redis] = None
    
    async def initialize(self):
        """Initialize the Redis connection pool"""
        try:
            redis_url = f"redis://{self.host}:{self.port}/{self.db}"
            if self.password:
                redis_url = f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
            
            self.client = await aioredis.from_url(
                redis_url,
                max_connections=self.max_connections,
                decode_responses=self.decode_responses,
            )
            
            # Test connection
            await self.client.ping()
            
            logger.info(
                f"Redis pool initialized: {self.host}:{self.port}, "
                f"max_connections={self.max_connections}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Redis pool: {e}")
            raise
    
    async def close(self):
        """Close the Redis connection pool"""
        if self.client:
            await self.client.close()
            logger.info("Redis pool closed")
    
    def get_client(self) -> aioredis.Redis:
        """Get the Redis client"""
        if not self.client:
            raise RuntimeError("Redis pool not initialized")
        return self.client
    
    async def health_check(self) -> bool:
        """Check if Redis connection is healthy"""
        try:
            if self.client:
                await self.client.ping()
                return True
            return False
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
    
    # Convenience methods
    async def get(self, key: str) -> Optional[str]:
        """Get a value from Redis"""
        return await self.client.get(key)
    
    async def set(self, key: str, value: str, ex: Optional[int] = None):
        """Set a value in Redis"""
        await self.client.set(key, value, ex=ex)
    
    async def delete(self, *keys: str):
        """Delete keys from Redis"""
        await self.client.delete(*keys)
    
    async def exists(self, *keys: str) -> int:
        """Check if keys exist"""
        return await self.client.exists(*keys)


# Global pool instances (to be initialized on app startup)
db_pool: Optional[DatabasePool] = None
redis_pool: Optional[RedisPool] = None


async def initialize_pools(database_url: str, redis_host: str = "redis", redis_port: int = 6379):
    """
    Initialize all connection pools.
    
    Call this in your FastAPI startup event.
    """
    global db_pool, redis_pool
    
    # Initialize database pool
    db_pool = DatabasePool(database_url)
    await db_pool.initialize()
    
    # Initialize Redis pool
    redis_pool = RedisPool(host=redis_host, port=redis_port)
    await redis_pool.initialize()
    
    logger.info("All connection pools initialized")


async def close_pools():
    """
    Close all connection pools.
    
    Call this in your FastAPI shutdown event.
    """
    global db_pool, redis_pool
    
    if db_pool:
        await db_pool.close()
    
    if redis_pool:
        await redis_pool.close()
    
    logger.info("All connection pools closed")
