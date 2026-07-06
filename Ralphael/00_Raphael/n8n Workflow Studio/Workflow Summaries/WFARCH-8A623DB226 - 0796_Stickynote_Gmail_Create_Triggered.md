# Archived n8n Workflow WFARCH-8A623DB226

## Workflow ID

WFARCH-8A623DB226

## Name

0796_Stickynote_Gmail_Create_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0796_Stickynote_Gmail_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.sendInBlue`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Email Send
- Gmail
- Gmail Trigger
- If
- Lm Chat Google Gemini
- Send In Blue
- Sticky Note
- Text Classifier

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- sendInBlueApi (type only; no credential value stored)
- smtp (type only; no credential value stored)

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
