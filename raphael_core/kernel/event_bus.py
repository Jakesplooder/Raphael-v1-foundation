import asyncio
import sqlite3
import json
import os
from typing import Callable, Coroutine, Dict, List, Any
from collections import defaultdict

from .interfaces import ServiceModule, Event, ModuleHealth
from .observability import ObservabilityLayer
from .state import store

EventHandler = Callable[[Event], Coroutine[Any, Any, None]]

class EventBus(ServiceModule):
    """
    80.1 Event Bus (Hybrid Durability)
    Routes events asynchronously. Volatile events use memory, Durable use SQLite.
    """
    
    def __init__(self):
        self._subscribers: Dict[str, List[EventHandler]] = defaultdict(list)
        self._wildcard_subscribers: List[EventHandler] = []
        self._volatile_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._worker_task = None
        self._db_path = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", "."), "kernel_events.db")
        self._conn = None
        
    @property
    def name(self) -> str:
        return "EventBus"

    @property
    def depends_on(self) -> list[str]:
        return []

    async def initialize(self) -> None:
        """One-time setup for the durable SQLite store."""
        import asyncio
        self._loop = asyncio.get_running_loop()
        ObservabilityLayer.info(self.name, f"Initializing EventBus DB at {self._db_path}")
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.execute('''
            CREATE TABLE IF NOT EXISTS durable_events (
                id TEXT PRIMARY KEY,
                timestamp REAL,
                trace_id TEXT,
                source TEXT,
                target TEXT,
                type TEXT,
                priority INTEGER,
                payload TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        self._conn.commit()
        store.set_state(self.name, "status", "initialized")

    async def start(self) -> None:
        self._running = True
        self._worker_task = asyncio.create_task(self._event_loop())
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "EventBus started.")

    async def heartbeat(self) -> bool:
        # Check if the DB is still responsive and loop is running
        if not self._running or self._worker_task is None or self._worker_task.done():
            return False
        try:
            self._conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    async def stop(self) -> None:
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        store.set_state(self.name, "status", "stopped")

    async def shutdown(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "EventBus shut down.")

    def health(self) -> ModuleHealth:
        if self._running and self._conn:
            return ModuleHealth.OK
        if self._conn is None:
            return ModuleHealth.FAILED
        return ModuleHealth.DEGRADED

    def status(self) -> str:
        qsize = self._volatile_queue.qsize()
        return f"Running. Queue size: {qsize}"

    def metrics(self) -> Dict[str, Any]:
        return {
            "queue_size": self._volatile_queue.qsize(),
            "subscribers": sum(len(handlers) for handlers in self._subscribers.values())
        }

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type == "*":
            self._wildcard_subscribers.append(handler)
            ObservabilityLayer.debug(self.name, "Subscribed wildcard handler")
        else:
            self._subscribers[event_type].append(handler)
            ObservabilityLayer.debug(self.name, f"Subscribed handler to {event_type}")

    async def publish(self, event: Event) -> None:
        """Publish an event to the bus."""
        import logging
        logger = logging.getLogger("event_bus_publish")
        logger.debug(f"EventBus publish called for {event.type}. Queue id: {id(self._volatile_queue)}")
        ObservabilityLayer.debug(
            self.name, 
            f"Publishing event {event.type} from {event.source}",
            trace_id=event.trace_id
        )
        
        if event.is_durable:
            self._persist_durable_event(event)
            
        if hasattr(self, '_loop') and self._loop is not None:
            self._loop.call_soon_threadsafe(self._volatile_queue.put_nowait, event)
        else:
            self._volatile_queue.put_nowait(event)

    def _persist_durable_event(self, event: Event) -> None:
        if not self._conn:
            ObservabilityLayer.error(self.name, "Failed to persist durable event: EventBus DB connection is None", trace_id=event.trace_id)
            return
        try:
            self._conn.execute(
                "INSERT INTO durable_events (id, timestamp, trace_id, source, target, type, priority, payload) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (event.id, event.timestamp, event.trace_id, event.source, event.target or "", event.type.value, event.priority.value, json.dumps(event.payload))
            )
            self._conn.commit()
        except Exception as e:
            ObservabilityLayer.error(self.name, f"Failed to persist durable event: {e}", trace_id=event.trace_id)

    async def _event_loop(self) -> None:
        """Background task that pulls events from the volatile queue and dispatches them."""
        import logging
        logger = logging.getLogger("event_bus_loop")
        logger.debug(f"EventBus _event_loop started. Queue id: {id(self._volatile_queue)}")
        while self._running:
            try:
                event = await self._volatile_queue.get()
                logger.debug(f"EventBus pulled event: {event.type} from queue {id(self._volatile_queue)}")
                handlers = self._subscribers.get(event.type, [])
                logger.debug(f"EventBus found handlers for {event.type}: {len(handlers)}")
                
                # In a massive system, we'd use asyncio.gather for parallel dispatch,
                # but we'll do simple iteration for predictability in v1
                all_handlers = handlers + self._wildcard_subscribers
                for handler in all_handlers:
                    try:
                        await handler(event)
                    except Exception as e:
                        ObservabilityLayer.error(self.name, f"Handler failed for event {event.type}: {e}", trace_id=event.trace_id)
                        
                # If durable, mark processed
                if event.is_durable:
                    self._conn.execute("UPDATE durable_events SET status = 'processed' WHERE id = ?", (event.id,))
                    self._conn.commit()
                    
                self._volatile_queue.task_done()
            except Exception as e:
                ObservabilityLayer.error(self.name, f"Event loop error: {e}")
                await asyncio.sleep(1)

global_event_bus = EventBus()

def emit(type_str: str, source: str, payload: dict):
    print(f"EVENT: {type_str} from {source}: {payload}")


