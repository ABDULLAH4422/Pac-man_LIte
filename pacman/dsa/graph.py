"""
Graph Data Structure (Adjacency List Representation)
Syllabus: Representation of Graphs, BFS, DFS, Shortest Path
Used for: Converting the 2D maze into a formal mathematical graph G = (V, E)
where V = walkable corridor tiles/intersections, E = direct passable connections.
"""

class Graph:
    """
    Adjacency List Graph representation.
    Maps each vertex u to a list of neighboring vertices (and edge weights).
    """

    def __init__(self):
        # Dictionary mapping vertex -> list of neighbor vertices
        self._adj = {}
        self._edge_count = 0

    def add_node(self, u) -> None:
        """
        Add a vertex u to the graph if not already present.
        Time Complexity: O(1).
        """
        if u not in self._adj:
            self._adj[u] = []

    def add_edge(self, u, v, weight: float = 1.0, bidirectional: bool = True) -> None:
        """
        Add an edge between vertex u and vertex v.
        Time Complexity: O(1).
        """
        self.add_node(u)
        self.add_node(v)

        if v not in self._adj[u]:
            self._adj[u].append(v)
            self._edge_count += 1

        if bidirectional:
            if u not in self._adj[v]:
                self._adj[v].append(u)

    def get_neighbors(self, u) -> list:
        """
        Return the list of adjacent neighbors for vertex u.
        Time Complexity: O(1).
        """
        return self._adj.get(u, [])

    def has_node(self, u) -> bool:
        """Check if vertex u exists in the graph."""
        return u in self._adj

    def has_edge(self, u, v) -> bool:
        """Check if direct edge exists between u and v."""
        return u in self._adj and v in self._adj[u]

    def degree(self, u) -> int:
        """Return the number of connected edges for vertex u."""
        return len(self._adj.get(u, []))

    def node_count(self) -> int:
        """Return total vertices |V|."""
        return len(self._adj)

    def edge_count(self) -> int:
        """Return total edges |E|."""
        return self._edge_count

    def get_all_nodes(self) -> list:
        """Return list of all vertices in G."""
        return list(self._adj.keys())

    def clear(self) -> None:
        """Reset graph."""
        self._adj.clear()
        self._edge_count = 0

    def __repr__(self) -> str:
        return f"Graph(|V|={self.node_count()}, |E|={self._edge_count})"
