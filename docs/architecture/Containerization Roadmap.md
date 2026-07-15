# Long-Term Containerization Vision and Roadmap (Raphael Architecture Version 1.0)

Given the current state of RaphaelOS, the ultimate north star is an autonomous AI operating system running on a service-oriented microservice architecture with sensible, strict boundaries.
**The host OS only provides hardware, files, GPU access, and Docker. Everything else runs in containers.**

*Crucial Guideline: Containerize by architectural boundaries, not by class or module. If every subsystem becomes its own container too early, more time will be spent managing networking, deployment, and versioning than building intelligence.*

## Semantic Versioning Roadmap

We treat RaphaelOS like a true operating system. Phases are implementation history; Versions are release history.

- **v1.0**: Foundation (Core infrastructure, RRK, Dashboard, RAG, World Model, Nginx)
- **v1.5**: Executive Intelligence (Executive Board, Reasoning, Strategic Planning)
- **v2.0**: Runtime Kernel (RRK hard-boundary separation, Service Mesh, Workflow)
- **v2.5**: Microservices (Containerized intelligence, Orchestrator, Registries)
- **v3.0**: Autonomous Workforce (Independent agent runtimes with shared skills)
- **v4.0**: Self-Improving Operating System (Evolution, optimization, autonomous learning)

## The Four Brains
Over the long term, Raphael's intelligence maps into four domains:
1. **Knowledge Brain** (What do I know?) -> RAG, Search, World Model, Memory.
2. **Reasoning Brain** (What does it mean?) -> Reasoning Engine, Patterns, Simulation.
3. **Executive Brain** (What should I do?) -> Executive Board, Planning, Prediction.
4. **Operational Brain** (How do I execute it?) -> RRK, Workflow, Agents, Skills.

## System Topology & Organization

### 1. Infrastructure Layer
- **`raphael-rrk`**: The strict Kernel. Operates invisibly. Owns Scheduler, Job Queue, Event Bus, Health, Registry, Recovery, and Runtime State. (Never knows about LLMs, Builder, etc. - behaves like a Linux Kernel).
- **`raphael-api-gateway`**: REST API, Command API, Websocket API, Gateway.
- **`raphael-service-mesh`**: Internal DNS and routing (Traefik/Envoy/Linkerd).
- **`raphael-identity`**: Authentication, Authorization, RBAC, Permissions, API Keys, Tokens.
- **`raphael-observability`**: Prometheus, Grafana, Loki, Tempo, OpenTelemetry. The nervous system tracing every agent, job, event, and LLM call.
- **`raphael-workflow`**: Raphael's own workflow engine for multi-agent orchestration, rollback, and retries.
- **`raphael-model-gateway`**: Central routing hub for all LLM calls. Handles routing, caching, consensus, retries, and budget.

### 2. Knowledge Layer
- **`raphael-rag` (Knowledge)**: Retrieval-Augmented Generation infrastructure. Vault indexing, OCR, Chunking, Embeddings, Citation Engine, Document Search. *Stores documents.*
- **`raphael-search`**: Semantic Search, Keyword Search, Hybrid Search.
- **`raphael-world-model`**: Stores relationships, causal graphs, ontology, and the memory graph. *Stores relationships.*
- **`raphael-memory`**: Long-Term Memory, Short-Term Context, Institutional Memory.

### 3. Intelligence Layer
- **`raphael-executive`**: Executive Board, Strategic Planner, Decision Engine.
- **`raphael-reasoning`**: Reasoning Engine, Consensus Engine.
- **`raphael-planning`**: Task planning and breakdown.
- **`raphael-prediction`**: Forecast Engine, Prediction History.
- **`raphael-patterns`**: Pattern Discovery.

### 4. Skills Layer (The Execution Bridge)
Sits between Intelligence and Agents. Agents do not implement actions directly; they invoke shared skills.
- **`raphael-skill-registry`**: The central nervous system for capabilities. Every callable skill is discoverable (Version, Inputs, Outputs, Permissions, Dependencies, Latency, Cost, Provider, Health).
- **Shared Skills**: Code Skill, Docker Skill, Git Skill, Testing Skill, Deployment Skill, Tool Skill.

### 5. Agent Layer
Every agent is structurally identical (Identity, State, Memory, Capabilities, Skills, Reasoning, Planning, Execution, Reflection, Metrics) but differs in prompts, permissions, and available skills. They communicate ONLY through the RRK event bus/mesh.
- `raphael-agent-builder`
- `raphael-agent-developer`
- `raphael-agent-ceo`
- `raphael-agent-coo`
- `raphael-agent-research`
- `raphael-agent-marketing`

### 6. Storage Layer
- **`postgres`**, **`redis`**, **`neo4j`**, **`qdrant`**, **`minio`**

### 7. Platform Layer
- **`docker`**
- **`raphael-orchestrator`**: The brain that manages Docker natively. Deploys, restarts, updates containers, monitors resources.
- **`raphael-registry`**: Container registry where Raphael builds and pushes deployable services automatically.
- **`raphael-architecture`**: Architecture registry storing system topology, dependencies, ADRs, service contracts, and container maps. Allows Raphael to inspect and answer questions about its own architecture.

### 8. Future / Evolution Layer
- **`raphael-evolution`**: Raphael's "learning" subsystem owning benchmarking, code improvement, prompt evolution, and knowledge refinement.
- **`raphael-optimization`**: Optimization Engine.
- **`raphael-autonomous-learning`**: Autonomous Learning.

## Governance
This architecture is frozen as **Version 1.0**. The focus now shifts entirely to implementation, writing integration tests, and executing the roadmap. Future architectural tweaks should only amend ADR-011 rather than rewriting it.
