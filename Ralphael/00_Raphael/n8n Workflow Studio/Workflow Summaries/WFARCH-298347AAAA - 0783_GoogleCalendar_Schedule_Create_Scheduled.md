# Archived n8n Workflow WFARCH-298347AAAA

## Workflow ID

WFARCH-298347AAAA

## Name

0783_GoogleCalendar_Schedule_Create_Scheduled

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0783_GoogleCalendar_Schedule_Create_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 22
- Connections: 16
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleCalendar`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Filter
- Gmail
- Google Calendar
- Google Calendar Tool
- Lm Chat Open Ai
- Output Parser Structured
- Remove Duplicates
- Schedule Trigger
- Set
- Split In Batches
- Sticky Note

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleCalendarOAuth2Api (type only; no credential value stored)
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
