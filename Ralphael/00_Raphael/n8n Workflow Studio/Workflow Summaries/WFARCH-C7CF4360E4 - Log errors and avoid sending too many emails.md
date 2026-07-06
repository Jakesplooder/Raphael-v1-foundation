# Archived n8n Workflow WFARCH-C7CF4360E4

## Workflow ID

WFARCH-C7CF4360E4

## Name

Log errors and avoid sending too many emails

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1777_Error_Postgres_Send_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.code`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.errorTrigger`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.postgres`
- `n8n-nodes-base.pushover`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Code
- Email Send
- Error Trigger
- Execute Workflow
- Execute Workflow Trigger
- If
- Manual Trigger
- No Op
- Postgres
- Pushover
- Sticky Note

## Required Credentials

- postgres (type only; no credential value stored)
- pushoverApi (type only; no credential value stored)
- smtp (type only; no credential value stored)

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
