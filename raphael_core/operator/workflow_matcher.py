from typing import Optional, Dict, Any
from .workflow_aliases import WORKFLOW_ALIASES
from .capability_aggregator import capability_aggregator

class WorkflowMatcher:
    def match(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Attempts to match the user's prompt to a registered workflow 
        using aliases.
        Returns the matched workflow dict from the capability registry, or None.
        """
        prompt_lower = prompt.lower()
        
        # 1. Find a matched ID based on aliases
        matched_id = None
        for wf_id, aliases in WORKFLOW_ALIASES.items():
            if any(alias in prompt_lower for alias in aliases):
                matched_id = wf_id
                break
                
        if not matched_id:
            return None
            
        # 2. Return the full workflow metadata from the registry
        manifest = capability_aggregator.load()
        for wf in manifest.get("workflows", []):
            if wf.get("id") == matched_id:
                return wf
                
        return None

workflow_matcher = WorkflowMatcher()
