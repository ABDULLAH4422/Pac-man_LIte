"""
Depth-First Search (DFS) Algorithm
Syllabus: Graph algorithms: Depth First Search, Stack representation & applications
Used by: Blinky (DFS Ghost)

Properties:
- Time Complexity: O(V + E)
- Space Complexity: O(V)
- Optimality: Does NOT guarantee shortest path; explores deep branches first.
- Data Structure: ArrayStack (LIFO)
"""

import time
from dsa.stack import ArrayStack

def dfs_search(graph, start: tuple, target: tuple, forbidden_first: tuple = None):
    """
    Execute Depth-First Search from start to target using an explicit ArrayStack.
    
    Args:
        graph: Graph object with get_neighbors(u) method.
        start: (row, col) coordinates of start node.
        target: (row, col) coordinates of destination node.
        forbidden_first: Optional (row, col) of previous tile to prevent 180° immediate reversal.
        
    Returns:
        dict: {
            'path': list of (row, col) tuples from start to target,
            'visited': list of visited (row, col) in exploration order,
            'nodes_expanded': int,
            'max_ds_size': int (peak stack memory),
            'execution_time_ms': float,
            'algorithm': 'DFS'
        }
    """
    start_time = time.perf_counter()

    if start == target:
        return {
            'path': [start],
            'visited': [start],
            'nodes_expanded': 1,
            'max_ds_size': 0,
            'execution_time_ms': 0.0,
            'algorithm': 'DFS'
        }

    stack = ArrayStack(initial_capacity=128)
    stack.push(start)

    visited = set()
    visited_order = []
    parent = {start: None}

    nodes_expanded = 0
    max_stack_size = 1
    found = False

    while not stack.is_empty():
        curr = stack.pop()

        if curr in visited:
            continue

        visited.add(curr)
        visited_order.append(curr)
        nodes_expanded += 1

        if curr == target:
            found = True
            break

        # Retrieve neighbors from graph
        neighbors = graph.get_neighbors(curr)
        
        # Filter out forbidden reverse step on initial move unless it's a dead end
        candidate_neighbors = []
        for nxt in neighbors:
            if curr == start and nxt == forbidden_first and len(neighbors) > 1:
                continue
            if nxt not in visited:
                candidate_neighbors.append(nxt)

        # Sort candidate neighbors by distance to target descending
        # Since Stack is LIFO, the element with smallest distance is pushed last and popped FIRST
        candidate_neighbors.sort(
            key=lambda n: abs(n[0] - target[0]) + abs(n[1] - target[1]),
            reverse=True
        )

        for nxt in candidate_neighbors:
            if nxt not in parent:
                parent[nxt] = curr
            stack.push(nxt)
            if stack.size() > max_stack_size:
                max_stack_size = stack.size()

    # Reconstruct path
    path = []
    if found:
        curr = target
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)
        path.reverse()

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return {
        'path': path,
        'visited': visited_order,
        'nodes_expanded': nodes_expanded,
        'max_ds_size': max_stack_size,
        'execution_time_ms': elapsed_ms,
        'algorithm': 'DFS'
    }
