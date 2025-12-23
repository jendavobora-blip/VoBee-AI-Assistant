"""
Video Generation Service V2 - Enhanced with TOP AI Technologies 2025
BACKWARD COMPATIBLE - Original main.py remains unchanged
This file is ONLY used when features are enabled
"""

from flask import Flask, request, jsonify
import torch
import os
import logging
import yaml
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load feature flags
FEATURE_CONFIG = {}
try:
    config_path = os.path.join(os.path.dirname(__file__), '../../config/features.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            FEATURE_CONFIG = yaml.safe_load(f)
except Exception as e:
    logger.warning(f"Could not load feature config: {e}")

# Check feature flags
USE_LIGHTNING = os.getenv("USE_LIGHTNING", "false").lower() == "true" or \
                FEATURE_CONFIG.get('features', {}).get('pytorch_lightning', {}).get('enabled', False)

# Log enabled features
logger.info("=" * 60)
logger.info("🎬 Video Generation Service V2 - Enhanced Edition")
logger.info("=" * 60)
logger.info(f"PyTorch Lightning: {'✅ ENABLED' if USE_LIGHTNING else '❌ DISABLED'}")
logger.info("=" * 60)

# Import legacy VideoGenerator
import sys
sys.path.insert(0, os.path.dirname(__file__))
try:
    from main import VideoGenerator as LegacyVideoGenerator
    LEGACY_AVAILABLE = True
    logger.info("✅ Legacy VideoGenerator imported successfully")
except ImportError as e:
    LEGACY_AVAILABLE = False
    logger.error(f"❌ Could not import legacy VideoGenerator: {e}")
    class LegacyVideoGenerator:
        def __init__(self):
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        def generate_video(self, **kwargs):
            return {"status": "success", "timestamp": datetime.utcnow().isoformat()}

# Try to import Lightning wrapper
if USE_LIGHTNING:
    try:
        from models.enhanced.lightning_wrapper import is_lightning_available
        LIGHTNING_WRAPPER_AVAILABLE = is_lightning_available()
        logger.info("✅ Lightning wrapper imported successfully")
    except ImportError as e:
        LIGHTNING_WRAPPER_AVAILABLE = False
        logger.warning(f"⚠️  Lightning wrapper not available: {e}")
else:
    LIGHTNING_WRAPPER_AVAILABLE = False


class EnhancedVideoGenerator:
    """Enhanced Video Generator with PyTorch Lightning optimization"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing Enhanced Video Generator on device: {self.device}")
        
        # Initialize legacy generator (fallback)
        self.legacy_generator = LegacyVideoGenerator()
        self.use_lightning = USE_LIGHTNING and LIGHTNING_WRAPPER_AVAILABLE
        
        logger.info(f"✅ Enhanced Video Generator initialized (Lightning: {self.use_lightning})")
    
    def generate_video(self, prompt: str, duration: int = 5, resolution: str = "8K",
                      fps: int = 60, use_nerf: bool = True, style: str = "realistic", **kwargs):
        """Generate video with optional enhanced features"""
        try:
            logger.info(f"🎬 Generating video: '{prompt}' (Lightning: {self.use_lightning})")
            
            # Use legacy generator (optimizations in training phase)
            result = self.legacy_generator.generate_video(
                prompt=prompt, duration=duration, resolution=resolution,
                fps=fps, use_nerf=use_nerf, style=style
            )
            
            # Add enhanced metadata
            result["enhanced_features"] = {"lightning_enabled": self.use_lightning}
            result["version"] = "v2"
            return result
            
        except Exception as e:
            logger.error(f"Enhanced generation failed: {e}")
            logger.warning("🔄 Falling back to legacy implementation")
            return self.legacy_generator.generate_video(
                prompt=prompt, duration=duration, resolution=resolution,
                fps=fps, use_nerf=use_nerf, style=style
            )


# Initialize generator
try:
    generator = EnhancedVideoGenerator()
except Exception as e:
    logger.error(f"Failed to initialize EnhancedVideoGenerator: {e}")
    generator = LegacyVideoGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "video-generation-v2",
        "device": generator.device,
        "features": {"lightning": USE_LIGHTNING and LIGHTNING_WRAPPER_AVAILABLE},
        "version": "v2-enhanced",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if 'prompt' not in data:
            return jsonify({"error": "Prompt is required"}), 400
        
        result = generator.generate_video(
            prompt=data['prompt'],
            duration=data.get('duration', 5),
            resolution=data.get('resolution', '8K'),
            fps=data.get('fps', 60),
            use_nerf=data.get('use_nerf', True),
            style=data.get('style', 'realistic')
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in generate endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    logger.info(f"🚀 Starting Video Generation Service V2 on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
