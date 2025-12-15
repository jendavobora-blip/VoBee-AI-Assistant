# Advanced Compression Service

High-performance compression service using cutting-edge algorithms for optimal memory usage.

## Features

- **Brotli Compression** - Best compression ratio (20-30% better than gzip)
- **Zstandard (Zstd)** - Fast compression with excellent ratio
- **LZ4** - Ultra-fast compression/decompression
- **Memory-efficient streaming** for large datasets
- **Auto-selection** of best algorithm based on priority
- **Real-time benchmarking** across all algorithms

## Algorithms

### Brotli
- **Best for**: Text, JSON, HTML, CSS
- **Compression ratio**: Excellent (highest)
- **Speed**: Moderate
- **Quality levels**: 0-11 (11 = best compression)

### Zstandard (Zstd)
- **Best for**: Large files, database dumps
- **Compression ratio**: Excellent
- **Speed**: Fast (2-3x faster than Brotli)
- **Compression levels**: 1-22 (19 = very high compression)

### LZ4
- **Best for**: Real-time streaming, low-latency applications
- **Compression ratio**: Good
- **Speed**: Ultra-fast (10x+ faster than gzip)
- **Compression levels**: 0-12 (9 = high compression)

## API Endpoints

### Compress Data
```bash
POST /compress
Content-Type: application/json

{
  "data": "SGVsbG8gV29ybGQh...",  # base64 encoded
  "algorithm": "auto",             # brotli|zstd|lz4|auto
  "priority": "balanced"           # ratio|balanced|speed
}
```

**Response:**
```json
{
  "status": "success",
  "algorithm": "zstd",
  "original_size": 1024,
  "compressed_size": 256,
  "compression_ratio": 4.0,
  "space_saved_percent": 75.0,
  "compressed_data": "base64_encoded_compressed_data",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Decompress Data
```bash
POST /decompress
Content-Type: application/json

{
  "data": "compressed_base64_data",
  "algorithm": "zstd"
}
```

### Get Statistics
```bash
GET /stats
```

**Response:**
```json
{
  "total_compressed": 1000,
  "total_decompressed": 950,
  "bytes_saved": 1048576,
  "algorithms_used": {
    "brotli": 300,
    "zstd": 500,
    "lz4": 200
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Benchmark Algorithms
```bash
POST /benchmark
Content-Type: application/json

{
  "data": "base64_encoded_data"
}
```

**Response:**
```json
{
  "original_size": 1024,
  "results": {
    "brotli": {
      "compressed_size": 200,
      "ratio": 5.12,
      "compression_time_ms": 45.2,
      "space_saved_percent": 80.5
    },
    "zstd": {
      "compressed_size": 220,
      "ratio": 4.65,
      "compression_time_ms": 15.8,
      "space_saved_percent": 78.5
    },
    "lz4": {
      "compressed_size": 350,
      "ratio": 2.93,
      "compression_time_ms": 2.1,
      "space_saved_percent": 65.8
    }
  }
}
```

## Usage Examples

### Compress with Auto-Selection
```python
import requests
import base64

data = b"Your data here..."
encoded_data = base64.b64encode(data).decode('utf-8')

response = requests.post('http://localhost:5006/compress', json={
    'data': encoded_data,
    'algorithm': 'auto',
    'priority': 'balanced'
})

result = response.json()
print(f"Compression ratio: {result['compression_ratio']}x")
print(f"Space saved: {result['space_saved_percent']}%")
```

### Benchmark All Algorithms
```python
import requests
import base64

data = b"Your data here..."
encoded_data = base64.b64encode(data).decode('utf-8')

response = requests.post('http://localhost:5006/benchmark', json={
    'data': encoded_data
})

results = response.json()
for algo, stats in results['results'].items():
    print(f"{algo}: {stats['ratio']}x ratio, {stats['compression_time_ms']}ms")
```

## Configuration

Environment variables:
- `LOG_LEVEL` - Logging level (default: info)

## Docker

```bash
# Build
docker build -t compression-service .

# Run
docker run -p 5006:5006 compression-service
```

## Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "compression",
  "algorithms": ["brotli", "zstd", "lz4"],
  "timestamp": "2024-01-01T00:00:00Z"
}
```
