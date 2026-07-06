import os
import json
import time
import urllib.request
from typing import Any
from .base_provider import BaseProvider, ReasoningResult

class AnthropicProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "claude"

    def reason(self, model: str, system_prompt: str, context: str, task: str) -> ReasoningResult:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
            
        start_time = time.time()
        url = "https://api.anthropic.com/v1/messages"
        
        req_model = model if model and model != "default" else "claude-3-haiku-20240307"
        
        data = {
            "model": req_model,
            "max_tokens": 4096,
            "system": f"{system_prompt}\nRule: Only reason from the supplied evidence. Do not invent facts.",
            "messages": [
                {"role": "user", "content": f"Context/Evidence:\n{context}\n\nTask:\n{task}"}
            ]
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Anthropic request failed: {e}")
            
        latency = time.time() - start_time
        message_content = result.get("content", [{}])[0].get("text", "")
        token_count = result.get("usage", {}).get("output_tokens", 0)
        
        # Simple cost estimation placeholder
        cost = token_count * 0.000001
        
        res = ReasoningResult(
            provider_name=self.provider_name,
            model_name=req_model,
            response=message_content,
            latency_sec=latency,
            token_count=token_count,
            raw_output=result
        )
        res.cost = cost
        return res
