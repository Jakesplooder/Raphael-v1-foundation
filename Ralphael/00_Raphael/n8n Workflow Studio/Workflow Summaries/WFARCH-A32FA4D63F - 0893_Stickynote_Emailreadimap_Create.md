# Archived n8n Workflow WFARCH-A32FA4D63F

## Workflow ID

WFARCH-A32FA4D63F

## Name

0893_Stickynote_Emailreadimap_Create

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0893_Stickynote_Emailreadimap_Create.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 13
- Connections: 9
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.hubspot`
- `n8n-nodes-base.if`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Llm
- Email Read Imap
- Hubspot
- If
- Lm Chat Open Ai
- Output Parser Structured
- Set
- Sticky Note

## Required Credentials

- hubspotOAuth2Api (type only; no credential value stored)
- imap (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
