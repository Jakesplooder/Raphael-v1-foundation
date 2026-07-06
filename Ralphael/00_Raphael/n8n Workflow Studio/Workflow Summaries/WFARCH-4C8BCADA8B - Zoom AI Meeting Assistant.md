# Archived n8n Workflow WFARCH-4C8BCADA8B

## Workflow ID

WFARCH-4C8BCADA8B

## Name

Zoom AI Meeting Assistant

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1894_Stopanderror_Clickup_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 25
- Connections: 24
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatAnthropic`
- `@n8n/n8n-nodes-langchain.toolThink`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.clickUp`
- `n8n-nodes-base.code`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.microsoftOutlookTool`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.stopAndError`
- `n8n-nodes-base.zoom`

## API and Service Analysis

- Agent
- Click Up
- Code
- Email Send
- Execute Workflow Trigger
- Extract From File
- Filter
- Http Request
- Lm Chat Anthropic
- Manual Trigger
- Microsoft Outlook Tool
- Set
- Split In Batches
- Split Out
- Sticky Note
- Stop And Error
- Tool Think
- Tool Workflow
- Zoom

## Required Credentials

- anthropicApi (type only; no credential value stored)
- clickUpOAuth2Api (type only; no credential value stored)
- microsoftOutlookOAuth2Api (type only; no credential value stored)
- smtp (type only; no credential value stored)
- zoomOAuth2Api (type only; no credential value stored)

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
