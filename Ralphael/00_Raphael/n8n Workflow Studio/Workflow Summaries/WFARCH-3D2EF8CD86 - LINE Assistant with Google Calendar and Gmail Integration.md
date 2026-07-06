# Archived n8n Workflow WFARCH-3D2EF8CD86

## Workflow ID

WFARCH-3D2EF8CD86

## Name

LINE Assistant with Google Calendar and Gmail Integration

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1778_HTTP_Googlecalendartool_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 14
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.toolWikipedia`
- `n8n-nodes-base.gmailTool`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.set`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Gmail Tool
- Google Calendar Tool
- Http Request
- Lm Chat Open Ai
- Memory Buffer Window
- Open Ai
- Set
- Switch
- Tool Wikipedia
- Webhook

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleCalendarOAuth2Api (type only; no credential value stored)

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
