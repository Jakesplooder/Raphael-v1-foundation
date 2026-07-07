import logging
import time
from typing import Any, Dict, Optional
import uuid

# Set up a central logger for the RRK
_logger = logging.getLogger("RRK")
_logger.setLevel(logging.DEBUG)

# In production, this would route to a sophisticated backend (e.g., ELK, Datadog, or SQLite logs)
# For now, we use a rich console handler if available, else standard stream.
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [Trace: %(trace_id)s] [%(source)s] %(message)s")
handler.setFormatter(formatter)
_logger.addHandler(handler)


class ObservabilityLayer:
    """
    First-class Observability System for the Raphael Runtime Kernel.
    Modules must use this instead of the standard `logging` module.
    """

    @classmethod
    def emit_log(cls, level: int, source: str, message: str, trace_id: Optional[str] = None, **kwargs: Any) -> None:
        """Centralized logging emitter."""
        if not trace_id:
            trace_id = "00000000-0000-0000-0000-000000000000"
        
        extra = {"trace_id": trace_id, "source": source}
        
        # Combine message with extra kwargs
        if kwargs:
            message = f"{message} | {kwargs}"
            
        _logger.log(level, message, extra=extra)

    @classmethod
    def info(cls, source: str, message: str, trace_id: Optional[str] = None, **kwargs: Any) -> None:
        cls.emit_log(logging.INFO, source, message, trace_id, **kwargs)

    @classmethod
    def debug(cls, source: str, message: str, trace_id: Optional[str] = None, **kwargs: Any) -> None:
        cls.emit_log(logging.DEBUG, source, message, trace_id, **kwargs)

    @classmethod
    def warning(cls, source: str, message: str, trace_id: Optional[str] = None, **kwargs: Any) -> None:
        cls.emit_log(logging.WARNING, source, message, trace_id, **kwargs)

    @classmethod
    def error(cls, source: str, message: str, trace_id: Optional[str] = None, exc_info: bool = False, **kwargs: Any) -> None:
        cls.emit_log(logging.ERROR, source, message, trace_id, **kwargs)

    @classmethod
    def record_metric(cls, source: str, metric_name: str, value: float, trace_id: Optional[str] = None) -> None:
        """
        Record a numerical metric.
        In a full implementation, this routes to a time-series DB (like Prometheus or Qdrant for RRK).
        """
        cls.info(source, f"Metric [{metric_name}]: {value}", trace_id)

    @classmethod
    def time_execution(cls, source: str, operation: str, trace_id: Optional[str] = None):
        """Context manager/decorator utility for timing."""
        class TimerContext:
            def __enter__(self):
                self.start = time.time()
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                duration = time.time() - self.start
                cls.info(source, f"Timing [{operation}]: {duration:.4f}s", trace_id)
        
        return TimerContext()
