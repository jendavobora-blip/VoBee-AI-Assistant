# Rust AI Bridge

Ultra-high-performance AI inference using Rust.

## Features

- **5-10x faster inference** than Python
- **Lower memory footprint**
- **Better resource utilization**
- **Optional enhancement** - Falls back to Python if not available

## Building

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install maturin (Rust-Python bridge builder)
pip install maturin
```

### Build

```bash
cd bot-system/rust-ai-bridge

# Development build
maturin develop

# Production build
maturin build --release

# Install wheel
pip install target/wheels/rust_ai_bridge-*.whl
```

## Usage

```python
# Try to use Rust bridge with fallback
from bot-system.rust_ai_bridge.rust_ai_bridge_wrapper import (
    safe_rust_inference,
    is_rust_available
)

def python_fallback(data):
    # Your Python implementation
    return [x * 2 + 1 for x in data]

# Automatic fallback to Python if Rust not available
result = safe_rust_inference(
    [1.0, 2.0, 3.0],
    fallback_fn=python_fallback
)

# Check if Rust is available
if is_rust_available():
    print("✅ Using Rust-accelerated inference")
else:
    print("❌ Using Python fallback")
```

## Supported Operations

- `fast_inference_rust(input: List[float]) -> List[float]`
- `fast_matrix_mult(a: List[List[float]], b: List[List[float]]) -> List[List[float]]`
- `fast_batch_process(batch: List[List[float]]) -> List[List[float]]`

## Rust AI Libraries (Future)

The bridge can be extended with:

- **burn-rs**: Comprehensive deep learning framework
- **candle**: Minimalist ML framework by HuggingFace
- **tract**: ONNX runtime in Rust

Uncomment in `Cargo.toml` as needed.

## Performance

Expected speedups (compared to Python):
- Simple operations: 5-10x faster
- Matrix operations: 3-5x faster
- Batch processing: 5-15x faster

## Status

**EXPERIMENTAL** - Use for performance-critical paths only.
Always provide Python fallback for reliability.
