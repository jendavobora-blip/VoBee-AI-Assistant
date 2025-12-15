"""
Advanced Compression Service
Implements cutting-edge compression algorithms for optimal memory usage
Supports Brotli, Zstandard (Zstd), and LZ4 compression methods
"""

from flask import Flask, request, jsonify, send_file
import brotli
import zstandard as zstd
import lz4.frame
import io
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import base64
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class AdvancedCompression:
    """
    Advanced compression engine using state-of-the-art algorithms
    - Brotli: Best compression ratio, excellent for text/web content
    - Zstandard (Zstd): Fast compression with great ratio, real-time friendly
    - LZ4: Ultra-fast compression/decompression, minimal CPU overhead
    """
    
    def __init__(self):
        self.compression_stats = {
            'total_compressed': 0,
            'total_decompressed': 0,
            'bytes_saved': 0,
            'algorithms_used': {
                'brotli': 0,
                'zstd': 0,
                'lz4': 0
            }
        }
        logger.info("Advanced Compression Engine initialized")
    
    def compress_brotli(self, data: bytes, quality: int = 11) -> bytes:
        """
        Compress using Brotli (quality: 0-11, 11 = best compression)
        Best for: Text, JSON, HTML, CSS - achieves 20-30% better compression than gzip
        """
        try:
            compressed = brotli.compress(data, quality=quality)
            self.compression_stats['algorithms_used']['brotli'] += 1
            self._update_stats(len(data), len(compressed))
            logger.info(f"Brotli compression: {len(data)} -> {len(compressed)} bytes "
                       f"({self._compression_ratio(len(data), len(compressed)):.2f}x)")
            return compressed
        except Exception as e:
            logger.error(f"Brotli compression failed: {e}")
            raise
    
    def decompress_brotli(self, data: bytes) -> bytes:
        """Decompress Brotli compressed data"""
        try:
            decompressed = brotli.decompress(data)
            self.compression_stats['total_decompressed'] += 1
            return decompressed
        except Exception as e:
            logger.error(f"Brotli decompression failed: {e}")
            raise
    
    def compress_zstd(self, data: bytes, level: int = 19) -> bytes:
        """
        Compress using Zstandard (level: 1-22, 19 = very high compression)
        Best for: Large files, database dumps - 2-3x faster than brotli with similar ratio
        """
        try:
            cctx = zstd.ZstdCompressor(level=level)
            compressed = cctx.compress(data)
            self.compression_stats['algorithms_used']['zstd'] += 1
            self._update_stats(len(data), len(compressed))
            logger.info(f"Zstd compression: {len(data)} -> {len(compressed)} bytes "
                       f"({self._compression_ratio(len(data), len(compressed)):.2f}x)")
            return compressed
        except Exception as e:
            logger.error(f"Zstd compression failed: {e}")
            raise
    
    def decompress_zstd(self, data: bytes) -> bytes:
        """Decompress Zstandard compressed data"""
        try:
            dctx = zstd.ZstdDecompressor()
            decompressed = dctx.decompress(data)
            self.compression_stats['total_decompressed'] += 1
            return decompressed
        except Exception as e:
            logger.error(f"Zstd decompression failed: {e}")
            raise
    
    def compress_lz4(self, data: bytes, compression_level: int = 9) -> bytes:
        """
        Compress using LZ4 (compression_level: 0-12, 9 = high compression)
        Best for: Real-time streaming, low-latency - 10x+ faster than gzip
        """
        try:
            compressed = lz4.frame.compress(
                data, 
                compression_level=compression_level,
                block_size=lz4.frame.BLOCKSIZE_MAX4MB
            )
            self.compression_stats['algorithms_used']['lz4'] += 1
            self._update_stats(len(data), len(compressed))
            logger.info(f"LZ4 compression: {len(data)} -> {len(compressed)} bytes "
                       f"({self._compression_ratio(len(data), len(compressed)):.2f}x)")
            return compressed
        except Exception as e:
            logger.error(f"LZ4 compression failed: {e}")
            raise
    
    def decompress_lz4(self, data: bytes) -> bytes:
        """Decompress LZ4 compressed data"""
        try:
            decompressed = lz4.frame.decompress(data)
            self.compression_stats['total_decompressed'] += 1
            return decompressed
        except Exception as e:
            logger.error(f"LZ4 decompression failed: {e}")
            raise
    
    def compress_streaming(self, data: bytes, algorithm: str = "zstd", chunk_size: int = 1048576):
        """
        Memory-efficient streaming compression for large files
        Processes data in chunks to minimize memory footprint
        """
        try:
            if algorithm == "zstd":
                cctx = zstd.ZstdCompressor(level=19)
                compressed_chunks = []
                
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i + chunk_size]
                    compressed_chunk = cctx.compress(chunk)
                    compressed_chunks.append(compressed_chunk)
                
                return b''.join(compressed_chunks)
            
            elif algorithm == "lz4":
                compressed_chunks = []
                
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i + chunk_size]
                    compressed_chunk = lz4.frame.compress(chunk, compression_level=9)
                    compressed_chunks.append(compressed_chunk)
                
                return b''.join(compressed_chunks)
            
            else:
                raise ValueError(f"Unsupported streaming algorithm: {algorithm}")
                
        except Exception as e:
            logger.error(f"Streaming compression failed: {e}")
            raise
    
    def auto_select_algorithm(self, data: bytes, priority: str = "ratio") -> tuple:
        """
        Automatically select best compression algorithm based on priority
        - ratio: Best compression ratio (Brotli)
        - balanced: Good ratio + speed (Zstd)
        - speed: Fastest compression (LZ4)
        """
        if priority == "ratio":
            return "brotli", self.compress_brotli(data, quality=11)
        elif priority == "balanced":
            return "zstd", self.compress_zstd(data, level=19)
        elif priority == "speed":
            return "lz4", self.compress_lz4(data, compression_level=9)
        else:
            raise ValueError(f"Unknown priority: {priority}")
    
    def _compression_ratio(self, original_size: int, compressed_size: int) -> float:
        """Calculate compression ratio"""
        if compressed_size == 0:
            return 0.0
        return original_size / compressed_size
    
    def _update_stats(self, original_size: int, compressed_size: int):
        """Update compression statistics"""
        self.compression_stats['total_compressed'] += 1
        self.compression_stats['bytes_saved'] += (original_size - compressed_size)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get compression statistics"""
        return {
            **self.compression_stats,
            'timestamp': datetime.utcnow().isoformat()
        }

# Initialize compression engine
compressor = AdvancedCompression()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "compression",
        "algorithms": ["brotli", "zstd", "lz4"],
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/compress', methods=['POST'])
def compress_data():
    """
    Compress data using specified algorithm
    
    Request body:
    {
        "data": "base64_encoded_data",
        "algorithm": "brotli|zstd|lz4|auto",
        "priority": "ratio|balanced|speed" (for auto mode)
    }
    """
    try:
        request_data = request.get_json()
        
        if 'data' not in request_data:
            return jsonify({"error": "Data field is required"}), 400
        
        # Decode base64 input
        data = base64.b64decode(request_data['data'])
        algorithm = request_data.get('algorithm', 'auto')
        priority = request_data.get('priority', 'balanced')
        
        original_size = len(data)
        
        if algorithm == 'auto':
            algorithm_used, compressed = compressor.auto_select_algorithm(data, priority)
        elif algorithm == 'brotli':
            compressed = compressor.compress_brotli(data)
            algorithm_used = 'brotli'
        elif algorithm == 'zstd':
            compressed = compressor.compress_zstd(data)
            algorithm_used = 'zstd'
        elif algorithm == 'lz4':
            compressed = compressor.compress_lz4(data)
            algorithm_used = 'lz4'
        else:
            return jsonify({"error": f"Unknown algorithm: {algorithm}"}), 400
        
        compressed_size = len(compressed)
        
        return jsonify({
            "status": "success",
            "algorithm": algorithm_used,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": round(original_size / compressed_size, 2),
            "space_saved_percent": round((1 - compressed_size / original_size) * 100, 2),
            "compressed_data": base64.b64encode(compressed).decode('utf-8'),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Compression failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/decompress', methods=['POST'])
def decompress_data():
    """
    Decompress data using specified algorithm
    
    Request body:
    {
        "data": "base64_encoded_compressed_data",
        "algorithm": "brotli|zstd|lz4"
    }
    """
    try:
        request_data = request.get_json()
        
        if 'data' not in request_data or 'algorithm' not in request_data:
            return jsonify({"error": "Data and algorithm fields are required"}), 400
        
        # Decode base64 input
        compressed_data = base64.b64decode(request_data['data'])
        algorithm = request_data['algorithm']
        
        if algorithm == 'brotli':
            decompressed = compressor.decompress_brotli(compressed_data)
        elif algorithm == 'zstd':
            decompressed = compressor.decompress_zstd(compressed_data)
        elif algorithm == 'lz4':
            decompressed = compressor.decompress_lz4(compressed_data)
        else:
            return jsonify({"error": f"Unknown algorithm: {algorithm}"}), 400
        
        return jsonify({
            "status": "success",
            "algorithm": algorithm,
            "decompressed_size": len(decompressed),
            "decompressed_data": base64.b64encode(decompressed).decode('utf-8'),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Decompression failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_compression_stats():
    """Get compression statistics"""
    return jsonify(compressor.get_stats())

@app.route('/benchmark', methods=['POST'])
def benchmark_algorithms():
    """
    Benchmark all compression algorithms with given data
    
    Request body:
    {
        "data": "base64_encoded_data"
    }
    """
    try:
        request_data = request.get_json()
        
        if 'data' not in request_data:
            return jsonify({"error": "Data field is required"}), 400
        
        data = base64.b64decode(request_data['data'])
        original_size = len(data)
        
        results = {}
        
        # Benchmark Brotli
        start = time.time()
        brotli_compressed = compressor.compress_brotli(data, quality=11)
        brotli_time = time.time() - start
        results['brotli'] = {
            "compressed_size": len(brotli_compressed),
            "ratio": round(original_size / len(brotli_compressed), 2),
            "compression_time_ms": round(brotli_time * 1000, 2),
            "space_saved_percent": round((1 - len(brotli_compressed) / original_size) * 100, 2)
        }
        
        # Benchmark Zstd
        start = time.time()
        zstd_compressed = compressor.compress_zstd(data, level=19)
        zstd_time = time.time() - start
        results['zstd'] = {
            "compressed_size": len(zstd_compressed),
            "ratio": round(original_size / len(zstd_compressed), 2),
            "compression_time_ms": round(zstd_time * 1000, 2),
            "space_saved_percent": round((1 - len(zstd_compressed) / original_size) * 100, 2)
        }
        
        # Benchmark LZ4
        start = time.time()
        lz4_compressed = compressor.compress_lz4(data, compression_level=9)
        lz4_time = time.time() - start
        results['lz4'] = {
            "compressed_size": len(lz4_compressed),
            "ratio": round(original_size / len(lz4_compressed), 2),
            "compression_time_ms": round(lz4_time * 1000, 2),
            "space_saved_percent": round((1 - len(lz4_compressed) / original_size) * 100, 2)
        }
        
        return jsonify({
            "original_size": original_size,
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=False)
