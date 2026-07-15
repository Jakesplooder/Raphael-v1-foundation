import logging
from typing import Dict, Any, List

from ..ai_gateway import AIGateway

logger = logging.getLogger("rrk.services.builder.reviewers")

class SpecializedReviewer:
    """Base class for specialized workflow reviewers."""
    def __init__(self, ai_gateway: AIGateway):
        self.ai_gateway = ai_gateway
        
    @property
    def capability(self) -> str:
        return "reviewing"
        
    @property
    def specialization(self) -> str:
        raise NotImplementedError

    def review(self, files: Dict[str, str]) -> List[str]:
        task = f"Perform a {self.specialization} review on the following files:\n"
        for k, v in files.items():
            task += f"\n--- {k} ---\n{v}\n"
            
        from pydantic import BaseModel, Field
        from typing import List
        class ReviewFinding(BaseModel):
            description: str = Field(..., description="A specific finding or issue.")
            severity: str = Field(..., description="LOW, MEDIUM, HIGH, or CRITICAL.")
            
        class ReviewResponse(BaseModel):
            findings: List[ReviewFinding]
            
        response = self.ai_gateway.generate(
            capability=self.capability,
            task=task,
            context={"specialization": self.specialization},
            schema_model=ReviewResponse
        )
        
        if response.get("status") == "success":
            data = response.get("response", {})
            return [f"[{f['severity']}] {f['description']}" for f in data.get("findings", [])]
            
        return [f"{self.specialization} review failed to complete."]

class SecurityReviewer(SpecializedReviewer):
    @property
    def specialization(self) -> str:
        return "security"

class ArchitectureReviewer(SpecializedReviewer):
    @property
    def specialization(self) -> str:
        return "architecture"

class StyleReviewer(SpecializedReviewer):
    @property
    def specialization(self) -> str:
        return "style"

class PerformanceReviewer(SpecializedReviewer):
    @property
    def specialization(self) -> str:
        return "performance"
