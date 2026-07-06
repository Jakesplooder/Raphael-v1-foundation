# Archived n8n Workflow WFARCH-713A4AD61C

## Workflow ID

WFARCH-713A4AD61C

## Name

Email AI Auto-responder. Summerize and send email

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1962_Emailreadimap_Manual_Send_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 26
- Connections: 21
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chain Llm
- Chain Summarization
- Document Default Data Loader
- Email Read Imap
- Email Send
- Embeddings Open Ai
- Google Drive
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- Markdown
- No Op
- Sticky Note
- Text Classifier
- Text Splitter Token Splitter
- Vector Store Qdrant

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- imap (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)
- smtp (type only; no credential value stored)

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
