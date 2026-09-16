"""
Maze Grid Representation & Graph Extraction
Syllabus: Linear Array & its representation in memory, Multidimensional Array, Graph Representation
"""

import pygame
from config import (
    TILE_SIZE, MAZE_ROWS, MAZE_COLS, HEADER_HEIGHT,
    COLOR_MAZE_WALL, COLOR_MAZE_WALL_INNER, COLOR_MAZE_FLOOR,
    COLOR_PELLET, COLOR_POWER_PELLET, POINTS_PELLET, POINTS_POWER_PELLET
)
from dsa.graph import Graph

# 21x21 Symmetric Maze Layout
# 1 = Wall, 0 = Pellet, 2 = Power Pellet, 3 = Empty corridor, 4 = Ghost House interior
MAZE_LAYOUT_21X21 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], # Open center corridor at col 10
    [1, 1, 1, 1, 0, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 0, 1, 1, 1, 1], # Exit straight up from ghost house
    [1, 1, 1, 1, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 3, 1, 1, 4, 4, 4, 1, 1, 3, 1, 0, 1, 1, 1, 1],
    [3, 3, 3, 3, 0, 3, 3, 1, 4, 4, 4, 4, 4, 1, 3, 3, 0, 3, 3, 3, 3], # Wrap-around tunnel
    [1, 1, 1, 1, 0, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 2, 0, 1, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 1, 0, 2, 1], # Row 16: Pac-man spawn at (16, 10)
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Maze:
    """
    Manages the 2D matrix representing the maze, pellets, and collisions.
    Also builds and maintains the Graph Adjacency List representation.
    """

    def __init__(self):
        self.rows = MAZE_ROWS
        self.cols = MAZE_COLS
        self.grid = [row[:] for row in MAZE_LAYOUT_21X21]
        self.total_pellets = 0
        self.pellets_remaining = 0
        self._count_pellets()
        self.graph = self._build_graph()

    def _count_pellets(self):
        self.total_pellets = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] in (0, 2):
                    self.total_pellets += 1
        self.pellets_remaining = self.total_pellets

    def _build_graph(self) -> Graph:
        """
        Converts the 2D maze into an unweighted graph G = (V, E).
        Vertices are all non-wall tiles. Edges connect orthogonally adjacent walkable tiles.
        """
        g = Graph()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.is_walkable(r, c):
                    g.add_node((r, c))
                    # Check 4 cardinal directions
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        # Support tunnel wrap-around at row 10
                        if r == 10 and (nc < 0 or nc >= self.cols):
                            wrapped_c = (nc + self.cols) % self.cols
                            g.add_edge((r, c), (r, wrapped_c))
                        elif 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.is_walkable(nr, nc):
                                g.add_edge((r, c), (nr, nc))
        return g

    def is_wall(self, r: int, c: int) -> bool:
        """Check if grid cell is a wall."""
        if r < 0 or r >= self.rows:
            return True
        if c < 0 or c >= self.cols:
            return False  # Allowed for wrap-around tunnel
        return self.grid[r][c] == 1

    def is_walkable(self, r: int, c: int) -> bool:
        """Walkable if inside maze and not a wall."""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] != 1
        # Tunnel ends are walkable
        if r == 10 and (c < 0 or c >= self.cols):
            return True
        return False

    def eat_pellet(self, r: int, c: int) -> tuple:
        """
        Eats pellet at (r, c) if present.
        Returns: (points_earned, is_power_pellet)
        """
        if 0 <= r < self.rows and 0 <= c < self.cols:
            val = self.grid[r][c]
            if val == 0:  # Normal pellet
                self.grid[r][c] = 3
                self.pellets_remaining -= 1
                return POINTS_PELLET, False
            elif val == 2:  # Power pellet
                self.grid[r][c] = 3
                self.pellets_remaining -= 1
                return POINTS_POWER_PELLET, True
        return 0, False

    def reset_pellets(self):
        """Restore all original pellets."""
        self.grid = [row[:] for row in MAZE_LAYOUT_21X21]
        self._count_pellets()

    def render(self, surface: pygame.Surface, offset_y: int = HEADER_HEIGHT):
        """
        Render the maze walls, pellets, and ghost pen.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.grid[r][c]
                px = c * TILE_SIZE
                py = offset_y + r * TILE_SIZE
                rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)

                if val == 1:
                    # Wall block with stylish double border
                    pygame.draw.rect(surface, COLOR_MAZE_WALL_INNER, rect)
                    pygame.draw.rect(surface, COLOR_MAZE_WALL, rect, 2, border_radius=4)
                elif val == 4:
                    # Ghost house floor
                    pygame.draw.rect(surface, (25, 25, 45), rect)
                else:
                    # Empty floor
                    pygame.draw.rect(surface, COLOR_MAZE_FLOOR, rect)

                    if val == 0:
                        # Normal pellet (small circle)
                        center = (px + TILE_SIZE // 2, py + TILE_SIZE // 2)
                        pygame.draw.circle(surface, COLOR_PELLET, center, 3)
                    elif val == 2:
                        # Power pellet (larger pulsing circle)
                        center = (px + TILE_SIZE // 2, py + TILE_SIZE // 2)
                        pygame.draw.circle(surface, COLOR_POWER_PELLET, center, 7)
                        pygame.draw.circle(surface, (255, 255, 200), center, 4)
