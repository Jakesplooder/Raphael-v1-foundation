import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext
from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore

logger = logging.getLogger("creator.video_queue")

class VideoQueueManager:
    def __init__(self, queue_path: Path, engine: VideoPipelineFSM):
        self.queue_path = queue_path
        self.engine = engine
        self._load_queue()

    def _load_queue(self):
        if self.queue_path.exists():
            try:
                data = json.loads(self.queue_path.read_text())
                self.queue = data.get("remaining", [])
                self.completed = data.get("completed", [])
            except json.JSONDecodeError:
                self.queue = []
                self.completed = []
        else:
            self.queue = []
            self.completed = []
            
    def _save_queue(self):
        # Clean out any non-serializable objects (like the brand object) from payload
        def clean_payload(q):
            cleaned = []
            for item in q:
                c = dict(item)
                c["payload"] = {k:v for k,v in item["payload"].items() if k != "brand"}
                cleaned.append(c)
            return cleaned

        data = {
            "remaining": clean_payload(self.queue),
            "completed": clean_payload(self.completed)
        }
        self.queue_path.write_text(json.dumps(data, indent=2))

    def enqueue(self, request_id: str, brand_contexts: List[BrandContext], payload: Dict[str, Any]):
        """
        Enqueues a fan-out generation request for multiple brands.
        """
        for brand in brand_contexts:
            job = {
                "request_id": request_id,
                "brand_id": brand.brand_id,
                "payload": payload,
                # We serialize the brand context so it persists across restarts
                "brand_context": {
                    "brand_id": brand.brand_id,
                    "youtube_credentials_ref": brand.youtube_credentials_ref,
                    "voice_profile": brand.voice_profile,
                    "visual_style": brand.visual_style,
                    "content_categories": brand.content_categories,
                    "publish_default": brand.publish_default
                }
            }
            # Only enqueue if not already completed or in queue
            if not any(c["request_id"] == request_id and c["brand_id"] == brand.brand_id for c in self.completed):
                if not any(q["request_id"] == request_id and q["brand_id"] == brand.brand_id for q in self.queue):
                    self.queue.append(job)
        
        self._save_queue()

    def process_queue(self):
        """
        Processes the queue sequentially. 
        Acts as a mutex ensuring only one GPU workload executes at a time.
        """
        while self.queue:
            job = self.queue[0]
            brand_data = job["brand_context"]
            brand = BrandContext(**brand_data)
            
            logger.info(f"Processing Job for Brand: {brand.brand_id}")
            
            # The engine runs synchronously. It will block until PUBLISHED or FAILED.
            result = self.engine.run_pipeline(job["request_id"], job["payload"], brand)
            
            if result["final_state"] == "PUBLISHED":
                self.completed.append(job)
                self.queue.pop(0)
                self._save_queue()
            else:
                logger.error(f"Job failed for Brand: {brand.brand_id} with state {result['final_state']}")
                # Depending on policy, we might pop or leave in queue. 
                # For this proof, we will leave it in queue to simulate a block, or pop it to continue.
                # The user's test implies crash recovery, which interrupts the python process entirely.
                break
