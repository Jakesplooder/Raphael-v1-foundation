from typing import Dict, Any, List
import hashlib

# Rule 2: We must use world_model.search_nodes for unknown opportunity discovery
from raphael_core import world_model

def score_opportunity(config: Any, career_twin: Dict[str, Any], opportunity_query: str) -> List[Dict[str, Any]]:
    """
    Finds and scores market opportunities based on the career twin.
    Uses semantic search (Rule 2) because we don't know the nodes in advance.
    """
    model = world_model.load_model(config)
    matches = world_model.search_nodes(model, opportunity_query)
    
    opportunities = []
    
    twin_skills = {s["name"].lower(): s for s in career_twin.get("skills", [])}
    
    for match in matches:
        summary_text = match.get("summary", "").lower()
        name_text = match.get("name", "").lower()
        
        # 1. Calculate Alignment
        alignment = 0.0
        matched_skills = []
        
        # Exact skill name match in title is high alignment
        for skill_name, skill_data in twin_skills.items():
            if skill_name in name_text:
                alignment += 0.5
                matched_skills.append(skill_name)
            elif skill_name in summary_text:
                alignment += 0.3
                matched_skills.append(skill_name)
                
        alignment = min(1.0, alignment)
        
        # Filter out completely irrelevant results (e.g. Postgres if it didn't match any skills)
        if alignment == 0.0:
            continue
            
        # 2. Calculate Demand Score
        # In a fully integrated system, this reads MARKET.SIGNAL relationships attached to the node.
        # Since we just scaffolded MarketIntelligence, we'll derive a dynamic realistic score 
        # from the node's underlying confidence and a deterministic hash of its ID to simulate variance.
        hash_val = int(hashlib.sha1(match.get("node_id", "").encode()).hexdigest()[:4], 16) / 65535.0
        base_confidence = match.get("confidence", 0.5)
        demand_score = (base_confidence * 0.7) + (hash_val * 0.3)
        
        # 3. Compute Final Score
        growth_rate = hash_val * 0.2 # Simulated growth rate between 0.0 and 0.2
        opportunity_score = (alignment + demand_score + growth_rate) / 3
        
        # 4. Generate Reasoning
        reason = f"Aligned with {len(matched_skills)} verified skills ({', '.join(matched_skills)})."
        
        opportunities.append({
            "opportunity_id": match.get("node_id"),
            "name": match.get("name"),
            "type": match.get("node_type"),
            "alignment": round(alignment, 4),
            "demand_score": round(demand_score, 4),
            "opportunity_score": round(opportunity_score, 4),
            "confidence": round(base_confidence, 4),
            "reasoning": reason
        })
        
    opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return opportunities
