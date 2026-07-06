# Archived n8n Workflow WFARCH-AD7456C047

## Workflow ID

WFARCH-AD7456C047

## Name

ClockifyBlockiaWorkflow

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1754_Executiondata_Slack_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 15
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `@n8n/n8n-nodes-langchain.toolCode`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.executionData`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.slackTrigger`

## API and Service Analysis

- Agent
- Execution Data
- Lm Chat Open Ai
- Memory Buffer Window
- Slack
- Slack Trigger
- Tool Calculator
- Tool Code
- Tool Http Request

## Required Credentials

- clockifyApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- slackApi (type only; no credential value stored)

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
