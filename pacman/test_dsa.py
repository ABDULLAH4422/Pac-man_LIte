"""
Unit Tests for Custom Data Structures & Algorithms
Validates Stack, Queue, PriorityQueue/MinHeap, DoublyLinkedList, BST, Graph, BFS, DFS, A*, and Sorting.
"""

import sys
import os

# Ensure workspace root is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dsa.stack import ArrayStack, StackUnderflowError
from dsa.queue import CircularQueue, QueueUnderflowError
from dsa.priority_queue import MinHeapPriorityQueue, PriorityQueueEmptyError
from dsa.linked_list import DoublyLinkedList
from dsa.graph import Graph
from dsa.bst import BinarySearchTree
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.astar import astar_search
from algorithms.sorting import quick_sort, merge_sort

def test_stack():
    print("[TEST] Testing ArrayStack...")
    stack = ArrayStack(initial_capacity=4)
    assert stack.is_empty()
    assert stack.size() == 0

    for i in range(10):
        stack.push(i)
    assert stack.size() == 10
    assert stack.peek() == 9

    popped = [stack.pop() for _ in range(10)]
    assert popped == list(reversed(range(10)))
    assert stack.is_empty()

    try:
        stack.pop()
        assert False, "Should have raised StackUnderflowError"
    except StackUnderflowError:
        pass
    print("  -> ArrayStack passed!")


def test_queue():
    print("[TEST] Testing CircularQueue...")
    queue = CircularQueue(initial_capacity=4)
    assert queue.is_empty()

    for i in range(8):
        queue.enqueue(i)
    assert queue.size() == 8
    assert queue.peek() == 0

    dequeued = [queue.dequeue() for _ in range(8)]
    assert dequeued == list(range(8))
    assert queue.is_empty()

    # Test wraparound behavior
    for i in range(15):
        queue.enqueue(i)
        assert queue.dequeue() == i
    assert queue.is_empty()

    try:
        queue.dequeue()
        assert False, "Should have raised QueueUnderflowError"
    except QueueUnderflowError:
        pass
    print("  -> CircularQueue passed!")


def test_min_heap_priority_queue():
    print("[TEST] Testing MinHeapPriorityQueue...")
    pq = MinHeapPriorityQueue()
    assert pq.is_empty()

    items = [(45, 'Task A'), (12, 'Task B'), (89, 'Task C'), (5, 'Task D'), (23, 'Task E')]
    for prio, item in items:
        pq.insert(item, priority=prio)

    extracted = []
    while not pq.is_empty():
        item, prio = pq.extract_min_with_priority()
        extracted.append(prio)

    assert extracted == sorted([p for p, _ in items]), f"Got {extracted}"
    print("  -> MinHeapPriorityQueue passed!")


def test_doubly_linked_list():
    print("[TEST] Testing DoublyLinkedList...")
    dll = DoublyLinkedList()
    assert dll.is_empty()

    dll.append(1)
    dll.append(2)
    dll.prepend(0)
    # 0 <-> 1 <-> 2
    assert dll.to_list() == [0, 1, 2]
    assert dll.size() == 3

    assert dll.find(1) is True
    assert dll.find(99) is False

    assert dll.remove(1) is True
    assert dll.to_list() == [0, 2]

    assert dll.pop_front() == 0
    assert dll.pop_back() == 2
    assert dll.is_empty()
    print("  -> DoublyLinkedList passed!")


def test_bst():
    print("[TEST] Testing BinarySearchTree...")
    bst = BinarySearchTree()
    scores = [(350, "Alice"), (720, "Bob"), (150, "Charlie"), (990, "Dave"), (500, "Eve")]

    for score, name in scores:
        bst.insert(score, name)

    inorder = bst.inorder_traversal()
    inorder_keys = [k for k, v in inorder]
    assert inorder_keys == sorted([s for s, _ in scores]), f"Got {inorder_keys}"

    top_3 = bst.get_top_n(3)
    assert [k for k, v in top_3] == [990, 720, 500]
    assert bst.search(720) == "Bob"
    assert bst.search(9999) is None
    print("  -> BinarySearchTree passed!")


def test_graph_and_pathfinding():
    print("[TEST] Testing Graph, BFS, DFS, and A*...")
    # Create a 5x5 grid graph
    # 0 . . . 4
    # . # # . .
    # . . . . .
    g = Graph()
    for r in range(5):
        for c in range(5):
            # Add obstacle at (1, 1), (1, 2)
            if (r, c) in {(1, 1), (1, 2)}:
                continue
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 5 and 0 <= nc < 5 and (nr, nc) not in {(1, 1), (1, 2)}:
                    g.add_edge((r, c), (nr, nc))

    start = (0, 0)
    target = (4, 4)

    # 1. BFS
    bfs_res = bfs_search(g, start, target)
    assert bfs_res['path'][0] == start
    assert bfs_res['path'][-1] == target
    bfs_len = len(bfs_res['path'])

    # 2. A*
    astar_res = astar_search(g, start, target)
    assert astar_res['path'][0] == start
    assert astar_res['path'][-1] == target
    astar_len = len(astar_res['path'])

    # A* and BFS must find the exact shortest path length
    assert bfs_len == astar_len, f"BFS len {bfs_len} != A* len {astar_len}"

    # 3. DFS
    dfs_res = dfs_search(g, start, target)
    assert dfs_res['path'][0] == start
    assert dfs_res['path'][-1] == target

    print(f"  -> Path lengths: BFS={bfs_len}, A*={astar_len}, DFS={len(dfs_res['path'])}")
    print(f"  -> Nodes expanded: BFS={bfs_res['nodes_expanded']}, A*={astar_res['nodes_expanded']}, DFS={dfs_res['nodes_expanded']}")
    print("  -> Graph & Pathfinding Algorithms passed!")


def test_sorting():
    print("[TEST] Testing QuickSort & MergeSort...")
    arr = [42, 12, 88, 3, 27, 95, 14, 50]
    sorted_asc = sorted(arr)
    sorted_desc = sorted(arr, reverse=True)

    assert quick_sort(arr) == sorted_asc
    assert quick_sort(arr, reverse=True) == sorted_desc

    assert merge_sort(arr) == sorted_asc
    assert merge_sort(arr, reverse=True) == sorted_desc
    print("  -> QuickSort & MergeSort passed!")


if __name__ == "__main__":
    print("========================================")
    print("Running Pac-Man Lite DSA Test Suite")
    print("========================================")
    test_stack()
    test_queue()
    test_min_heap_priority_queue()
    test_doubly_linked_list()
    test_bst()
    test_graph_and_pathfinding()
    test_sorting()
    print("========================================")
    print("ALL DATA STRUCTURES & ALGORITHMS PASSED!")
    print("========================================")
