# Archived n8n Workflow WFARCH-FE3B58850A

## Workflow ID

WFARCH-FE3B58850A

## Name

1328_Jiratool_Schedule_Automate_Scheduled

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1328_Jiratool_Schedule_Automate_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 36
- Connections: 29
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.sentimentAnalysis`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.jira`
- `n8n-nodes-base.jiraTool`
- `n8n-nodes-base.notionTool`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Aggregate
- Chain Llm
- Execute Workflow
- Execute Workflow Trigger
- If
- Jira
- Jira Tool
- Lm Chat Open Ai
- Notion Tool
- Output Parser Structured
- Schedule Trigger
- Sentiment Analysis
- Set
- Slack
- Sticky Note
- Text Classifier

## Required Credentials

- jiraSoftwareCloudApi (type only; no credential value stored)
- notionApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- slackApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Research
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
