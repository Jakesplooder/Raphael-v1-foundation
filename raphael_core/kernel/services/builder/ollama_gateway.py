import urllib.request
import json
import logging
from typing import Dict, Any, List

from raphael_core.kernel.services.ai_gateway import AIGateway

logger = logging.getLogger("rrk.services.builder.ollama_gateway")

class OllamaGateway(AIGateway):
    def __init__(self, model: str = "llama3.1:latest", url: str = "http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def generate_code(self, prompt: str, context: Dict[str, Any] = None) -> str:
        logger.info(f"OllamaGateway generating code with prompt: {prompt[:50]}...")
        
        # Enforce raw code output without markdown blocks
        system_prompt = "You are a code generator. Output ONLY the raw code requested. Do not use markdown wrappers like ```html or ```. No explanations."
        full_prompt = f"{system_prompt}\n\n{prompt}"
        
        data = json.dumps({
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        }).encode("utf-8")
        
        req = urllib.request.Request(self.url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                res = json.loads(response.read().decode())
                raw_code = res.get("response", "").strip()
                # Strip markdown if model disobeys
                if raw_code.startswith("```"):
                    lines = raw_code.split("\n")
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    raw_code = "\n".join(lines)
                return raw_code
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise

    def review_code(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        return {"status": "approved"}
