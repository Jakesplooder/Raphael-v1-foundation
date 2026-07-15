# ADR-013: Stabilization Before Expansion

**Date**: 2026-07-07  
**Status**: Accepted  

## Context
During the Epic C architectural restoration of Raphael OS, the migration to the Runtime Kernel (RRK) and API Gateway inadvertently disconnected the core command pipeline. The frontend chat UI no longer dispatches requests to the Command Bus, Intent Router, Builder, World Model, or external integrations (ComfyUI, Ollama, etc.).

Furthermore, integration points like Qdrant exhibit connectivity issues due to Docker hostname mismatches (e.g., using `localhost` instead of `qdrant` within the containerized network).

Because the entire OS relies on this centralized routing and execution pipeline, new feature development must be paused. We must prioritize system stability and integration parity.

## Constitution

1. **Rule 1: No New Epics Until Regression Count is Zero**
   We will not expand Raphael's capabilities until the core foundation is demonstrably stable.
2. **Rule 2: Every Migrated Subsystem Must Pass Feature Parity**
   All systems migrated to RRK or the API Gateway must function identically to their pre-migration state.
3. **Rule 3: Every Previous Feature Must Still Function**
   The Command Bus, Intent Router, Search, Builder Engine, ComfyUI, Docker, and Qdrant connections must be fully operational.
4. **Rule 4: The Command Pipeline is the Highest Priority**
   The `/api/chat` dispatching mechanism must be reconnected to the Intent Router and command execution paths immediately.
5. **Rule 5: Dashboard Parity Before UI Redesign**
   The Classic View and Matrix View must achieve 100% data and action parity before introducing Workspace Managers or Activity Bars.
6. **Rule 6: RRK Parity Before New Runtime Features**
   The Runtime Kernel must faithfully replicate legacy data parsing and event handling before adding novel AI agent workflows.

## Epic D — System Stabilization & Feature Parity

Success criteria for this stabilization sprint:
- Every command in the chat routes correctly.
- Qdrant responds through the API Gateway.
- Builder works end-to-end.
- Search works end-to-end.
- ComfyUI works end-to-end.
- The Classic and Matrix views render correctly.
- There are zero "No response" or "unknown" results for supported commands.
