# Archived n8n Workflow WFARCH-53C5B74721

## Workflow ID

WFARCH-53C5B74721

## Name

1733_Webhook_Slack_Automate_Webhook

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1733_Webhook_Slack_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 38
- Connections: 27
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.venafiTlsProtectCloud`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Execute Workflow
- Http Request
- If
- Merge
- No Op
- Open Ai
- Respond To Webhook
- Set
- Slack
- Sticky Note
- Switch
- Venafi Tls Protect Cloud
- Webhook

## Required Credentials

- openAiApi (type only; no credential value stored)
- slackApi (type only; no credential value stored)
- venafiTlsProtectCloudApi (type only; no credential value stored)
- virusTotalApi (type only; no credential value stored)

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
