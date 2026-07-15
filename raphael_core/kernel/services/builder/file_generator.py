import json
import logging
from typing import Dict, Any, List

from ..ai_gateway import AIGateway
from ...models.code_graph import CodeGraph

logger = logging.getLogger("rrk.services.builder.file_generator")

class FileGeneratorService:
    """
    Responsible for generating entire architectural Artifacts at a time (e.g., 'Authentication', 'Dashboard').
    It maps these abstract Artifacts into concrete file paths and code contents,
    ensuring rich context by leveraging the CodeGraph and AIGateway.
    """
    
    def __init__(self, ai_gateway: AIGateway):
        self.ai_gateway = ai_gateway
        
    def generate_artifact(self, artifact_name: str, requirements: str, graph: CodeGraph) -> Dict[str, str]:
        """
        Asks the AI Gateway to generate the necessary files for a logical Artifact.
        Returns a dictionary mapping file paths to file contents.
        """
        logger.info(f"Generating artifact: {artifact_name}")
        
        # We pass the semantic context (features and symbol graph) to the model
        context = {
            "workspace_id": graph.workspace_id,
            "existing_symbols": {k: [s.name for s in v] for k, v in graph.symbols.items()},
            "semantic_features": {k: v.description for k, v in graph.features.items()}
        }
        
        prompt = (
            f"You are the Builder. Map the architectural Artifact '{artifact_name}' to concrete files.\n"
            f"Requirements: {requirements}\n"
            "Return a JSON object with a 'files' array, where each item has a 'path' and 'content' string."
        )
        
        from pydantic import BaseModel, Field
        from typing import List
        class FileItem(BaseModel):
            path: str = Field(..., description="The relative file path.")
            content: str = Field(..., description="The exact code content for the file.")
            
        class GenerationSchema(BaseModel):
            files: List[FileItem]
        
        response = self.ai_gateway.generate(
            capability="coding",
            task=prompt,
            context=context,
            schema_model=GenerationSchema
        )
        
        if response.get("status") == "success":
            data = response.get("response", {})
            if "files" in data:
                return {f["path"]: f["content"] for f in data["files"]}
                
        logger.error(f"Failed to generate artifact. AI Gateway response: {response.get('error', 'Unknown Error')}")
        return {f"src/generated_{artifact_name.lower()}.ts": "// Fallback generated file"}
