from typing import List, Dict, Any, Optional
from pathlib import Path

from raphael_core.kernel.models.knowledge import KnowledgeItem, KnowledgeCategory, KnowledgeTrack, KnowledgeImportance
from raphael_core.kernel.repositories.knowledge_repository import KnowledgeRepository
from raphael_core.kernel.providers.knowledge.extraction_provider import TextExtractionProvider
from raphael_core.kernel.providers.knowledge.summarization_provider import KnowledgeSummarizationProvider
from raphael_core.kernel.providers.knowledge.embedding_provider import KnowledgeEmbeddingProvider


class KnowledgeService:
    """
    Business logic for explicit information.
    Handles taxonomy, relationships, and metadata injection.
    """
    def __init__(
        self,
        repository: KnowledgeRepository,
        extractor: TextExtractionProvider,
        summarizer: KnowledgeSummarizationProvider,
        embedder: KnowledgeEmbeddingProvider
    ):
        self.repository = repository
        self.extractor = extractor
        self.summarizer = summarizer
        self.embedder = embedder

    def detect_knowledge_category(self, path: Path, text: str) -> KnowledgeCategory:
        """Heuristics to determine the broad category of the knowledge item."""
        text_lower = text.lower()
        if "research" in str(path).lower() or "methodology" in text_lower:
            return KnowledgeCategory.RESEARCH
        if "programming" in str(path).lower() or "def " in text_lower or "class " in text_lower:
            return KnowledgeCategory.PROGRAMMING
        if "business" in str(path).lower() or "strategy" in text_lower or "market" in text_lower:
            return KnowledgeCategory.BUSINESS
        if "academic" in str(path).lower() or "citation" in text_lower:
            return KnowledgeCategory.ACADEMIC
            
        return KnowledgeCategory.GENERAL

    def knowledge_relationship_analysis(self, text: str) -> List[str]:
        """
        Extracts conceptual taxonomies and relationships.
        e.g., Python -> ML -> TensorFlow.
        """
        relationships = []
        text_lower = text.lower()
        
        # Simple heuristic taxonomy examples
        if "python" in text_lower:
            relationships.append("python")
            if "machine learning" in text_lower or "ml" in text_lower:
                relationships.append("machine_learning")
        
        if "strategy" in text_lower and "business" in text_lower:
            relationships.append("business_strategy")
            
        return relationships

    async def ingest_file(self, file_path: Path, importance: KnowledgeImportance = KnowledgeImportance.NORMAL) -> KnowledgeItem:
        """
        Process a file into a structured KnowledgeItem.
        """
        text = self.extractor.extract_text(file_path)
        summary = await self.summarizer.summarize(text)
        
        category = self.detect_knowledge_category(file_path, text)
        relationships = self.knowledge_relationship_analysis(text)
        
        item = KnowledgeItem(
            title=file_path.stem,
            source_path=str(file_path),
            category=category,
            importance=importance,
            summary=summary,
            extracted_text=text,
            relationships=relationships
        )
        
        self.repository.save_knowledge_item(item)
        return item
