# ADR 012: Kernel Sovereignty

**Status:** Accepted
**Date:** 2026-07-15
**Context:** 
Raphael OS has evolved into a kernel-based architecture where `raphael_core` provides foundational operating system primitives and domain applications consume those primitives. 

Previous architecture exploration introduced a parallel `raphael-platform` implementation containing duplicate infrastructure concepts (Event Platform, Policy Engine, World Model, Memory Layer, Capability Runtime, Governance Rules). Although these designs contained valuable domain concepts, duplicating kernel responsibilities creates architectural drift, conflicting sources of truth, and independent governance systems. 

RRK is now the authoritative Raphael kernel.

**Decision:**
All future Raphael domains must run on top of RRK primitives. The dependency direction is strictly: `Applications -> Domain Packages -> RRK Kernel`. The kernel never depends on domain logic.

Domains may contain:
- Domain entities and schemas
- Domain scoring algorithms
- Domain simulations
- Domain-specific capabilities and projections
- Domain knowledge models

**Forbidden Domain Responsibilities:**
Domain packages MUST NOT create infrastructure. Specifically:
- ❌ **EventBus implementations**: All event communication must flow through RRK EventBus governance.
- ❌ **Policy Engine implementations**: Governance must remain centralized.
- ❌ **Memory systems**: Memory lifecycle, indexing, retrieval, and promotion belong to RRK.
- ❌ **World Model implementations**: Reality representation must have one authoritative source.
- ❌ **Agent runtimes**: Agent lifecycle, permissions, and execution belong to RRK.
- ❌ **Constitutions or governance documents**: Raphael has one constitutional authority.
- ❌ **Domain-specific approval mechanisms**: Human approval workflows are kernel responsibilities.
- ❌ **`executor_provider.py`**: External execution reliability is a kernel primitive. Domains must request execution through RRK's execution infrastructure.
- ❌ **`idempotency_store.py`**: Idempotent execution guarantees must exist once at the kernel level. Duplicating retry and recovery logic across domains will recreate the reliability failures already solved by the Reliability Sprint.

**General Rule (beyond this enumerated list):**
Any module that provides cross-cutting infrastructure — persistence, governance, scheduling, retry semantics, access control, or reality representation — belongs to the kernel by default, regardless of whether it appears explicitly in this list. 
When in doubt: if a proposed domain module would still make sense to exist even if the domain were deleted entirely, it is kernel infrastructure, not domain logic, and belongs in `raphael_core/kernel/`.

**Consequences:**
- **Positive**: One kernel, one constitution, one event system, one policy layer, one reliability layer, multiple domain applications.
- **Negative**: Domains require more discipline. Domain development depends on stable kernel APIs.

### Appendix: Query Contract for Domain Packages

Domains querying the World Model for a KNOWN entity's KNOWN 
relationship type (e.g. "what skills does person X have") MUST 
use `world_model.related(node_id)` or a scoped traversal function, 
never the free-text `query()` path.

The free-text `query()` endpoint is reserved for genuine open-ended 
discovery questions where the relevant `node_id` and relationship 
type are not yet known.

Violating this will silently degrade to keyword-matching behavior 
and miss real graph data, as demonstrated in the Career domain 
validation test (2026-07-15).
