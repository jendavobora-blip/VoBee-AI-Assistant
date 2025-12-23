"""
Rust AI Bridge - Ultra-High-Performance Inference
Python wrapper for Rust-based AI inference
EXPERIMENTAL - Optional, falls back to Python if not available
"""

try:
    # Try to import compiled Rust module
    import rust_ai_bridge
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    # Create mock module for when Rust bridge is not compiled
    class MockRustBridge:
        @staticmethod
        def fast_inference_rust(data):
            raise NotImplementedError("Rust bridge not compiled")
        
        @staticmethod
        def fast_matrix_mult(a, b):
            raise NotImplementedError("Rust bridge not compiled")
    
    rust_ai_bridge = MockRustBridge()


def is_rust_available():
    """Check if Rust AI bridge is available"""
    return RUST_AVAILABLE


def safe_rust_inference(data, fallback_fn=None):
    """
    Safely call Rust inference with fallback
    
    Args:
        data: Input data for inference
        fallback_fn: Python function to use if Rust not available
    
    Returns:
        Inference result from Rust or fallback
    """
    if RUST_AVAILABLE:
        try:
            return rust_ai_bridge.fast_inference_rust(data)
        except Exception as e:
            if fallback_fn:
                return fallback_fn(data)
            raise
    else:
        if fallback_fn:
            return fallback_fn(data)
        raise RuntimeError("Rust bridge not available and no fallback provided")


# Example usage:
"""
from rust_ai_bridge_wrapper import safe_rust_inference, is_rust_available

def python_inference(data):
    # Your Python implementation
    return processed_data

# Use Rust if available, otherwise Python
result = safe_rust_inference(input_data, fallback_fn=python_inference)
"""
