# Archived n8n Workflow WFARCH-A7580868E1

## Workflow ID

WFARCH-A7580868E1

## Name

0451_Filter_Slack_Update_Webhook

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0451_Filter_Slack_Update_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 12
- Connections: 10
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.linear`
- `n8n-nodes-base.linearTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Filter
- Http Request
- If
- Linear
- Linear Trigger
- Merge
- Open Ai
- Set
- Slack
- Sticky Note

## Required Credentials

- linearApi (type only; no credential value stored)
- linearOAuth2Api (type only; no credential value stored)
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
