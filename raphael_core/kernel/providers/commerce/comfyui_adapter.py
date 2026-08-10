import asyncio
import time
from typing import Dict, Any, Optional

from .renderer import Renderer
from ...models.media_generation import GenerationRequest, GenerationJob, GenerationStatus
from ...services.media_generation.comfyui_client import ComfyUIClient, ComfyUIError

class ComfyUIAdapter(Renderer):
    """
    Implements the Renderer interface for ComfyUI.
    Dumb adapter: translates requests, submits, polls, and returns standard outputs.
    """
    
    def __init__(self, client: Optional[ComfyUIClient] = None):
        self.client = client or ComfyUIClient()
        
    @property
    def renderer_name(self) -> str:
        return "comfyui"

    def _build_workflow(self, request: GenerationRequest) -> Dict[str, Any]:
        mode = request.metadata.get("mode", "mock")
        if mode == "real":
            workflow = {
                "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "flux1-schnell-fp8-e4m3fn.safetensors", "weight_dtype": "default"}},
                "2": {"class_type": "DualCLIPLoader", "inputs": {"clip_name1": "t5xxl_fp8_e4m3fn.safetensors", "clip_name2": "clip_l.safetensors", "type": "flux"}},
                "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
                "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
                "5": {"class_type": "CLIPTextEncode", "inputs": {"text": request.prompt, "clip": ["2", 0]}},
                "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "", "clip": ["2", 0]}},
                "7": {"class_type": "KSampler", "inputs": {"seed": int(request.metadata.get("seed", 12345)), "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0, "model": ["1", 0], "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["4", 0]}},
                "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
                "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "flux", "images": ["8", 0]}}
            }
        else:
            # Mock / Passthrough Mode (Default)
            import random
            # Convert seed to a deterministic integer for width variation (prevents ComfyUI caching identical graphs)
            seed_val = request.metadata.get("seed")
            if seed_val:
                width = 1024 + (hash(str(seed_val)) % 10)
            else:
                width = 1024 + random.randint(0, 9)
            height = 1024
            
            workflow = {
                "1": {"class_type": "EmptyImage", "inputs": {"width": width, "height": height, "batch_size": 1, "color": 0}},
                "2": {"class_type": "PreviewImage", "inputs": {"images": ["1", 0]}}
            }
            if request.prompt == "FAIL_NOW":
                workflow["3"] = {"class_type": "NonExistentNode", "inputs": {}}
            
        return workflow

    async def submit(self, request: GenerationRequest) -> GenerationJob:
        workflow = self._build_workflow(request)
        try:
            import time
            submit_start = time.time()
            # ComfyUIClient is synchronous in its current implementation, so we wrap it
            prompt_id = await asyncio.to_thread(self.client.queue_prompt, workflow)
            submit_end = time.time()
            
            job = GenerationJob(
                job_id=prompt_id,
                request=request,
                status=GenerationStatus.RUNNING,
                started_at=submit_end,
                telemetry={"renderer": "comfyui", "submit_latency_sec": submit_end - submit_start}
            )
            return job
        except ComfyUIError as e:
            job = GenerationJob(
                job_id=f"failed-{int(time.time())}",
                request=request,
                status=GenerationStatus.FAILED,
                error_message=str(e),
                telemetry={"renderer": "comfyui"}
            )
            return job

    async def status(self, job_id: str) -> GenerationJob:
        # Real polling logic is managed by the Service, which calls retrieve_outputs
        raise NotImplementedError("Use retrieve_outputs for completion check")

    async def cancel(self, job_id: str) -> bool:
        # ComfyUI cancellation API not strictly defined in client yet, ignoring for D15.1
        return False

    async def retrieve_outputs(self, job_id: str) -> Dict[str, Any]:
        """Polls history to see if job is done, and returns outputs if so."""
        try:
            history = await asyncio.to_thread(self.client.get_history, job_id)
            if history:
                # Check for error status
                hist_status = history.get("status", {})
                
                # Extract timestamps
                start_ts = None
                end_ts = None
                for msg in hist_status.get("messages", []):
                    if msg[0] == "execution_start":
                        start_ts = msg[1].get("timestamp")
                    elif msg[0] in ("execution_success", "execution_error"):
                        end_ts = msg[1].get("timestamp")
                        
                render_duration = None
                if start_ts and end_ts:
                    render_duration = (end_ts - start_ts) / 1000.0
                
                if hist_status.get("status_str") == "error":
                    # Extract the exception message if available
                    err_msg = "Unknown ComfyUI Error"
                    for msg in hist_status.get("messages", []):
                        if msg[0] == "execution_error":
                            err_msg = msg[1].get("exception_message", err_msg)
                    return {"status": "failed", "error": err_msg, "duration": render_duration, "model_name": "none/passthrough"}

                # Extract model name dynamically from the prompt workflow
                model_name = "none/passthrough"
                prompt_data = history.get("prompt", [])
                if len(prompt_data) > 2:
                    workflow_dict = prompt_data[2]
                    for node in workflow_dict.values():
                        class_type = node.get("class_type", "")
                        if class_type == "UNETLoader":
                            model_name = node.get("inputs", {}).get("unet_name", model_name)
                            break
                        elif class_type == "CheckpointLoaderSimple":
                            model_name = node.get("inputs", {}).get("ckpt_name", model_name)
                            break

                # Parse outputs
                outputs = history.get("outputs", {})
                images = []
                import os
                base_dirs = {
                    "temp": "C:/ComfyUI/temp",
                    "output": "C:/ComfyUI/output",
                    "input": "C:/ComfyUI/input"
                }
                for node_id, node_output in outputs.items():
                    if "images" in node_output:
                        for img in node_output["images"]:
                            # Resolve full host path
                            img_type = img.get("type", "output")
                            subfolder = img.get("subfolder", "")
                            filename = img.get("filename", "")
                            base = base_dirs.get(img_type, base_dirs["output"])
                            
                            # Update the filename to be the absolute path so downstream services can verify it
                            img["filename"] = os.path.join(base, subfolder, filename).replace("\\", "/")
                            images.append(img)
                return {"status": "completed", "images": images, "duration": render_duration, "model_name": model_name}
            return {"status": "running"}
        except ComfyUIError as e:
             return {"status": "failed", "error": str(e)}
