import os
from pathlib import Path
from typing import List, Optional

from raphael_core.kernel.models.knowledge import KnowledgeItem


class KnowledgeRepository:
    """
    Strictly handles physical IO in the 09_Knowledge vault directory.
    No intelligence or clustering logic exists here.
    """
    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.knowledge_dir = self.vault_root / "09_Knowledge"
        
        # Ensure directories exist
        self._ensure_dirs()
        
    def _ensure_dirs(self):
        """Creates standard knowledge directories if they don't exist."""
        directories = [
            "Academic", "Programming", "Research", "Business",
            "Lessons Learned", "Inventories", "Curation", "Relationships"
        ]
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        for d in directories:
            (self.knowledge_dir / d).mkdir(parents=True, exist_ok=True)

    def scan_files(self) -> List[Path]:
        """Scans the Knowledge directory for all valid files."""
        valid_extensions = {".md", ".txt", ".rst", ".rtf", ".tex", ".csv", ".json"}
        results = []
        for root, dirs, files in os.walk(self.knowledge_dir):
            for file in files:
                p = Path(root) / file
                if p.suffix.lower() in valid_extensions:
                    results.append(p)
        return results

    def save_knowledge_item(self, item: KnowledgeItem) -> None:
        """Persist metadata alongside or inside the file. 
        For now, this is a mock interface since files are the primary truth."""
        pass
        
    def load_knowledge_item(self, item_id: str) -> Optional[KnowledgeItem]:
        """Load a specific knowledge item by ID."""
        pass
