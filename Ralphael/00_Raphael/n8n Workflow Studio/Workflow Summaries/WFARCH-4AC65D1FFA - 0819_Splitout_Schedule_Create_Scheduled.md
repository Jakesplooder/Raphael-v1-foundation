# Archived n8n Workflow WFARCH-4AC65D1FFA

## Workflow ID

WFARCH-4AC65D1FFA

## Name

0819_Splitout_Schedule_Create_Scheduled

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0819_Splitout_Schedule_Create_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 36
- Connections: 29
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- `n8n-nodes-base.if`
- `n8n-nodes-base.jira`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.sort`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`

## API and Service Analysis

- Agent
- Document Default Data Loader
- Embeddings Open Ai
- If
- Information Extractor
- Jira
- Lm Chat Open Ai
- No Op
- Remove Duplicates
- Schedule Trigger
- Set
- Sort
- Split In Batches
- Split Out
- Sticky Note
- Summarize
- Text Splitter Recursive Character Text Splitter
- Vector Store Supabase

## Required Credentials

- jiraSoftwareCloudApi (type only; no credential value stored)
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
