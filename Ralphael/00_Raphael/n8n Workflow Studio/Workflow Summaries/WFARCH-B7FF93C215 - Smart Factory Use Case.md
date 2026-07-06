# Archived n8n Workflow WFARCH-B7FF93C215

## Workflow ID

WFARCH-B7FF93C215

## Name

Smart Factory Use Case

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0212_Noop_Cratedb_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 9
- Connections: 8
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.amqpTrigger`
- `n8n-nodes-base.crateDb`
- `n8n-nodes-base.function`
- `n8n-nodes-base.if`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.pagerDuty`
- `n8n-nodes-base.set`

## API and Service Analysis

- Amqp Trigger
- Crate Db
- Function
- If
- No Op
- Pager Duty
- Set

## Required Credentials

- amqp (type only; no credential value stored)
- crateDb (type only; no credential value stored)
- pagerDutyApi (type only; no credential value stored)

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
