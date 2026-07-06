# Archived n8n Workflow WFARCH-253CC38012

## Workflow ID

WFARCH-253CC38012

## Name

0527_Schedule_Manual_Update_Scheduled

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0527_Schedule_Manual_Update_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 22
- Connections: 14
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolSerpApi`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Google Sheets
- Lm Chat Open Ai
- Manual Trigger
- Merge
- Output Parser Structured
- Schedule Trigger
- Set
- Split In Batches
- Sticky Note
- Tool Serp Api
- Tool Workflow

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- serpApi (type only; no credential value stored)

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
