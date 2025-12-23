"""
PyTorch JIT Compilation and Model Quantization Template

This template shows how to optimize PyTorch models with:
1. JIT (Just-In-Time) compilation for faster inference
2. Dynamic quantization for reduced model size and faster computation
3. Model caching to avoid reloading
"""

import torch
import torch.nn as nn
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class OptimizedModelLoader:
    """
    Load and optimize PyTorch models with JIT and quantization.
    """
    
    def __init__(self, cache_dir: str = "./models/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.model_cache = {}
    
    def optimize_model(
        self,
        model: nn.Module,
        use_jit: bool = True,
        use_quantization: bool = True,
        quantization_dtype: torch.dtype = torch.qint8,
    ) -> nn.Module:
        """
        Optimize a PyTorch model with JIT and/or quantization.
        
        Args:
            model: The PyTorch model to optimize
            use_jit: Whether to use JIT compilation
            use_quantization: Whether to use dynamic quantization
            quantization_dtype: Data type for quantization (torch.qint8 or torch.float16)
        
        Returns:
            Optimized model
        """
        model.eval()
        optimized = model
        
        # Apply JIT compilation
        if use_jit:
            try:
                optimized = torch.jit.script(optimized)
                logger.info("✅ JIT compilation applied")
            except Exception as e:
                logger.warning(f"JIT compilation failed, skipping: {e}")
        
        # Apply quantization
        if use_quantization:
            try:
                if quantization_dtype == torch.qint8:
                    # Dynamic INT8 quantization
                    optimized = torch.quantization.quantize_dynamic(
                        optimized,
                        {torch.nn.Linear, torch.nn.Conv2d},
                        dtype=torch.qint8
                    )
                    logger.info("✅ INT8 quantization applied")
                elif quantization_dtype == torch.float16:
                    # FP16 half precision
                    optimized = optimized.half()
                    logger.info("✅ FP16 quantization applied")
            except Exception as e:
                logger.warning(f"Quantization failed, skipping: {e}")
        
        return optimized
    
    def load_and_optimize(
        self,
        model_path: str,
        model_class: nn.Module = None,
        use_jit: bool = True,
        use_quantization: bool = True,
    ) -> nn.Module:
        """
        Load a model from disk and optimize it.
        
        Args:
            model_path: Path to the model file
            model_class: Model class to instantiate (if not loading full model)
            use_jit: Whether to use JIT compilation
            use_quantization: Whether to use dynamic quantization
        
        Returns:
            Optimized model ready for inference
        """
        cache_key = f"{model_path}_{use_jit}_{use_quantization}"
        
        # Check cache
        if cache_key in self.model_cache:
            logger.info(f"Loading model from cache: {model_path}")
            return self.model_cache[cache_key]
        
        # Load model
        if model_class:
            model = model_class()
            model.load_state_dict(torch.load(model_path))
        else:
            model = torch.load(model_path)
        
        # Optimize
        optimized_model = self.optimize_model(model, use_jit, use_quantization)
        
        # Cache
        self.model_cache[cache_key] = optimized_model
        logger.info(f"Model loaded and optimized: {model_path}")
        
        return optimized_model


# Example usage for Stable Diffusion / Image Generation models
def optimize_image_generation_model(model: nn.Module) -> nn.Module:
    """
    Optimize image generation models (e.g., Stable Diffusion, DALL-E).
    
    Example:
        model = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2")
        model.unet = optimize_image_generation_model(model.unet)
    """
    loader = OptimizedModelLoader()
    
    # For large models, use FP16 instead of INT8
    optimized = loader.optimize_model(
        model,
        use_jit=False,  # JIT can be problematic with some diffusion models
        use_quantization=True,
        quantization_dtype=torch.float16,
    )
    
    # Enable memory-efficient attention if available
    if hasattr(optimized, 'enable_attention_slicing'):
        optimized.enable_attention_slicing()
        logger.info("✅ Memory-efficient attention enabled")
    
    return optimized


# Example usage for transformer models
def optimize_transformer_model(model: nn.Module) -> nn.Module:
    """
    Optimize transformer models (BERT, GPT, etc.).
    
    Example:
        from transformers import AutoModel
        model = AutoModel.from_pretrained("bert-base-uncased")
        model = optimize_transformer_model(model)
    """
    loader = OptimizedModelLoader()
    
    optimized = loader.optimize_model(
        model,
        use_jit=True,
        use_quantization=True,
        quantization_dtype=torch.qint8,
    )
    
    return optimized


# Benchmark function
def benchmark_model(model: nn.Module, input_shape: tuple, num_runs: int = 100):
    """
    Benchmark model inference speed.
    
    Args:
        model: Model to benchmark
        input_shape: Input tensor shape (batch_size, ...)
        num_runs: Number of inference runs
    
    Returns:
        Average inference time in milliseconds
    """
    import time
    
    model.eval()
    dummy_input = torch.randn(*input_shape)
    
    # Warmup
    with torch.no_grad():
        for _ in range(10):
            _ = model(dummy_input)
    
    # Benchmark
    start_time = time.time()
    with torch.no_grad():
        for _ in range(num_runs):
            _ = model(dummy_input)
    end_time = time.time()
    
    avg_time_ms = ((end_time - start_time) / num_runs) * 1000
    logger.info(f"Average inference time: {avg_time_ms:.2f} ms")
    
    return avg_time_ms
