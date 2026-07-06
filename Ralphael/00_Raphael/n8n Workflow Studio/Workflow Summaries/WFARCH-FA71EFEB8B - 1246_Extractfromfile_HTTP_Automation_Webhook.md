# Archived n8n Workflow WFARCH-FA71EFEB8B

## Workflow ID

WFARCH-FA71EFEB8B

## Name

1246_Extractfromfile_HTTP_Automation_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1246_Extractfromfile_HTTP_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 33
- Connections: 23
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.toolVectorStore`
- `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.supabase`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Agent
- Aggregate
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Extract From File
- Http Request
- If
- Lm Chat Open Ai
- Manual Trigger
- Merge
- Split In Batches
- Sticky Note
- Supabase
- Switch
- Text Splitter Recursive Character Text Splitter
- Tool Vector Store
- Vector Store Supabase

## Required Credentials

- openAiApi (type only; no credential value stored)
- supabaseApi (type only; no credential value stored)

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
