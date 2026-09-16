"""
Binary Search Tree (BST)
Syllabus: Tree representation in memory, Traversing binary tree, BST, Insertion & Deletion
Used for: Managing and querying high score leaderboards with O(log N) lookup.
"""

class BSTNode:
    """Node in a Binary Search Tree."""
    def __init__(self, key: int, value=None):
        self.key = key          # Sorting key (e.g. score)
        self.value = value      # Associated payload (e.g. player name / date)
        self.left = None
        self.right = None

    def __repr__(self):
        return f"BSTNode(key={self.key}, val={self.value})"


class BinarySearchTree:
    """
    Binary Search Tree implementation.
    Maintains property: left.key <= node.key < right.key (or strictly less).
    """

    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, key: int, value=None) -> None:
        """
        Insert a new (key, value) pair into the BST.
        Average Time Complexity: O(log N), Worst Case: O(N).
        """
        self.root = self._insert_recursive(self.root, key, value)
        self._size += 1

    def _insert_recursive(self, node: BSTNode, key: int, value) -> BSTNode:
        if node is None:
            return BSTNode(key, value)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        else:
            # Equal or greater scores go to right subtree
            node.right = self._insert_recursive(node.right, key, value)

        return node

    def search(self, key: int):
        """
        Search for a node with the given key.
        Average Time Complexity: O(log N).
        """
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return curr.value
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def inorder_traversal(self) -> list:
        """
        In-order traversal (Left, Root, Right).
        Returns elements sorted in ASCENDING order.
        Time Complexity: O(N).
        """
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: BSTNode, result: list) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)

    def get_top_n(self, n: int = 5) -> list:
        """
        Reverse in-order traversal (Right, Root, Left).
        Returns top N highest scores in DESCENDING order.
        Time Complexity: O(N).
        """
        result = []
        self._reverse_inorder(self.root, result, n)
        return result

    def _reverse_inorder(self, node: BSTNode, result: list, limit: int) -> None:
        if node is None or len(result) >= limit:
            return
        self._reverse_inorder(node.right, result, limit)
        if len(result) < limit:
            result.append((node.key, node.value))
        self._reverse_inorder(node.left, result, limit)

    def find_min(self):
        """Find minimum key in BST."""
        if self.root is None:
            return None
        curr = self.root
        while curr.left is not None:
            curr = curr.left
        return curr.key, curr.value

    def find_max(self):
        """Find maximum key in BST."""
        if self.root is None:
            return None
        curr = self.root
        while curr.right is not None:
            curr = curr.right
        return curr.key, curr.value

    def size(self) -> int:
        """Return total number of nodes in tree."""
        return self._size

    def is_empty(self) -> bool:
        """Return True if tree is empty."""
        return self.root is None

    def clear(self) -> None:
        """Reset tree."""
        self.root = None
        self._size = 0
