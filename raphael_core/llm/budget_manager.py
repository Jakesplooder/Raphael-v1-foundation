from typing import List

def get_routing_tier(mode: str) -> List[str]:
    """
    Returns the preferred order of providers based on budget mode.
    Modes: offline, cheap, balanced, best
    """
    mode = mode.lower()
    
    if mode == "offline":
        return ["ollama", "local_reasoner"]
        
    if mode == "cheap":
        return ["ollama", "local_reasoner", "gemini", "claude"]
        
    if mode == "balanced":
        return ["gemini", "ollama", "claude", "openai"]
        
    if mode == "best":
        return ["claude", "gemini", "openai", "ollama"]
        
    # Default to cheap if unknown
    return ["ollama", "gemini", "claude"]
