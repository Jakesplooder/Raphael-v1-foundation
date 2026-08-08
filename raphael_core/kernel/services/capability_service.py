import os
import uuid
import asyncio
from typing import Dict, Any

from raphael_core.kernel.registry import registry
from raphael_core.kernel.interfaces import Event, EventType

class CapabilityService:
    """
    Acts as the operational bridge between capability intent (from UI/legacy)
    and the physical execution engines.
    
    Responsibilities:
    - Initiative / Mission creation
    - Event lifecycle emission
    - Launching workflows
    """
    
    @staticmethod
    def execute(capability_id: str, context: Dict[str, Any] = None, execution_id: str = None) -> Dict[str, Any]:
        """
        Executes a capability by name, wrapping it in the full operational lifecycle.
        """
        context = context or {}
        req_id = execution_id or f"stbd-{uuid.uuid4().hex[:8]}"
        
        # 1. Ensure services are loaded
        event_bus = registry.get_service("EventBus")
        
        # 2. Initiative / Mission Creation
        initiative_id = f"INIT-{uuid.uuid4().hex[:4].upper()}"
        
        if event_bus and not execution_id:
            try:
                loop = asyncio.get_event_loop()
                event = Event(
                    source="CapabilityService",
                    type=EventType.MISSION_CREATED,
                    execution_id=req_id,
                    node_id="capability_dispatch",
                    payload={"capability": capability_id, "initiative_id": initiative_id}
                )
                if not loop.is_running():
                    loop.run_until_complete(event_bus.publish(event))
                else:
                    asyncio.create_task(event_bus.publish(event))
            except Exception:
                pass
                
        print(f"[{initiative_id}] Dispatched capability {capability_id}")
        
        # 3. Launch specific engines
        result = {}
        
        from raphael_core.legacy import load_config, DEFAULT_SETTINGS_PATH
        config = load_config(DEFAULT_SETTINGS_PATH)
        
        if capability_id == "video.generate":
            from raphael_domains.creator.video_engine import VideoEngine
            from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
            
            store = IdempotencyStore(os.path.join(config.os_root, "idempotency.db"))
            engine = VideoEngine(store, str(config.os_root))
            result = engine.run_pipeline(req_id, context)
            
        elif capability_id == "pod.generate":
            from raphael_core.legacy import pod_pipeline
            result = {"status": "success", "pipeline": pod_pipeline(config)}
            
        elif capability_id == "builder.application":
            from raphael_core.legacy import build_council_plan, create_build_request, make_build_id
            spec = context.get("spec", "")
            build_id = req_id
            if spec:
                try:
                    create_build_request(config, spec)
                    build_id = make_build_id(spec)
                except Exception:
                    pass
            result = {"status": "success", "build": str(build_council_plan(config, build_id))}
        else:
            raise ValueError(f"Unknown capability: {capability_id}")
            
        if event_bus:
            try:
                loop = asyncio.get_event_loop()
                event = Event(
                    source="CapabilityService",
                    type=EventType.WORKFLOW_COMPLETED,
                    execution_id=req_id,
                    node_id="capability_dispatch",
                    payload={"capability": capability_id, "result": result, "initiative_id": initiative_id}
                )
                if not loop.is_running():
                    loop.run_until_complete(event_bus.publish(event))
                else:
                    asyncio.create_task(event_bus.publish(event))
            except Exception:
                pass
                
        return result
