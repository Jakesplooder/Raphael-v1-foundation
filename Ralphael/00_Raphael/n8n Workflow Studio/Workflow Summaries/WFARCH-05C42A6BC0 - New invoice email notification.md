# Archived n8n Workflow WFARCH-05C42A6BC0

## Workflow ID

WFARCH-05C42A6BC0

## Name

New invoice email notification

## Category

Finance

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1194_Slack_Emailreadimap_Create.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 6
- Connections: 6
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.if`
- `n8n-nodes-base.mindee`
- `n8n-nodes-base.slack`

## API and Service Analysis

- Email Read Imap
- Email Send
- If
- Mindee
- Slack

## Required Credentials

- imap (type only; no credential value stored)
- mindeeInvoiceApi (type only; no credential value stored)
- slackApi (type only; no credential value stored)
- smtp (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Finance
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
