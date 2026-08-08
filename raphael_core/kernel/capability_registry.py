from typing import Dict, Any, List, Optional

CAPABILITY_REGISTRY: List[Dict[str, Any]] = [
    {
        "id": "storyboard_factory",
        "triggers": [
            "run storyboard",
            "create storyboard",
            "make video",
            "storyboard pipeline"
        ],
        "handler": "VideoEngine.run_pipeline",
        "cli_command": "storyboard-run",
        "workflow": "ltx_storyboard_factory",
        "requires_confirmation": True
    },
    {
        "id": "pod_studio",
        "triggers": [
            "run pod",
            "create pod",
            "pod studio",
            "run pod studio"
        ],
        "handler": "pod_pipeline",
        "cli_command": "pod-pipeline",
        "workflow": "pod_generation_pipeline",
        "requires_confirmation": True
    },
    {
        "id": "builder",
        "triggers": [
            "run builder",
            "start builder",
            "build app"
        ],
        "handler": "build_council_plan",
        "cli_command": "build-council-plan",
        "workflow": "builder_workspace_generation",
        "requires_confirmation": True
    }
]

def resolve_capability(text: str) -> Optional[Dict[str, Any]]:
    """
    Returns the capability dictionary if the text matches any of its triggers.
    """
    text_lower = text.lower().strip()
    for cap in CAPABILITY_REGISTRY:
        if any(trigger in text_lower for trigger in cap["triggers"]):
            return cap
    return None
