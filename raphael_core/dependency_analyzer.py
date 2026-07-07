from typing import List, Dict, Any, Tuple

class ConstitutionalViolationError(Exception):
    pass

def detect_cycles(project_id: str, adj: dict) -> List[List[str]]:
    """
    Returns list of cycles found in dependency graph.
    If any cycles exist, critical_path() should not run.
    Instead surface a ConstitutionalViolationError with the cycle.
    """
    visited = set()
    path = []
    cycles = []
    
    def dfs(node_id: str):
        if node_id in path:
            cycle_start = path.index(node_id)
            cycles.append(path[cycle_start:] + [node_id])
            return
        if node_id in visited:
            return
        path.append(node_id)
        for dep in adj.get("outbound", {}).get(node_id, {}).get("DEPENDS_ON", []):
            dfs(dep["to_node"])
        path.pop()
        visited.add(node_id)
    
    dfs(project_id)
    return cycles

def find_critical_path(project_id: str, world_model: Dict[str, Any], adj: dict) -> Dict[str, Any]:
    """
    Returns the critical path through project dependencies.
    The critical path is the longest dependency chain —
    shortening it is the highest-leverage optimization.
    """
    cycles = detect_cycles(project_id, adj)
    if cycles:
        raise ConstitutionalViolationError(f"Circular dependency detected: {' -> '.join(cycles[0])}")
        
    # BFS/DFS traversal to find longest path
    # Simplified mock for implementation
    longest_path = [project_id]
    total_effort = 10  # Mock effort
    bottleneck_node = project_id
    
    # In a real implementation, this would compute true path weights based on task effort estimates
    outbound_deps = adj.get("outbound", {}).get(project_id, {}).get("DEPENDS_ON", [])
    if outbound_deps:
        # Mocking finding a deep dependency
        bottleneck_node = outbound_deps[0]["to_node"]
        longest_path.append(bottleneck_node)
        total_effort += 5
        
    return {
        "path_nodes": longest_path,
        "total_effort_weeks": total_effort,
        "bottleneck_node": bottleneck_node
    }
