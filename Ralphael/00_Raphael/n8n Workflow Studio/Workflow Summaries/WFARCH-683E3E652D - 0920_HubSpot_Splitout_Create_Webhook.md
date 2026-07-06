# Archived n8n Workflow WFARCH-683E3E652D

## Workflow ID

WFARCH-683E3E652D

## Name

0920_HubSpot_Splitout_Create_Webhook

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0920_HubSpot_Splitout_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 31
- Connections: 23
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.hubspot`
- `n8n-nodes-base.hubspotTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Execute Workflow Trigger
- Filter
- Gmail
- Google Calendar Tool
- Http Request
- Hubspot
- Hubspot Trigger
- If
- Lm Chat Open Ai
- Markdown
- Output Parser Structured
- Set
- Split Out
- Sticky Note
- Tool Workflow
- Webhook

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleCalendarOAuth2Api (type only; no credential value stored)
- hubspotDeveloperApi (type only; no credential value stored)
- hubspotOAuth2Api (type only; no credential value stored)
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
