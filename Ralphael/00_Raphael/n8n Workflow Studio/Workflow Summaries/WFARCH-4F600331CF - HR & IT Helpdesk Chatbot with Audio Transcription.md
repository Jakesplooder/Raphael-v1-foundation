# Archived n8n Workflow WFARCH-4F600331CF

## Workflow ID

WFARCH-4F600331CF

## Name

HR & IT Helpdesk Chatbot with Audio Transcription

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

2038_Telegram_Extractfromfile_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 27
- Connections: 20
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.toolVectorStore`
- `@n8n/n8n-nodes-langchain.vectorStorePGVector`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Agent
- Document Default Data Loader
- Embeddings Open Ai
- Extract From File
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- Memory Postgres Chat
- Open Ai
- Set
- Sticky Note
- Switch
- Telegram
- Telegram Trigger
- Text Splitter Recursive Character Text Splitter
- Tool Vector Store
- Vector Store P G Vector

## Required Credentials

- openAiApi (type only; no credential value stored)
- postgres (type only; no credential value stored)
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
