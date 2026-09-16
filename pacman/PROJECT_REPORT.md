# Pac-Man Lite: Data Structures & Algorithms Project Report
**Course**: ECE 2103: Data Structure & Algorithms (Lab: ECE 2104)  
**Project Title**: Pac-Man Lite - Interactive Game & Real-Time DSA Pathfinding Visualizer

---

## 1. Executive Summary & Objective

**Pac-Man Lite** is an interactive, academic-grade 2D arcade game built from the ground up to demonstrate core linear and non-linear data structures, graph theory, and pathfinding search algorithms in a live, real-time environment.

The player navigates Pac-Man through a 2D maze matrix, consuming pellets and power-pellets while evading four distinct AI ghosts. Each ghost is engineered using a different pathfinding algorithm powered by a custom data structure implemented from scratch in pure Python without reliance on black-box libraries (`collections.deque`, `heapq`, etc.).

---

## 2. ECE 2103 Course Syllabus Alignment

| Syllabus Topic | Game Component | Implementation File | Mathematical / Asymptotic Detail |
| :--- | :--- | :--- | :--- |
| **Linear Array & Matrices** | 2D Maze Grid & collision map | [`world/maze.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/world/maze.py) | $21 \times 21$ static matrix, row/col index mapping |
| **Stack (PUSH & POP)** | DFS ghost path exploration & backtrack | [`dsa/stack.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/dsa/stack.py) | `ArrayStack`: $O(1)$ push/pop, dynamic array resizing |
| **Queue (FIFO, Enqueue & Dequeue)** | BFS shortest-path search | [`dsa/queue.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/dsa/queue.py) | `CircularQueue`: $O(1)$ enqueue/dequeue via modulo arithmetic |
| **Priority Queue & Heaps** | A\* search open set | [`dsa/priority_queue.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/dsa/priority_queue.py) | `MinHeapPriorityQueue`: $O(\log N)$ insert, $O(\log N)$ extract-min |
| **Linked List (Two-way)** | Dynamic path tracking & breadcrumbs | [`dsa/linked_list.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/dsa/linked_list.py) | `DoublyLinkedList`: $O(1)$ head/tail operations, bi-directional pointers |
| **Graph Representation** | Maze converted to graph $G=(V,E)$ | [`dsa/graph.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/dsa/graph.py) | Adjacency List: $O(1)$ edge query, space $O(\|V\| + \|E\|)$ |
| **Tree & BST** | Leaderboard & high-score storage | [`dsa/bst.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/dsa/bst.py) | `BinarySearchTree`: $O(\log N)$ search/insert, $O(N)$ sorted in-order traversal |
| **Sorting Algorithms** | Leaderboard rank sorting | [`algorithms/sorting.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/algorithms/sorting.py) | `quick_sort` $O(N \log N)$, `merge_sort` $O(N \log N)$ stable |
| **Complexity Analysis** | Live Algorithm HUD & Telemetry | [`world/visualizer.py`](file:///c:/Academic/2.1st%20sem/ECE%202104/pacman/world/visualizer.py) | Real-time computation of nodes expanded, memory size, and time (ms) |

---

## 3. Ghost AI Architecture & Algorithm Comparison

### 3.1 Pinky - Breadth-First Search (BFS)
- **Data Structure**: `CircularQueue` (FIFO)
- **Optimality**: **Optimal** for unweighted graphs; mathematically guaranteed to find the shortest path in terms of steps.
- **Frontier Expansion**: Expands radially outward like ripples across water.
- **Complexity**: Time: $O(V + E)$, Space: $O(V)$.

### 3.2 Blinky - Depth-First Search (DFS)
- **Data Structure**: `ArrayStack` (LIFO)
- **Optimality**: **Non-optimal**. Follows branch paths deeply before backtracking.
- **Frontier Expansion**: Winding exploration; showcases the stark difference between stack-based exploration and queue-based level order.
- **Complexity**: Time: $O(V + E)$, Space: $O(V)$.

### 3.3 Inky - A\* Heuristic Search
- **Data Structure**: `MinHeapPriorityQueue`
- **Evaluation Function**:
  $$f(n) = g(n) + h(n)$$
  where $g(n)$ is the exact cost from start to $n$, and $h(n)$ is the Manhattan distance:
  $$h(n) = |r_n - r_{target}| + |c_n - c_{target}|$$
- **Optimality**: **Optimal**. Because Manhattan distance is admissible ($h(n) \le h^*(n)$) and consistent on 4-connected grid graphs, A\* guarantees the shortest path while pruning unproductive branches.
- **Comparison to BFS**: In test runs, A\* achieved the exact same 13-tile shortest path as BFS, but expanded **only 26 nodes compared to BFS's 101 nodes** (nearly a 4x reduction in expanded states).

### 3.4 Clyde - Patrol / Scatter AI
- Uses distance threshold switching: when Pac-Man is within 6 tiles, Clyde retreats to his scatter corner; otherwise, pursues using A\* pathfinding.

---

## 4. Live DSA Visualization Mode (Press `V`)

When the user presses **`V`**:
1. **Search Frontier Overlay**: Explored nodes in the search tree are drawn directly over the maze tiles using translucent colored highlights (Cyan for A\*, Pink for BFS, Red for DFS).
2. **Path Rays**: The calculated path is drawn as a glowing vector line leading directly to Pac-Man.
3. **Telemetry Sidebar**:
   - Live nodes expanded count
   - Peak data structure memory usage (elements in Queue/Stack/Heap)
   - Search execution time in milliseconds
   - Side-by-side comparative table updating at 60 FPS

---

## 5. How to Run the Project

### Prerequisites
- Python 3.8+ (Python 3.10 installed on system)
- Pygame (`pip install pygame`)

### Run Automated Unit Tests (Verify All DSA Classes)
```bash
python test_dsa.py
```
*Outputs verification tests for `ArrayStack`, `CircularQueue`, `MinHeapPriorityQueue`, `DoublyLinkedList`, `BinarySearchTree`, `Graph`, `BFS`, `DFS`, `A*`, and `Sorting`.*

### Launch the Game
```bash
python main.py
```

### Controls & Keybindings
| Key | Action |
| :--- | :--- |
| **Arrow Keys / WASD** | Move Pac-Man |
| **V** | Toggle DSA Real-Time Frontier Overlay |
| **1, 2, 3, 4** | Focus HUD on Pinky (BFS), Blinky (DFS), Inky (A\*), or All |
| **P** | Pause / Resume game |
| **R** | Restart current game |
| **SPACE / ENTER** | Start game from menu |
| **ESC** | Return to Menu / Exit |
