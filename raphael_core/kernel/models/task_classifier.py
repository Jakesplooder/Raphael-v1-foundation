import re
from typing import Tuple

class TaskClassifier:
    """
    Classifies tasks into complexity and required capabilities.
    For D21 Phase 2, uses robust heuristics. Can be replaced with a fast LLM call (e.g. Phi-3) later.
    """
    
    COMPLEXITY_LOW = "LOW"
    COMPLEXITY_HIGH = "HIGH"
    COMPLEXITY_VERY_HIGH = "VERY_HIGH"

    def __init__(self):
        self.coding_keywords = ["code", "docker", "python", "javascript", "refactor", "bug", "script", "frontend", "backend", "api"]
        self.vision_keywords = ["image", "screenshot", "ocr", "ui", "visual", "look at", "picture"]
        self.planning_keywords = ["plan", "strategy", "roadmap", "architecture", "design", "business", "market"]
        self.reasoning_keywords = ["find weakness", "analyze algorithm", "mathematics", "complex", "deep dive", "proof"]

    def classify(self, prompt: str) -> Tuple[str, str]:
        """
        Returns (capability_category, complexity)
        """
        prompt_lower = prompt.lower()
        
        # Determine Capability Category
        if any(k in prompt_lower for k in self.vision_keywords):
            category = "vision"
        elif any(k in prompt_lower for k in self.coding_keywords):
            category = "engineering"
        elif any(k in prompt_lower for k in self.planning_keywords):
            category = "strategic_reasoning"
        elif any(k in prompt_lower for k in self.reasoning_keywords):
            category = "deep_reasoning"
        else:
            category = "fast_reasoning"
            
        # Determine Complexity
        word_count = len(prompt.split())
        complexity = self.COMPLEXITY_LOW
        
        if category == "deep_reasoning":
            complexity = self.COMPLEXITY_VERY_HIGH
        elif category in ["engineering", "strategic_reasoning"]:
            complexity = self.COMPLEXITY_HIGH
        elif word_count > 100:
            complexity = self.COMPLEXITY_HIGH
            
        return category, complexity
