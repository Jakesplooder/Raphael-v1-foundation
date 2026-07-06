# Archived n8n Workflow WFARCH-2CF9B50567

## Workflow ID

WFARCH-2CF9B50567

## Name

Receive messages from a topic and send an SMS

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0209_Noop_Kafka_Send_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 4
- Connections: 3
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.if`
- `n8n-nodes-base.kafkaTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.vonage`

## API and Service Analysis

- If
- Kafka Trigger
- No Op
- Vonage

## Required Credentials

- kafka (type only; no credential value stored)
- vonageApi (type only; no credential value stored)

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
