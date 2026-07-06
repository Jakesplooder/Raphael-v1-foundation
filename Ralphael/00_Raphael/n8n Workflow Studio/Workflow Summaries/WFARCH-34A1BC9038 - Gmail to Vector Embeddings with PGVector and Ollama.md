# Archived n8n Workflow WFARCH-34A1BC9038

## Workflow ID

WFARCH-34A1BC9038

## Name

Gmail to Vector Embeddings with PGVector and Ollama

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1783_Splitout_Postgres_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 20
- Connections: 17
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOllama`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStorePGVector`
- `n8n-nodes-base.code`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.postgres`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Code
- Document Default Data Loader
- Embeddings Ollama
- Gmail
- Gmail Trigger
- If
- Manual Trigger
- No Op
- Postgres
- Set
- Split In Batches
- Split Out
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Vector Store P G Vector

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
