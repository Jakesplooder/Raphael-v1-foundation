from __future__ import annotations

import json
import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.support import TempRaphael


class CommandBusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()

    def tearDown(self) -> None:
        self.os.close()

    def test_build_requests_route_through_confirmation(self) -> None:
        result = self.os.run("command-bus-test", "build me a simple calculator")
        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("build_with_council", payload["intent"])
        self.assertTrue(payload["requires_confirmation"])

    def test_blocked_command_has_no_cli_args(self) -> None:
        result = self.os.run("command-bus-test", "execute arbitrary shell command")
        payload = json.loads(result.stdout)
        self.assertEqual("blocked", payload["status"])
        self.assertEqual([], payload["cli_args"])

    def test_pod_success_queues_next_confirmed_pipeline_action(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("pod_chain_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        state: dict[str, object] = {}
        outputs = [
            r"Created POD concept: C:\vault\PODCON-ABC123 - july.md",
            r"Generated POD design prompts: C:\vault\PODCON-ABC123 - Design Prompts.md",
            r"Created POD generation request: C:\vault\PODGEN-REQ123 - PODCON-ABC123 - sdxl.md",
        ]

        with patch.object(
            bus.voice_gateway,
            "run_raphael",
            side_effect=[
                subprocess.CompletedProcess([], 0, stdout=output, stderr="") for output in outputs
            ],
        ):
            first = bus._run_command(
                "create concept", "create concept", "pod_concept", "pod_design_studio",
                ["pod-concept", "4th of July shirts"], "command_bus_confirm", state,
            )
            self.assertEqual("needs_confirmation", first["status"])
            self.assertEqual(["pod-prompt", "PODCON-ABC123"], state["pending_command_bus_route"]["cli_args"])

            second = bus.confirm(str(state["pending_confirmation_key"]), state)
            self.assertEqual("needs_confirmation", second["status"])
            self.assertEqual(
                ["pod-generation-request", "PODCON-ABC123", "sdxl"],
                state["pending_command_bus_route"]["cli_args"],
            )

            third = bus.confirm(str(state["pending_confirmation_key"]), state)
            self.assertEqual("needs_confirmation", third["status"])
            self.assertEqual(["pod-generate", "PODGEN-REQ123"], state["pending_command_bus_route"]["cli_args"])

    def test_typography_and_inkscape_routes_require_confirmation(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("typography_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        cases = {
            "create typography LAND OF THE FREE": ["pod-typography-create", "land of the free"],
            "compose pod design C:\\RaphaelOS\\PODStudio\\input\\art.png PODTYPE-ABC123": [
                "pod-compose-design", "c:\\raphaelos\\podstudio\\input\\art.png", "PODTYPE-ABC123"
            ],
            "export SVG PODCOMP-ABC123": ["pod-svg-export", "PODCOMP-ABC123"],
            "export print-ready design PODCOMP-ABC123": ["pod-print-export", "PODCOMP-ABC123"],
        }
        for phrase, expected in cases.items():
            with self.subTest(phrase=phrase):
                result = bus.route(phrase, "test", {})
                self.assertEqual("needs_confirmation", result["status"])
                self.assertEqual(expected, result["cli_args"])

    def test_bootstrap_destructive_controls_require_confirmation(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("bootstrap_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        for phrase, command in [
            ("restart bootstrap services", "bootstrap-restart"),
            ("stop bootstrap services", "bootstrap-stop"),
            ("install Raphael startup", "bootstrap-install-startup"),
            ("remove Raphael startup", "bootstrap-remove-startup"),
        ]:
            with self.subTest(phrase=phrase):
                result = bus.route(phrase, "test", {})
                self.assertEqual("needs_confirmation", result["status"])
                self.assertEqual(command, result["cli_args"][0])

    def test_bootstrap_health_and_open_are_not_confirmation_gated(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("bootstrap_read_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        for phrase, command in [
            ("run bootstrap health", "bootstrap-health"),
            ("open dashboard", "bootstrap-open-dashboard"),
            ("start bootstrap services", "bootstrap-start"),
        ]:
            with self.subTest(phrase=phrase):
                route = bus.voice_gateway.route_intent(phrase, bus.voice_config)
                self.assertFalse(route.confirmation_required)
                self.assertEqual(command, route.command[0])

    def test_service_manager_routes_are_allowlisted_and_confirmed(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("service_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        for phrase, expected in [
            ("start ComfyUI", ["service-start", "comfyui"]),
            ("start creative stack", ["service-start", "creative"]),
            ("restart failed services", ["service-restart-failed"]),
            ("restart Raphael services", ["service-restart", "managed"]),
        ]:
            with self.subTest(phrase=phrase):
                result = bus.route(phrase, "test", {})
                self.assertEqual("needs_confirmation", result["status"])
                self.assertEqual(expected, result["cli_args"])

    def test_docker_routes_are_allowlisted_and_confirmed(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("docker_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        for phrase, expected in [
            ("start Qdrant", ["docker-start", "qdrant"]),
            ("restart Qdrant", ["docker-restart", "qdrant"]),
            ("stop Qdrant", ["docker-stop", "qdrant"]),
        ]:
            with self.subTest(phrase=phrase):
                result = bus.route(phrase, "test", {})
                self.assertEqual("needs_confirmation", result["status"])
                self.assertEqual(expected, result["cli_args"])
        status = bus.route("docker health", "test", {})
        self.assertEqual("routed", status["status"])
        self.assertEqual(["docker-health"], status["cli_args"])

    def test_self_healing_routes_and_voice_phrases(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("self_healing_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        read_cases = {
            "check system health": ["self-healing-status"],
            "Raphael check yourself": ["observe-system"],
            "detect issues": ["detect-issues"],
            "Raphael diagnose issues": ["detect-issues"],
            "show reliability brief": ["reliability-brief"],
        }
        for phrase, expected in read_cases.items():
            with self.subTest(phrase=phrase):
                route = bus.voice_gateway.route_intent(phrase, bus.voice_config)
                self.assertEqual(expected, route.command)
                self.assertFalse(route.confirmation_required)
        write_cases = {
            "repair issue ISSUE-20260624-ABCDEF12": ["repair-plan", "ISSUE-20260624-ABCDEF12"],
            "approve repair REPAIR-20260624-ABCDEF12": ["repair-approve", "REPAIR-20260624-ABCDEF12"],
            "repair approved issue REPAIR-20260624-ABCDEF12": ["repair-run", "REPAIR-20260624-ABCDEF12"],
        }
        for phrase, expected in write_cases.items():
            with self.subTest(phrase=phrase):
                result = bus.route(phrase, "test", {})
                self.assertEqual("needs_confirmation", result["status"])
                self.assertEqual(expected, result["cli_args"])

    def test_workflow_archive_ids_route_to_n8n_studio_not_general_chat(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("workflow_archive_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        cases = {
            "what can you do with WFARCH-D2A37F5A8B": ["workflow-archive-show", "WFARCH-D2A37F5A8B"],
            "summarize workflow archive WFARCH-D2A37F5A8B": ["workflow-archive-summary", "WFARCH-D2A37F5A8B"],
            "search workflow archive Youtube_Automation": ["workflow-archive-search", "youtube_automation"],
        }
        for phrase, expected in cases.items():
            with self.subTest(phrase=phrase):
                route = bus.voice_gateway.route_intent(phrase, bus.voice_config)
                self.assertEqual(expected, route.command)
                self.assertFalse(route.confirmation_required)

    def test_searxng_and_research_stack_require_confirmation(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("research_stack_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        for phrase, expected in [
            ("start SearXNG", ["searxng-start"]),
            ("start research stack", ["service-start", "research"]),
        ]:
            result = bus.route(phrase, "test", {})
            self.assertEqual("needs_confirmation", result["status"])
            self.assertEqual(expected, result["cli_args"])

    def test_workflow_runner_routes_execution_reads_and_cancel_safely(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("workflow_runner_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        execute = bus.route("run workflow daily-executive-brief", "test", {})
        self.assertEqual("needs_confirmation", execute["status"])
        self.assertEqual(["workflow-execute", "daily-executive-brief"], execute["cli_args"])
        cancel = bus.route("cancel workflow WFEXEC-20260621-ABCDEF12", "test", {})
        self.assertEqual("needs_confirmation", cancel["status"])
        self.assertEqual(["workflow-cancel", "WFEXEC-20260621-ABCDEF12"], cancel["cli_args"])

    def test_internet_queries_route_through_confirmation(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("internet_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        for phrase in [
            "search the web for FastAPI release notes",
            "look up current Etsy trends",
            "latest POD niches",
            "software docs for Python packaging",
        ]:
            with self.subTest(phrase=phrase):
                result = bus.route(phrase, "test", {})
                self.assertEqual("needs_confirmation", result["status"])
                self.assertEqual("internet-headless-search", result["cli_args"][0])

    def test_internet_login_and_external_actions_stay_blocked(self) -> None:
        result = self.os.run("command-bus-test", "log in to Etsy and upload a listing")
        payload = json.loads(result.stdout)
        self.assertEqual("blocked", payload["status"])
        self.assertEqual([], payload["cli_args"])

    def test_internet_followups_use_latest_request(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("internet_followup_command_bus_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        cases = {
            "show snippets": ["internet-latest-snippets"],
            "show sources": ["internet-latest-snippets"],
            "raw JSON": ["internet-raw-json", "LATEST"],
            "what did it find": ["internet-latest-overview"],
            "summarize that": ["internet-latest-overview"],
            "save to knowledge": ["internet-save-to-knowledge", "LATEST"],
        }
        for phrase, expected in cases.items():
            with self.subTest(phrase=phrase):
                result = bus.route(phrase, "test", {})
                self.assertEqual(expected, result["cli_args"])

    def test_local_pod_workflows_are_not_misclassified_as_spending(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("local_pod_safety_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        cases = {
            "perform a local POD Studio test": ["pod-workflow", "perform a local POD Studio test"],
            "generate POD design using ComfyUI": ["pod-workflow", "generate POD design using ComfyUI"],
            "create Etsy listing draft": ["pod-listing-draft", "LATEST"],
        }
        for phrase, expected in cases.items():
            with self.subTest(phrase=phrase):
                result = bus.route(phrase, "dashboard", {})
                self.assertIn(result["status"], {"needs_confirmation", "routed"})
                self.assertEqual(expected, result["cli_args"])
                self.assertNotIn("spending", result["safety_reason"].lower())

    def test_full_pod_requests_use_workflow_orchestrator_priority(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("pod_workflow_routing_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        cases = [
            "Perform a local POD Studio test with typography and SVG export",
            "Start a POD Studio workflow for a camping shirt",
            "Research current trends and create a POD shirt using Flux, ComfyUI, and Inkscape",
        ]
        with patch.object(
            bus.voice_gateway,
            "run_raphael",
            return_value=subprocess.CompletedProcess(
                [], 0,
                stdout=json.dumps({
                    "workflow_id": "PODFLOW-20260621-ABCDEF12",
                    "status": "awaiting_confirmation",
                    "completed_stage": 1,
                    "stage_count": 13,
                    "next_stage_number": 3,
                    "next_stage": "create concept",
                    "message": "POD workflow started. Stage 1/13 complete. Next: create concept. Say confirm to continue.",
                    "ids": {},
                    "outputs": {},
                }),
                stderr="",
            ),
        ):
            for phrase in cases:
                with self.subTest(phrase=phrase):
                    state: dict[str, object] = {}
                    result = bus.route(phrase, "dashboard", state)
                    self.assertEqual("needs_confirmation", result["status"])
                    self.assertEqual("pod-workflow-continue", state["pending_command_bus_route"]["cli_args"][0])
                    self.assertNotEqual("build_with_council", result["intent"])

    def test_show_detail_and_typography_next_step_routes(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("detail_route_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        routes = {
            "Show details for BUILD-20260621-ABC123": ["build-status", "BUILD-20260621-ABC123"],
            "Review DELIB-20260621-ABC123": ["deliberation-show", "DELIB-20260621-ABC123"],
            "Review PLAN-20260621-ABC123": ["execution-plan-show", "PLAN-20260621-ABC123"],
        }
        for phrase, expected in routes.items():
            result = bus.route(phrase, "test", {})
            self.assertEqual(expected, result["cli_args"])
        typography = bus.route("Generate PODTYPE-ABC123", "test", {})
        self.assertEqual("routed", typography["status"])
        self.assertEqual([], typography["cli_args"])
        self.assertIn("pod-compose-design", typography["full_response"])

    def test_confirm_recovers_latest_persistent_pod_workflow(self) -> None:
        path = Path("C:/RaphaelOS/command_bus.py")
        spec = importlib.util.spec_from_file_location("pod_workflow_recovery_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        bus.settings["runtime_path"] = str(self.os.runtime)
        root = self.os.runtime / "PODStudio" / "workflows"
        root.mkdir(parents=True, exist_ok=True)
        workflow_id = "PODFLOW-20260621-ABCDEF12"
        (root / f"{workflow_id}.json").write_text(json.dumps({
            "workflow_id": workflow_id,
            "status": "awaiting_confirmation",
            "next_stage": 3,
        }), encoding="utf-8")
        completed = subprocess.CompletedProcess([], 0, stdout=json.dumps({
            "workflow_id": workflow_id,
            "status": "completed",
            "message": "POD workflow complete.",
        }), stderr="")
        with patch.object(bus.voice_gateway, "run_raphael", return_value=completed) as run:
            result = bus.confirm("", {})
        self.assertEqual("routed", result["status"])
        run.assert_called_once_with(
            ["pod-workflow-continue", workflow_id],
            confirmed=True,
        )

    def test_external_pod_commerce_actions_remain_blocked(self) -> None:
        cases = [
            "publish to Etsy",
            "upload to Printify",
            "buy samples",
            "spend $20 on ads",
            "Create a POD shirt design and publish to Etsy",
            "Generate POD artwork and upload to Printify",
        ]
        for phrase in cases:
            with self.subTest(phrase=phrase):
                result = self.os.run("command-bus-test", phrase)
                payload = json.loads(result.stdout)
                self.assertEqual("blocked", payload["status"])
                self.assertEqual([], payload["cli_args"])
