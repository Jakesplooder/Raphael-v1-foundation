# Archived n8n Workflow WFARCH-CD8E6D674F

## Workflow ID

WFARCH-CD8E6D674F

## Name

0911_Schedule_Removeduplicates_Create_Scheduled

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0911_Schedule_Removeduplicates_Create_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 12
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.jira`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.microsoftOutlook`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Llm
- Jira
- Lm Chat Open Ai
- Markdown
- Microsoft Outlook
- Output Parser Structured
- Remove Duplicates
- Schedule Trigger
- Sticky Note

## Required Credentials

- jiraSoftwareCloudApi (type only; no credential value stored)
- microsoftOutlookOAuth2Api (type only; no credential value stored)
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
