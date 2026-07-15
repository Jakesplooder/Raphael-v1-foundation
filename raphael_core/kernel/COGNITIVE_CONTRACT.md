# RRK Cognitive Contract

This document defines the unyielding architectural rules that all domains must follow as Raphael transitions into a fully native Cognitive Operating System. Violation of these principles will result in architectural decay and memory pollution.

## Rule 1: No Direct Domain Mutation
**No domain directly modifies another domain.**
- **Wrong**: `KnowledgeManager` calls `MemoryManager.write()`
- **Correct**: `KnowledgeManager` publishes `KNOWLEDGE_CREATED` to the `EventBus`. `MemoryManager` evaluates the event independently.
- Communication between distinct cognitive domains (Memory, Knowledge, Goals, Agents, World Model) MUST occur through asynchronous events on the Hybrid Event Bus.

## Rule 2: Strict Layer Responsibility
The `Manager -> Service -> Repository -> Provider` architecture must remain pure:
- **Managers orchestrate**: They subscribe to events, publish events, expose endpoints, and connect the domain to the rest of the OS. They contain NO business logic.
- **Services reason**: They contain all business logic, taxonomy rules, heuristics, and domain-specific intelligence.
- **Repositories store**: They strictly handle physical I/O (Database, Vector Index, File System). They contain NO intelligence.
- **Providers connect**: They abstract external capabilities (LLMs, API clients, Text Extractors).

## Rule 3: Memory is Earned
**Nothing enters memory automatically.**
- Memory is experiential and behavioral, not a dump for logs or files.
- Memory must be promoted through a **Promotion Gate**.
- Examples: 
  - A basic README generation does NOT enter memory. 
  - A failed business experiment with high CAC DOES enter memory.
  - A `STRATEGIC` knowledge document DOES enter memory.

## Rule 4: The World Model Owns Reality
**Agents do not own truth. The World Model owns reality.**
- Agents are transient operators with limited perspectives.
- The World Model maintains the absolute state of external reality, entities, relationships, and context.
- When conflicts arise between an Agent's perception and the World Model, the World Model wins.
