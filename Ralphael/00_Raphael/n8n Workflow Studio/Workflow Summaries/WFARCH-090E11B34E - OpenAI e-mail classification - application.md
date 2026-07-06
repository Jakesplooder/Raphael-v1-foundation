# Archived n8n Workflow WFARCH-090E11B34E

## Workflow ID

WFARCH-090E11B34E

## Name

OpenAI e-mail classification - application

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0929_Noop_Extractfromfile_Automation.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 10
- Connections: 8
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Email Read Imap
- Extract From File
- Information Extractor
- Lm Chat Open Ai
- No Op
- Sticky Note
- Text Classifier

## Required Credentials

- imap (type only; no credential value stored)
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
