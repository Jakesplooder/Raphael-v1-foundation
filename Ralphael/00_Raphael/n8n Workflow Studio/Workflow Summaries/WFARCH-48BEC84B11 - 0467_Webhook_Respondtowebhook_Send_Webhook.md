# Archived n8n Workflow WFARCH-48BEC84B11

## Workflow ID

WFARCH-48BEC84B11

## Name

0467_Webhook_Respondtowebhook_Send_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0467_Webhook_Respondtowebhook_Send_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 17
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainRetrievalQa`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.retrieverVectorStore`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Chain Retrieval Qa
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Google Drive
- Lm Chat Open Ai
- Manual Trigger
- Respond To Webhook
- Retriever Vector Store
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Vector Store Qdrant
- Webhook

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
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
