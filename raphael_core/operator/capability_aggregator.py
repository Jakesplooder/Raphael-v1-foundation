import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from raphael_core.kernel.registry import registry

class CapabilityAggregator:
    """
    Builds the structured capability manifest used as the source of truth
    for the Chat, Command Palette, Galaxy, and other OS UI layers.
    """
    def __init__(self):
        self.output_path = Path(os.environ.get("RAPHAEL_RUNTIME_DIR", "C:/Users/cyber/Downloads/RalphaelOS")) / "config" / "raphael_capabilities.json"
        
    def aggregate(self) -> Dict[str, Any]:
        """Builds the structured operational metadata."""
        
        manifest = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "workflows": [
                {
                    "id": "ltx_storyboard_factory",
                    "name": "LTX Storyboard Factory",
                    "domain": "creative",
                    "available": True,
                    "requires_confirmation": True
                },
                {
                    "id": "commerce_store_factory",
                    "name": "Commerce Store Factory",
                    "domain": "business",
                    "available": True,
                    "requires_confirmation": True
                },
                {
                    "id": "pod_studio",
                    "name": "POD Studio",
                    "domain": "creative",
                    "available": True,
                    "requires_confirmation": True
                },
                {
                    "id": "builder_workflow",
                    "name": "Builder Workflow",
                    "domain": "engineering",
                    "available": True,
                    "requires_confirmation": True
                }
            ],
            "engines": [
                {
                    "id": "comfyui",
                    "status": "online",
                    "capabilities": [
                        "image_generation",
                        "video_generation"
                    ]
                },
                {
                    "id": "ltx",
                    "status": "online",
                    "capabilities": [
                        "video_generation"
                    ]
                },
                {
                    "id": "n8n",
                    "status": "online",
                    "capabilities": [
                        "workflow_automation",
                        "api_integration"
                    ]
                }
            ],
            "councils": [
                "Commerce Council",
                "Agency Council",
                "Creator Council",
                "Executive Council",
                "Engineering Council"
            ]
        }
        
        return manifest

    def export(self) -> str:
        manifest = self.aggregate()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
            
        return str(self.output_path)
        
    def load(self) -> Dict[str, Any]:
        if not self.output_path.exists():
            self.export()
        with open(self.output_path, 'r', encoding='utf-8') as f:
            return json.load(f)

capability_aggregator = CapabilityAggregator()
