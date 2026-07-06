# Archived n8n Workflow WFARCH-4887A39CC6

## Workflow ID

WFARCH-4887A39CC6

## Name

Qdrant Vector Database Embedding Pipeline

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1776_Manual_Ftp_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 13
- Connections: 8
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.textSplitterCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.ftp`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Document Default Data Loader
- Embeddings Open Ai
- Ftp
- Manual Trigger
- Split In Batches
- Sticky Note
- Text Splitter Character Text Splitter
- Vector Store Qdrant

## Required Credentials

- ftp (type only; no credential value stored)
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
