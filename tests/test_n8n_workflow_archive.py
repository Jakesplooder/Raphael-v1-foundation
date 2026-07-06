from __future__ import annotations

import json
import unittest

from raphael_core.config import load_config
from raphael_core.legacy import n8n_root, n8n_workflow_archive_search, n8n_workflow_archive_show, n8n_workflow_archive_summary
from tests.support import TempRaphael


class N8nWorkflowArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)
        root = n8n_root(self.config) / "Workflow Summaries"
        root.mkdir(parents=True, exist_ok=True)
        (root / "WFARCH-D2A37F5A8B - Youtube_Automation.md").write_text(
            """# Archived n8n Workflow WFARCH-D2A37F5A8B

## Workflow ID

WFARCH-D2A37F5A8B

## Name

Youtube_Automation

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\\n8n-workflows-main\\n8n-workflows-main\\workflows

## Source Workflow

2000_Wait_Code_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 33
- Connections: 27
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.youTube`
- `n8n-nodes-base.httpRequest`
- `@n8n/n8n-nodes-langchain.openAi`

## API and Service Analysis

- Manual Trigger
- Schedule Trigger
- You Tube
- Http Request
- Open Ai

## Required Credentials

- youTubeOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Creator

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.os.close()

    def test_archive_show_returns_required_detail_fields(self) -> None:
        result = n8n_workflow_archive_show(self.config, "WFARCH-D2A37F5A8B")
        self.assertEqual("WFARCH-D2A37F5A8B", result["workflow_id"])
        self.assertEqual("Youtube_Automation", result["workflow_name"])
        self.assertEqual("Creator", result["category"])
        self.assertEqual(33, result["node_count"])
        self.assertIn("n8n-nodes-base.youTube", result["node_types"])
        self.assertIn("n8n-nodes-base.manualTrigger", result["triggers"])
        self.assertIn("You Tube", result["external_services"])
        self.assertIn("youTubeOAuth2Api", result["credentials_required"])
        self.assertEqual("high", result["risk_level"])
        self.assertTrue(result["reusable_patterns"])
        self.assertTrue(result["potential_raphael_uses"])

    def test_archive_search_finds_known_workflow_name(self) -> None:
        result = n8n_workflow_archive_search(self.config, "Youtube_Automation")
        self.assertEqual(1, result["count"])
        self.assertEqual("WFARCH-D2A37F5A8B", result["results"][0]["workflow_id"])

    def test_archive_summary_is_json_serializable_and_safe(self) -> None:
        result = n8n_workflow_archive_summary(self.config, "WFARCH-D2A37F5A8B")
        text = json.dumps(result)
        self.assertIn("WFARCH-D2A37F5A8B", text)
        self.assertFalse(result["safety"]["workflow_executed"])
        self.assertFalse(result["safety"]["credential_values_stored"])


if __name__ == "__main__":
    unittest.main()
