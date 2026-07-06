# Archived n8n Workflow WFARCH-12F8EE6683

## Workflow ID

WFARCH-12F8EE6683

## Name

MiniBear Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1494_Microsofttodo_Webhook_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 45
- Connections: 26
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.microsoftOneDrive`
- `n8n-nodes-base.microsoftTeams`
- `n8n-nodes-base.microsoftToDo`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Http Request
- If
- Lm Chat Open Router
- Microsoft One Drive
- Microsoft Teams
- Microsoft To Do
- Output Parser Structured
- Sticky Note
- Switch
- Webhook

## Required Credentials

- httpHeaderAuth (type only; no credential value stored)
- microsoftOneDriveOAuth2Api (type only; no credential value stored)
- microsoftTeamsOAuth2Api (type only; no credential value stored)
- microsoftToDoOAuth2Api (type only; no credential value stored)
- openRouterApi (type only; no credential value stored)

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
