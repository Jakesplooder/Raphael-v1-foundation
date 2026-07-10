import json
import re
from typing import Dict
from .llm.providers.ollama import OllamaProvider

SYSTEM_PROMPT = """You are Raphael Builder, an elite Senior UI Engineer and Software Architect.
Your task is to design and implement comprehensive web applications.

CRITICAL REQUIREMENTS:
1. Return ONLY valid JSON in the exact format requested. Do not include markdown formatting like ```json or any other text before or after the JSON.
2. Modern Aesthetics: Use vibrant colors, dark modes, glassmorphism, or beautiful tailwind/vanilla CSS. The design MUST wow the user.
3. Fully Functional: Ensure the logic is robust and completely implemented. Do not use placeholders.
4. Comprehensive: Include all necessary components, styles, and logic files.

The JSON format must be a flat mapping of relative file paths to their string contents:
{
  "src/App.jsx": "...",
  "src/main.jsx": "...",
  "index.html": "...",
  "src/styles.css": "..."
}
"""

class BuilderEngine:
    def __init__(self):
        self.provider = OllamaProvider()
        
    def request_build_blueprint(self, description: str, app_name: str, framework: str = "react") -> Dict[str, str]:
        context = f"Framework requested: {framework}"
        task = f"Build a comprehensive, stunning app named '{app_name}'.\nDescription: {description}"
        
        result = self.provider.reason("llama3.1", SYSTEM_PROMPT, context, task)
        response_text = result.response.strip()
        
        # Robust JSON extraction: find the largest block from `{` to the last `}` that parses as JSON
        end_idx = response_text.rfind('}')
        if end_idx != -1:
            for i in range(len(response_text)):
                if response_text[i] == '{':
                    try:
                        json.loads(response_text[i:end_idx+1])
                        response_text = response_text[i:end_idx+1]
                        break
                    except json.JSONDecodeError:
                        continue
                        
        response_text = response_text.strip()
        
        try:
            files = json.loads(response_text)
            if not isinstance(files, dict):
                raise ValueError("LLM did not return a dictionary object.")
            return files
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Builder failed to parse JSON from LLM: {e}\nRaw output: {response_text}")
