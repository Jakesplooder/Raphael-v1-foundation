# Archived n8n Workflow WFARCH-E35876A3BC

## Workflow ID

WFARCH-E35876A3BC

## Name

Prod: Notion to Vector Store - Dimension 768

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1570_Filter_Summarize_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 8
- Connections: 7
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.vectorStorePinecone`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.notion`
- `n8n-nodes-base.notionTrigger`
- `n8n-nodes-base.summarize`

## API and Service Analysis

- Document Default Data Loader
- Embeddings Google Gemini
- Filter
- Notion
- Notion Trigger
- Summarize
- Text Splitter Token Splitter
- Vector Store Pinecone

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- notionApi (type only; no credential value stored)
- pineconeApi (type only; no credential value stored)

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
