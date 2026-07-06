# Archived n8n Workflow WFARCH-3053E13FE1

## Workflow ID

WFARCH-3053E13FE1

## Name

0245_HTTP_Stripe_Create_Webhook

## Category

Finance

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0245_HTTP_Stripe_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 7
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.pipedrive`
- `n8n-nodes-base.pipedriveTrigger`
- `n8n-nodes-base.stripe`

## API and Service Analysis

- Http Request
- If
- Merge
- Pipedrive
- Pipedrive Trigger
- Stripe

## Required Credentials

- pipedriveApi (type only; no credential value stored)
- stripeApi (type only; no credential value stored)

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
