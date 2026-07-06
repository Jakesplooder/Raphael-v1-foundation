import os
import json
import time
import urllib.request
from typing import Any
from .base_provider import BaseProvider, ReasoningResult

class GeminiProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "gemini"

    def reason(self, model: str, system_prompt: str, context: str, task: str) -> ReasoningResult:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
            
        start_time = time.time()
        
        req_model = model if model and model != "default" else "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{req_model}:generateContent?key={api_key}"
        
        data = {
            "contents": [
                {"role": "user", "parts": [{"text": f"System:\n{system_prompt}\nRule: Only reason from the supplied evidence. Do not invent facts.\n\nContext/Evidence:\n{context}\n\nTask:\n{task}"}]}
            ]
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={
            "Content-Type": "application/json"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Gemini request failed: {e}")
            
        latency = time.time() - start_time
        message_content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        token_count = result.get("usageMetadata", {}).get("candidatesTokenCount", 0)
        
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
