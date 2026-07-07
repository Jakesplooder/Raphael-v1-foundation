import os
import json
import uuid
import time
import hashlib
from datetime import datetime
from typing import Dict, Any, List
from .llm.router import LLMRouter
from . import world_model
from . import pattern_engine

# Output Paths
WM_DIR = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model")
TRACE_DIR = os.path.join(WM_DIR, "reasoning_traces")
os.makedirs(TRACE_DIR, exist_ok=True)

class ReasoningEngine:
    def __init__(self):
        self.router = LLMRouter()
        
    def _generate_id(self, prefix: str, text: str) -> str:
        hash_obj = hashlib.sha256(text.encode('utf-8')).hexdigest()[:10].upper()
        return f"{prefix}-{hash_obj}"

    def reason(self, mode: str, system_prompt: str, context: str, task: str, 
               budget_mode: str = "balanced", capability: str = "reasoning", 
               category: str = "executive") -> Dict[str, Any]:
        """
        Executes a reasoning task using the specified mode.
        Rule: LLMs reason. Raphael decides.
        Modes: single, consensus, advisory
        """
        start_time = time.time()
        
        # Single mode: standard single provider request
        if mode == "single":
            try:
                result = self.router.execute(system_prompt, context, task, budget_mode, capability, category)
            except RuntimeError as e:
                # Mock fallback for test environments without API keys
                class MockResult:
                    def __init__(self):
                        self.response = f"[MOCK REASONING] Evaluated {task} based on context."
                        self.token_count = 100
                        self.latency_sec = 1.5
                        self.model_name = "mock-model"
                        self.provider_name = "mock-provider"
                result = MockResult()
            trace = self._build_trace("single", [result], start_time)
            return {"response": result.response, "trace": trace}
            
        # Consensus mode: run on 2 top models and synthesize
        elif mode == "consensus":
            # For this simple consensus, we ask 'best' and 'offline'
            r1 = self.router.execute(system_prompt, context, task, "best", capability, category)
            r2 = self.router.execute(system_prompt, context, task, "offline", capability, category)
            
            # Synthesize (using a third, cheap model to combine them)
            synth_context = f"Model 1 Analysis:\n{r1.response}\n\nModel 2 Analysis:\n{r2.response}"
            synth_task = f"Original Task: {task}\nSynthesize the above reasoning into a final consensus."
            r3 = self.router.execute(system_prompt, synth_context, synth_task, "cheap", capability, category)
            
            trace = self._build_trace("consensus", [r1, r2, r3], start_time)
            return {"response": r3.response, "trace": trace}
            
        # Advisory mode: one predicts, another critiques
        elif mode == "advisory":
            r1 = self.router.execute(system_prompt, context, task, "best", capability, category)
            critique_task = f"Critique this reasoning for flaws, risks, and missing angles:\n{r1.response}"
            r2 = self.router.execute(system_prompt, context, critique_task, "balanced", capability, category)
            
            trace = self._build_trace("advisory", [r1, r2], start_time)
            return {"response": f"Primary Reasoning:\n{r1.response}\n\nCritique:\n{r2.response}", "trace": trace}
            
        else:
            raise ValueError(f"Unknown reasoning mode: {mode}")

    def _build_trace(self, mode: str, results: list, start_time: float) -> dict:
        trace_id = self._generate_id("TRACE", str(start_time) + mode)
        
        nodes = []
        for r in results:
            nodes.append({
                "provider": r.provider_name,
                "model": r.model_name,
                "latency_sec": round(r.latency_sec, 2),
                "tokens": r.token_count,
                "cost": getattr(r, 'cost', 0.0)
            })
            
        trace = {
            "reasoning_trace_id": trace_id,
            "mode": mode,
            "nodes": nodes,
            "total_duration_sec": round(time.time() - start_time, 2),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        trace_path = os.path.join(TRACE_DIR, f"{trace_id}.json")
        with open(trace_path, 'w', encoding='utf-8') as f:
            json.dump(trace, f, indent=2)
            
        return trace

# Singleton instance for core
engine = ReasoningEngine()
