import asyncio
from typing import Callable, Any
from raphael_core.kernel.repositories.world_repository import WorldRepository

class VerificationResult:
    def __init__(self, passed: bool, message: str, metrics: dict):
        self.passed = passed
        self.message = message
        self.metrics = metrics

async def wait_for_events(delay: float = 0.5):
    await asyncio.sleep(delay)

async def verify_duplicate_safety(repo: WorldRepository, write_fn: Callable, *args) -> VerificationResult:
    """
    Standard graph-count diff test for any domain write path.
    Proves that a duplicate exact write call does NOT inflate the graph node/relationship count.
    """
    initial_nodes = len(repo.get_nodes())
    initial_rels = len(repo.get_relationships())
    
    # Call 1
    write_fn(*args)
    await wait_for_events()
    
    post_run_1_nodes = len(repo.get_nodes())
    post_run_1_rels = len(repo.get_relationships())
    
    diff_nodes_1 = post_run_1_nodes - initial_nodes
    diff_rels_1 = post_run_1_rels - initial_rels
    
    # Call 2 (Duplicate)
    write_fn(*args)
    await wait_for_events()
    
    post_run_2_nodes = len(repo.get_nodes())
    post_run_2_rels = len(repo.get_relationships())
    
    diff_nodes_2 = post_run_2_nodes - post_run_1_nodes
    diff_rels_2 = post_run_2_rels - post_run_1_rels
    
    passed = diff_nodes_2 == 0 and diff_rels_2 == 0
    message = "Duplicate safety verified." if passed else f"Duplicate safety FAILED. Diff: {diff_nodes_2} nodes, {diff_rels_2} rels."
    
    return VerificationResult(
        passed=passed,
        message=message,
        metrics={
            "initial": (initial_nodes, initial_rels),
            "post_1": (post_run_1_nodes, post_run_1_rels),
            "diff_1": (diff_nodes_1, diff_rels_1),
            "post_2": (post_run_2_nodes, post_run_2_rels),
            "diff_2": (diff_nodes_2, diff_rels_2)
        }
    )

async def verify_update_safety(repo: WorldRepository, write_fn: Callable, entity_name: str, check_fn: Callable, first_args: tuple, second_args: tuple) -> VerificationResult:
    """
    Standard confidence/value-diff test for any domain write path.
    Proves that a non-identical update correctly overwrites graph state without silently discarding data.
    `check_fn` should return the exact value expected to be updated (e.g. confidence float)
    """
    initial_nodes = len(repo.get_nodes())
    
    # Call 1 (Base write)
    write_fn(*first_args)
    await wait_for_events()
    
    post_run_1_nodes = len(repo.get_nodes())
    val_1 = check_fn(repo, entity_name)
    
    # Call 2 (Update write)
    write_fn(*second_args)
    await wait_for_events()
    
    post_run_2_nodes = len(repo.get_nodes())
    val_2 = check_fn(repo, entity_name)
    
    node_diff = post_run_2_nodes - post_run_1_nodes
    
    passed = node_diff == 0 and val_1 != val_2
    
    if passed:
        message = f"Update safety verified. Value mutated successfully ({val_1} -> {val_2}) without node duplication."
    else:
        message = f"Update safety FAILED. Node diff: {node_diff}. Value diff: {val_1} -> {val_2}."
        
    return VerificationResult(
        passed=passed,
        message=message,
        metrics={
            "val_1": val_1,
            "val_2": val_2,
            "node_diff": node_diff
        }
    )
