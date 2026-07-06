# Archived n8n Workflow WFARCH-02C0CB8D2F

## Workflow ID

WFARCH-02C0CB8D2F

## Name

0821_Manual_Noop_Create_Triggered

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0821_Manual_Noop_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 17
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.hubspot`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Gmail
- Hubspot
- Information Extractor
- Lm Chat Google Gemini
- Manual Trigger
- No Op
- Set
- Split In Batches
- Sticky Note

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- hubspotAppToken (type only; no credential value stored)

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
