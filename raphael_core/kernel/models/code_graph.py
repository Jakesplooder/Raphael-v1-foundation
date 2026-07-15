from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class FileNode(BaseModel):
    path: str
    extension: str
    size_bytes: int
    hash: str
    
class SymbolNode(BaseModel):
    name: str
    type: str # e.g. 'function', 'class', 'interface', 'variable'
    file_path: str
    line_start: int
    line_end: int

class DependencyEdge(BaseModel):
    source_path: str
    target_path: str
    import_statement: str

class SemanticFeature(BaseModel):
    name: str
    description: str
    associated_files: List[str] = Field(default_factory=list)
    associated_symbols: List[str] = Field(default_factory=list)

class CodeGraph(BaseModel):
    """
    Comprehensive representation of a software workspace.
    """
    workspace_id: str
    
    # File Graph: Tracks physical files
    files: Dict[str, FileNode] = Field(default_factory=dict)
    
    # Symbol Graph: Tracks logical code elements
    symbols: Dict[str, List[SymbolNode]] = Field(default_factory=dict)
    
    # Dependency Graph: Tracks imports and requires
    dependencies: List[DependencyEdge] = Field(default_factory=list)
    
    # Semantic Graph: Tracks high-level features (e.g. Auth, Payments)
    features: Dict[str, SemanticFeature] = Field(default_factory=dict)
    
    def to_json(self) -> str:
        return self.model_dump_json(indent=2)
