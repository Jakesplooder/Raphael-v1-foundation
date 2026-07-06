# Archived n8n Workflow WFARCH-8EC041D464

## Workflow ID

WFARCH-8EC041D464

## Name

0530_Splitout_GoogleCalendar_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0530_Splitout_GoogleCalendar_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 28
- Connections: 17
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.googleCalendar`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Agent
- Execute Workflow Trigger
- Extract From File
- Google Calendar
- Google Drive
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- Output Parser Structured
- Set
- Split Out
- Sticky Note
- Switch
- Tool Workflow

## Required Credentials

- googleCalendarOAuth2Api (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googleOAuth2Api (type only; no credential value stored)
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
