# Archived n8n Workflow WFARCH-D40DF2380B

## Workflow ID

WFARCH-D40DF2380B

## Name

0898_Code_Schedule_Create_Scheduled

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0898_Code_Schedule_Create_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 45
- Connections: 33
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolThink`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Code
- Email Send
- Execute Workflow Trigger
- Form Trigger
- Html
- Http Request
- Lm Chat Open Ai
- Memory Buffer Window
- Merge
- Open Ai
- Output Parser Structured
- Schedule Trigger
- Set
- Sticky Note
- Tool Think
- Tool Workflow

## Required Credentials

- httpHeaderAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
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
