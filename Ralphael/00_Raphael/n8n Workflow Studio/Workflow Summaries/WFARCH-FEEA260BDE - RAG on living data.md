# Archived n8n Workflow WFARCH-FEEA260BDE

## Workflow ID

WFARCH-FEEA260BDE

## Name

RAG on living data

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1527_Limit_Schedule_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 34
- Connections: 19
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainRetrievalQa`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.retrieverVectorStore`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.notion`
- `n8n-nodes-base.notionTrigger`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`
- `n8n-nodes-base.supabase`

## API and Service Analysis

- Chain Retrieval Qa
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Limit
- Lm Chat Open Ai
- No Op
- Notion
- Notion Trigger
- Retriever Vector Store
- Schedule Trigger
- Split In Batches
- Sticky Note
- Summarize
- Supabase
- Text Splitter Token Splitter
- Vector Store Supabase

## Required Credentials

- notionApi (type only; no credential value stored)
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
