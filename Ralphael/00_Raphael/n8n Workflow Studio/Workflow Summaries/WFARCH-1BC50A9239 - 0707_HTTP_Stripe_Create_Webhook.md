# Archived n8n Workflow WFARCH-1BC50A9239

## Workflow ID

WFARCH-1BC50A9239

## Name

0707_HTTP_Stripe_Create_Webhook

## Category

Finance

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0707_HTTP_Stripe_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 10
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.quickbooks`
- `n8n-nodes-base.stripe`
- `n8n-nodes-base.stripeTrigger`

## API and Service Analysis

- Http Request
- If
- Merge
- Quickbooks
- Stripe
- Stripe Trigger

## Required Credentials

- httpCustomAuth (type only; no credential value stored)
- quickBooksOAuth2Api (type only; no credential value stored)
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
