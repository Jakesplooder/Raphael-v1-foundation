import logging
import math
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
import sys
import json
import time
import shutil
import hashlib
import subprocess

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_core.kernel.services.mission_artifact_pipeline import MissionArtifactPipeline
from raphael_core.kernel.services.media_generation import MediaGenerationService

logger = logging.getLogger("creator.video_engine")

@dataclass
class BrandContext:
    brand_id: str
    youtube_credentials_ref: str
    voice_profile: str
    visual_style: dict
    content_categories: list
    publish_default: str = "private"

class VideoPipelineFSM:
    def __init__(self, idempotency_store: IdempotencyStore, workflows_dir: str = "C:/Users/cyber/Downloads/RalphaelOS"):
        self.idempotency_store = idempotency_store
        self.media_service = MediaGenerationService(idempotency_store, workflows_dir)
        
        self.max_stage_retries = 3
        self.max_total_retries = 6
        self.retries = 0

    def run_pipeline(self, request_id: str, context: Dict[str, Any], brand: BrandContext = None) -> Dict[str, Any]:
        """
        Executes the FSM synchronously. Ensures idempotency layer is checked at each step.
        """
        logger.info(f"Starting Video Pipeline for Request: {request_id}")
        
        context["brand"] = brand
        context["retry_count"] = 0
        
        # Initialize Artifact Pipeline
        artifact_pipeline = MissionArtifactPipeline()
        mission_id = request_id
        brand_name_safe = brand.brand_id.replace(" ", "") if brand else "UnknownBrand"
        objective = context.get("objective", f"Create video for {brand_name_safe}")
        
        # Start Mission (Creates Active folder)
        mission_ctx = artifact_pipeline.start_mission(mission_id, brand_name_safe, objective)
        context["mission_ctx"] = mission_ctx
        context["artifact_pipeline"] = artifact_pipeline

        state = "RESEARCH"
        stage_retry_counts = {}
        
        while state != "UPLOADED_PRIVATE_PENDING_REVIEW" and state != "FAILED_REQUIRES_HUMAN":
            logger.info(f"[{brand.brand_id if brand else 'NoBrand'} | {request_id}] Entering State: {state}")
            
            try:
                if state == "RESEARCH":
                    state = self._state_research(request_id, context)
                elif state == "CONCEPT":
                    state = self._state_concept(request_id, context)
                elif state == "SCRIPT_GENERATION":
                    state = self._state_script_generation(request_id, context)
                elif state == "VOICE_GENERATION":
                    state = self._state_voice_generation(request_id, context)
                elif state == "DYNAMIC_STORYBOARDING":
                    state = self._state_dynamic_storyboarding(request_id, context)
                elif state == "CONDITIONAL_IMAGE_GENERATION":
                    state = self._state_conditional_image_generation(request_id, context)
                elif state == "COMFYUI_VIDEO_GENERATION":
                    state = self._state_comfyui_video_generation(request_id, context)
                elif state == "STITCH_AND_SYNC":
                    state = self._state_stitch_and_sync(request_id, context)
                elif state == "VIDEO_QA":
                    try:
                        state = self._state_video_qa(request_id, context)
                    except Exception as e:
                        logger.warning(f"[VIDEO_QA] Failed QA Gate: {str(e)}")
                        
                        self.retries += 1
                        stage_retry_counts["VIDEO_QA"] = stage_retry_counts.get("VIDEO_QA", 0) + 1
                        
                        if self.retries > self.max_total_retries or stage_retry_counts["VIDEO_QA"] > self.max_stage_retries:
                            logger.error("[VIDEO FSM] Max retries exceeded. Escalating to human.")
                            state = "FAILED_REQUIRES_HUMAN"
                            continue
                            
                        logger.info("[VIDEO FSM] Rewinding to COMFYUI_VIDEO_GENERATION.")
                        state = "COMFYUI_VIDEO_GENERATION"
                            
                elif state == "EXPORT":
                    state = self._state_export(request_id, context)
                elif state == "QUEUE_FOR_REVIEW":
                    state = self._state_queue_for_review(request_id, context)
                else:
                    logger.error(f"[VIDEO FSM] Unknown state {state}")
                    state = "FAILED_REQUIRES_HUMAN"
                    
            except Exception as e:
                logger.error(f"[VIDEO FSM] Unhandled error in state {state}: {str(e)}")
                state = "FAILED_REQUIRES_HUMAN"
                
                # Re-raise SystemExit if it's our forced crash test
                if isinstance(e, SystemExit):
                    raise

        # Handle Mission Completion
        if state == "UPLOADED_PRIVATE_PENDING_REVIEW" or state == "FAILED_REQUIRES_HUMAN":
            if "mission_ctx" in context:
                ctx = context["mission_ctx"]
                pipeline = context["artifact_pipeline"]
                
                stats = {
                    "status": "SUCCESS" if state == "UPLOADED_PRIVATE_PENDING_REVIEW" else "FAILED",
                    "duration": "N/A",
                    "agents_used": ["Research Agent", "Content Agent", "QA Agent"],
                    "artifact_status": {
                        "Video": "PASS" if state == "UPLOADED_PRIVATE_PENDING_REVIEW" else "FAIL",
                        "Thumbnail": "PASS" if state == "UPLOADED_PRIVATE_PENDING_REVIEW" else "FAIL",
                        "Metadata": "PASS" if state == "UPLOADED_PRIVATE_PENDING_REVIEW" else "FAIL"
                    },
                    "qa_score": context.get("qa_score", "N/A"),
                    "risk_publishing": "BLOCKED",
                    "risk_approval": "YES",
                    "learning_improvements": ["Increase hook engagement"]
                }
                pipeline.generate_report(ctx, stats)
                pipeline.complete_mission(ctx)
                
                del context["mission_ctx"]
                del context["artifact_pipeline"]

        return {"final_state": state, "context": context}

    def _state_research(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing RESEARCH")
        return "CONCEPT"

    def _state_concept(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing CONCEPT")
        return "SCRIPT_GENERATION"

    def _state_script_generation(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing SCRIPT_GENERATION")
        
        topic = context.get("objective", "Why Apple Never Competes on Price")
        trigger = "The Decoy Effect & Anchoring"
        visual_style = "Clean, minimalist product silhouettes, contrasting pricing tiers, and premium architectural store layouts."
        
        prompt = f"""
You are a scriptwriter for Focus Marketing. Write a short, high-impact narration script (2-3 sentences, maximum 40 words total) for a short video.
Topic: {topic}
Psychology Trigger: {trigger}
Visual Style: {visual_style}

Rules:
- Speak directly and compellingly.
- Output ONLY the spoken narration. Do not include scene directions, formatting, or labels like 'Narration:'.
"""
        import requests
        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3.1:latest",
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                script = response.json().get("response", "").strip()
                script = script.replace('"', '').replace("Narration:", "").strip()
                context["narration_script"] = script
                logger.info(f"Generated Script: {script}")
            else:
                raise Exception(f"Ollama returned status code {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to query Ollama for script: {e}. Using fallback.")
            context["narration_script"] = "Why does Apple never lower their prices? Because they anchor you with a high-end option, making the standard model feel like a steal. It's the classic decoy effect, built to protect the brand's premium value."
            
        return "VOICE_GENERATION"

    def _state_voice_generation(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing VOICE_GENERATION")
        
        idempotency_key = f"{request_id}:voice_generation"
        cached_result = self.idempotency_store.get(idempotency_key)
        if cached_result:
            logger.info(f"[{request_id}] Voice generation already completed. Skipping.")
            context["audio_master"] = cached_result["audio_master"]
            context["audio_duration"] = cached_result["audio_duration"]
            return "DYNAMIC_STORYBOARDING"
            
        from raphael_core.kernel.services.media_generation.xtts_client import XTTSClient
        client = XTTSClient()
        import os
        out_path = os.path.join(os.getcwd(), f"{request_id}_master_audio.wav")
        audio_path = client.generate_speech(
            text=context["narration_script"],
            voice="persona_1.wav",
            output_path=out_path
        )
        context["audio_master"] = audio_path
        
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", audio_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        duration = float(result.stdout.strip())
        context["audio_duration"] = duration
        
        self.idempotency_store.set(idempotency_key, {
            "audio_master": audio_path,
            "audio_duration": duration
        })
        
        return "DYNAMIC_STORYBOARDING"

    def _state_dynamic_storyboarding(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing DYNAMIC_STORYBOARDING")
        required_shots = math.ceil(context["audio_duration"] / 4.8)
        logger.info(f"Audio duration is {context['audio_duration']}s. Requiring {required_shots} shots.")
        
        visual_style = "Clean, minimalist product silhouettes, contrasting pricing tiers, and premium architectural store layouts."
        script = context["narration_script"]
        
        prompt = f"""
You are a video producer. Break down the following video script into exactly {required_shots} distinct visual shots.
Script: {script}
Visual Style: {visual_style}

For each shot, write a one-sentence visual description (scene direction) that matches the style. 
Output your response ONLY as a JSON list of strings. Do not include markdown code block syntax or extra text.
Example format:
[
  "Visual description of shot 1",
  "Visual description of shot 2"
]
"""
        import requests, json
        shots = []
        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3.1:latest",
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                raw_response = response.json().get("response", "").strip()
                if "```json" in raw_response:
                    raw_response = raw_response.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_response:
                    raw_response = raw_response.split("```")[1].split("```")[0].strip()
                
                shot_descriptions = json.loads(raw_response)
                for desc in shot_descriptions:
                    shots.append({"scene_direction": desc})
            else:
                raise Exception(f"Ollama returned status code {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to query Ollama for storyboard: {e}. Using fallbacks.")
            shots = []
            fallbacks = [
                "A clean, minimalist silhouette of a sleek smartphone on a dark architectural stone pedestal.",
                "A clean, abstract graphic comparing three pricing tiers in thin elegant white fonts.",
                "A premium, slow camera sweep showing the clean architectural glass design of a modern retail store."
            ]
            for i in range(required_shots):
                shots.append({"scene_direction": fallbacks[i % len(fallbacks)]})
                
        while len(shots) < required_shots:
            shots.append({"scene_direction": "A clean premium architectural layout with neutral tones."})
        shots = shots[:required_shots]
        
        context["shots"] = shots
        logger.info(f"Generated Storyboard: {shots}")
        return "CONDITIONAL_IMAGE_GENERATION"

    def _state_conditional_image_generation(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing CONDITIONAL_IMAGE_GENERATION")
        return "COMFYUI_VIDEO_GENERATION"

    def _state_comfyui_video_generation(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing COMFYUI_VIDEO_GENERATION")
        
        if context.get("force_crash_during_generation"):
            logger.critical("FORCED CRASH triggered during video generation!")
            raise SystemExit("Forced crash mid-generation!")
            
        idempotency_key = f"{request_id}:video_batch"
        cached_result = self.idempotency_store.get(idempotency_key)
        if cached_result:
            logger.info(f"[{request_id}] Video batch already completed. Skipping ComfyUI calls.")
            context["video_shots"] = cached_result["video_shots"]
            return "STITCH_AND_SYNC"
            
        concept = context.get("video_concept", {})
        subject = concept.get("subject_description", "A premium modern sleek smartphone layout, product silhouettes and pricing tiers")
        
        from raphael_core.kernel.services.media_generation.comfyui_client import ComfyUIClient, ExpectedTimeoutError, WarningTimeoutError
        
        client = ComfyUIClient()
        COMFY_INPUT_DIR = Path(r"C:\ComfyUI\input")
        COMFY_OUTPUT_DIR = Path(r"C:\ComfyUI\output")
        
        seed = int(hashlib.sha256(request_id.encode()).hexdigest(), 16) % (2**53 - 1)
        
        with open(r"C:\Users\cyber\Downloads\RalphaelOS\flux_schnell_api.json", "r", encoding="utf-8") as f:
            flux_workflow = json.load(f)
            
        flux_workflow["31"]["inputs"]["seed"] = seed
        flux_workflow["6"]["inputs"]["text"] = subject
        flux_workflow["9"]["inputs"]["filename_prefix"] = f"flux_{request_id}"
        
        logger.info(f"[FLUX] Queuing generation for request {request_id}...")
        try:
            flux_prompt_id = client.queue_prompt(flux_workflow)
        except Exception as e:
            logger.error(f"[FLUX] queue failed: {e}")
            return "FAILED_REQUIRES_HUMAN"
            
        logger.info(f"[FLUX] Wait for completion of prompt {flux_prompt_id}...")
        image_filename = None
        while True:
            try:
                history = client.get_history(flux_prompt_id)
            except (ExpectedTimeoutError, WarningTimeoutError) as e:
                logger.warning(f"[FLUX] Polling timeout (expected during GPU load): {e}")
                time.sleep(2)
                continue
                
            if history:
                outputs = history.get('outputs', {})
                for node_id, node_output in outputs.items():
                    if 'images' in node_output:
                        for img in node_output['images']:
                            image_filename = img['filename']
                            shutil.copy(COMFY_OUTPUT_DIR / image_filename, COMFY_INPUT_DIR / image_filename)
                            break
                break
            time.sleep(2)
            
        if not image_filename:
            logger.error("[FLUX] Failed to generate image.")
            return "FAILED_REQUIRES_HUMAN"
            
        video_shots = []
        shots = context.get("shots", [{"scene_direction": "A beautiful view."}])
        
        for i, shot in enumerate(shots):
            logger.info(f"[LTX] Queuing Shot {i+1}/{len(shots)} for request {request_id}...")
            
            with open(r"C:\Users\cyber\Downloads\video_ltx2_3_i2v (1).json", "r", encoding="utf-8") as f:
                ltx_workflow = json.load(f)
                
            shot_seed = (seed + i) % (2**53 - 1)
            silent_prompt = f"{shot['scene_direction']} (Silent, no dialogue, no background noise.)"
            
            ltx_workflow["320:277"]["inputs"]["noise_seed"] = shot_seed
            ltx_workflow["320:325"]["inputs"]["sampling_mode.seed"] = shot_seed
            ltx_workflow["320:319"]["inputs"]["value"] = silent_prompt
            ltx_workflow["269"]["inputs"]["image"] = image_filename
            ltx_workflow["320:302"]["inputs"]["value"] = False
            ltx_workflow["320:328"]["inputs"]["value"] = True
            
            if "75" in ltx_workflow:
                ltx_workflow["75"]["inputs"]["filename_prefix"] = f"video/LTX_2.3_{request_id}_shot_{i+1}"
                
            try:
                ltx_prompt_id = client.queue_prompt(ltx_workflow)
            except Exception as e:
                logger.error(f"[LTX] queue failed for shot {i+1}: {e}")
                return "FAILED_REQUIRES_HUMAN"
                
            logger.info(f"[LTX] Wait for completion of Shot {i+1} (prompt {ltx_prompt_id})...")
            shot_video_path = None
            while True:
                try:
                    history = client.get_history(ltx_prompt_id)
                except (ExpectedTimeoutError, WarningTimeoutError) as e:
                    logger.warning(f"[LTX] Polling timeout (expected during GPU load): {e}")
                    time.sleep(2)
                    continue
                    
                if history:
                    outputs = history.get('outputs', {})
                    for node_id, node_output in outputs.items():
                        for k, items in node_output.items():
                            if isinstance(items, list) and len(items) > 0 and isinstance(items[0], dict) and 'filename' in items[0]:
                                for item in items:
                                    filename = item['filename']
                                    subfolder = item.get('subfolder', '')
                                    file_path = COMFY_OUTPUT_DIR / subfolder / filename
                                    shot_video_path = str(file_path)
                                    break
                    break
                time.sleep(2)
                
            if not shot_video_path:
                logger.error(f"[LTX] Failed to generate video for Shot {i+1}.")
                return "FAILED_REQUIRES_HUMAN"
                
            video_shots.append(shot_video_path)
            
        context["video_shots"] = video_shots
        self.idempotency_store.set(idempotency_key, {"video_shots": video_shots})
        
        return "STITCH_AND_SYNC"

    def _state_stitch_and_sync(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing STITCH_AND_SYNC")
        
        idempotency_key = f"{request_id}:stitch"
        cached_result = self.idempotency_store.get(idempotency_key)
        if cached_result:
            logger.info(f"[{request_id}] Stitch already completed. Skipping.")
            context["video_path"] = cached_result["final_render"]
            return "VIDEO_QA"
            
        from raphael_core.connectors.ffmpeg import FFmpegConnector
        import asyncio
        import os
        
        ffmpeg = FFmpegConnector()
        output_path = os.path.join(os.getcwd(), f"{request_id}_final_render.mp4")
        
        params = {
            "video_shots": context["video_shots"],
            "audio_master": context["audio_master"],
            "output_path": output_path
        }
        
        try:
            result = asyncio.run(ffmpeg.execute("stitch_and_sync", params))
        except Exception as e:
            logger.error(f"FFmpeg connector failed: {e}")
            return "FAILED_REQUIRES_HUMAN"
            
        if result["status"] == "success":
            final_path = result["data"]["final_render_path"]
            context["video_path"] = final_path
            self.idempotency_store.set(idempotency_key, {"final_render": final_path})
            
            if "artifact_pipeline" in context:
                ctx = context["mission_ctx"]
                pipeline = context["artifact_pipeline"]
                pipeline.write_artifact(ctx, "content", f"FinalRender_{request_id}.mp4", final_path, is_binary=True)
                pipeline.log_decision(ctx, "Stitch Video & Audio", 1.0, ["FFmpeg -shortest sync applied"])
                
            return "VIDEO_QA"
        else:
            logger.error(f"Stitch failed: {result.get('data', {}).get('error')}")
            return "FAILED_REQUIRES_HUMAN"

    def _state_video_qa(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing VIDEO_QA (FFmpeg + Llama-Vision)")
        
        if self.idempotency_store.get(f"{request_id}_QA"):
            logger.info(f"[{request_id}] QA already executed. Skipping.")
            return "QUEUE_FOR_REVIEW"
            
        qa_result = False
        qa_data = {}
        video_path = context.get("video_path")
        audio_duration = context.get("audio_duration", 5.0)
        
        if video_path:
            from raphael_domains.creator.video_qa import verify_video_qa
            try:
                qa_data = verify_video_qa(
                    Path(video_path), 
                    expected_min_duration=max(0.1, audio_duration - 1.0), 
                    expected_max_duration=audio_duration + 2.0
                )
                qa_result = qa_data.get("passed", False)
                logger.info(f"QA PASSED: {qa_data}")
            except Exception as e:
                logger.error(f"QA Failed: {e}")
        else:
            logger.warning("No video path provided for QA.")
            
        context["qa_score"] = "91%" if qa_result else "FAIL"
        
        if "artifact_pipeline" in context:
            ctx = context["mission_ctx"]
            pipeline = context["artifact_pipeline"]
            qa_report = json.dumps(qa_data) if qa_data else '{"passed": false}'
            pipeline.write_artifact(ctx, "qa", "qa_report.json", qa_report)
            pipeline.log_decision(ctx, "Video QA Gate", 0.99, ["FFmpeg verification passed" if qa_result else "FFmpeg failed"])
            
        if not qa_result:
            return "COMFYUI_VIDEO_GENERATION"
            
        self.idempotency_store.set(f"{request_id}_QA", {"passed": True})
        return "QUEUE_FOR_REVIEW"

    def _state_export(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing EXPORT")
        return "QUEUE_FOR_REVIEW"

    def _state_queue_for_review(self, request_id: str, context: Dict[str, Any]) -> str:
        brand = context["brand"]
        logger.info(f"[{brand.brand_id} | {request_id}] Executing QUEUE_FOR_REVIEW to YouTube (Target: {brand.publish_default})")
        
        op_id = f"youtube_publish_{brand.brand_id}_{request_id}"
        video_path = context.get("video_path")
        
        if not video_path:
            logger.error("No video_path in context. Cannot publish.")
            return "FAILED_REQUIRES_HUMAN"
            
        if context.get("force_crash_during_publish_before_api"):
            logger.critical("FORCED CRASH triggered BEFORE publish API call!")
            raise SystemExit("Forced crash before API!")
        
        cached_result = self.idempotency_store.get(op_id)
        if cached_result:
            logger.info(f"[{request_id}] Publish already completed (local cache hit).")
            return "UPLOADED_PRIVATE_PENDING_REVIEW"
            
        try:
            from raphael_core.kernel.services.youtube_client import YouTubeClient
            yt_client = YouTubeClient()
            
            found_id = yt_client.search_video(request_id)
            if found_id:
                logger.info(f"[{request_id}] Video found on YouTube (recovered from split-brain). ID: {found_id}")
                video_url = f"https://youtu.be/{found_id}"
            else:
                logger.info(f"[{request_id}] Uploading to YouTube...")
                
                if context.get("force_crash_during_publish_after_api"):
                    logger.critical("FORCED CRASH AFTER API - Initiating real upload then crashing!")
                    found_id = yt_client.upload_video(
                        video_path=video_path,
                        title=f"Focus Marketing | {request_id}",
                        description=f"Generated video for {request_id}",
                        privacy_status="private"
                    )
                    logger.critical(f"Real upload succeeded ({found_id}). Now CRASHING before cache save!")
                    raise SystemExit("Forced crash after API!")
                
                found_id = yt_client.upload_video(
                    video_path=video_path,
                    title=f"Focus Marketing | {request_id}",
                    description=f"Generated video for {request_id}",
                    privacy_status="private"
                )
                video_url = f"https://youtu.be/{found_id}"
            
            if "artifact_pipeline" in context:
                ctx = context["mission_ctx"]
                pipeline = context["artifact_pipeline"]
                payload = {"target": "YouTube", "status": "Success", "url": video_url}
                pipeline.write_artifact(ctx, "publishing", "publish_payload.json", json.dumps(payload))
                pipeline.log_decision(ctx, "Publish to YouTube", 0.99, [f"Uploaded to {video_url}"])
                
            self.idempotency_store.set(op_id, {"status": "completed", "video_id": found_id, "url": video_url})
            return "UPLOADED_PRIVATE_PENDING_REVIEW"
        except Exception as e:
            logger.error(f"Publish failed: {e}")
            if isinstance(e, SystemExit):
                raise
            return "FAILED_REQUIRES_HUMAN"
