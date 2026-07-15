import json
import logging
import os
import time
from typing import Dict, Any

logger = logging.getLogger("rrk.services.telemetry")

class TelemetryService:
    """
    Global Telemetry Service.
    Intercepts system events and writes them to a JSONL trace file for high-fidelity observability.
    """
    def __init__(self, trace_file: str = ".system_generated/traces.jsonl"):
        os.makedirs(os.path.dirname(trace_file), exist_ok=True)
        self.trace_file = trace_file

    async def log_event(self, event_type: str, payload: Dict[str, Any], event_timestamp: float = None):
        """
        Logs a structured event to the trace file.
        """
        import datetime
        if event_timestamp:
            ts_str = datetime.datetime.fromtimestamp(event_timestamp, tz=datetime.timezone.utc).isoformat()
        else:
            ts_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
        trace = {
            "timestamp": ts_str,
            "event_type": event_type,
            "payload": payload
        }
        
        try:
            with open(self.trace_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(trace) + "\n")
        except Exception as e:
            logger.error(f"Failed to write telemetry trace: {e}")
            
    # Mocking an event bus subscriber callback
    async def on_event(self, event_type: str, payload: Dict[str, Any]):
        await self.log_event(event_type, payload)
