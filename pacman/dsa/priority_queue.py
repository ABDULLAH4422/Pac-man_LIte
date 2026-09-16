"""
Binary Min-Heap Priority Queue
Syllabus: Priority Queues, heaps, shortest path (Dijkstra, A*)
Used by: Inky (A* Ghost) to dynamically select candidate nodes with minimum f(n) = g(n) + h(n).
"""

class PriorityQueueEmptyError(Exception):
    """Raised when attempting to extract from an empty priority queue."""
    pass


class MinHeapPriorityQueue:
    """
    Array-based Binary Min-Heap Priority Queue.
    Maintains the Min-Heap Property: heap[parent] <= heap[child].
    
    Each node stores a tuple: (priority, tie_breaker, item)
    """

    def __init__(self):
        self._heap = []
        self._counter = 0  # Tie-breaker to ensure stable FIFO ordering on equal priorities

    def insert(self, item, priority: float) -> None:
        """
        Insert an element with an associated numeric priority.
        Time Complexity: O(log N).
        """
        entry = (priority, self._counter, item)
        self._counter += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def extract_min(self):
        """
        Remove and return the item with the minimum priority key.
        Time Complexity: O(log N).
        Raises: PriorityQueueEmptyError if queue is empty.
        """
        if self.is_empty():
            raise PriorityQueueEmptyError("Cannot extract from an empty Priority Queue.")

        # Swap root with last element
        min_entry = self._heap[0]
        last_entry = self._heap.pop()

        if self._heap:
            self._heap[0] = last_entry
            self._sift_down(0)

        return min_entry[2]  # Return item

    def extract_min_with_priority(self):
        """
        Remove and return (item, priority).
        Time Complexity: O(log N).
        """
        if self.is_empty():
            raise PriorityQueueEmptyError("Cannot extract from an empty Priority Queue.")

        min_entry = self._heap[0]
        last_entry = self._heap.pop()

        if self._heap:
            self._heap[0] = last_entry
            self._sift_down(0)

        return min_entry[2], min_entry[0]

    def peek_min(self):
        """
        Inspect the item with the lowest priority without removing it.
        Time Complexity: O(1).
        """
        if self.is_empty():
            return None
        return self._heap[0][2]

    def is_empty(self) -> bool:
        """Return True if heap contains no elements."""
        return len(self._heap) == 0

    def size(self) -> int:
        """Return total number of elements in the priority queue."""
        return len(self._heap)

    def clear(self) -> None:
        """Reset heap."""
        self._heap.clear()
        self._counter = 0

    def _sift_up(self, idx: int) -> None:
        """
        Bubble element up to restore min-heap invariant.
        Time Complexity: O(log N).
        """
        child_idx = idx
        while child_idx > 0:
            parent_idx = (child_idx - 1) // 2
            # Compare (priority, counter)
            if self._heap[child_idx][0] < self._heap[parent_idx][0] or (
                self._heap[child_idx][0] == self._heap[parent_idx][0] and 
                self._heap[child_idx][1] < self._heap[parent_idx][1]
            ):
                self._heap[child_idx], self._heap[parent_idx] = self._heap[parent_idx], self._heap[child_idx]
                child_idx = parent_idx
            else:
                break

    def _sift_down(self, idx: int) -> None:
        """
        Push element down to restore min-heap invariant.
        Time Complexity: O(log N).
        """
        n = len(self._heap)
        curr = idx
        while True:
            left = 2 * curr + 1
            right = 2 * curr + 2
            smallest = curr

            if left < n and (
                self._heap[left][0] < self._heap[smallest][0] or (
                    self._heap[left][0] == self._heap[smallest][0] and 
                    self._heap[left][1] < self._heap[smallest][1]
                )
            ):
                smallest = left

            if right < n and (
                self._heap[right][0] < self._heap[smallest][0] or (
                    self._heap[right][0] == self._heap[smallest][0] and 
                    self._heap[right][1] < self._heap[smallest][1]
                )
            ):
                smallest = right

            if smallest != curr:
                self._heap[curr], self._heap[smallest] = self._heap[smallest], self._heap[curr]
                curr = smallest
            else:
                break

    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return f"MinHeapPriorityQueue(size={self.size()})"
