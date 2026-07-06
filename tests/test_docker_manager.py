from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from raphael_core import docker_manager
from raphael_core.config import load_config
from tests.support import TempRaphael


class DockerManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)
        self.config.docker_enabled = True

    def tearDown(self) -> None:
        self.os.close()

    def test_registry_is_allowlisted_and_localhost_only(self) -> None:
        rows = docker_manager.load_registry(self.config)["services"]
        self.assertEqual({"qdrant", "n8n", "postgres", "redis", "searxng"}, {row["service_id"] for row in rows})
        for row in rows:
            self.assertTrue(all(port.startswith("127.0.0.1:") for port in row["ports"]))
            self.assertTrue(row["container_name"].startswith("raphael-"))

    def test_status_gives_clear_docker_desktop_result(self) -> None:
        completed = subprocess.CompletedProcess(
            ["docker"], 0, '{"Version":"29.0.1","Platform":{"Name":"Docker Desktop"}}', ""
        )
        with patch("raphael_core.docker_manager._run", return_value=completed):
            result = docker_manager.docker_status(self.config)
        self.assertTrue(result["available"])
        self.assertEqual("29.0.1", result["version"])

    def test_start_creates_only_allowlisted_labeled_local_container(self) -> None:
        calls: list[list[str]] = []

        def fake_run(args: list[str], **_kwargs):
            calls.append(args)
            if args[1:3] == ["image", "inspect"]:
                return subprocess.CompletedProcess(args, 0, "[]", "")
            if args[1] == "create":
                return subprocess.CompletedProcess(args, 0, "abc123456789", "")
            return subprocess.CompletedProcess(args, 0, "ok", "")

        with (
            patch("raphael_core.docker_manager.docker_status", return_value={"available": True}),
            patch("raphael_core.docker_manager._inspect_container", return_value=None),
            patch("raphael_core.docker_manager._run", side_effect=fake_run),
            patch("raphael_core.docker_manager.docker_health", return_value={"services": [{"healthy": True}]}),
        ):
            result = docker_manager.docker_start(self.config, "qdrant", confirmed=True)
        self.assertEqual("created_and_started", result["result"])
        create = next(args for args in calls if args[1] == "create")
        self.assertIn("raphael.managed=true", create)
        self.assertIn("raphael.service_id=qdrant", create)
        self.assertIn("127.0.0.1:6333:6333", create)
        self.assertNotIn("0.0.0.0:6333:6333", create)

    def test_unlabeled_container_is_never_stopped_or_restarted(self) -> None:
        info = {"Config": {"Labels": {}, "Image": "qdrant/qdrant"}, "State": {"Running": True, "Status": "running"}}
        with (
            patch("raphael_core.docker_manager._inspect_container", return_value=info),
            patch("raphael_core.docker_manager._run") as run,
        ):
            stopped = docker_manager.docker_stop(self.config, "qdrant", confirmed=True)
            restarted = docker_manager.docker_restart(self.config, "qdrant", confirmed=True)
        self.assertEqual("not_managed", stopped["result"])
        self.assertEqual("not_managed", restarted["result"])
        run.assert_not_called()

    def test_unknown_service_and_destructive_operations_are_blocked(self) -> None:
        with self.assertRaises(KeyError):
            docker_manager.get_service(self.config, "unknown-image")
        with self.assertRaises(RuntimeError):
            docker_manager._run(["docker", "prune"])
        with self.assertRaises(RuntimeError):
            docker_manager._run(["docker", "exec", "raphael-qdrant", "sh"])

    def test_stop_command_does_not_remove_container_or_volume(self) -> None:
        info = {
            "Id": "abc123456789",
            "Config": {"Labels": {"raphael.managed": "true", "raphael.service_id": "qdrant"}, "Image": "qdrant/qdrant"},
            "State": {"Running": True, "Status": "running"},
        }
        completed = subprocess.CompletedProcess(["docker"], 0, "raphael-qdrant", "")
        with (
            patch("raphael_core.docker_manager._inspect_container", return_value=info),
            patch("raphael_core.docker_manager._run", return_value=completed) as run,
        ):
            result = docker_manager.docker_stop(self.config, "qdrant", confirmed=True)
        self.assertEqual("stopped", result["result"])
        args = run.call_args.args[0]
        self.assertEqual("stop", args[1])
        self.assertNotIn("rm", args)
        self.assertNotIn("volume", args)
