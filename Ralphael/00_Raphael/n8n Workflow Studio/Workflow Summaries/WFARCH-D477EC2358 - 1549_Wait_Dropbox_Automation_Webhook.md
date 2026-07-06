# Archived n8n Workflow WFARCH-D477EC2358

## Workflow ID

WFARCH-D477EC2358

## Name

1549_Wait_Dropbox_Automation_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1549_Wait_Dropbox_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 20
- Connections: 18
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.dropbox`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Dropbox
- Execute Workflow Trigger
- Http Request
- Manual Trigger
- Merge
- Set
- Sticky Note
- Switch
- Wait

## Required Credentials

- dropboxOAuth2Api (type only; no credential value stored)
- httpCustomAuth (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)

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
