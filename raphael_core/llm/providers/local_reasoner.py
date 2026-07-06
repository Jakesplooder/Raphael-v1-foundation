from .base_provider import BaseProvider, ReasoningResult

class LocalReasonerProvider(BaseProvider):
    @property
    def provider_name(self) -> str:
        return "local_reasoner"

    def reason(self, model: str, system_prompt: str, context: str, task: str) -> ReasoningResult:
        """
        Placeholder interface for Raphael's future self-hosted reasoning model.
        """
        raise NotImplementedError("LocalReasonerProvider is a placeholder for future Raphael self-hosted model.")
