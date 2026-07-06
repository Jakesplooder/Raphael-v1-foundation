# Archived n8n Workflow WFARCH-ADF379A058

## Workflow ID

WFARCH-ADF379A058

## Name

0547_Wait_Splitout_Create_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0547_Wait_Splitout_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 39
- Connections: 30
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.notion`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Agent
- Http Request
- Limit
- Lm Chat Open Ai
- Manual Trigger
- Notion
- Output Parser Structured
- Remove Duplicates
- Set
- Split In Batches
- Split Out
- Sticky Note
- Tool Http Request
- Wait

## Required Credentials

- httpHeaderAuth (type only; no credential value stored)
- notionApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- serpApi (type only; no credential value stored)

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
