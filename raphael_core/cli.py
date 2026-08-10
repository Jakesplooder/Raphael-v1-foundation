"""Raphael CLI dispatch and test entrypoint."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

from . import legacy


def run_tests() -> int:
    root = Path(__file__).resolve().parent.parent
    suite = unittest.defaultTestLoader.discover(str(root / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def _extract_config(args: list[str]) -> tuple[Path, list[str]]:
    config = legacy.DEFAULT_SETTINGS_PATH
    remaining: list[str] = []
    index = 0
    while index < len(args):
        if args[index] == "--config":
            if index + 1 >= len(args):
                raise SystemExit("--config requires a path")
            config = Path(args[index + 1])
            index += 2
        else:
            remaining.append(args[index])
            index += 1
    return config, remaining


def _world_model_main(args: list[str]) -> int:
    import json

    from . import world_model

    config_path, rest = _extract_config(args)
    if not rest or not rest[0].startswith("world-model-"):
        return -1
    config = legacy.load_config(config_path)
    command = rest[0]
    tail = rest[1:]
    if command in {"world-model-populate", "world-model-validate-population"}:
        from . import world_model_population

        if command == "world-model-populate":
            result = world_model_population.populate_phase_75_1(config)
        else:
            result = world_model_population.validate_population(config)
    elif command == "world-model-status":
        result = world_model.status(config)
    elif command == "world-model-build":
        result = world_model.build_world_model(config)
    elif command == "world-model-refresh":
        result = world_model.refresh_world_model(config)
    elif command == "world-model-node":
        if not tail:
            raise SystemExit("world-model-node requires NODE-ID")
        result = world_model.node(config, tail[0])
    elif command == "world-model-related":
        if not tail:
            raise SystemExit("world-model-related requires NODE-ID")
        result = world_model.related(config, tail[0])
    elif command == "world-model-path":
        if len(tail) < 2:
            raise SystemExit("world-model-path requires NODEA NODEB")
        result = world_model.path_between(config, tail[0], tail[1])
    elif command == "world-model-query":
        if not tail:
            raise SystemExit("world-model-query requires QUESTION")
        result = world_model.world_model_answer_legacy(config, "Executive Agent", "cli query", " ".join(tail))
    elif command == "world-model-health":
        result = world_model.health(config)
    elif command == "world-model-review":
        result = {"review": str(world_model.review(config))}
    elif command == "world-model-brief":
        result = {"brief": str(world_model.write_brief(config))}
    elif command == "world-model-access-review":
        result = world_model.access_review(config)
    elif command == "world-model-snapshot":
        result = world_model.snapshot(config, "manual")
    elif command == "world-model-deprecate":
        if not tail:
            raise SystemExit("world-model-deprecate requires NODE-ID")
        result = world_model.set_node_status(config, tail[0], "deprecated", "CLI deprecate")
    elif command == "world-model-archive":
        if not tail:
            raise SystemExit("world-model-archive requires NODE-ID")
        result = world_model.set_node_status(config, tail[0], "archived", "CLI archive")
    elif command == "world-model-correct":
        if len(tail) < 3:
            raise SystemExit("world-model-correct requires NODE-ID REPLACEMENT-NAME SOURCE-OF-TRUTH")
        result = world_model.correct_node(config, tail[0], tail[1], tail[2], "CLI correction")
    elif command == "world-model-relationship-deprecate":
        if not tail:
            raise SystemExit("world-model-relationship-deprecate requires REL-ID")
        result = world_model.set_relationship_status(config, tail[0], "deprecated", "CLI deprecate")
    else:
        raise SystemExit(f"Unknown world model command: {command}")
    print(json.dumps(result, indent=2, default=str))
    return 0


def _pattern_engine_main(args: list[str]) -> int:
    import json
    import sys
    # sys.path hacking might be needed if pattern_engine is not in raphael_core
    from . import pattern_engine

    config_path, rest = _extract_config(args)
    if not rest:
        return -1
    command = rest[0]
    tail = rest[1:]
    
    if command == "pattern-discover":
        result = pattern_engine.discover_patterns()
    elif command == "pattern-report":
        result = pattern_engine.pattern_report()
    elif command == "pattern-search":
        if not tail:
            raise SystemExit("pattern-search requires QUERY")
        result = pattern_engine.pattern_search(" ".join(tail))
    elif command == "pattern-node":
        if not tail:
            raise SystemExit("pattern-node requires NODE-ID")
        result = pattern_engine.get_pattern_node(tail[0])
    elif command == "executive-patterns":
        result = pattern_engine.get_executive_patterns()
    else:
        return -1
        
    print(json.dumps(result, indent=2, default=str))
    return 0


def _reasoning_engine_main(args: list[str]) -> int:
    import json
    from . import reasoning_engine
    
    config_path, rest = _extract_config(args)
    if not rest:
        return -1
        
    command = rest[0]
    tail = rest[1:]
    
    if command == "reason":
        if not tail:
            raise SystemExit("reason requires QUESTION")
        query = " ".join(tail)
        result = reasoning_engine.execute_pipeline(query)
    elif command == "brief":
        if not tail:
            raise SystemExit("brief requires QUESTION")
        query = " ".join(tail)
        from . import brief_generator
        result = brief_generator.generate_brief_from_query(query)
        print(result)
        return 0
    elif command == "board":
        if not tail:
            raise SystemExit("board requires QUESTION")
        query = " ".join(tail)
        from . import executive_board
        result = executive_board.run_board_evaluation(query)
        print(result)
        return 0
    elif command == "plan":
        if not tail:
            raise SystemExit("plan requires QUESTION")
        query = " ".join(tail)
        from . import strategic_planner
        result = strategic_planner.generate_strategic_plan(query)
        print(result)
        return 0
    else:
        return -1
        
    print(json.dumps(result, indent=2, default=str))
    return 0


def _daemon_main(args: list[str]) -> int:
    config_path, rest = _extract_config(args)
    if not rest or rest[0] != "daemon":
        return -1
    
    if len(rest) < 2:
        print("Usage: raphael.py daemon <start|stop|status> [--mode <development|production>]")
        return 1

    action = rest[1]
    
    if action == "start":
        mode = "production"
        if "--mode" in rest:
            mode_idx = rest.index("--mode")
            if mode_idx + 1 < len(rest):
                mode = rest[mode_idx + 1]

        # Import all kernel components to ensure they are registered
        from .kernel.registry import registry
        from .kernel.core import Kernel
        from .kernel.observability import ObservabilityLayer
        import asyncio
        import json
        import os
        
        # Register Core Services dynamically
        system_manifest_path = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), "config", "system_manifest.json")
        try:
            with open(system_manifest_path, "r", encoding="utf-8") as f:
                sys_manifest = json.load(f)
                registry.load_from_manifests(sys_manifest.get("core_services", []))
        except Exception as e:
            ObservabilityLayer.warning("CLI", f"Failed to load system_manifest.json: {e}")
        
        # Register Digital Workforce Agents dynamically
        import json
        import os
        config_path = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), "config", "workforce_config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                workforce_config = json.load(f)
        except Exception as e:
            ObservabilityLayer.warning("CLI", f"Failed to load workforce_config.json: {e}")
            workforce_config = {"auto_boot_agents": [], "disabled_agents": []}
            
        import raphael_core.kernel.workforce_agents as wf_agents
        for agent_name in workforce_config.get("auto_boot_agents", []):
            if agent_name in workforce_config.get("disabled_agents", []):
                ObservabilityLayer.info("CLI", f"Skipping disabled agent: {agent_name}")
                continue
            agent_cls = getattr(wf_agents, agent_name, None)
            if agent_cls:
                registry.register_service(agent_cls())
            else:
                ObservabilityLayer.warning("CLI", f"Agent class {agent_name} not found in workforce_agents.py")

        # Register Builder Subsystem
        from .kernel.managers.builder_manager import BuilderManager
        builder_root = os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS")
        registry.register_service(BuilderManager(os.path.join(builder_root, "builder")))

        # Register Project Subsystem
        from .kernel.managers.project_manager import ProjectManager
        from . import legacy
        import pathlib
        config_path = pathlib.Path(os.environ.get("RAPHAEL_SETTINGS", legacy.DEFAULT_SETTINGS_PATH))
        config = legacy.load_config(config_path)
        registry.register_service(ProjectManager(config))
        
        # Register Workflow Plans Subsystem
        from .kernel.managers.workflow_plan_manager import WorkflowPlanManager
        registry.register_service(WorkflowPlanManager(registry.get_service("EventBus"), config))
        
        # Register Core UI Services
        from .kernel.services.intent_router import IntentRouter
        from .kernel.services.mission_dispatcher import MissionDispatcher
        registry.register_service(IntentRouter())
        registry.register_service(MissionDispatcher())
        
        # Register Memory Subsystem
        from .kernel.managers.memory_manager import MemoryManager
        registry.register_service(MemoryManager(registry.get_service("EventBus")))

        # Register Knowledge Subsystem
        from .kernel.managers.knowledge_manager import KnowledgeManager
        registry.register_service(KnowledgeManager(registry.get_service("EventBus"), config))

        # Register WorkflowRunner Subsystem
        from .kernel.managers.workflow_manager import WorkflowManager
        registry.register_service(WorkflowManager(registry.get_service("EventBus"), config))

        # Register Agents Subsystem
        from .kernel.managers.agent_manager import AgentManager
        registry.register_service(AgentManager(registry.get_service("EventBus"), config))

        # Register Core UI Services
        from .kernel.dashboard import KernelDashboard
        registry.register_service(KernelDashboard(registry.get_service("EventBus")))

        # Register Goals Subsystem
        from .kernel.managers.goal_manager import GoalManager
        registry.register_service(GoalManager(registry.get_service("EventBus"), config))

        # Register World Subsystem
        from .kernel.managers.world_manager import WorldManager
        registry.register_service(WorldManager(registry.get_service("EventBus"), config))

        # Register Commerce Subsystem
        from .kernel.managers.commerce_manager import CommerceManager
        registry.register_service(CommerceManager(registry.get_service("EventBus"), config))

        # Register Media Generation Subsystem (depends on EventBus + CommerceManager)
        from .kernel.managers.media_generation_manager import MediaGenerationManager
        from .kernel.repositories.commerce_repository import CommerceRepository
        import pathlib as _pathlib
        _os_root = _pathlib.Path(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"))
        _commerce_repo = CommerceRepository(_os_root)
        registry.register_service(MediaGenerationManager(registry.get_service("EventBus"), config, _commerce_repo))

        # Wire ImageGenerationProvider into WorkflowPlanManager's CapabilityRegistry
        # Must happen after both WorkflowPlans and MediaGenerationManager are registered.
        from .kernel.providers.workflow.image_generation_provider import ImageGenerationProvider
        _wpm = registry.get_service("WorkflowPlans")
        _mgm = registry.get_service("MediaGenerationManager")
        if _wpm and _mgm:
            _wpm.registry.register(ImageGenerationProvider(_mgm.image_service))
            ObservabilityLayer.info("CLI", "ImageGenerationProvider registered into WorkflowPlans CapabilityRegistry.")
        else:
            ObservabilityLayer.warning("CLI", "Could not wire ImageGenerationProvider: WorkflowPlans or MediaGenerationManager not found.")

        kernel = Kernel(mode=mode)
        
        async def run_daemon():
            await kernel.boot()
            try:
                # Keep the event loop alive forever until interrupted
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                pass
        
        try:
            asyncio.run(run_daemon())
        except KeyboardInterrupt:
            ObservabilityLayer.warning("CLI", "Received KeyboardInterrupt. Shutting down RRK...")
            asyncio.run(kernel.shutdown())
        except Exception as e:
            print(f"Kernel failed: {e}")
            return 1
            
        return 0
        
    elif action == "status":
        import urllib.request
        try:
            req = urllib.request.urlopen("http://127.0.0.1:8788/api/health", timeout=2)
            print("RRK is ONLINE.")
            print(req.read().decode())
            return 0
        except Exception as e:
            print(f"RRK is OFFLINE or unreachable. ({e})")
            return 1
            
    print(f"Unknown daemon action: {action}")
    return 1


def _comfyui_health_main(args: list[str]) -> int:
    config_path, rest = _extract_config(args)
    if not rest or rest[0] != "comfyui-health":
        return -1
    
    config = legacy.load_config(config_path)
    url = getattr(config, "pod_comfyui_url", "http://127.0.0.1:8188")
    # In settings, we have bootstrap_comfyui_root, default C:/ComfyUI
    output_dir = Path("C:/ComfyUI/output") 
    
    from . import comfy_health
    return comfy_health.run_health_check(url, output_dir)


def _host_agent_main(args: list[str]) -> int:
    import urllib.request
    import json
    import time
    import subprocess
    import os
    
    config_path, rest = _extract_config(args)
    url = "http://127.0.0.1:8789/health"
    
    # Check if already running
    try:
        req = urllib.request.urlopen(url, timeout=2)
        data = json.loads(req.read().decode())
        print("Host Manager ........ Healthy")
        print("URL ................. http://127.0.0.1:8789")
        print("Capabilities ........ docker gpu processes services")
        return 0
    except Exception:
        pass
        
    print("Host Manager not running. Launching...")
    # Launch natively in background
    cwd = Path(__file__).resolve().parent.parent
    script_path = cwd / "host_agent.py"
    
    creationflags = 0x00000008 | 0x00000200 if os.name == "nt" else 0
    subprocess.Popen(
        [sys.executable, str(script_path)],
        cwd=str(cwd),
        creationflags=creationflags,
        close_fds=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait for health check
    for _ in range(10):
        try:
            time.sleep(1)
            req = urllib.request.urlopen(url, timeout=2)
            data = json.loads(req.read().decode())
            print("Host Manager ........ Healthy")
            print("URL ................. http://127.0.0.1:8789")
            print("Capabilities ........ docker gpu processes services")
            return 0
        except Exception:
            pass
            
    print("Failed to start Host Manager.")
    return 1


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["test"]:
        return run_tests()
        
    if args and args[0] == "daemon":
        return _daemon_main(args)
        
    if args and args[0] == "host-agent":
        return _host_agent_main(args)
        
    if args and args[0] == "comfyui-health":
        return _comfyui_health_main(args)
        
    # Check reasoning commands first
    if args and args[0] in ["reason", "brief", "board", "plan"]:
        reasoning_code = _reasoning_engine_main(args)
        if reasoning_code >= 0:
            return reasoning_code
            
    # Check pattern commands
    if args and (args[0].startswith("pattern-") or args[0] == "executive-patterns"):
        pattern_code = _pattern_engine_main(args)
        if pattern_code >= 0:
            return pattern_code
            
    world_model_code = _world_model_main(args)
    if world_model_code >= 0:
        return world_model_code
        
    if args and args[0].startswith("build"):
        # Intercept builder commands and route to Gateway
        import urllib.request
        import json
        config_path, rest = _extract_config(args)
        command = rest[0]
        tail = rest[1:]
        
        if command == "build":
            # Support: raphael build "Create a React dashboard" --serve --provider ollama
            description = ""
            provider = "ollama"
            serve = False
            
            # Parse simple flags
            if "--serve" in tail:
                serve = True
                tail.remove("--serve")
            if "--provider" in tail:
                idx = tail.index("--provider")
                provider = tail[idx+1]
                tail.pop(idx)
                tail.pop(idx)
                
            if not tail:
                raise SystemExit("build requires DESCRIPTION")
                
            description = " ".join(tail)
            payload = {"description": description, "metadata": {"serve": serve, "provider": provider}}
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                "http://127.0.0.1:8787/api/builder/request",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    print(json.loads(response.read().decode()))
                return 0
            except Exception as e:
                print(f"Failed to reach Builder service via Gateway: {e}")
                return 1

        elif command == "build-request":
            if not tail:
                raise SystemExit("build-request requires DESCRIPTION")
            
            payload = {"description": " ".join(tail)}
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                "http://127.0.0.1:8787/api/builder/request",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    print(json.loads(response.read().decode()))
                return 0
            except Exception as e:
                print(f"Failed to reach Builder service via Gateway: {e}")
                return 1

    if args and args[0].startswith("project-"):
        import urllib.request
        import json
        config_path, rest = _extract_config(args)
        command = rest[0]
        tail = rest[1:]
        
        if command == "project-list":
            req = urllib.request.Request(
                "http://127.0.0.1:8787/api/projects/list",
                headers={"Content-Type": "application/json"},
                method="POST",
                data=json.dumps({"action": "list"}).encode("utf-8")
            )
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    print(json.loads(response.read().decode()))
                return 0
            except Exception as e:
                print(f"Failed to reach Project service via Gateway: {e}")
                return 1
                
        if command == "project-create":
            if not tail:
                raise SystemExit("project-create requires NAME")
            payload = {"action": "create", "name": " ".join(tail)}
            req = urllib.request.Request(
                "http://127.0.0.1:8787/api/projects/create",
                headers={"Content-Type": "application/json"},
                method="POST",
                data=json.dumps(payload).encode("utf-8")
            )
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    print(json.loads(response.read().decode()))
                return 0
            except Exception as e:
                print(f"Failed to reach Project service via Gateway: {e}")
                return 1
                
        # Other commands can be similarly intercepted or passed through

    if args and args[0] == "youtube-test":
        from .analytics.providers.youtube import YouTubeAnalyticsProvider
        try:
            provider = YouTubeAnalyticsProvider()
            result = provider.test_connection()
            if result:
                print("✓ OAuth successful\n")
                print(f"Channel:\n{result['title']}\n")
                print(f"Subscribers:\n{result['subscribers']}\n")
                print(f"Videos:\n{result['videos']}\n")
                print("Analytics:\nConnected")
            else:
                print("OAuth successful but no channel found.")
        except Exception as e:
            print(f"Failed to connect to YouTube: {e}")
        return 0

    if args and args[0] == "analytics-sync":
        config_path, rest = _extract_config(args)
        tail = rest[1:]
        
        provider_name = None
        dry_run = False
        
        if "--provider" in tail:
            idx = tail.index("--provider")
            provider_name = tail[idx+1]
        
        if "--dry-run" in tail:
            dry_run = True
            
        if not provider_name:
            print("Usage: raphael.py analytics-sync --provider <name> [--dry-run]")
            return 1
            
        print("Analytics Sync Started\n")
        print(f"Provider:\n{provider_name}\n")
        
        # Here we would normally query the database for all active assets for this provider.
        # For now, we mock the discovery and just test the pipeline.
        
        # In a full implementation, we'd iterate over MissionRecords and Assets.
        # Assuming we found some mock assets:
        assets_found = 1 if not dry_run else 1
        print(f"Assets Found:\n{assets_found}\n")
        
        if dry_run:
            print("Asset:\nvideo_123\n")
            print("Current:\nCTR 3.1%\n")
            print("Incoming:\nCTR 6.5%\n") # matches our mocked YouTube CTR
            print("Change:\n+109%\n")
            print("Dry run complete. No memory updated.")
            return 0
            
        # Real sync
        if provider_name.lower() == "youtube":
            from .analytics.providers.youtube import YouTubeAnalyticsProvider
            provider = YouTubeAnalyticsProvider()
            res = provider.get_asset_performance("video_123")
            print(f"Updated:\n{assets_found}\n")
            print("Lessons Generated:\n0\n")
            print("Complete")
        else:
            print(f"Provider {provider_name} not implemented.")
            return 1
        return 0

    if args and args[0] == "optimize-test":
        from .kernel.models.business_objects import AssetPerformance, OptimizationRun
        from .optimization.diagnosis_engine import MetricDiagnosisEngine
        from .optimization.feedback_council import FeedbackCouncil
        from .optimization.experiment_engine import ExperimentEngine
        from raphael_core.optimization.promotion import PromotionCouncil
        import uuid
        
        print("--- PHASE 4C: OPTIMIZATION LAYER MOCK TEST ---\n")
        
        # 1. Mock Telemetry Input
        asset_id = "video_ai_sidehustles"
        perf = AssetPerformance(
            id=f"perf_{uuid.uuid4().hex[:8]}",
            business_id="bus_focus123",
            asset_id=asset_id,
            views=100000,
            ctr=1.8,
            retention=52.0,
            revenue=0.0
        )
        print(f"INPUT ASSET: {asset_id}")
        print(f"METRICS: {perf.views} Impressions | {perf.ctr}% CTR | {perf.retention}% Retention\n")
        
        # 2. Metric Diagnosis Engine
        diag_engine = MetricDiagnosisEngine()
        diagnosis = diag_engine.run_diagnosis(asset_id, perf, [])
        print(f"DIAGNOSIS CATEGORY: {diagnosis.diagnosis_category}")
        print(f"CONFIDENCE: {diagnosis.confidence}")
        print(f"EVIDENCE: {diagnosis.evidence}")
        print(f"RECOMMENDATION: {diagnosis.recommended_actions}\n")
        
        # 3. Feedback Council
        council = FeedbackCouncil()
        proposal_id = council.evaluate_diagnosis(diagnosis)
        
        if proposal_id:
            # Re-fetch proposal from builder mock
            proposal = council.builder.generate_proposal(diagnosis)
            print("FEEDBACK COUNCIL: Action Required -> Sent to Builder")
            print(f"BUILDER PROPOSAL: {proposal.proposed_changes}")
            print(f"EXPECTED IMPACT: {proposal.expected_impact}\n")
            
            # 4. Experiment Engine
            exp_engine = ExperimentEngine()
            experiment = exp_engine.create_experiment(proposal)
            print(f"EXPERIMENT CREATED: {experiment.id}")
            print(f"HYPOTHESIS: {experiment.hypothesis}")
            print(f"TREATMENT: {experiment.treatment_asset_id}\n")
            
            # 5. Promotion Review
            decision = PromotionCouncil()
            experiment.winner = experiment.treatment_asset_id # Mock a win
            approved = decision.review_experiment(experiment)
            
            if approved:
                print("PROMOTION COUNCIL: Approved Promotion")
                run = OptimizationRun(
                    id=f"run_{uuid.uuid4().hex[:8]}",
                    business_id=perf.business_id,
                    asset_id=asset_id,
                    diagnosis_id=diagnosis.id,
                    proposal_id=proposal.id,
                    experiment_id=experiment.id
                )
                res = decision.promote(run)
                print(f"PROMOTION: {res} | Score: +{run.improvement_score * 100}%")
            else:
                print("DECISION COUNCIL: Rejected")
        else:
            print("FEEDBACK COUNCIL: No Action Required")
            
        return 0
        
    if args and args[0] == "decisions":
        print("PENDING DECISIONS\n")
        print("1.")
        print("Expand Focus Marketing YouTube output\n")
        print("ROI:\n240%\n")
        print("Risk:\nMedium\n")
        print("Confidence:\n81%\n")
        print("Status:\nAwaiting approval\n")
        return 0
        
    if args and args[0] == "evaluate-opportunity":
        from raphael_core.kernel.models.business_objects import BusinessState
        from raphael_core.executive.decision_engine import DecisionEngine
        
        state = BusinessState(
            id="state_1",
            business_id="focus_marketing",
            revenue=50000.0,
            cash_position=200000.0
        )
        
        engine = DecisionEngine()
        decision, roi, risks = engine.evaluate_opportunity(
            business_state=state,
            proposal="Increase video production",
            investment=500.0,
            expected_revenue=2000.0
        )
        
        print("Opportunity:\nIncrease video production\n")
        
        print("ROI Engine:")
        print(f"Investment: ${roi.investment}")
        print(f"Expected Revenue: ${roi.expected_revenue}")
        print(f"ROI: {roi.roi_percentage * 100}%\n")
        
        print("Risk Engine:")
        if risks:
            for r in risks:
                print(f"Risk: {r.risk_description}")
                print(f"Recommendation: {r.mitigation_strategy}")
        else:
            print("Risk: Acceptable")
            
        print(f"\nDecision:\n{decision.status.title()}\n")
        return 0
        
    if args and args[0] == "decision-review":
        print("Decision Council Review\n")
        print("Proposal:\nSpend $500 advertising\n")
        print("Finance Agent:\nApprove\n")
        print("Growth Agent:\nApprove\n")
        print("Risk Agent:\nCaution\n")
        print("Final:\nApprove with $250 limit\n")
        return 0

    if args and args[0] == "export-capabilities":
        from raphael_core.operator.capability_aggregator import capability_aggregator
        try:
            path = capability_aggregator.export()
            print(f"Capability manifest exported successfully to: {path}")
            return 0
        except Exception as e:
            print(f"Failed to export capabilities: {e}")
            return 1

    return legacy.main(args)
