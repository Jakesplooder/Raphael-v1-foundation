import json
import time
import urllib.request
from typing import Any
from .base_provider import BaseProvider, ReasoningResult

class OllamaProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "ollama"

    def reason(self, model: str, system_prompt: str, context: str, task: str) -> ReasoningResult:
        """
        Calls local Ollama instance on localhost:11434.
        """
        start_time = time.time()
        url = "http://localhost:11434/api/chat"
        
        # Merge system, context, and task into a clear prompt array
        messages = [
            {"role": "system", "content": f"{system_prompt}\nRule: Only reason from the supplied evidence. Do not invent facts."},
            {"role": "user", "content": f"Context/Evidence:\n{context}\n\nTask:\n{task}"}
        ]
        
        data = {
            "model": model if model and model != "default" else "llama3.1",
            "messages": messages,
            "stream": False
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Ollama request failed: {e}")
            
        latency = time.time() - start_time
        message_content = result.get("message", {}).get("content", "")
        token_count = result.get("eval_count", 0) # Ollama returns eval_count
        
        return ReasoningResult(
            provider_name=self.provider_name,
            model_name=data["model"],
            response=message_content,
            latency_sec=latency,
            token_count=token_count,
            raw_output=result
        )
