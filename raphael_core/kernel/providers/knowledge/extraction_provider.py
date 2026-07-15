import abc
from pathlib import Path

class TextExtractionProvider(abc.ABC):
    """Abstract interface for extracting text from raw files."""
    
    @abc.abstractmethod
    def extract_text(self, file_path: Path) -> str:
        """Extract plain text from the file."""
        pass


class BasicMarkdownExtractionProvider(TextExtractionProvider):
    """Basic extraction for markdown and plaintext files."""
    
    def extract_text(self, file_path: Path) -> str:
        if not file_path.exists() or not file_path.is_file():
            return ""
            
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                # Naive chunking for now
                text = f.read(18000)
                return text
        except Exception:
            return ""
