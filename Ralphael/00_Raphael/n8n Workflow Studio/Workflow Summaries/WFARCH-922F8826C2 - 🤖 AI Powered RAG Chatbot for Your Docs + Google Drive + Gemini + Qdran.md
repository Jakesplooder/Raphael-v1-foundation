# Archived n8n Workflow WFARCH-922F8826C2

## Workflow ID

WFARCH-922F8826C2

## Name

🤖 AI Powered RAG Chatbot for Your Docs + Google Drive + Gemini + Qdrant

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1185_Telegram_Wait_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 50
- Connections: 35
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.code`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.googleDocs`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.wait`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Chat Trigger
- Code
- Document Default Data Loader
- Embeddings Open Ai
- Extract From File
- Google Docs
- Google Drive
- If
- Information Extractor
- Lm Chat Google Gemini
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- Merge
- Set
- Split In Batches
- Sticky Note
- Summarize
- Telegram
- Text Splitter Token Splitter
- Vector Store Qdrant
- Wait
- Webhook

## Required Credentials

- googleDocsOAuth2Api (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

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
