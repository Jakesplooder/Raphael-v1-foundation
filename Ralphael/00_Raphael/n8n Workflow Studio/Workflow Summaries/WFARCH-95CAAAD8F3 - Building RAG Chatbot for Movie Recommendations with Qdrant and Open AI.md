# Archived n8n Workflow WFARCH-95CAAAD8F3

## Workflow ID

WFARCH-95CAAAD8F3

## Name

Building RAG Chatbot for Movie Recommendations with Qdrant and Open AI

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1363_Splitout_GitHub_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 27
- Connections: 24
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.github`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Aggregate
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Execute Workflow Trigger
- Extract From File
- Github
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- Merge
- Set
- Split Out
- Sticky Note
- Text Splitter Token Splitter
- Tool Workflow
- Vector Store Qdrant

## Required Credentials

- githubApi (type only; no credential value stored)
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
