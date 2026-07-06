# Archived n8n Workflow WFARCH-D38355D120

## Workflow ID

WFARCH-D38355D120

## Name

Store Notion's Pages as Vector Documents into Supabase with OpenAI

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1414_Filter_Summarize_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 9
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.notion`
- `n8n-nodes-base.notionTrigger`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`

## API and Service Analysis

- Document Default Data Loader
- Embeddings Open Ai
- Filter
- Notion
- Notion Trigger
- Sticky Note
- Summarize
- Text Splitter Token Splitter
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
