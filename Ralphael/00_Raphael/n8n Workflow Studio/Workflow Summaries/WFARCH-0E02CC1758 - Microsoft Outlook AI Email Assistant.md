# Archived n8n Workflow WFARCH-0E02CC1758

## Workflow ID

WFARCH-0E02CC1758

## Name

Microsoft Outlook AI Email Assistant

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1551_Mondaycom_Schedule_Send_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 28
- Connections: 23
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.microsoftOutlook`
- `n8n-nodes-base.mondayCom`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Airtable
- If
- Lm Chat Open Ai
- Manual Trigger
- Markdown
- Merge
- Microsoft Outlook
- Monday Com
- Output Parser Structured
- Schedule Trigger
- Set
- Split In Batches
- Sticky Note

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- microsoftOutlookOAuth2Api (type only; no credential value stored)
- mondayComApi (type only; no credential value stored)
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
