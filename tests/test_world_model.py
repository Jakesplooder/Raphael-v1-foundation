from __future__ import annotations

import datetime as dt
import json
import unittest

from raphael_core import legacy, world_model
from tests.support import TempRaphael


class WorldModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = legacy.load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def test_build_creates_governed_connected_graph(self) -> None:
        result = world_model.build_world_model(self.config)

        self.assertGreaterEqual(result["node_count"], 18)
        self.assertGreaterEqual(result["relationship_count"], 18)
        self.assertGreaterEqual(result["event_count"], 1)
        self.assertGreaterEqual(result["hypothesis_count"], 1)
        self.assertTrue(result["minimum_viable_graph_connected"])

        health = world_model.health(self.config)
        self.assertEqual([], health["active_nodes_missing_source_reference"])
        self.assertGreaterEqual(health["quality"]["nodes_confidence_gt_0_7_ratio"], 0.8)
        self.assertGreaterEqual(health["quality"]["relationships_with_evidence_ratio"], 0.8)

    def test_revenue_query_preserves_hypothesis_state(self) -> None:
        world_model.build_world_model(self.config)

        answer = world_model.world_model_answer(
            self.config,
            "Executive Agent",
            "executive brief",
            "What business is most likely to generate revenue?",
        )

        self.assertTrue(answer["allowed"])
        self.assertEqual("hypothesis", answer["epistemic_status"])
        self.assertEqual("active", answer["hypothesis_status"])
        self.assertIn("confidence", answer)
        self.assertTrue(answer["supporting_evidence"])

    def test_conflicted_relationship_query_surfaces_review_warning(self) -> None:
        world_model.build_world_model(self.config)
        model = world_model.load_model(self.config)
        project = next(row for row in model["nodes"] if row["node_type"] == "Project")
        clone = dict(project)
        clone["node_id"] = project["node_id"] + "-ALT"
        clone["status"] = "paused"
        clone["confidence"] = 0.82
        clone["source_reference"] = "test-conflict"
        model["nodes"].append(clone)
        conflicts = world_model.detect_conflicts(model["nodes"], model["relationships"])
        world_model.save_model(self.config, model["nodes"], model["relationships"], model["events"], model["hypotheses"], conflicts)

        answer = world_model.world_model_answer(
            self.config,
            "Executive Agent",
            "status check",
            f"What is the status of {project['name']}?",
        )

        self.assertEqual("conflict", answer["epistemic_status"])
        self.assertIn("conflict_warning", answer)
        self.assertTrue(answer["competing_evidence"])
        self.assertIn("Aaron review", answer["recommendation"])

    def test_dormant_relationship_excluded_from_default_traversal_but_auditable(self) -> None:
        world_model.build_world_model(self.config)
        model = world_model.load_model(self.config)
        rel = model["relationships"][0]
        rel["confidence"] = 0.12
        rel["confidence_state"] = "dormant"
        rel["status"] = "dormant"
        world_model.save_model(self.config, model["nodes"], model["relationships"], model["events"], model["hypotheses"], [])

        default_related = world_model.related(self.config, rel["from_node"])
        audit_related = world_model.related(self.config, rel["from_node"], include_dormant=True)

        self.assertFalse(any(row["relationship"]["relationship_id"] == rel["relationship_id"] for row in default_related["related"]))
        self.assertTrue(any(row["relationship"]["relationship_id"] == rel["relationship_id"] for row in audit_related["related"]))

    def test_confidence_decay_marks_stale_relationship_dormant(self) -> None:
        world_model.build_world_model(self.config)
        model = world_model.load_model(self.config)
        rel = next(row for row in model["relationships"] if row["relationship_type"] == "BLOCKED_BY") if any(row["relationship_type"] == "BLOCKED_BY" for row in model["relationships"]) else model["relationships"][0]
        rel["relationship_type"] = "BLOCKED_BY"
        rel["confidence"] = 0.22
        rel["updated_at"] = (dt.datetime.now() - dt.timedelta(days=45)).isoformat(timespec="seconds")
        world_model.save_model(self.config, model["nodes"], model["relationships"], model["events"], model["hypotheses"], [])

        decayed = world_model.load_model(self.config)["relationships"]
        changed = next(row for row in decayed if row["relationship_id"] == rel["relationship_id"])
        self.assertIn(changed["confidence_state"], {"dormant", "deprecated"})

    def test_cli_commands_are_available(self) -> None:
        result = self.os.run("world-model-build")
        self.assertEqual(0, result.returncode, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["minimum_viable_graph_connected"])

        query = self.os.run("world-model-query", "What business is most likely to generate revenue?")
        self.assertEqual(0, query.returncode, query.stderr or query.stdout)
        self.assertEqual("hypothesis", json.loads(query.stdout)["epistemic_status"])


if __name__ == "__main__":
    unittest.main()
