import os
import hashlib
from pathlib import Path
import json
import logging

from ..models.code_graph import CodeGraph, FileNode

logger = logging.getLogger("rrk.services.workspace_scanner")

class WorkspaceScanner:
    """
    Scans a workspace directory to build or update a CodeGraph.
    Includes persistent snapshots for fast re-loads.
    """
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        
    def _hash_file(self, path: Path) -> str:
        h = hashlib.sha256()
        try:
            h.update(path.read_bytes())
            return h.hexdigest()
        except:
            return ""

    def load_graph(self, workspace_id: str) -> CodeGraph:
        """Loads a persistent graph snapshot if it exists, otherwise creates a new one."""
        snapshot_path = self.workspace_root / workspace_id / "codegraph.json"
        if snapshot_path.exists():
            try:
                data = json.loads(snapshot_path.read_text(encoding="utf-8"))
                return CodeGraph(**data)
            except Exception as e:
                logger.warning(f"Failed to load CodeGraph snapshot: {e}")
                
        return CodeGraph(workspace_id=workspace_id)

    def save_graph(self, graph: CodeGraph):
        """Persists the graph snapshot."""
        snapshot_path = self.workspace_root / graph.workspace_id / "codegraph.json"
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(graph.to_json(), encoding="utf-8")

    def scan_workspace(self, workspace_id: str) -> CodeGraph:
        """
        Scans the physical workspace and updates the FileGraph.
        In a full implementation, it would also parse ASTs for the SymbolGraph and DependencyGraph,
        and use the AIGateway to update the SemanticGraph.
        """
        graph = self.load_graph(workspace_id)
        target_dir = self.workspace_root / workspace_id
        
        if not target_dir.exists():
            return graph
            
        current_files = {}
        for root, _, files in os.walk(target_dir):
            if ".git" in root or "node_modules" in root or "__pycache__" in root:
                continue
                
            for file in files:
                if file == "codegraph.json":
                    continue
                    
                full_path = Path(root) / file
                rel_path = full_path.relative_to(target_dir).as_posix()
                
                current_files[rel_path] = FileNode(
                    path=rel_path,
                    extension=full_path.suffix,
                    size_bytes=full_path.stat().st_size,
                    hash=self._hash_file(full_path)
                )
                
        # Update graph with new/modified files
        graph.files = current_files
        
        # MOCK AST & SEMANTIC SCAN
        # In a real system, we'd diff the files, extract symbols, update imports, 
        # and ask AIGateway to map new files to SemanticFeatures.
        
        self.save_graph(graph)
        return graph
