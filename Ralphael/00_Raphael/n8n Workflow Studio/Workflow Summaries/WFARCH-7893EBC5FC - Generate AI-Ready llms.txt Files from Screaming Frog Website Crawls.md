# Archived n8n Workflow WFARCH-7893EBC5FC

## Workflow ID

WFARCH-7893EBC5FC

## Name

Generate AI-Ready llms.txt Files from Screaming Frog Website Crawls

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1791_Filter_Summarize_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 23
- Connections: 10
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`

## API and Service Analysis

- Convert To File
- Extract From File
- Filter
- Form Trigger
- Lm Chat Open Ai
- No Op
- Set
- Sticky Note
- Summarize
- Text Classifier

## Required Credentials

- openAiApi (type only; no credential value stored)

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
