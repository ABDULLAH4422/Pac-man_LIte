"""
Doubly Linked List (Two-way List)
Syllabus: Linked list & representation, Traversing, Searching, Insertion & Deletion, Two-way lists
Used for: Real-time path breadcrumbs, entity history, dynamic pellet lists.
"""

class ListNode:
    """Node in a Doubly Linked List."""
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"ListNode({self.data})"


class DoublyLinkedList:
    """
    Two-way linked list maintaining head and tail pointers.
    Provides O(1) insertion/deletion at both ends and linear traversal.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._count = 0

    def append(self, data) -> ListNode:
        """
        Insert an element at the tail of the list.
        Time Complexity: O(1).
        """
        node = ListNode(data)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._count += 1
        return node

    def prepend(self, data) -> ListNode:
        """
        Insert an element at the head of the list.
        Time Complexity: O(1).
        """
        node = ListNode(data)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._count += 1
        return node

    def pop_front(self):
        """
        Remove and return data from the head.
        Time Complexity: O(1).
        """
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is not None:
            self.head.prev = None
        else:
            self.tail = None
        self._count -= 1
        return data

    def pop_back(self):
        """
        Remove and return data from the tail.
        Time Complexity: O(1).
        """
        if self.tail is None:
            return None
        data = self.tail.data
        self.tail = self.tail.prev
        if self.tail is not None:
            self.tail.next = None
        else:
            self.head = None
        self._count -= 1
        return data

    def remove(self, data) -> bool:
        """
        Search and delete the first node matching data.
        Time Complexity: O(N).
        """
        curr = self.head
        while curr is not None:
            if curr.data == data:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next

                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev

                self._count -= 1
                return True
            curr = curr.next
        return False

    def find(self, data) -> bool:
        """
        Search for an element in the linked list.
        Time Complexity: O(N).
        """
        curr = self.head
        while curr is not None:
            if curr.data == data:
                return True
            curr = curr.next
        return False

    def clear(self) -> None:
        """Empty the linked list."""
        self.head = None
        self.tail = None
        self._count = 0

    def size(self) -> int:
        """Return total elements in list."""
        return self._count

    def is_empty(self) -> bool:
        """Return True if list has no nodes."""
        return self._count == 0

    def to_list(self) -> list:
        """
        Traverse list forward from head to tail.
        Time Complexity: O(N).
        """
        res = []
        curr = self.head
        while curr is not None:
            res.append(curr.data)
            curr = curr.next
        return res

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.data
            curr = curr.next

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return f"DoublyLinkedList(size={self._count}, elements={self.to_list()[:5]}...)"
