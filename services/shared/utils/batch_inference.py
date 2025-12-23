"""
Batch Inference Engine for ML Services
Provides efficient batching for model inference requests
"""
import asyncio
from typing import List, Any, Callable
import logging

logger = logging.getLogger(__name__)


class BatchInferenceEngine:
    """
    Batch inference engine for efficient model processing.
    
    Accumulates requests and processes them in batches to maximize GPU utilization.
    """
    
    def __init__(
        self,
        model: Any,
        batch_size: int = 32,
        max_wait_time: float = 0.1,
        batch_fn: Callable = None
    ):
        """
        Initialize batch inference engine.
        
        Args:
            model: The ML model to use for inference
            batch_size: Maximum number of items per batch
            max_wait_time: Maximum time to wait before processing batch (seconds)
            batch_fn: Optional custom batch processing function
        """
        self.model = model
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.batch_fn = batch_fn or self._default_batch_fn
        self.queue: List[tuple] = []
        self.processing_lock = asyncio.Lock()
        self._background_task = None
        
    async def start(self):
        """Start the background batch processing task"""
        if self._background_task is None:
            self._background_task = asyncio.create_task(self._process_batches())
            logger.info("Batch inference engine started")
    
    async def stop(self):
        """Stop the background batch processing task"""
        if self._background_task:
            self._background_task.cancel()
            try:
                await self._background_task
            except asyncio.CancelledError:
                pass
            logger.info("Batch inference engine stopped")
    
    async def infer(self, input_data: Any) -> Any:
        """
        Queue an inference request and wait for result.
        
        Args:
            input_data: Input data for the model
            
        Returns:
            Model output
        """
        future = asyncio.Future()
        
        async with self.processing_lock:
            self.queue.append((input_data, future))
            
            # Process batch if it's full
            if len(self.queue) >= self.batch_size:
                await self._process_batch()
        
        return await future
    
    async def _process_batches(self):
        """Background task to process batches periodically"""
        while True:
            await asyncio.sleep(self.max_wait_time)
            async with self.processing_lock:
                if self.queue:
                    await self._process_batch()
    
    async def _process_batch(self):
        """Process a batch of queued requests"""
        if not self.queue:
            return
        
        # Extract batch
        batch = self.queue[:self.batch_size]
        self.queue = self.queue[self.batch_size:]
        
        inputs = [item[0] for item in batch]
        
        try:
            # Process batch
            results = await self.batch_fn(self.model, inputs)
            
            # Set results for all futures
            for (_, future), result in zip(batch, results):
                if not future.done():
                    future.set_result(result)
                    
            logger.info(f"Processed batch of {len(batch)} items")
            
        except Exception as e:
            logger.error(f"Batch processing error: {e}")
            # Set exception for all futures
            for _, future in batch:
                if not future.done():
                    future.set_exception(e)
    
    async def _default_batch_fn(self, model: Any, inputs: List[Any]) -> List[Any]:
        """
        Default batch processing function.
        
        Override this or provide custom batch_fn for specific models.
        """
        # This is a placeholder - implement model-specific logic
        if hasattr(model, 'batch_predict'):
            return await model.batch_predict(inputs)
        elif hasattr(model, 'predict'):
            return [await model.predict(inp) for inp in inputs]
        else:
            raise NotImplementedError("Model must have batch_predict or predict method")


class AsyncBatchProcessor:
    """
    Generic async batch processor for any async operations.
    
    Useful for batching API calls, database queries, etc.
    """
    
    def __init__(self, batch_size: int = 100, max_wait_time: float = 0.5):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.queue: List[tuple] = []
        self.lock = asyncio.Lock()
    
    async def add_task(self, task_fn: Callable, *args, **kwargs) -> Any:
        """
        Add a task to the batch queue.
        
        Args:
            task_fn: Async function to execute
            *args, **kwargs: Arguments for the function
            
        Returns:
            Result of the function
        """
        future = asyncio.Future()
        
        async with self.lock:
            self.queue.append((task_fn, args, kwargs, future))
            
            if len(self.queue) >= self.batch_size:
                await self._process_batch()
        
        # Wait with timeout
        try:
            return await asyncio.wait_for(future, timeout=self.max_wait_time * 2)
        except asyncio.TimeoutError:
            async with self.lock:
                await self._process_batch()
            return await future
    
    async def _process_batch(self):
        """Process all queued tasks"""
        if not self.queue:
            return
        
        batch = self.queue[:]
        self.queue = []
        
        # Execute all tasks concurrently
        tasks = [task_fn(*args, **kwargs) for task_fn, args, kwargs, _ in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Set results
        for (_, _, _, future), result in zip(batch, results):
            if not future.done():
                if isinstance(result, Exception):
                    future.set_exception(result)
                else:
                    future.set_result(result)
