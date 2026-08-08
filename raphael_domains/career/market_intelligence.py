from typing import Dict, Any, List
import uuid
import time
import logging

from raphael_core.kernel.interfaces import Event, EventType
from raphael_core.kernel.event_bus import emit
from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore

logger = logging.getLogger("career.market_intelligence")

def fetch_market_signals(signal_query: str, idempotency_key: str = None) -> List[Dict[str, Any]]:
    """
    Fetches external market signals (e.g. from an API).
    Wrapped with IdempotencyStore to prevent duplicate ingestion.
    Emits MARKET_SIGNAL_ACQUIRED events to write to the World Model.
    """
    store = IdempotencyStore()
    
    if not idempotency_key:
        idempotency_key = f"fetch_market_{hash(signal_query)}"
        
    existing = store.get(idempotency_key)
    if existing:
        logger.info(f"[IDEMPOTENCY] Market signal fetch for {signal_query} already processed.")
        return existing
        
    try:
        # Simulate external API call
        time.sleep(0.5) 
        
        # Mock payload
        signals = [
            {"signal_type": "demand_increase", "content": "Containerization skills demand up 18%", "role": "Cloud Engineer"}
        ]
        
        # Emit events for each signal
        for sig in signals:
            event = Event(
                source="market_intelligence",
                type=EventType.MARKET_SIGNAL_ACQUIRED,
                payload=sig
            )
            emit(event.type, "market_intelligence", event.payload)
            
        # Store result for idempotency
        store.set(idempotency_key, signals)
        
        return signals
    except Exception as e:
        # In a real system, we might use ExecutorProvider for retries
        logger.error(f"Error fetching signals: {e}")
        raise
