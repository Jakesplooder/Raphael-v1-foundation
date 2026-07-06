# Archived n8n Workflow WFARCH-FE7D71B019

## Workflow ID

WFARCH-FE7D71B019

## Name

0601_Extractfromfile_Manual_Create_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0601_Extractfromfile_Manual_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 28
- Connections: 16
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.toolVectorStore`
- `@n8n/n8n-nodes-langchain.vectorStoreInMemory`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.whatsApp`
- `n8n-nodes-base.whatsAppTrigger`

## API and Service Analysis

- Agent
- Document Default Data Loader
- Embeddings Open Ai
- Extract From File
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- Sticky Note
- Switch
- Text Splitter Recursive Character Text Splitter
- Tool Vector Store
- Vector Store In Memory
- Whats App
- Whats App Trigger

## Required Credentials

- openAiApi (type only; no credential value stored)
- whatsAppApi (type only; no credential value stored)
- whatsAppTriggerApi (type only; no credential value stored)

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
