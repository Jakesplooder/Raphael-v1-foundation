# Archived n8n Workflow WFARCH-12623AC0B7

## Workflow ID

WFARCH-12623AC0B7

## Name

Airtop Web Agent

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1681_Airtoptool_Slack_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 19
- Connections: 15
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatAnthropic`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.airtop`
- `n8n-nodes-base.airtopTool`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Airtop
- Airtop Tool
- Execute Workflow Trigger
- Form Trigger
- Lm Chat Anthropic
- Output Parser Structured
- Set
- Slack
- Sticky Note
- Tool Workflow

## Required Credentials

- airtopApi (type only; no credential value stored)
- anthropicApi (type only; no credential value stored)
- slackOAuth2Api (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Notifications
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
