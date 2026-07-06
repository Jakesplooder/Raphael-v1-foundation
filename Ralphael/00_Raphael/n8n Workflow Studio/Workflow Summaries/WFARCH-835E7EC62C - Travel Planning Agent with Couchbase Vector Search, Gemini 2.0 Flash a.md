# Archived n8n Workflow WFARCH-835E7EC62C

## Workflow ID

WFARCH-835E7EC62C

## Name

Travel Planning Agent with Couchbase Vector Search, Gemini 2.0 Flash and OpenAI

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1703_Stickynote_Webhook_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 13
- Connections: 9
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`
- `n8n-nodes-couchbase.vectorStoreCouchbaseSearch`

## API and Service Analysis

- Agent
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Lm Chat Google Gemini
- Memory Buffer Window
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Vector Store Couchbase Search
- Webhook

## Required Credentials

- None declared in source workflow.

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Research
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
