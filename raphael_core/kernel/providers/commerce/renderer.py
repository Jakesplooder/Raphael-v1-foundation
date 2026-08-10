import abc
from typing import Dict, Any
from ...models.media_generation import GenerationRequest, GenerationJob

class Renderer(abc.ABC):
    """
    Capability interface for image generation renderers.
    Implementations (ComfyUIAdapter, OpenAIImageAdapter) translate requests to backend jobs.
    """
    
    @property
    @abc.abstractmethod
    def renderer_name(self) -> str:
        pass

    @abc.abstractmethod
    async def submit(self, request: GenerationRequest) -> GenerationJob:
        """Submit a new generation request to the renderer."""
        pass

    @abc.abstractmethod
    async def status(self, job_id: str) -> GenerationJob:
        """Check the status of a running generation job."""
        pass

    @abc.abstractmethod
    async def cancel(self, job_id: str) -> bool:
        """Cancel an active generation job."""
        pass

    @abc.abstractmethod
    async def retrieve_outputs(self, job_id: str) -> Dict[str, Any]:
        """Retrieve output files/metadata for a completed job."""
        pass
