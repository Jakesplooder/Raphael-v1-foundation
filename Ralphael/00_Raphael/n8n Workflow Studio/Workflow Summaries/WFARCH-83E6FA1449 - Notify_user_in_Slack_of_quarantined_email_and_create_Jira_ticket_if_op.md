# Archived n8n Workflow WFARCH-83E6FA1449

## Workflow ID

WFARCH-83E6FA1449

## Name

Notify_user_in_Slack_of_quarantined_email_and_create_Jira_ticket_if_opened

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1541_Webhook_Code_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 13
- Connections: 9
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.code`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.jira`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Code
- Http Request
- If
- Jira
- No Op
- Slack
- Sticky Note
- Webhook

## Required Credentials

- httpHeaderAuth (type only; no credential value stored)
- jiraSoftwareCloudApi (type only; no credential value stored)
- slackApi (type only; no credential value stored)
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
