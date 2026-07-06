# Archived n8n Workflow WFARCH-659694079B

## Workflow ID

WFARCH-659694079B

## Name

1647_Splitout_Limit_Automation_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1647_Splitout_Limit_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 15
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Summarization
- Document Default Data Loader
- Html
- Http Request
- Limit
- Lm Chat Open Ai
- Manual Trigger
- Merge
- Set
- Split Out
- Sticky Note
- Text Splitter Recursive Character Text Splitter

## Required Credentials

- openAiApi (type only; no credential value stored)

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
