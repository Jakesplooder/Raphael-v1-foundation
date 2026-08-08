from typing import Dict, Any, List
from collections import Counter
from .executive_state import StateProducer, ProducerResult

class EventProducer(StateProducer):
    """
    Produces structured summaries of recent events from the Event Fabric.
    """
    def __init__(self):
        pass
        
    def name(self) -> str:
        return "events"
        
    def category(self) -> str:
        return "events"
        
    def collect(self) -> ProducerResult:
        try:
            from raphael_core.kernel.event_bus import global_event_bus
            
            raw_events = global_event_bus.get_recent_events()
            
            # Tally event types
            counts = Counter()
            for ev in raw_events:
                # _recent_events stores dictionaries
                ev_type = ev.get("type", "UNKNOWN")
                counts[ev_type] += 1
                
            # Grab the last 10 for 'recent' slice
            recent_slice = raw_events[-10:] if raw_events else []
            last_event = raw_events[-1] if raw_events else None
            
            data = {
                "recent": recent_slice,
                "counts": dict(counts),
                "last_event": last_event,
                "total_recent_tracked": len(raw_events)
            }
            
            return ProducerResult(
                producer_name=self.name(),
                success=True,
                data=data,
                completeness=1.0
            )
        except Exception as e:
            return ProducerResult(
                producer_name=self.name(),
                success=False,
                data={},
                completeness=0.0,
                errors=[f"Failed to collect events: {str(e)}"]
            )
