# RRK Agent Contract

This contract governs the design and operation of all Agents within Raphael OS. Any subsystem that introduces autonomous behavior must abide by these invariants.

## Rule 1: Agents Do Not Execute Directly
Agents are cognitive constructs, not execution environments. An agent's reasoning loop must NEVER execute automation directly (e.g., executing Python scripts, making API calls, invoking shell commands). 
Instead, agents form **intentions** and translate them into a `WORKFLOW_REQUESTED` event. The `WorkflowManager` is exclusively responsible for execution.

## Rule 2: Agents Have Strict Identity
An agent is not merely a model and a prompt. Every agent must have a discrete identity composed of:
- **Definition**: The template outlining the agent's role, core capabilities, and base permissions.
- **Instance**: A specific running agent with its own ID, lifecycle state, memory scope, and context.

Agents must not exceed the capabilities or roles defined in their Identity.

## Rule 3: Agents Do Not Own Memory
Agents cannot directly write to, mutate, or delete from the memory index.
Agents only generate cognitive events on the `EventBus`. The `MemoryManager` (acting as the Promotion Gate) evaluates these events and decides whether to persist them to the memory repository.

## Rule 4: Agents Need Permissions
Agent capabilities must be gated by a Permission Service. An agent must hold the explicit permission (e.g., `marketing`, `finance`, `infrastructure`) to request a specific capability. Access attempts beyond these boundaries must emit an `AGENT_PERMISSION_DENIED` event.
