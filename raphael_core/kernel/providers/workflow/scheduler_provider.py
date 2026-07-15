import asyncio
import logging
from typing import Dict, Callable, Awaitable

logger = logging.getLogger("rrk.workflow.scheduler")

class SchedulerProvider:
    """
    Manages an isolated asyncio task pool for queueing and triggering workflows.
    Does NOT rely on a kernel-wide cron daemon.
    """
    def __init__(self):
        self._tasks: Dict[str, asyncio.Task] = {}
        self._execution_callbacks: Dict[str, Callable[[str], Awaitable[None]]] = {}

    def register_callback(self, name: str, callback: Callable[[str], Awaitable[None]]):
        """Register the workflow execution callback."""
        self._execution_callbacks[name] = callback

    def schedule_execution(self, execution_id: str):
        """
        Schedules a workflow execution asynchronously.
        """
        if "default" not in self._execution_callbacks:
            logger.error("No default callback registered for scheduler.")
            return

        callback = self._execution_callbacks["default"]
        task = asyncio.create_task(self._run_execution(execution_id, callback))
        self._tasks[execution_id] = task

    async def _run_execution(self, execution_id: str, callback: Callable[[str], Awaitable[None]]):
        try:
            await callback(execution_id)
        except Exception as e:
            logger.error(f"Execution {execution_id} failed abruptly: {e}")
        finally:
            self._tasks.pop(execution_id, None)

    def cancel_execution(self, execution_id: str):
        """Cancels a scheduled or running execution."""
        if execution_id in self._tasks:
            self._tasks[execution_id].cancel()
            self._tasks.pop(execution_id, None)
            logger.info(f"Execution {execution_id} cancelled by scheduler.")
