# Archived n8n Workflow WFARCH-7F371206F5

## Workflow ID

WFARCH-7F371206F5

## Name

Prevent concurrent workflow runs using Redis

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0925_Stopanderror_Wait_Automate_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 43
- Connections: 24
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.redis`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.stopAndError`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Execute Workflow
- Execute Workflow Trigger
- If
- Manual Trigger
- No Op
- Redis
- Set
- Sticky Note
- Stop And Error
- Switch
- Wait

## Required Credentials

- redis (type only; no credential value stored)

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
