from typing import Any, Dict
from .providers.base_provider import BaseProvider, ReasoningResult
from .provider_manager import ProviderManager
from .cache import CacheManager
from .providers.ollama import OllamaProvider
from .providers.anthropic import AnthropicProvider
from .providers.openai import OpenAIProvider
from .providers.gemini import GeminiProvider
from .providers.local_reasoner import LocalReasonerProvider

class LLMRouter:
    def __init__(self):
        self.manager = ProviderManager()
        self.providers: Dict[str, BaseProvider] = {
            "ollama": OllamaProvider(),
            "claude": AnthropicProvider(),
            "openai": OpenAIProvider(),
            "gemini": GeminiProvider(),
            "local_reasoner": LocalReasonerProvider()
        }
        
    def execute(self, system_prompt: str, context: str, task: str, 
                budget_mode: str = "balanced", capability: str = "reasoning", 
                category: str = "executive") -> ReasoningResult:
        """
        Routes the task to the optimal provider and returns the ReasoningResult.
        Rule: LLMs reason. Raphael decides.
        """
        # Try cache first
        provider_name = self.manager.select_provider(budget_mode, capability)
        cached = CacheManager.get(provider_name, system_prompt, context, task, category)
        if cached:
            # We return the cached result but flag it in the trace (could add cache_hit=True)
            return cached
            
        provider = self.providers.get(provider_name)
        if not provider:
            provider = self.providers["ollama"]
            
        try:
            result = provider.reason("default", system_prompt, context, task)
            # Record success and cache
            cost = getattr(result, 'cost', 0.0) # Providers might return cost
            self.manager.record_success(provider_name, result.latency_sec, result.token_count, cost)
            CacheManager.set("default", system_prompt, context, task, result)
            return result
        except Exception as e:
            is_429 = "429" in str(e) or "rate" in str(e).lower()
            is_timeout = "timeout" in str(e).lower()
            self.manager.record_failure(provider_name, is_429=is_429, is_timeout=is_timeout)
            raise RuntimeError(f"LLM routing failed for provider {provider_name}: {e}")
