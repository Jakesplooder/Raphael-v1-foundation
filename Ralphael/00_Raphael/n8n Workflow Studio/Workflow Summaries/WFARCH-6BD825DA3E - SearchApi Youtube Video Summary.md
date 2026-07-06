# Archived n8n Workflow WFARCH-6BD825DA3E

## Workflow ID

WFARCH-6BD825DA3E

## Name

SearchApi Youtube Video Summary

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1552_Manual_Summarize_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 9
- Connections: 6
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@searchapi/n8n-nodes-searchapi.searchApi`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`

## API and Service Analysis

- Chain Summarization
- Lm Chat Open Ai
- Manual Trigger
- Search Api
- Split Out
- Sticky Note
- Summarize
- Text Splitter Recursive Character Text Splitter

## Required Credentials

- None declared in source workflow.

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Creator
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
