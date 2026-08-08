from typing import List, Dict, Any

class CapabilityRegistry:
    """
    Registry of system capabilities to inform the Operator Shell planner
    of what is possible to automate or connect.
    """
    
    def __init__(self):
        self.capabilities = [
            {"id": "n8n", "type": "workflow_engine", "description": "Node-based automation for APIs and logic"},
            {"id": "comfyui", "type": "image_engine", "description": "Node-based image and video generation pipeline"},
            {"id": "ffmpeg", "type": "media_processing", "description": "Video and audio processing"},
            {"id": "youtube", "type": "publishing", "description": "YouTube API integration for uploads"},
            {"id": "gemini", "type": "llm", "description": "Google Gemini for planning and reasoning"},
            {"id": "ollama", "type": "llm", "description": "Local LLM reasoning and coding"},
            {"id": "qwen", "type": "llm", "description": "Local coding specialist"},
            {"id": "analytics_gateway", "type": "service", "description": "Raphael Analytics subsystem"},
            {"id": "business_manager", "type": "service", "description": "Raphael Business Objects Manager"},
            {"id": "matrix", "type": "ui", "description": "The Matrix Dashboard view"}
        ]
        
    def get_all_capabilities(self) -> List[Dict[str, Any]]:
        return self.capabilities
        
    def format_for_prompt(self) -> str:
        lines = ["Available System Capabilities:"]
        for cap in self.capabilities:
            lines.append(f"- {cap['id']} ({cap['type']}): {cap['description']}")
        return "\n".join(lines)

capability_registry = CapabilityRegistry()
