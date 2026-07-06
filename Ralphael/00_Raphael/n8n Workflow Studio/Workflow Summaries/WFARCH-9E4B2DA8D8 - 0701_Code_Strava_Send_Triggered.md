# Archived n8n Workflow WFARCH-9E4B2DA8D8

## Workflow ID

WFARCH-9E4B2DA8D8

## Name

0701_Code_Strava_Send_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0701_Code_Strava_Send_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 15
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.code`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.stravaTrigger`
- `n8n-nodes-base.whatsApp`

## API and Service Analysis

- Agent
- Code
- Email Send
- Gmail
- Lm Chat Google Gemini
- Sticky Note
- Strava Trigger
- Whats App

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- smtp (type only; no credential value stored)
- stravaOAuth2Api (type only; no credential value stored)
- whatsAppApi (type only; no credential value stored)

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
