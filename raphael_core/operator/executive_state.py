from typing import Any, Dict, List, Protocol
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import logging
import time

logger = logging.getLogger("operator.executive_state")


class ProducerResult(BaseModel):
    """Metadata and payload for a single producer's contribution to the snapshot."""
    producer_name: str
    version: str = "1.0"
    data: Dict[str, Any] = Field(default_factory=dict)
    success: bool = True
    latency_ms: int = 0
    freshness: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    completeness: float = 1.0
    errors: List[str] = Field(default_factory=list)


class StateCategories(BaseModel):
    """Namespaces for the raw facts collected by producers."""
    system: Dict[str, Any] = Field(default_factory=dict)
    executions: Dict[str, Any] = Field(default_factory=dict)
    initiatives: Dict[str, Any] = Field(default_factory=dict)
    agents: Dict[str, Any] = Field(default_factory=dict)
    councils: Dict[str, Any] = Field(default_factory=dict)
    events: Dict[str, Any] = Field(default_factory=dict)
    kpis: Dict[str, Any] = Field(default_factory=dict)
    finance: Dict[str, Any] = Field(default_factory=dict)
    portfolio: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)


class ExecutiveSnapshot(BaseModel):
    """
    An immutable, versioned snapshot of Raphael's runtime state at a point in time.
    Describes reality (raw facts), without analysis or interpretation.
    """
    snapshot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    version: str = "1.1.0"
    
    # State Quality
    completeness: float = 0.0
    producer_results: List[ProducerResult] = Field(default_factory=list)
    
    # Raw Fact Data
    state: StateCategories = Field(default_factory=StateCategories)


class StateProducer(Protocol):
    """
    Protocol for any subsystem that wants to contribute raw facts to the ExecutiveSnapshot.
    """
    def name(self) -> str:
        """The specific name of this producer (e.g. 'system_health', 'active_workflows')."""
        ...
        
    def category(self) -> str:
        """The StateCategories namespace this producer populates (e.g. 'system', 'executions')."""
        ...
        
    def collect(self) -> ProducerResult:
        """Collects state data, returning a standard ProducerResult wrapper."""
        ...


class ExecutiveStateEngine:
    """
    Aggregates data from registered StateProducers to generate an immutable ExecutiveSnapshot.
    """
    def __init__(self):
        self._producers: List[StateProducer] = []
        
    def register(self, producer: StateProducer) -> None:
        """Register a new producer."""
        self._producers.append(producer)
        logger.info(f"Registered StateProducer: {producer.name()} targeting category {producer.category()}")
        
    def snapshot(self) -> ExecutiveSnapshot:
        """
        Polls all registered producers and generates a new, immutable snapshot of reality.
        """
        categories = StateCategories()
        results: List[ProducerResult] = []
        total_completeness = 0.0
        
        for producer in self._producers:
            start_time = time.time()
            try:
                res = producer.collect()
            except Exception as e:
                logger.error(f"Error collecting from producer {producer.name()}: {e}")
                res = ProducerResult(
                    producer_name=producer.name(),
                    success=False,
                    completeness=0.0,
                    errors=[str(e)]
                )
            
            # Ensure latency is recorded
            if res.latency_ms == 0:
                res.latency_ms = int((time.time() - start_time) * 1000)
                
            results.append(res)
            total_completeness += res.completeness
            
            # Merge data into the target category
            cat_name = producer.category()
            if hasattr(categories, cat_name):
                # Avoid overriding dict if multiple producers target the same category,
                # merge them under the producer's specific name.
                getattr(categories, cat_name)[producer.name()] = res.data
            else:
                logger.warning(f"Producer {producer.name()} specified unknown category {cat_name}")

        overall_completeness = (total_completeness / len(self._producers)) if self._producers else 1.0
        
        return ExecutiveSnapshot(
            completeness=round(overall_completeness, 2),
            producer_results=results,
            state=categories
        )

# Global singleton
executive_state = ExecutiveStateEngine()
executive_state.register(SystemHealthProducer())
executive_state.register(CapabilityProducer())
