# Archived n8n Workflow WFARCH-81CF50119C

## Workflow ID

WFARCH-81CF50119C

## Name

Personalized AI Tech Newsletter Using RSS, OpenAI and Gmail

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1934_Splitout_Schedule_Create_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 24
- Connections: 15
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreInMemory`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.rssFeedRead`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Document Default Data Loader
- Embeddings Open Ai
- Gmail
- Lm Chat Open Ai
- Markdown
- Rss Feed Read
- Schedule Trigger
- Set
- Split Out
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Vector Store In Memory

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
