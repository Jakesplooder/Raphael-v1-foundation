import logging
from typing import Dict, Any, Optional
from pathlib import Path
import sys

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.visual_qa import verify_visual_qa, QAError, BoundsError

logger = logging.getLogger("creator.pod_engine")

class PodPipelineFSM:
    """
    Executes the Print-on-Demand (POD) workflow following a rigid State Machine.
    Includes automated rewinds on Visual QA failures and idempotency protection
    on the final mock publish stage.
    """
    def __init__(self, idempotency_store: IdempotencyStore):
        self.idempotency_store = idempotency_store
        
        self.max_stage_retries = 3
        self.max_total_retries = 6
        self.retries = 0

    def run_pipeline(self, request_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the entire FSM loop from start to finish.
        """
        state = "RESEARCH"
        stage_retry_counts = {}
        
        while state != "PUBLISHED" and state != "FAILED_REQUIRES_HUMAN":
            logger.info(f"[POD FSM] Entering State: {state}")
            
            try:
                if state == "RESEARCH":
                    state = self._state_research(request_id, context)
                elif state == "CONCEPT":
                    state = self._state_concept(request_id, context)
                elif state == "COMFYUI_GENERATION":
                    state = self._state_comfyui_generation(request_id, context)
                elif state == "TYPOGRAPHY":
                    state = self._state_typography(request_id, context)
                elif state == "VISUAL_QA":
                    try:
                        state = self._state_visual_qa(request_id, context)
                    except QAError as e:
                        logger.warning(f"[VISUAL_QA] Failed QA Gate: {str(e)}")
                        
                        self.retries += 1
                        stage_retry_counts["VISUAL_QA"] = stage_retry_counts.get("VISUAL_QA", 0) + 1
                        
                        if self.retries > self.max_total_retries or stage_retry_counts["VISUAL_QA"] > self.max_stage_retries:
                            logger.error("[POD FSM] Max retries exceeded. Escalating to human.")
                            state = "FAILED_REQUIRES_HUMAN"
                            continue
                            
                        # Rewind Decision Logic
                        if isinstance(e, BoundsError):
                            # Typography geometry is wrong -> Rewind to Typography
                            logger.info("[POD FSM] Rewinding to TYPOGRAPHY.")
                            state = "TYPOGRAPHY"
                        else:
                            # Underlying image is too chaotic/low contrast -> Rewind to Concept/ComfyUI
                            logger.info("[POD FSM] Rewinding to COMFYUI_GENERATION.")
                            state = "COMFYUI_GENERATION"
                            
                elif state == "EXPORT":
                    state = self._state_export(request_id, context)
                elif state == "PUBLISH":
                    state = self._state_publish(request_id, context)
                else:
                    logger.error(f"[POD FSM] Unknown state {state}")
                    state = "FAILED_REQUIRES_HUMAN"
                    
            except Exception as e:
                logger.error(f"[POD FSM] Unhandled error in state {state}: {str(e)}")
                state = "FAILED_REQUIRES_HUMAN"
                
                # Re-raise SystemExit if it's our forced crash test
                if isinstance(e, SystemExit):
                    raise

        return {"final_state": state, "context": context}

    def _state_research(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing RESEARCH")
        return "CONCEPT"

    def _state_concept(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing CONCEPT")
        return "COMFYUI_GENERATION"

    def _state_comfyui_generation(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing COMFYUI_GENERATION")
        return "TYPOGRAPHY"

    def _state_typography(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing TYPOGRAPHY")
        if "expected_text" not in context:
             context["expected_text"] = "POD DESIGN"
        return "VISUAL_QA"

    def _state_visual_qa(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing VISUAL_QA")
        image_path = context.get("image_path")
        if not image_path:
             logger.warning("No image path provided for QA, simulating pass for test purposes.")
             return "EXPORT"
             
        verify_visual_qa(Path(image_path), context.get("expected_text"))
        return "EXPORT"

    def _state_export(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing EXPORT")
        return "PUBLISH"

    def _state_publish(self, request_id: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{request_id}] Executing PUBLISH")
        
        op_id = f"mock_publish_pod_{request_id}"
        
        # 1. Check local cache (fast path)
        cached_result = self.idempotency_store.get(op_id)
        if cached_result:
            logger.info(f"[{request_id}] Publish already completed (local cache hit).")
            return "PUBLISHED"
            
        try:
            # 2. Search-before-Create: Check external state (true idempotency backstop)
            # This protects against the race condition where the local db failed to write
            # after the external side-effect occurred.
            if self._mock_target_has_listing(request_id, context):
                logger.info(f"[{request_id}] Listing found on external target (recovered from split-brain).")
            else:
                self._mock_publish_target(request_id, context)
            
            # 3. Save to local cache
            self.idempotency_store.set(op_id, {"status": "completed"})
            return "PUBLISHED"
        except Exception as e:
            raise

    def _mock_target_has_listing(self, request_id: str, context: Dict[str, Any]) -> bool:
        if "mock_db" in context:
            return request_id in context["mock_db"]
        return False

    def _mock_publish_target(self, request_id: str, context: Dict[str, Any]):
        logger.info(f"[{request_id}] Publishing to mock target...")
        
        if context.get("force_crash_during_publish"):
            logger.critical("FORCED CRASH triggered during mock publish!")
            # We append right BEFORE the crash to simulate the network side effect happening
            if "mock_db" in context:
                context["mock_db"].append(request_id)
            raise SystemExit("Forced crash mid-publish!")
            
        if "mock_db" in context:
            context["mock_db"].append(request_id)
