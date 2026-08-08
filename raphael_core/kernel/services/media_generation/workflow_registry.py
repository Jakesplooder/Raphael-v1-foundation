import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("kernel.media_generation.workflow_registry")

class WorkflowValidationError(Exception):
    pass

class WorkflowRegistry:
    def __init__(self, workflows_dir: str):
        self.workflows_dir = workflows_dir
        
    def load_workflow(self, workflow_name: str) -> Dict:
        """Loads a ComfyUI API-format workflow from disk."""
        import os
        path = os.path.join(self.workflows_dir, f"{workflow_name}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise WorkflowValidationError(f"Failed to load workflow {workflow_name}: {e}")

    def validate_topology(self, workflow: Dict, expected_outputs: list) -> bool:
        """
        Validates that required nodes exist in the workflow graph.
        Detects silent graph-pruning issues (e.g. SaveVideo disappears).
        """
        keys = set(workflow.keys())
        for out in expected_outputs:
            if out not in keys:
                raise WorkflowValidationError(f"WORKFLOW_VALIDATION_FAILURE: Expected output node '{out}' is missing from the graph!")
        return True

    def inject_ltx2_i2v(self, workflow: Dict, concept: Dict, request_id: str, seed: int) -> Dict:
        """
        Specific injector for LTX 2.3 I2V workflow.
        """
        try:
            # 1. Seed override
            workflow["320:277"]["inputs"]["noise_seed"] = seed
            workflow["320:325"]["inputs"]["sampling_mode.seed"] = seed
            
            # 2. Prompt injection
            # In real usage, this might be 'subject_description' or 'scene_direction'
            workflow["320:319"]["inputs"]["value"] = concept.get("scene_direction", "Default prompt")
            
            # 3. Filename
            workflow["75"]["inputs"]["filename_prefix"] = f"video/LTX_{request_id}"
            
            # 4. Modes (Text-to-video vs Image-to-video)
            # 320:302 false = image to video, true = text to video
            is_t2v = concept.get("mode") == "text_to_video"
            workflow["320:302"]["inputs"]["value"] = is_t2v
            
            # Ensure topology has the SaveVideo node (75)
            self.validate_topology(workflow, ["75"])
            
            return workflow
        except KeyError as e:
            raise WorkflowValidationError(f"WORKFLOW_VALIDATION_FAILURE: Missing expected node/input in LTX workflow: {e}")
