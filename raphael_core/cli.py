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
        from .kernel.event_bus import EventBus
        from .kernel.job_system import JobSystem
        from .kernel.calendar import ExecutiveCalendar
        from .kernel.health import HealthMonitor
        from .kernel.healing import SelfHealingRuntime
        from .kernel.dashboard import KernelDashboard
        from .kernel.core import Kernel
        from .kernel.observability import ObservabilityLayer
        from .world_model import WorldModelService
        import asyncio

        # Register Core Services
        registry.register_service(EventBus())
        registry.register_service(JobSystem())
        registry.register_service(ExecutiveCalendar())
        registry.register_service(HealthMonitor())
        registry.register_service(SelfHealingRuntime())
        registry.register_service(KernelDashboard())
        registry.register_service(WorldModelService())

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


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["test"]:
        return run_tests()
        
    if args and args[0] == "daemon":
        return _daemon_main(args)
        
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
    return legacy.main(args)
