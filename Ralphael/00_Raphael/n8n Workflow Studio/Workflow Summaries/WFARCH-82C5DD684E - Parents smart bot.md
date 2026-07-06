# Archived n8n Workflow WFARCH-82C5DD684E

## Workflow ID

WFARCH-82C5DD684E

## Name

Parents smart bot

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1596_Telegram_Code_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 27
- Connections: 30
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `@n8n/n8n-nodes-langchain.toolWikipedia`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.code`
- `n8n-nodes-base.if`
- `n8n-nodes-base.set`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Agent
- Code
- Document Default Data Loader
- Embeddings Open Ai
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Open Ai
- Set
- Switch
- Telegram
- Telegram Trigger
- Text Splitter Recursive Character Text Splitter
- Tool Calculator
- Tool Http Request
- Tool Wikipedia
- Tool Workflow
- Vector Store Qdrant

## Required Credentials

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
