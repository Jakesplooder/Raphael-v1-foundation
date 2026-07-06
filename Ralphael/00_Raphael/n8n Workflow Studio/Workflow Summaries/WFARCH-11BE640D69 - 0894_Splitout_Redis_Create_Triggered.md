# Archived n8n Workflow WFARCH-11BE640D69

## Workflow ID

WFARCH-11BE640D69

## Name

0894_Splitout_Redis_Create_Triggered

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0894_Splitout_Redis_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 46
- Connections: 36
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.mcpClientTool`
- `@n8n/n8n-nodes-langchain.mcpTrigger`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.if`
- `n8n-nodes-base.n8n`
- `n8n-nodes-base.redis`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Agent
- Aggregate
- Chat Trigger
- Execute Workflow
- Execute Workflow Trigger
- Filter
- If
- Lm Chat Open Ai
- Mcp Client Tool
- Mcp Trigger
- Memory Buffer Window
- N8N
- Redis
- Set
- Split Out
- Sticky Note
- Switch
- Tool Workflow

## Required Credentials

- n8nApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- redis (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Agency
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
