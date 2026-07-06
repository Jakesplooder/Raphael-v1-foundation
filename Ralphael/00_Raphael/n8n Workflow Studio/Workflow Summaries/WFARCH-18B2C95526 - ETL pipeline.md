# Archived n8n Workflow WFARCH-18B2C95526

## Workflow ID

WFARCH-18B2C95526

## Name

ETL pipeline

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1108_Postgres_Googlecloudnaturallanguage_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 9
- Connections: 8
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.cron`
- `n8n-nodes-base.googleCloudNaturalLanguage`
- `n8n-nodes-base.if`
- `n8n-nodes-base.mongoDb`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.postgres`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.twitter`

## API and Service Analysis

- Cron
- Google Cloud Natural Language
- If
- Mongo Db
- No Op
- Postgres
- Set
- Slack
- Twitter

## Required Credentials

- googleCloudNaturalLanguageOAuth2Api (type only; no credential value stored)
- mongoDb (type only; no credential value stored)
- postgres (type only; no credential value stored)
- slackApi (type only; no credential value stored)
- twitterOAuth1Api (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Notifications
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
