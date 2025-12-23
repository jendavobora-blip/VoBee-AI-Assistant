"""
ONNX Model Export Utility
Convert PyTorch models to ONNX format for cross-platform deployment
OPTIONAL UTILITY - Does not affect existing functionality
"""

import torch
import torch.nn as nn
import os
import logging
from typing import Optional, Tuple, Dict, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import ONNX
try:
    import onnx
    import onnxruntime as ort
    ONNX_AVAILABLE = True
    logger.info("✅ ONNX libraries available")
except ImportError:
    ONNX_AVAILABLE = False
    logger.warning("⚠️  ONNX not available. Install with: pip install onnx onnxruntime")


class ONNXExporter:
    """
    Utility class for exporting PyTorch models to ONNX format
    
    Benefits of ONNX:
    - 2-5x faster inference
    - Cross-platform deployment (CPU, GPU, mobile, edge)
    - Lower memory footprint
    - Framework interoperability
    """
    
    def __init__(self):
        if not ONNX_AVAILABLE:
            raise ImportError(
                "ONNX not available. Install with:\n"
                "pip install onnx onnxruntime onnxruntime-gpu"
            )
        
        logger.info("🔧 ONNX Exporter initialized")
    
    def export_model(
        self,
        model: nn.Module,
        output_path: str,
        input_shape: Tuple[int, ...],
        input_names: Optional[list] = None,
        output_names: Optional[list] = None,
        dynamic_axes: Optional[Dict[str, Any]] = None,
        opset_version: int = 14
    ) -> bool:
        """
        Export PyTorch model to ONNX format
        
        Args:
            model: PyTorch model to export
            output_path: Path to save ONNX model
            input_shape: Input tensor shape (e.g., (1, 3, 224, 224))
            input_names: Names for input tensors
            output_names: Names for output tensors
            dynamic_axes: Dynamic axes for variable input shapes
            opset_version: ONNX opset version
        
        Returns:
            True if export successful, False otherwise
        """
        try:
            logger.info("=" * 60)
            logger.info("📦 Exporting PyTorch model to ONNX")
            logger.info(f"   Output: {output_path}")
            logger.info(f"   Input shape: {input_shape}")
            logger.info("=" * 60)
            
            # Set model to eval mode
            model.eval()
            
            # Create dummy input
            dummy_input = torch.randn(*input_shape)
            
            # Default names
            if input_names is None:
                input_names = ["input"]
            if output_names is None:
                output_names = ["output"]
            
            # Export to ONNX
            torch.onnx.export(
                model,
                dummy_input,
                output_path,
                export_params=True,
                opset_version=opset_version,
                do_constant_folding=True,
                input_names=input_names,
                output_names=output_names,
                dynamic_axes=dynamic_axes
            )
            
            logger.info("✅ Model exported to ONNX successfully")
            
            # Verify exported model
            self.verify_model(output_path)
            
            # Test inference
            inference_time = self.test_inference(output_path, input_shape)
            logger.info(f"✅ ONNX inference test passed ({inference_time:.2f}ms)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ ONNX export failed: {e}")
            return False
    
    def verify_model(self, onnx_path: str) -> bool:
        """
        Verify exported ONNX model
        
        Args:
            onnx_path: Path to ONNX model file
        
        Returns:
            True if model is valid
        """
        try:
            logger.info("🔍 Verifying ONNX model...")
            
            # Load and check model
            onnx_model = onnx.load(onnx_path)
            onnx.checker.check_model(onnx_model)
            
            logger.info("✅ ONNX model is valid")
            
            # Print model info
            logger.info(f"   IR version: {onnx_model.ir_version}")
            logger.info(f"   Producer: {onnx_model.producer_name}")
            logger.info(f"   Inputs: {[input.name for input in onnx_model.graph.input]}")
            logger.info(f"   Outputs: {[output.name for output in onnx_model.graph.output]}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Model verification failed: {e}")
            return False
    
    def test_inference(
        self,
        onnx_path: str,
        input_shape: Tuple[int, ...]
    ) -> float:
        """
        Test ONNX model inference
        
        Args:
            onnx_path: Path to ONNX model
            input_shape: Input tensor shape
        
        Returns:
            Inference time in milliseconds
        """
        try:
            # Create inference session
            session = ort.InferenceSession(onnx_path)
            
            # Get input name
            input_name = session.get_inputs()[0].name
            
            # Create dummy input
            dummy_input = torch.randn(*input_shape).numpy()
            
            # Warm-up
            session.run(None, {input_name: dummy_input})
            
            # Measure inference time
            import time
            start = time.time()
            outputs = session.run(None, {input_name: dummy_input})
            end = time.time()
            
            inference_time = (end - start) * 1000  # Convert to ms
            
            return inference_time
            
        except Exception as e:
            logger.error(f"Inference test failed: {e}")
            return -1.0
    
    def compare_models(
        self,
        pytorch_model: nn.Module,
        onnx_path: str,
        input_shape: Tuple[int, ...],
        num_runs: int = 100
    ) -> Dict[str, Any]:
        """
        Compare PyTorch and ONNX model performance
        
        Args:
            pytorch_model: Original PyTorch model
            onnx_path: Path to ONNX model
            input_shape: Input shape for testing
            num_runs: Number of inference runs for averaging
        
        Returns:
            Dictionary with comparison results
        """
        try:
            logger.info("⚖️  Comparing PyTorch vs ONNX performance...")
            
            import time
            import numpy as np
            
            # Create test input
            test_input = torch.randn(*input_shape)
            
            # PyTorch inference timing
            pytorch_model.eval()
            with torch.no_grad():
                # Warm-up
                _ = pytorch_model(test_input)
                
                # Measure
                pytorch_times = []
                for _ in range(num_runs):
                    start = time.time()
                    _ = pytorch_model(test_input)
                    pytorch_times.append((time.time() - start) * 1000)
            
            pytorch_avg = np.mean(pytorch_times)
            
            # ONNX inference timing
            session = ort.InferenceSession(onnx_path)
            input_name = session.get_inputs()[0].name
            test_input_numpy = test_input.numpy()
            
            # Warm-up
            _ = session.run(None, {input_name: test_input_numpy})
            
            # Measure
            onnx_times = []
            for _ in range(num_runs):
                start = time.time()
                _ = session.run(None, {input_name: test_input_numpy})
                onnx_times.append((time.time() - start) * 1000)
            
            onnx_avg = np.mean(onnx_times)
            
            # Calculate speedup
            speedup = pytorch_avg / onnx_avg
            
            results = {
                "pytorch_avg_ms": round(pytorch_avg, 2),
                "onnx_avg_ms": round(onnx_avg, 2),
                "speedup": round(speedup, 2),
                "improvement_percent": round((speedup - 1) * 100, 2),
                "num_runs": num_runs
            }
            
            logger.info("=" * 60)
            logger.info("📊 Performance Comparison Results")
            logger.info(f"   PyTorch: {results['pytorch_avg_ms']}ms")
            logger.info(f"   ONNX: {results['onnx_avg_ms']}ms")
            logger.info(f"   Speedup: {results['speedup']}x ({results['improvement_percent']}% faster)")
            logger.info("=" * 60)
            
            return results
            
        except Exception as e:
            logger.error(f"Comparison failed: {e}")
            return {}


def export_image_generation_model(output_dir: str = "models/onnx"):
    """
    Example: Export image generation model to ONNX
    
    Usage:
        python utils/onnx_export.py
    """
    if not ONNX_AVAILABLE:
        logger.error("ONNX not available")
        return
    
    logger.info("📦 Exporting Image Generation Model")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Example: Simple dummy model (replace with actual model)
    class DummyImageModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
            self.conv2 = nn.Conv2d(64, 3, 3, padding=1)
        
        def forward(self, x):
            x = torch.relu(self.conv1(x))
            x = torch.sigmoid(self.conv2(x))
            return x
    
    model = DummyImageModel()
    
    # Export
    exporter = ONNXExporter()
    output_path = os.path.join(output_dir, "image_model.onnx")
    
    success = exporter.export_model(
        model=model,
        output_path=output_path,
        input_shape=(1, 3, 256, 256),
        input_names=["image"],
        output_names=["generated_image"],
        dynamic_axes={
            "image": {0: "batch_size"},
            "generated_image": {0: "batch_size"}
        }
    )
    
    if success:
        logger.info(f"✅ Model exported successfully to {output_path}")
        
        # Compare performance
        exporter.compare_models(model, output_path, (1, 3, 256, 256))
    else:
        logger.error("❌ Export failed")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Export PyTorch models to ONNX")
    parser.add_argument("--model", type=str, default="image", help="Model to export (image, video, crypto)")
    parser.add_argument("--output-dir", type=str, default="models/onnx", help="Output directory")
    
    args = parser.parse_args()
    
    if args.model == "image":
        export_image_generation_model(args.output_dir)
    else:
        logger.info(f"Model type '{args.model}' export not yet implemented")
        logger.info("Use --model image for example export")
