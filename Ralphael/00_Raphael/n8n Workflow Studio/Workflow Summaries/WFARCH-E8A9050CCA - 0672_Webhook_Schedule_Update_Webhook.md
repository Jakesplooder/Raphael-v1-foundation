# Archived n8n Workflow WFARCH-E8A9050CCA

## Workflow ID

WFARCH-E8A9050CCA

## Name

0672_Webhook_Schedule_Update_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0672_Webhook_Schedule_Update_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 34
- Connections: 29
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainRetrievalQa`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.retrieverVectorStore`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `@n8n/n8n-nodes-langchain.vectorStoreInMemory`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.n8n`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Chain Retrieval Qa
- Embeddings Open Ai
- Http Request
- If
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- N8N
- No Op
- Respond To Webhook
- Retriever Vector Store
- Schedule Trigger
- Split In Batches
- Sticky Note
- Switch
- Tool Http Request
- Vector Store In Memory
- Webhook

## Required Credentials

- n8nApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
