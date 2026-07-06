# Archived n8n Workflow WFARCH-127AE46C04

## Workflow ID

WFARCH-127AE46C04

## Name

HDW Lead Geländewagen

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1955_Wait_Splitout_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 92
- Connections: 78
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.if`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.sort`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`
- `n8n-nodes-hdw.hdwLinkedin`
- `n8n-nodes-hdw.hdwLinkedinManagement`
- `n8n-nodes-hdw.hdwWebParserTool`

## API and Service Analysis

- Agent
- Aggregate
- Chat Trigger
- Code
- Google Sheets
- Hdw Linkedin
- Hdw Linkedin Management
- Hdw Web Parser Tool
- If
- Limit
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- Open Ai
- Output Parser Structured
- Schedule Trigger
- Sort
- Split In Batches
- Split Out
- Sticky Note
- Wait

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- hdwLinkedinApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Agency
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
