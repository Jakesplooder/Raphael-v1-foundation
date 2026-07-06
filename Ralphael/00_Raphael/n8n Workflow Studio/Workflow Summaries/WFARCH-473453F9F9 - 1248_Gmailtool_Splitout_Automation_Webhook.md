# Archived n8n Workflow WFARCH-473453F9F9

## Workflow ID

WFARCH-473453F9F9

## Name

1248_Gmailtool_Splitout_Automation_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1248_Gmailtool_Splitout_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 18
- Connections: 8
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.gmailTool`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Airtable
- Execute Workflow Trigger
- Gmail Tool
- Google Calendar Tool
- Http Request
- Lm Chat Open Ai
- Split Out
- Sticky Note
- Tool Workflow
- Webhook

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
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
