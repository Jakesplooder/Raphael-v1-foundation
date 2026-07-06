# Archived n8n Workflow WFARCH-3977F4C07A

## Workflow ID

WFARCH-3977F4C07A

## Name

UTM Link Creator & QR Code Generator with Scheduled Google Analytics Reports

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1644_Code_Schedule_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 9
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.code`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleAnalyticsTool`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Airtable
- Code
- Gmail
- Google Analytics Tool
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- Schedule Trigger
- Set
- Sticky Note

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- gmailOAuth2 (type only; no credential value stored)
- googleAnalyticsOAuth2 (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Creator
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
