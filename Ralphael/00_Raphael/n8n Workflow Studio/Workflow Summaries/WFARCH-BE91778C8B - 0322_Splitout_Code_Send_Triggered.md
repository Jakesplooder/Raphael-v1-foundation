# Archived n8n Workflow WFARCH-BE91778C8B

## Workflow ID

WFARCH-BE91778C8B

## Name

0322_Splitout_Code_Send_Triggered

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0322_Splitout_Code_Send_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 18
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.toolWikipedia`
- `n8n-nodes-base.code`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chain Summarization
- Code
- Document Default Data Loader
- Gmail
- Information Extractor
- Lm Chat Open Ai
- Manual Trigger
- Split Out
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Tool Wikipedia

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
