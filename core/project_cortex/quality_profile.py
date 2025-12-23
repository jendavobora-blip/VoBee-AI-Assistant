"""
Quality Profile - Speed vs Quality preference management.

Balances execution speed against output quality based on project preferences.
"""

import logging
from typing import Dict, Optional
from enum import Enum


class QualityPreference(Enum):
    """Quality vs Speed preferences."""
    SPEED = "speed"           # Prioritize fast execution
    BALANCED = "balanced"     # Balance speed and quality
    QUALITY = "quality"       # Prioritize high quality


class QualityProfile:
    """
    Manages speed vs quality preferences for a project.
    
    Features:
    - Configurable quality/speed tradeoffs
    - Resource allocation based on preference
    - Model selection guidance
    - Timeout and retry policies
    """
    
    def __init__(
        self,
        project_id: str,
        preference: str = "balanced"
    ):
        """
        Initialize quality profile.
        
        Args:
            project_id: Unique project identifier
            preference: 'speed', 'balanced', or 'quality'
        """
        self.project_id = project_id
        
        # Validate and set preference
        try:
            self.preference = QualityPreference(preference)
        except ValueError:
            logging.warning(
                f"Invalid preference '{preference}', defaulting to 'balanced'"
            )
            self.preference = QualityPreference.BALANCED
        
        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.{project_id}")
        self.logger.setLevel(logging.INFO)
        
        # Define profile configurations
        self.configs = self._build_configs()
        
        self.logger.info(
            f"QualityProfile initialized for project: {project_id}, "
            f"preference: {self.preference.value}"
        )
    
    def _build_configs(self) -> Dict:
        """Build configuration profiles for each preference."""
        return {
            QualityPreference.SPEED: {
                "timeout_multiplier": 0.5,
                "max_retries": 1,
                "use_cache": True,
                "parallel_execution": True,
                "model_tier": "fast",
                "sampling_strategy": "greedy",
                "batch_size": "large",
                "precision": "fp16",
                "description": "Optimized for fast execution"
            },
            QualityPreference.BALANCED: {
                "timeout_multiplier": 1.0,
                "max_retries": 2,
                "use_cache": True,
                "parallel_execution": True,
                "model_tier": "standard",
                "sampling_strategy": "temperature",
                "batch_size": "medium",
                "precision": "fp32",
                "description": "Balanced speed and quality"
            },
            QualityPreference.QUALITY: {
                "timeout_multiplier": 2.0,
                "max_retries": 3,
                "use_cache": False,
                "parallel_execution": False,
                "model_tier": "premium",
                "sampling_strategy": "nucleus",
                "batch_size": "small",
                "precision": "fp32",
                "description": "Optimized for highest quality"
            }
        }
    
    def get_config(self, key: Optional[str] = None):
        """
        Get configuration for current preference.
        
        Args:
            key: Specific config key to retrieve, or None for all
            
        Returns:
            Configuration value or full config dict
        """
        config = self.configs[self.preference]
        
        if key:
            return config.get(key)
        
        return config
    
    def get_timeout(self, base_timeout: float) -> float:
        """
        Calculate timeout based on preference.
        
        Args:
            base_timeout: Base timeout in seconds
            
        Returns:
            Adjusted timeout
        """
        multiplier = self.get_config("timeout_multiplier")
        return base_timeout * multiplier
    
    def get_model_recommendation(self, task_type: str) -> str:
        """
        Get recommended model based on preference and task.
        
        Args:
            task_type: Type of task (e.g., 'image_gen', 'text_gen', 'analysis')
            
        Returns:
            Recommended model identifier
        """
        tier = self.get_config("model_tier")
        
        # Model recommendations by tier and task
        # TODO: Expand with actual model registry integration
        model_map = {
            "image_gen": {
                "fast": "stable-diffusion-v1",
                "standard": "stable-diffusion-xl",
                "premium": "stable-diffusion-xl-refiner"
            },
            "text_gen": {
                "fast": "gpt-3.5-turbo",
                "standard": "gpt-4",
                "premium": "gpt-4-turbo"
            },
            "analysis": {
                "fast": "bert-base",
                "standard": "bert-large",
                "premium": "roberta-large"
            }
        }
        
        task_models = model_map.get(task_type, {})
        recommended = task_models.get(tier, task_models.get("standard", "default"))
        
        self.logger.debug(
            f"Model recommendation for {task_type}: {recommended} (tier: {tier})"
        )
        
        return recommended
    
    def should_use_cache(self) -> bool:
        """Determine if caching should be used."""
        return self.get_config("use_cache")
    
    def should_parallel_execute(self) -> bool:
        """Determine if parallel execution should be used."""
        return self.get_config("parallel_execution")
    
    def get_retry_policy(self) -> Dict:
        """
        Get retry policy configuration.
        
        Returns:
            Retry policy parameters
        """
        return {
            "max_retries": self.get_config("max_retries"),
            "backoff_factor": 1.5 if self.preference == QualityPreference.QUALITY else 1.0
        }
    
    def set_preference(self, preference: str):
        """
        Update the quality preference.
        
        Args:
            preference: New preference value
        """
        try:
            new_preference = QualityPreference(preference)
            self.preference = new_preference
            
            self.logger.info(
                f"Updated preference to: {self.preference.value}"
            )
        except ValueError:
            raise ValueError(
                f"Invalid preference '{preference}'. "
                f"Must be one of: speed, balanced, quality"
            )
    
    def get_summary(self) -> Dict:
        """
        Get a summary of the current profile.
        
        Returns:
            Profile summary
        """
        config = self.get_config()
        
        return {
            "project_id": self.project_id,
            "preference": self.preference.value,
            "description": config["description"],
            "config": config
        }
