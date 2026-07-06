# Archived n8n Workflow WFARCH-6611E251B3

## Workflow ID

WFARCH-6611E251B3

## Name

0539_Schedule_Twilio_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0539_Schedule_Twilio_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 36
- Connections: 22
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserAutofixing`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.twilio`
- `n8n-nodes-base.twilioTrigger`

## API and Service Analysis

- Agent
- Airtable
- Chain Llm
- Lm Chat Open Ai
- Output Parser Autofixing
- Output Parser Structured
- Schedule Trigger
- Sticky Note
- Switch
- Tool Http Request
- Twilio
- Twilio Trigger

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- calApi (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- twilioApi (type only; no credential value stored)

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
