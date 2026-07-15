import json
import os
import time
import logging
from typing import Dict, Any
from pydantic import BaseModel

logger = logging.getLogger("rrk.models.metrics")

class TaskMetric(BaseModel):
    model_name: str
    task_type: str
    latency_ms: float
    tokens_used: int
    success: bool
    user_rating: int = 0
    agent_performance: str = ""

class ModelMetricsTracker:
    def __init__(self, log_file: str = "raphael_storage/memory/metrics/model_performance.jsonl"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
    def record(self, metric: TaskMetric):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(metric.model_dump_json() + "\n")
        except Exception as e:
            logger.error(f"Failed to record metric: {e}")

    def get_summary(self, model_name: str) -> Dict[str, Any]:
        count = 0
        success_count = 0
        total_latency = 0.0
        
        if not os.path.exists(self.log_file):
            return {"count": 0}
            
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                data = json.loads(line)
                if data.get("model_name") == model_name:
                    count += 1
                    if data.get("success"): success_count += 1
                    total_latency += data.get("latency_ms", 0)
                    
        if count == 0:
            return {"count": 0}
            
        return {
            "count": count,
            "success_rate": success_count / count,
            "avg_latency_ms": total_latency / count
        }
