# Archived n8n Workflow WFARCH-69C2853483

## Workflow ID

WFARCH-69C2853483

## Name

0650_Splitout_Webhook_Create_Webhook

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0650_Splitout_Webhook_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 29
- Connections: 23
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.s3`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Aggregate
- Http Request
- If
- No Op
- Respond To Webhook
- S3
- Set
- Slack
- Split In Batches
- Split Out
- Sticky Note
- Switch
- Webhook

## Required Credentials

- s3 (type only; no credential value stored)
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
