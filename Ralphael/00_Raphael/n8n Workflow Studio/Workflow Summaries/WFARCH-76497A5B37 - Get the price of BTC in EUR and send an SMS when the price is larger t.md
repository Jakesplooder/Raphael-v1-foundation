# Archived n8n Workflow WFARCH-76497A5B37

## Workflow ID

WFARCH-76497A5B37

## Name

Get the price of BTC in EUR and send an SMS when the price is larger than EUR 9000

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1130_Noop_Twilio_Send_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 5
- Connections: 4
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.coinGecko`
- `n8n-nodes-base.cron`
- `n8n-nodes-base.if`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.twilio`

## API and Service Analysis

- Coin Gecko
- Cron
- If
- No Op
- Twilio

## Required Credentials

- twilioApi (type only; no credential value stored)

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
