"""
Safety System for Vobio AI Studio
Validates code execution, file operations, and API calls
"""

import os
import json
import logging
import re
from typing import Dict, Any, List, Optional
from pathlib import Path
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safer_getattr

logger = logging.getLogger(__name__)

CONFIG_DIR = Path(__file__).parent.parent / "config"
PROTECTED_FILES_PATH = CONFIG_DIR / "protected_files.json"


class SafetySystem:
    """Comprehensive safety checks for AI operations"""
    
    def __init__(self):
        self.protected_files = []
        self.allowed_write_dirs = []
        self._load_config()
    
    def _load_config(self):
        """Load protected files configuration"""
        try:
            if PROTECTED_FILES_PATH.exists():
                with open(PROTECTED_FILES_PATH) as f:
                    config = json.load(f)
                    self.protected_files = config.get("protected_files", [])
                    self.allowed_write_dirs = config.get("allowed_write_dirs", [])
                logger.info(f"Loaded {len(self.protected_files)} protected files")
        except Exception as e:
            logger.warning(f"Failed to load protected files config: {e}")
            self.protected_files = [
                "api_server_integrated.py",
                "safety_system.py",
                "feature_gates.py",
                ".env",
                "docker-compose.yml"
            ]
            self.allowed_write_dirs = ["skills/", "knowledge/", "temp/", "logs/"]
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """
        Validate Python code for dangerous operations
        Returns: {safe: bool, issues: List[str], risk_level: str}
        """
        issues = []
        risk_level = "safe"
        
        # Check for dangerous imports
        dangerous_imports = [
            "subprocess", "os.system", "eval", "exec", "compile",
            "__import__", "shutil.rmtree", "pathlib.unlink"
        ]
        
        for dangerous in dangerous_imports:
            if re.search(rf'\b{re.escape(dangerous)}\b', code):
                issues.append(f"Dangerous operation detected: {dangerous}")
                risk_level = "critical"
        
        # Check for file system operations
        file_operations = ["open(", "write(", "unlink(", "remove(", "rmdir("]
        for op in file_operations:
            if op in code:
                issues.append(f"File system operation detected: {op}")
                if risk_level == "safe":
                    risk_level = "medium"
        
        # Check for network operations
        network_operations = ["socket", "urllib", "requests", "httpx"]
        for op in network_operations:
            if re.search(rf'\b{re.escape(op)}\b', code):
                issues.append(f"Network operation detected: {op}")
                if risk_level == "safe":
                    risk_level = "medium"
        
        # Try to compile with RestrictedPython
        try:
            byte_code = compile_restricted(code, '<string>', 'exec')
            if byte_code.errors:
                for error in byte_code.errors:
                    issues.append(f"Compilation error: {error}")
                    risk_level = "high"
        except Exception as e:
            issues.append(f"Failed to compile: {str(e)}")
            risk_level = "critical"
        
        return {
            "safe": risk_level in ["safe", "medium"],
            "issues": issues,
            "risk_level": risk_level,
            "requires_approval": risk_level in ["medium", "high", "critical"]
        }
    
    def validate_file_operation(self, file_path: str, operation: str) -> Dict[str, Any]:
        """
        Validate file operations (read/write/delete)
        Returns: {allowed: bool, reason: str}
        """
        path = Path(file_path).resolve()
        
        # Check if file is protected
        if any(protected in str(path) for protected in self.protected_files):
            return {
                "allowed": False,
                "reason": f"File is protected: {file_path}"
            }
        
        # For write/delete operations, check allowed directories
        if operation in ["write", "delete"]:
            allowed = any(
                str(path).startswith(allowed_dir) 
                for allowed_dir in self.allowed_write_dirs
            )
            
            if not allowed:
                return {
                    "allowed": False,
                    "reason": f"Write/delete not allowed in this directory: {file_path}"
                }
        
        return {
            "allowed": True,
            "reason": "Operation allowed"
        }
    
    def validate_api_call(self, endpoint: str, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate API call for safety
        Returns: {allowed: bool, issues: List[str]}
        """
        issues = []
        
        # Check payload size
        payload_str = json.dumps(payload)
        if len(payload_str) > 1_000_000:  # 1MB limit
            issues.append("Payload too large (>1MB)")
        
        # Check for suspicious patterns in payload
        dangerous_patterns = [
            r"<script", r"javascript:", r"onerror=", r"onclick=",
            r"rm -rf", r"DROP TABLE", r"DELETE FROM"
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, payload_str, re.IGNORECASE):
                issues.append(f"Suspicious pattern detected: {pattern}")
        
        return {
            "allowed": len(issues) == 0,
            "issues": issues
        }
    
    def sanitize_output(self, output: Any) -> Any:
        """Sanitize output to prevent XSS and injection attacks"""
        if isinstance(output, str):
            # Basic HTML escaping
            output = output.replace("&", "&amp;")
            output = output.replace("<", "&lt;")
            output = output.replace(">", "&gt;")
            output = output.replace('"', "&quot;")
            output = output.replace("'", "&#x27;")
            return output
        elif isinstance(output, dict):
            return {k: self.sanitize_output(v) for k, v in output.items()}
        elif isinstance(output, list):
            return [self.sanitize_output(item) for item in output]
        else:
            return output
    
    def quarantine_file(self, file_path: str, reason: str) -> str:
        """Move dangerous file to quarantine"""
        quarantine_dir = Path("/app/quarantine")
        quarantine_dir.mkdir(exist_ok=True)
        
        source = Path(file_path)
        if source.exists():
            dest = quarantine_dir / f"{source.name}.quarantined"
            try:
                source.rename(dest)
                logger.warning(f"File quarantined: {file_path} -> {dest} (Reason: {reason})")
                return str(dest)
            except Exception as e:
                logger.error(f"Failed to quarantine file: {e}")
                return ""
        return ""


# Global instance
_safety_system = None


def get_safety_system() -> SafetySystem:
    """Get or create the global SafetySystem instance"""
    global _safety_system
    if _safety_system is None:
        _safety_system = SafetySystem()
    return _safety_system
