# Archived n8n Workflow WFARCH-8622D84783

## Workflow ID

WFARCH-8622D84783

## Name

On new Stripe Invoice Payment update Hubspot and notify the team in Slack

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0008_Slack_Stripe_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 8
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.hubspot`
- `n8n-nodes-base.if`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.stripeTrigger`

## API and Service Analysis

- Hubspot
- If
- Slack
- Stripe Trigger

## Required Credentials

- hubspotApi (type only; no credential value stored)
- hubspotOAuth2Api (type only; no credential value stored)
- slackApi (type only; no credential value stored)
- stripeApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Agency
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
