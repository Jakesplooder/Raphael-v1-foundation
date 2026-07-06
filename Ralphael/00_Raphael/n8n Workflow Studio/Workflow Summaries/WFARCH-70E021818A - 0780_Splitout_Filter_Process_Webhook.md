# Archived n8n Workflow WFARCH-70E021818A

## Workflow ID

WFARCH-70E021818A

## Name

0780_Splitout_Filter_Process_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0780_Splitout_Filter_Process_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 51
- Connections: 34
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatAnthropic`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.outputParserAutofixing`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.xml`

## API and Service Analysis

- Airtable
- Chain Llm
- Execute Workflow
- Execute Workflow Trigger
- Filter
- Html
- Http Request
- Information Extractor
- Lm Chat Anthropic
- Lm Chat Open Router
- Manual Trigger
- Merge
- Output Parser Autofixing
- Output Parser Structured
- Set
- Split Out
- Sticky Note
- Xml

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- anthropicApi (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- openRouterApi (type only; no credential value stored)

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
