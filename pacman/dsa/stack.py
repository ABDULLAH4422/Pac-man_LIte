"""
Stack Data Structure (LIFO - Last-In, First-Out)
Syllabus: Stack representation & applications, PUSH and POP operations on stack
Used by: Blinky (DFS Ghost) for path exploration and backtracking.
"""

class StackUnderflowError(Exception):
    """Raised when attempting to pop from an empty stack."""
    pass


class ArrayStack:
    """
    Fixed / dynamically resizable array-based stack implementation.
    
    Attributes:
        _capacity (int): Initial allocated capacity.
        _data (list): Internal contiguous linear array.
        _top (int): Pointer/index to the top element (-1 when empty).
    """

    def __init__(self, initial_capacity: int = 64):
        self._capacity = max(16, initial_capacity)
        self._data = [None] * self._capacity
        self._top = -1

    def push(self, item) -> None:
        """
        Push an item onto the top of the stack.
        Time Complexity: O(1) amortized.
        """
        # Dynamic resizing if array is full (linear array reallocation)
        if self._top + 1 >= self._capacity:
            self._resize(self._capacity * 2)

        self._top += 1
        self._data[self._top] = item

    def pop(self):
        """
        Remove and return the top item from the stack.
        Time Complexity: O(1).
        Raises: StackUnderflowError if stack is empty.
        """
        if self.is_empty():
            raise StackUnderflowError("Cannot pop from an empty Stack.")

        item = self._data[self._top]
        self._data[self._top] = None  # Facilitate garbage collection
        self._top -= 1

        # Shrink array if utilization drops below 25%
        if 0 < self._top + 1 <= self._capacity // 4 and self._capacity > 64:
            self._resize(self._capacity // 2)

        return item

    def peek(self):
        """
        Return the top item without removing it.
        Time Complexity: O(1).
        """
        if self.is_empty():
            return None
        return self._data[self._top]

    def is_empty(self) -> bool:
        """Return True if the stack contains no elements, False otherwise."""
        return self._top == -1

    def size(self) -> int:
        """Return the current number of elements in the stack."""
        return self._top + 1

    def clear(self) -> None:
        """Reset the stack to an empty state."""
        self._data = [None] * self._capacity
        self._top = -1

    def _resize(self, new_capacity: int) -> None:
        """
        Resize internal linear array to new_capacity.
        Time Complexity: O(N).
        """
        new_data = [None] * new_capacity
        for i in range(self._top + 1):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def to_list(self) -> list:
        """Return a snapshot of items in stack from bottom to top."""
        return [self._data[i] for i in range(self._top + 1)]

    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return f"ArrayStack(size={self.size()}, top={self.peek()})"
