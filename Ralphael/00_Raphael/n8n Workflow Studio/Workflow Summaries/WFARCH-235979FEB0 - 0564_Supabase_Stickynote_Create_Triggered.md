# Archived n8n Workflow WFARCH-235979FEB0

## Workflow ID

WFARCH-235979FEB0

## Name

0564_Supabase_Stickynote_Create_Triggered

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0564_Supabase_Stickynote_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 21
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainRetrievalQa`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.retrieverVectorStore`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.supabase`

## API and Service Analysis

- Chain Retrieval Qa
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Google Drive
- Lm Chat Open Ai
- Retriever Vector Store
- Set
- Sticky Note
- Supabase
- Text Splitter Recursive Character Text Splitter
- Vector Store Supabase

## Required Credentials

- None declared in source workflow.

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
