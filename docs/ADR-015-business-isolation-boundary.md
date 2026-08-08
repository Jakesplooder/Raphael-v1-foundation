# ADR-015: Business Isolation Boundary

## Status
Accepted

## Context
Phase 9 introduces multiple businesses into Raphael OS under `raphael_domains/` (e.g., `creator`, `commerce`, `agency`). If businesses begin implementing their own foundational logic, the architecture will fracture, leading to unmaintainable code, redundant systems, and unsafe intelligence silos.

## Decision
We establish the **Business Isolation Boundary**. Every business domain may implement its own:
- `business_twin.py`
- `strategy_engine.py`
- `mission_types.py`
- `analytics.py`

However, businesses are strictly **forbidden** from owning or implementing kernel-level infrastructure. A business may **not**:
- ❌ Own its own EventBus
- ❌ Own its own Memory
- ❌ Own its own ApprovalManager
- ❌ Own its own Economy/Financial layer
- ❌ Own its own IncidentManager

All of these capabilities must be centralized in the `raphael_core/kernel/` and exposed to the domains as services or via the EventBus.

## Consequences
- Guarantees uniform governance and auditing across the entire portfolio.
- Simplifies domain implementation, as domains only focus on their specific business logic and strategies.
- Eliminates fragmented learning; the Kernel captures all cross-domain incidents and financial events in a standardized way.
