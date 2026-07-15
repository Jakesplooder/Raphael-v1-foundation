# ADR-012: Command Center UX & Design Constitution

**Date**: 2026-07-07  
**Status**: Accepted  

## Context
During the Epic C architectural restoration of Raphael OS, the frontend dashboard was initially modernized into a generic React administration panel. This inadvertently discarded the core aesthetic and dense operating environment of the original Raphael Matrix Command Center. 

Raphael OS is not an analytics dashboard; it is an AI Operating System. The user experience and interface design must reflect this distinction.

## UX Constitution

1. **Rule 1: Desktop Environment**
   The Command Center is the desktop environment of Raphael OS. It must feel like an operating system (mission control, SOC dashboard, Bloomberg Terminal) rather than a website.
2. **Rule 2: Information Density**
   Dense information layout is required. Avoid generic SaaS layouts, oversized cards, and excessive whitespace.
3. **Rule 3: Permanent Identity & Navigation**
   The left sidebar is persistent and strictly structured around OS modules (Executive, Agency, Commerce, Builder, Projects, Goals, Tasks, Resource Allocation, Business Blueprints, Simulations).
4. **Rule 4: Persistent Intelligence**
   The right intelligence sidebar must constantly display live executive summaries, recommendations, active predictions, and authority requests.
5. **Rule 5: Three Operating Modes**
   - **Classic**: High-density operational view.
   - **Matrix**: Topological graph visualization for relationships and architecture.
   - **Focus**: Single-workspace takeover mode.
6. **Rule 6: Backward Compatibility**
   Until the Runtime Kernel (RRK) reaches feature parity with the legacy dashboard, Raphael SHALL preserve the complete Classic View experience through compatibility adapters. Compatibility adapters are temporary migration infrastructure and SHALL NOT become permanent business logic services.
7. **Rule 7: Bottom Command Console**
   The bottom console is a constitutional requirement. It must support multiple tabs, CLI, natural language, Builder, Docker, RRK, and streaming output.
8. **Rule 8: Pixel Compatibility**
   The purpose of the Compatibility Adapter is to reproduce the original Classic View with exact visual fidelity (identical layout, navigation, panels, workflows).

## Sunset Clause

The Legacy Compatibility Adapter exists solely to preserve the Classic View during migration. It must be progressively reduced and eventually deleted. 
Every time an RRK native feature achieves parity with a legacy feature, the corresponding responsibility is removed from the adapter. When the adapter reaches zero responsibilities, `legacy_adapter.py` will be permanently deleted.

### Feature Parity Checklist
**Legacy Adapter Responsibilities:**
- [x] Identity
- [x] Goals
- [x] Tasks
- [x] Projects
- [x] Builder
- [x] Memory
- [x] Commerce
- [x] Agency
- [x] Resource Allocation
- [x] Business Blueprints
- [x] World Model
- [x] Executive
- [x] Prediction
- [x] Pattern Discovery
- [x] Simulations

**RRK Native Parity (To Be Checked):**
- [ ] Identity
- [ ] Goals
- [ ] Tasks
- [ ] Projects
- [ ] Builder
- [ ] Memory
- [ ] Commerce
- [ ] Agency
- [ ] Resource Allocation
- [ ] Business Blueprints
- [ ] World Model
- [ ] Executive
- [ ] Prediction
- [ ] Pattern Discovery
- [ ] Simulations

## Translator Conventions

To prevent the compatibility translators from growing into a permanent shadow-architecture, the following conventions MUST be adhered to:

1. **No Business Logic**: Translators are purely for data transformation between the Legacy schema and the RRK native schema. They are strictly prohibited from embedding, executing, or managing business logic.
2. **Strict Ownership**: Every translator MUST declare an owner (the RRK Subsystem it translates for) and a target retirement milestone (Epic D).
3. **Immutability of Source**: Translators MUST NOT attempt to patch or fix legacy application logic. If the legacy code is broken, it stays broken or is ported to RRK natively.
4. **Visibility**: Translators must log deprecation warnings when invoked to ensure visibility on lingering legacy dependencies.
