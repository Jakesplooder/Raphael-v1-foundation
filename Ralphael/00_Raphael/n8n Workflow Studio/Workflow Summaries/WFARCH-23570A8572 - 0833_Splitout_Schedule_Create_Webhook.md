# Archived n8n Workflow WFARCH-23570A8572

## Workflow ID

WFARCH-23570A8572

## Name

0833_Splitout_Schedule_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0833_Splitout_Schedule_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 33
- Connections: 27
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.microsoftExcel`
- `n8n-nodes-base.microsoftOutlook`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Aggregate
- Chain Llm
- Html
- Http Request
- If
- Lm Chat Open Ai
- Merge
- Microsoft Excel
- Microsoft Outlook
- No Op
- Remove Duplicates
- Schedule Trigger
- Set
- Split In Batches
- Split Out
- Sticky Note

## Required Credentials

- microsoftExcelOAuth2Api (type only; no credential value stored)
- microsoftOutlookOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Automation
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
