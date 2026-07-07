import json
import os
from typing import Dict, Any

WM_DIR = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model")
PATTERN_NODES_OUT = os.path.join(WM_DIR, "pattern_nodes.json")

def process_reflection(reflection: Dict[str, Any], prediction: Dict[str, Any]):
    """
    Phase 69.5: Pattern Evolution Engine
    Decays or reinforces patterns based on executive reflection outcomes.
    """
    if not os.path.exists(PATTERN_NODES_OUT):
        return
        
    with open(PATTERN_NODES_OUT, 'r', encoding='utf-8') as f:
        patterns = json.load(f)
        
    adjustment = reflection.get("recommended_confidence_adjustment", 0)
    # The prediction object might not explicitly list the exact patterns used in this mock,
    # but let's assume it used a mock list or the first 2 patterns if unspecified.
    used_patterns = prediction.get("used_pattern_ids", [])
    
    updated = False
    for p in patterns:
        if p["pattern_id"] in used_patterns or len(used_patterns) == 0:
            # If mock, just adjust the first few patterns to simulate evolution
            old_conf = p["confidence_score"]
            new_conf = max(0.1, min(0.95, old_conf + adjustment))
            
            p["confidence_score"] = round(new_conf, 2)
            if new_conf < 0.4:
                p["confidence"] = "Low"
            elif new_conf < 0.7:
                p["confidence"] = "Medium"
            else:
                p["confidence"] = "High"
                
            p["status"] = "Decaying" if adjustment < 0 else "Confirmed"
            updated = True
            
            # Simulate only adjusting one if we didn't have explicit mappings
            if len(used_patterns) == 0:
                break
                
    if updated:
        with open(PATTERN_NODES_OUT, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, indent=2)
