"""
Breadth-First Search (BFS) Algorithm
Syllabus: Graph algorithms: Breadth First Search, Queue applications
Used by: Pinky (BFS Ghost)

Properties:
- Time Complexity: O(V + E)
- Space Complexity: O(V)
- Optimality: Guarantees shortest path in unweighted graphs.
- Data Structure: CircularQueue (FIFO)
"""

import time
from dsa.queue import CircularQueue

def bfs_search(graph, start: tuple, target: tuple, forbidden_first: tuple = None):
    """
    Execute Breadth-First Search from start to target.
    
    Args:
        graph: Graph object with get_neighbors(u) method.
        start: (row, col) coordinates of start node.
        target: (row, col) coordinates of destination node.
        forbidden_first: Optional (row, col) to exclude as first step to prevent 180° reversal.
        
    Returns:
        dict: {
            'path': list of (row, col) tuples from start to target,
            'visited': list of visited (row, col) in exploration order,
            'nodes_expanded': int,
            'max_ds_size': int (peak queue memory),
            'execution_time_ms': float,
            'algorithm': 'BFS'
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
            'algorithm': 'BFS'
        }

    queue = CircularQueue(initial_capacity=128)
    queue.enqueue(start)
    
    visited = set([start])
    visited_order = [start]
    parent = {start: None}
    
    nodes_expanded = 0
    max_queue_size = 1
    found = False

    while not queue.is_empty():
        curr = queue.dequeue()
        nodes_expanded += 1

        if curr == target:
            found = True
            break

        neighbors = graph.get_neighbors(curr)
        for nxt in neighbors:
            # Prevent 180-degree immediate reversal unless dead-end
            if curr == start and nxt == forbidden_first and len(neighbors) > 1:
                continue

            if nxt not in visited:
                visited.add(nxt)
                visited_order.append(nxt)
                parent[nxt] = curr
                queue.enqueue(nxt)
                if queue.size() > max_queue_size:
                    max_queue_size = queue.size()

    # Reconstruct path by following parent pointers backwards
    path = []
    if found:
        curr = target
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path.reverse()  # Start to target

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return {
        'path': path,
        'visited': visited_order,
        'nodes_expanded': nodes_expanded,
        'max_ds_size': max_queue_size,
        'execution_time_ms': elapsed_ms,
        'algorithm': 'BFS'
    }
