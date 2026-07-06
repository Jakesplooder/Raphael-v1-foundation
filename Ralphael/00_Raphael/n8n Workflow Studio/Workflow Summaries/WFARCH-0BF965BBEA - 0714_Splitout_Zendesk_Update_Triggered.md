# Archived n8n Workflow WFARCH-0BF965BBEA

## Workflow ID

WFARCH-0BF965BBEA

## Name

0714_Splitout_Zendesk_Update_Triggered

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0714_Splitout_Zendesk_Update_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 26
- Connections: 21
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.zendesk`

## API and Service Analysis

- Agent
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Extract From File
- Google Drive
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- No Op
- Output Parser Structured
- Split In Batches
- Split Out
- Sticky Note
- Text Splitter Token Splitter
- Vector Store Qdrant
- Zendesk

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)
- zendeskApi (type only; no credential value stored)

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
