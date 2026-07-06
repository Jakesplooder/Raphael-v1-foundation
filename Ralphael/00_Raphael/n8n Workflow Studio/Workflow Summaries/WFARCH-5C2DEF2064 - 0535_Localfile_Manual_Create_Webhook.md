# Archived n8n Workflow WFARCH-5C2DEF2064

## Workflow ID

WFARCH-5C2DEF2064

## Name

0535_Localfile_Manual_Create_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0535_Localfile_Manual_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 29
- Connections: 22
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainRetrievalQa`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsMistralCloud`
- `@n8n/n8n-nodes-langchain.lmChatMistralCloud`
- `@n8n/n8n-nodes-langchain.retrieverVectorStore`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.localFileTrigger`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.readWriteFile`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Chain Retrieval Qa
- Chat Trigger
- Document Default Data Loader
- Embeddings Mistral Cloud
- Http Request
- If
- Lm Chat Mistral Cloud
- Local File Trigger
- Manual Trigger
- Read Write File
- Retriever Vector Store
- Set
- Sticky Note
- Switch
- Text Splitter Recursive Character Text Splitter
- Vector Store Qdrant

## Required Credentials

- mistralCloudApi (type only; no credential value stored)
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
