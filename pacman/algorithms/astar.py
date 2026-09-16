"""
A* (A-Star) Pathfinding Algorithm
Syllabus: Shortest Path, Priority Queues & Heaps, Heuristic Graph Search
Used by: Inky (A* Ghost)

Properties:
- Evaluation Function: f(n) = g(n) + h(n)
  - g(n): Exact cost from start to current node n.
  - h(n): Admissible heuristic estimate from n to target (Manhattan distance).
- Optimality: Guaranteed shortest path since Manhattan distance is admissible & consistent on grid mazes.
- Data Structure: MinHeapPriorityQueue
"""

import time
from dsa.priority_queue import MinHeapPriorityQueue

def manhattan_distance(a: tuple, b: tuple) -> float:
    """Admissible grid heuristic: |r1 - r2| + |c1 - c2|."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_search(graph, start: tuple, target: tuple, forbidden_first: tuple = None, heuristic=manhattan_distance):
    """
    Execute A* Search from start to target.
    
    Args:
        graph: Graph object with get_neighbors(u) method.
        start: (row, col) coordinates of start node.
        target: (row, col) coordinates of destination node.
        forbidden_first: Optional (row, col) to exclude as first step to prevent 180° reversal.
        heuristic: Heuristic function h(u, v).
        
    Returns:
        dict: {
            'path': list of (row, col) tuples from start to target,
            'visited': list of visited (row, col) in exploration order,
            'nodes_expanded': int,
            'max_ds_size': int (peak priority queue memory),
            'execution_time_ms': float,
            'algorithm': 'A*'
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
            'algorithm': 'A*'
        }

    pq = MinHeapPriorityQueue()
    h_start = heuristic(start, target)
    pq.insert(start, priority=h_start)

    g_score = {start: 0.0}
    parent = {start: None}
    visited_order = []
    closed_set = set()

    nodes_expanded = 0
    max_pq_size = 1
    found = False

    while not pq.is_empty():
        curr = pq.extract_min()

        if curr in closed_set:
            continue

        closed_set.add(curr)
        visited_order.append(curr)
        nodes_expanded += 1

        if curr == target:
            found = True
            break

        curr_g = g_score[curr]
        neighbors = graph.get_neighbors(curr)

        for nxt in neighbors:
            # Prevent 180-degree immediate reversal unless dead-end
            if curr == start and nxt == forbidden_first and len(neighbors) > 1:
                continue

            tentative_g = curr_g + 1.0  # Unit step cost

            if nxt not in g_score or tentative_g < g_score[nxt]:
                g_score[nxt] = tentative_g
                parent[nxt] = curr
                f_nxt = tentative_g + heuristic(nxt, target)
                pq.insert(nxt, priority=f_nxt)

                if pq.size() > max_pq_size:
                    max_pq_size = pq.size()

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
        'max_ds_size': max_pq_size,
        'execution_time_ms': elapsed_ms,
        'algorithm': 'A*'
    }
