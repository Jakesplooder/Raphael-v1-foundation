# Archived n8n Workflow WFARCH-E63549B193

## Workflow ID

WFARCH-E63549B193

## Name

[1/3 - anomaly detection] [1/2 - KNN classification] Batch upload dataset to Qdrant (crops dataset)

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1728_Code_Filter_Import_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 25
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.code`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.googleCloudStorage`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Code
- Filter
- Google Cloud Storage
- Http Request
- If
- Manual Trigger
- Set
- Sticky Note

## Required Credentials

- googleCloudStorageOAuth2Api (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
