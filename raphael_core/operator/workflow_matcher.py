import re
from typing import Optional, Dict, Any, List
from .workflow_aliases import WORKFLOW_CONCEPTS
from .capability_aggregator import capability_aggregator

class WorkflowMatcher:
    def _extract_concepts(self, prompt: str) -> List[str]:
        prompt_lower = prompt.lower()
        # Split into words/tokens
        words = re.findall(r'\b\w+\b', prompt_lower)
        return words

    def match(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        4-Stage Semantic Pipeline:
        1. Concept Extraction
        2. Capability Filter (Mocked for now since all are available locally)
        3. Workflow Scoring
        4. Selection
        """
        extracted_concepts = self._extract_concepts(prompt)
        
        manifest = capability_aggregator.load()
        workflows = manifest.get("workflows", [])
        
        # 3. Workflow Scoring
        best_score = 0
        best_workflow_id = None
        
        for wf_id, wf_meta in WORKFLOW_CONCEPTS.items():
            concepts = wf_meta.get("concepts", [])
            
            score = 0
            for concept in concepts:
                if concept in extracted_concepts:
                    score += 20
                elif any(concept in word or word in concept for word in extracted_concepts if len(word) > 3):
                    # Partial match for similar terms (e.g. 'rapping' vs 'rap')
                    score += 10
            
            if score > best_score:
                best_score = score
                best_workflow_id = wf_id
                
        if best_score < 10 or not best_workflow_id:
            return None
            
        # 4. Selection
        for wf in workflows:
            if wf.get("id") == best_workflow_id:
                return wf
                
        return None

workflow_matcher = WorkflowMatcher()
