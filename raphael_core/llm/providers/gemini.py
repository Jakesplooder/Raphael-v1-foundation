import os
import json
import time
from typing import Any
from .base_provider import BaseProvider, ReasoningResult
from google import genai

class GeminiProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.client = None

    @property
    def provider_name(self) -> str:
        return "gemini"

    def _ensure_client(self):
        if not self.client:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set.")
            self.client = genai.Client(api_key=api_key)

    def reason(self, model: str, system_prompt: str, context: str, task: str) -> ReasoningResult:
        self._ensure_client()
        start_time = time.time()
        
        req_model = model if model and model != "default" else "gemini-2.0-flash"
        
        prompt = f"System:\n{system_prompt}\nRule: Only reason from the supplied evidence. Do not invent facts.\n\nContext/Evidence:\n{context}\n\nTask:\n{task}"
        
        try:
            response = self.client.models.generate_content(
                model=req_model,
                contents=prompt
            )
            message_content = response.text
            token_count = 0
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                token_count = response.usage_metadata.total_token_count
        except Exception as e:
            raise RuntimeError(f"Gemini request failed: {e}")
            
        latency = time.time() - start_time
        
        res = ReasoningResult(
            provider_name=self.provider_name,
            model_name=req_model,
            response=message_content,
            latency_sec=latency,
            token_count=token_count,
            raw_output={"text": message_content}
        )
        res.cost = token_count * 0.000001
        return res
