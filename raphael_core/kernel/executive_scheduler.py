import asyncio
import logging
from raphael_core.operator.executive_state import executive_state
from raphael_core.operator.executive_analysis import executive_analyzer
from raphael_core.operator.presentation_adapters.dashboard_adapter import dashboard_adapter
from raphael_core.kernel.event_bus import global_event_bus

logger = logging.getLogger("kernel.scheduler")

class ExecutiveScheduler:
    """
    D13-C: The continuous Executive Control Loop.
    A purely orchestrating loop that generates state, analysis, and presentation 
    viewmodels, publishing them to the event bus and UI. Contains zero business logic.
    """
    def __init__(self, interval_seconds: int = 60):
        self.interval_seconds = interval_seconds
        self._running = False
        self._task = None
        
    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._loop())
            logger.info("Executive Scheduler started.")
            
    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            logger.info("Executive Scheduler stopped.")
            
    async def _loop(self):
        while self._running:
            try:
                # 1. Generate Reality Snapshot
                snapshot = executive_state.snapshot()
                
                # 2. Analyze Reality
                analysis = executive_analyzer.analyze(snapshot)
                
                # 3. Generate ViewModels
                dashboard_view = dashboard_adapter.adapt(analysis)
                
                # 4. Publish (e.g. to websockets or event bus)
                # In D13-C, we emit a high-level event so listeners (like the UI or Discord bot)
                # can broadcast the updated DashboardViewModel.
                from raphael_core.kernel.event_bus import emit
                emit("EXECUTIVE_TICK", "executive_scheduler", dashboard_view.model_dump())
                
                logger.debug(f"Executive tick complete. Snapshot ID: {snapshot.snapshot_id}")
                
            except Exception as e:
                logger.error(f"Error in Executive Scheduler loop: {e}")
                
            # 5. Sleep
            await asyncio.sleep(self.interval_seconds)

# Global singleton
executive_scheduler = ExecutiveScheduler()
