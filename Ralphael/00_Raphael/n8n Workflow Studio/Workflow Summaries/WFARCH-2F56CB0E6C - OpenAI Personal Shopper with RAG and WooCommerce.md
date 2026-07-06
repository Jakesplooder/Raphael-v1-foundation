# Archived n8n Workflow WFARCH-2F56CB0E6C

## Workflow ID

WFARCH-2F56CB0E6C

## Name

OpenAI Personal Shopper with RAG and WooCommerce

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1599_Woocommercetool_Manual_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 25
- Connections: 19
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `@n8n/n8n-nodes-langchain.toolVectorStore`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wooCommerceTool`

## API and Service Analysis

- Agent
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Google Drive
- Http Request
- Information Extractor
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- Set
- Sticky Note
- Text Splitter Token Splitter
- Tool Calculator
- Tool Vector Store
- Vector Store Qdrant
- Woo Commerce Tool

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)
- wooCommerceApi (type only; no credential value stored)

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
