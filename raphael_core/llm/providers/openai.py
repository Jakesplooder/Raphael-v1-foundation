import os
import json
import time
import urllib.request
from typing import Any
from .base_provider import BaseProvider, ReasoningResult

class OpenAIProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "openai"

    def reason(self, model: str, system_prompt: str, context: str, task: str) -> ReasoningResult:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
            
        start_time = time.time()
        url = "https://api.openai.com/v1/chat/completions"
        
        req_model = model if model and model != "default" else "gpt-4o-mini"
        
        messages = [
            {"role": "system", "content": f"{system_prompt}\nRule: Only reason from the supplied evidence. Do not invent facts."},
            {"role": "user", "content": f"Context/Evidence:\n{context}\n\nTask:\n{task}"}
        ]
        
        data = {
            "model": req_model,
            "messages": messages
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"OpenAI request failed: {e}")
            
        latency = time.time() - start_time
        message_content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        token_count = result.get("usage", {}).get("completion_tokens", 0)
        
        res = ReasoningResult(
            provider_name=self.provider_name,
            model_name=req_model,
            response=message_content,
            latency_sec=latency,
            token_count=token_count,
            raw_output=result
        )
        res.cost = token_count * 0.000001
        return res
