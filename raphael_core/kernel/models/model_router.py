import logging
import time
from typing import Dict, Any, Optional

from .model_registry import MODELS
from .model_health import ModelHealthChecker
from .model_metrics import ModelMetricsTracker, TaskMetric
from .task_classifier import TaskClassifier
from ..event_bus import emit

logger = logging.getLogger("rrk.models.router")

class ModelRouter:
    def __init__(self):
        self.health = ModelHealthChecker()
        self.metrics = ModelMetricsTracker()
        self.classifier = TaskClassifier()
        
    def route_task(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Classify task, match capability, check hardware, and return selected model execution chain.
        """
        category, complexity = self.classifier.classify(prompt)
        
        # Override for complexity: if it's VERY_HIGH, force deep reasoning if available.
        # But if it's vision, vision overrides.
        if category != "vision" and complexity == TaskClassifier.COMPLEXITY_VERY_HIGH:
            category = "deep_reasoning"
        elif category == "fast_reasoning" and complexity == TaskClassifier.COMPLEXITY_HIGH:
            category = "strategic_reasoning"
            
        model_config = MODELS.get(category)
        if not model_config:
            model_config = MODELS.get("fast_reasoning") # ultimate fallback
            
        selected_model = self._select_best_available_model(model_config)
        
        emit("MODEL_ROUTED", "ModelRouter", {
            "category": category,
            "complexity": complexity,
            "selected_model": selected_model
        })
        
        return {
            "model": selected_model,
            "category": category,
            "complexity": complexity
        }

    def _select_best_available_model(self, model_config: Dict[str, Any]) -> str:
        # Check primary
        primary = model_config["model"]
        if self.health.can_load_model(primary):
            return primary
            
        # Check fallbacks
        for fallback in model_config.get("fallbacks", []):
            if self.health.can_load_model(fallback):
                logger.info(f"Primary model {primary} unavailable. Falling back to {fallback}")
                return fallback
                
        # If all checks fail, just return primary and let it crash/queue
        return primary

    def execute_and_track(self, prompt: str, execution_fn: callable) -> Any:
        start_time = time.time()
        routing_info = self.route_task(prompt)
        selected_model = routing_info["model"]
        
        success = False
        result = None
        try:
            # execution_fn must take the selected model and prompt
            result = execution_fn(selected_model, prompt)
            success = True
        except Exception as e:
            logger.error(f"Execution failed on {selected_model}: {e}")
            
        latency = (time.time() - start_time) * 1000
        
        metric = TaskMetric(
            model_name=selected_model,
            task_type=routing_info["category"],
            latency_ms=latency,
            tokens_used=0, # Placeholder
            success=success
        )
        self.metrics.record(metric)
        return result
