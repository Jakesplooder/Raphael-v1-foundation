# Archived n8n Workflow WFARCH-FEAFD39D6B

## Workflow ID

WFARCH-FEAFD39D6B

## Name

Adaptive RAG

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1829_Summarize_Respondtowebhook_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 39
- Connections: 32
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Agent
- Chat Trigger
- Embeddings Google Gemini
- Execute Workflow Trigger
- Lm Chat Google Gemini
- Memory Buffer Window
- Respond To Webhook
- Set
- Sticky Note
- Summarize
- Switch
- Vector Store Qdrant

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)

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
