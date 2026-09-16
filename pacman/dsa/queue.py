"""
Circular Queue Data Structure (FIFO - First-In, First-Out)
Syllabus: Queue representation, Insertion & deletion in Queue
Used by: Pinky (BFS Ghost) for breadth-first shortest path search.
"""

class QueueUnderflowError(Exception):
    """Raised when attempting to dequeue from an empty queue."""
    pass


class CircularQueue:
    """
    Circular Array implementation of a Queue.
    Avoids memory wastage by wrapping indices around using modulo arithmetic.
    
    Attributes:
        _capacity (int): Total allocated capacity.
        _data (list): Internal contiguous linear array.
        _front (int): Index of the first element.
        _rear (int): Index of the last element inserted.
        _count (int): Current number of stored elements.
    """

    def __init__(self, initial_capacity: int = 64):
        self._capacity = max(16, initial_capacity)
        self._data = [None] * self._capacity
        self._front = 0
        self._rear = -1
        self._count = 0

    def enqueue(self, item) -> None:
        """
        Add an item to the rear of the queue.
        Time Complexity: O(1) amortized.
        """
        if self._count == self._capacity:
            self._resize(self._capacity * 2)

        self._rear = (self._rear + 1) % self._capacity
        self._data[self._rear] = item
        self._count += 1

    def dequeue(self):
        """
        Remove and return the item from the front of the queue.
        Time Complexity: O(1).
        Raises: QueueUnderflowError if queue is empty.
        """
        if self.is_empty():
            raise QueueUnderflowError("Cannot dequeue from an empty Queue.")

        item = self._data[self._front]
        self._data[self._front] = None  # Facilitate garbage collection
        self._front = (self._front + 1) % self._capacity
        self._count -= 1

        # Shrink array if utilization drops below 25%
        if 0 < self._count <= self._capacity // 4 and self._capacity > 64:
            self._resize(self._capacity // 2)

        return item

    def peek(self):
        """
        Return the front item without removing it.
        Time Complexity: O(1).
        """
        if self.is_empty():
            return None
        return self._data[self._front]

    def is_empty(self) -> bool:
        """Return True if queue is empty, False otherwise."""
        return self._count == 0

    def is_full(self) -> bool:
        """Return True if queue is full at current capacity."""
        return self._count == self._capacity

    def size(self) -> int:
        """Return current number of items in the queue."""
        return self._count

    def clear(self) -> None:
        """Reset the queue to empty state."""
        self._data = [None] * self._capacity
        self._front = 0
        self._rear = -1
        self._count = 0

    def _resize(self, new_capacity: int) -> None:
        """
        Unroll circular array and re-index into a newly sized array.
        Time Complexity: O(N).
        """
        new_data = [None] * new_capacity
        for i in range(self._count):
            new_data[i] = self._data[(self._front + i) % self._capacity]
        self._data = new_data
        self._front = 0
        self._rear = self._count - 1
        self._capacity = new_capacity

    def to_list(self) -> list:
        """Return a snapshot of items in FIFO order."""
        return [self._data[(self._front + i) % self._capacity] for i in range(self._count)]

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return f"CircularQueue(size={self._count}, front={self.peek()})"
