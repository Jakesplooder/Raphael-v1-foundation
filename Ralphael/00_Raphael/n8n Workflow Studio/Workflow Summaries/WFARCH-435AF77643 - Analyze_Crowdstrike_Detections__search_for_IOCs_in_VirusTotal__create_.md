# Archived n8n Workflow WFARCH-435AF77643

## Workflow ID

WFARCH-435AF77643

## Name

Analyze_Crowdstrike_Detections__search_for_IOCs_in_VirusTotal__create_a_ticket_in_Jira_and_post_a_message_in_Slack

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1312_Wait_Schedule_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 18
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.itemLists`
- `n8n-nodes-base.jira`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Http Request
- Item Lists
- Jira
- Schedule Trigger
- Set
- Slack
- Split In Batches
- Sticky Note
- Wait

## Required Credentials

- crowdStrikeOAuth2Api (type only; no credential value stored)
- jiraSoftwareCloudApi (type only; no credential value stored)
- slackOAuth2Api (type only; no credential value stored)
- virusTotalApi (type only; no credential value stored)

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
