# ADR 011: Long-Term Microservice Architecture (Version 1.0)

## Context
As RaphaelOS evolves from a monolithic Python codebase and basic daemon into an autonomous AI operating system, it requires a robust, scalable, and resilient architecture. A naive approach of "containerizing everything immediately" risks creating a distributed monolith with immense networking and orchestration overhead. We need a stable, long-term architectural "North Star" defined by strict service boundaries to guide incremental development.

This document serves as the constitutional foundation (Version 1.0) for Raphael's architecture. Future epics must implement this vision; future architectural changes should only amend this document rather than rewriting it.

## Decision
We will transition to a service-oriented microservice architecture organized across distinct functional layers mapping to Four Domains (Knowledge, Reasoning, Executive, Operational).

1. **Infrastructure**: RRK (strict kernel operations only), Service Mesh (Traefik/Envoy), API Gateway, Identity, Observability, Workflow Engine, and a dedicated Model Gateway.
2. **Knowledge Layer**: RAG (document ingestion/chunking), Search, World Model (relationships/causal graphs), and Memory.
3. **Intelligence Layer**: Executive, Reasoning, Planning, Prediction, Patterns, Simulation.
4. **Skills Layer**: A dedicated registry (`raphael-skill-registry`) where shared capabilities (Git, Docker, Code, Testing) are managed, versioned, and made discoverable.
5. **Agent Layer**: Independent runtimes for specialized agents (Builder, Developer, CEO, COO, etc.). Every agent is structurally identical (Identity, State, Memory, Capabilities, Skills, Reasoning, Planning, Execution, Reflection, Metrics) and relies on the Skills Layer to act. They communicate exclusively through the RRK event bus/mesh.
6. **Storage Layer**: Postgres, Redis, Neo4j, Qdrant, MinIO.
7. **Platform Layer**: Orchestrator (managing Docker natively), Architecture Registry (for self-inspection and topology graphing), Container Registry, and external integrations.
8. **Evolution Layer**: Long-term self-improvement, autonomous learning, and optimization engines.

### Key Architectural Rules:
- **RRK Strict Boundaries**: RRK acts purely as an invisible kernel (Scheduler, Event Bus, Health, Recovery). It must never possess knowledge of LLMs, Builders, or specific agents. 
- **Model Gateway**: All LLM calls route through a single `raphael-model-gateway` which handles provider routing, caching, and budget. Agents never call providers directly.
- **Skills Over Hardcoding**: Agents do not directly implement tools; they invoke centralized, shared capabilities from the Skill Registry.
- **Internal Service Mesh**: Containers communicate via internal DNS and service mesh routing.
- **API Contracts**: Every service exposes its capabilities via OpenAPI/JSON Schema so the system is self-inspectable (via `raphael-architecture`).
- **Decoupled Data**: RAG exclusively handles document storage and embeddings; World Model exclusively handles relationships, causality, and ontology.
- **Semantic Versioning**: Raphael OS will be versioned conceptually (v1.0 Foundation -> v4.0 Self Improving OS) rather than by mere phase implementation.

## Consequences
- **Positive**: Provides a highly stable, enterprise-ready constitutional target for all future development. Prevents architectural churn. Allows independent scaling, swappable components, and massive code reuse via the Skills Layer. Architecture Registry allows the OS to introspect and answer questions about its own design.
- **Negative**: Increases operational complexity. Requires disciplined adherence to interface contracts, strict agent structural conformity, and message passing rather than direct function calls.
