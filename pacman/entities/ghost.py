"""
Ghost AI Entities backed by Custom Data Structures and Search Algorithms
- Blinky: DFS (ArrayStack)
- Pinky: BFS (CircularQueue)
- Inky: A* (MinHeapPriorityQueue)
- Clyde: Patrol / Graph Intersections
"""

import math
import random
import pygame
from config import (
    TILE_SIZE, HEADER_HEIGHT, GHOST_SPEED_NORMAL, GHOST_SPEED_SCARED,
    COLOR_BLINKY, COLOR_PINKY, COLOR_INKY, COLOR_CLYDE,
    COLOR_GHOST_SCARED, COLOR_GHOST_FLASH, SCARED_TIME, DIRECTIONS
)
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.astar import astar_search

class Ghost:
    def __init__(self, name: str, color: tuple, home_row: int, home_col: int, scatter_tile: tuple):
        self.name = name
        self.base_color = color
        self.home_row = home_row
        self.home_col = home_col
        self.scatter_tile = scatter_tile
        
        self.algorithm_name = "BASE"
        self.ds_name = "None"
        self.color = color
        
        # State: 'NORMAL', 'SCARED', 'EATEN'
        self.state = 'NORMAL'
        self.scared_timer = 0.0
        
        # Pathfinding, Memory & Telemetry Data
        self.current_path = []
        self.visited_frontier = []
        self.nodes_expanded = 0
        self.max_ds_size = 0
        self.search_time_ms = 0.0
        self.target_tile = (1, 1)
        
        # Anti-oscillation and intersection tracking
        self.prev_tile = None
        self.last_decision_tile = None
        self.repath_timer = 0.0
        
        self.reset_position()

    def reset_position(self):
        self.row = self.home_row
        self.col = self.home_col
        self.x = self.col * TILE_SIZE + TILE_SIZE // 2
        self.y = HEADER_HEIGHT + self.row * TILE_SIZE + TILE_SIZE // 2
        self.current_dir = 'UP'
        self.speed = GHOST_SPEED_NORMAL
        self.state = 'NORMAL'
        self.scared_timer = 0.0
        self.current_path = []
        self.visited_frontier = []
        self.prev_tile = None
        self.last_decision_tile = None
        self.repath_timer = 0.0

    def set_scared(self, duration: float = SCARED_TIME):
        if self.state != 'EATEN':
            self.state = 'SCARED'
            self.scared_timer = duration
            self.speed = GHOST_SPEED_SCARED
            # Allow 180° turn on entering scared mode
            self.prev_tile = None
            self.current_path = []

    def update(self, dt: float, maze, pacman_pos: tuple):
        # Handle scared mode countdown
        if self.state == 'SCARED':
            self.scared_timer -= dt
            if self.scared_timer <= 0:
                self.state = 'NORMAL'
                self.speed = GHOST_SPEED_NORMAL
                self.current_path = []

        self.repath_timer += dt
        curr_tile = (self.row, self.col)

        # Decide whether we need to compute/update path:
        # 1. No path currently exists or reached destination
        needs_repath = (not self.current_path or len(self.current_path) <= 1)
        
        # 2. Reached an intersection tile (degree > 2) where a strategic turn decision is made
        is_intersection = maze.graph.degree(curr_tile) > 2
        if is_intersection and curr_tile != self.last_decision_tile and self.repath_timer >= 0.2:
            needs_repath = True

        # 3. Timeout safety (re-sync path every 1.0 second)
        if self.repath_timer >= 1.0:
            needs_repath = True

        if needs_repath:
            self._recalculate_path(maze, pacman_pos)
            self.last_decision_tile = curr_tile
            self.repath_timer = 0.0

        # Move along current path
        if self.current_path and len(self.current_path) > 1:
            next_tile = self.current_path[1]
            target_px_x = next_tile[1] * TILE_SIZE + TILE_SIZE // 2
            target_px_y = HEADER_HEIGHT + next_tile[0] * TILE_SIZE + TILE_SIZE // 2

            dx = target_px_x - self.x
            dy = target_px_y - self.y
            dist = math.hypot(dx, dy)

            if dist <= self.speed:
                # Snap to tile center
                self.x = target_px_x
                self.y = target_px_y
                self.prev_tile = (self.row, self.col)
                self.row = next_tile[0]
                self.col = next_tile[1]
                self.current_path.pop(0)
            else:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed

                if abs(dx) > abs(dy):
                    self.current_dir = 'RIGHT' if dx > 0 else 'LEFT'
                else:
                    self.current_dir = 'DOWN' if dy > 0 else 'UP'
        else:
            # Fallback simple movement if path is empty (e.g. at edge of wrap tunnel)
            self._fallback_move(maze)

    def _fallback_move(self, maze):
        curr_r = self.row
        curr_c = self.col
        possible = []
        for d_name, (dx, dy) in DIRECTIONS.items():
            if d_name == 'NONE':
                continue
            nr, nc = curr_r + dy, curr_c + dx
            if maze.is_walkable(nr, nc) and (nr, nc) != self.prev_tile:
                possible.append((d_name, (nr, nc)))
        
        # If no non-reverse move found, allow any move (dead end)
        if not possible:
            for d_name, (dx, dy) in DIRECTIONS.items():
                if d_name == 'NONE':
                    continue
                nr, nc = curr_r + dy, curr_c + dx
                if maze.is_walkable(nr, nc):
                    possible.append((d_name, (nr, nc)))

        if possible:
            chosen_dir, chosen_tile = random.choice(possible)
            self.current_dir = chosen_dir
            dx, dy = DIRECTIONS[self.current_dir]
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.row = int((self.y - HEADER_HEIGHT) // TILE_SIZE)
            self.col = int(self.x // TILE_SIZE)

    def _recalculate_path(self, maze, pacman_pos: tuple):
        """Override in subclasses to invoke specific pathfinding algorithm."""
        pass

    def render(self, surface: pygame.Surface):
        """Draw classic arcade ghost sprite with cartoon eyes."""
        radius = TILE_SIZE // 2 - 2
        px = int(self.x)
        py = int(self.y)

        # Determine color
        if self.state == 'SCARED':
            if self.scared_timer < 2.0 and int(self.scared_timer * 6) % 2 == 0:
                body_color = COLOR_GHOST_FLASH
            else:
                body_color = COLOR_GHOST_SCARED
        elif self.state == 'EATEN':
            body_color = (100, 100, 100)
        else:
            body_color = self.base_color

        # Ghost top dome
        pygame.draw.circle(surface, body_color, (px, py - 2), radius)
        # Ghost body rectangle
        rect_top = py - 2
        body_rect = pygame.Rect(px - radius, rect_top, radius * 2, radius + 4)
        pygame.draw.rect(surface, body_color, body_rect)

        # Tentacle waves at bottom
        tentacle_count = 3
        t_width = (radius * 2) / tentacle_count
        base_y = rect_top + radius + 4
        for i in range(tentacle_count):
            t_center_x = px - radius + (i + 0.5) * t_width
            pygame.draw.circle(surface, body_color, (int(t_center_x), int(base_y)), int(t_width // 2))

        # Cartoon Eyes
        eye_offset_x = 4
        eye_offset_y = -3
        pupil_dx, pupil_dy = 0, 0
        if self.current_dir == 'LEFT':
            pupil_dx = -2
        elif self.current_dir == 'RIGHT':
            pupil_dx = 2
        elif self.current_dir == 'UP':
            pupil_dy = -2
        elif self.current_dir == 'DOWN':
            pupil_dy = 2

        # White eye bases
        pygame.draw.circle(surface, (255, 255, 255), (px - eye_offset_x, py + eye_offset_y), 4)
        pygame.draw.circle(surface, (255, 255, 255), (px + eye_offset_x, py + eye_offset_y), 4)
        # Blue pupils
        pupil_color = (0, 50, 200) if self.state != 'SCARED' else (255, 100, 100)
        pygame.draw.circle(surface, pupil_color, (px - eye_offset_x + pupil_dx, py + eye_offset_y + pupil_dy), 2)
        pygame.draw.circle(surface, pupil_color, (px + eye_offset_x + pupil_dx, py + eye_offset_y + pupil_dy), 2)


class PinkyBFS(Ghost):
    """
    BFS Ghost (Pink): Uses CircularQueue.
    Guarantees shortest unweighted path to target without 180° backward stutter.
    """
    def __init__(self):
        super().__init__(
            name="Pinky",
            color=COLOR_PINKY,
            home_row=9,
            home_col=9,
            scatter_tile=(1, 1)
        )
        self.algorithm_name = "BFS"
        self.ds_name = "CircularQueue (FIFO)"

    def _recalculate_path(self, maze, pacman_pos: tuple):
        start = (self.row, self.col)
        target = self.scatter_tile if self.state == 'SCARED' else pacman_pos
        self.target_tile = target

        if start == target or not maze.is_walkable(target[0], target[1]):
            return

        result = bfs_search(maze.graph, start, target, forbidden_first=self.prev_tile)
        if result['path']:
            self.current_path = result['path']
            self.visited_frontier = result['visited']
            self.nodes_expanded = result['nodes_expanded']
            self.max_ds_size = result['max_ds_size']
            self.search_time_ms = result['execution_time_ms']


class BlinkyDFS(Ghost):
    """
    DFS Ghost (Red): Uses ArrayStack.
    Demonstrates deep branch exploration with continuous progression and zero back-and-forth jitter.
    """
    def __init__(self):
        super().__init__(
            name="Blinky",
            color=COLOR_BLINKY,
            home_row=9,
            home_col=10,
            scatter_tile=(1, 19)
        )
        self.algorithm_name = "DFS"
        self.ds_name = "ArrayStack (LIFO)"

    def _recalculate_path(self, maze, pacman_pos: tuple):
        start = (self.row, self.col)
        target = self.scatter_tile if self.state == 'SCARED' else pacman_pos
        self.target_tile = target

        if start == target or not maze.is_walkable(target[0], target[1]):
            return

        result = dfs_search(maze.graph, start, target, forbidden_first=self.prev_tile)
        if result['path']:
            self.current_path = result['path']
            self.visited_frontier = result['visited']
            self.nodes_expanded = result['nodes_expanded']
            self.max_ds_size = result['max_ds_size']
            self.search_time_ms = result['execution_time_ms']


class InkyAStar(Ghost):
    """
    A* Ghost (Cyan): Uses MinHeapPriorityQueue.
    Uses Manhattan Distance Heuristic f(n) = g(n) + h(n).
    Demonstrates optimal heuristic search with minimal node expansions.
    """
    def __init__(self):
        super().__init__(
            name="Inky",
            color=COLOR_INKY,
            home_row=9,
            home_col=11,
            scatter_tile=(19, 1)
        )
        self.algorithm_name = "A*"
        self.ds_name = "MinHeap (PriorityQueue)"

    def _recalculate_path(self, maze, pacman_pos: tuple):
        start = (self.row, self.col)
        target = self.scatter_tile if self.state == 'SCARED' else pacman_pos
        self.target_tile = target

        if start == target or not maze.is_walkable(target[0], target[1]):
            return

        result = astar_search(maze.graph, start, target, forbidden_first=self.prev_tile)
        if result['path']:
            self.current_path = result['path']
            self.visited_frontier = result['visited']
            self.nodes_expanded = result['nodes_expanded']
            self.max_ds_size = result['max_ds_size']
            self.search_time_ms = result['execution_time_ms']


class ClydePatrol(Ghost):
    """
    Clyde (Orange): Patrols maze intersections and switches between
    A* pursuit and roaming based on distance to Pac-Man.
    """
    def __init__(self):
        super().__init__(
            name="Clyde",
            color=COLOR_CLYDE,
            home_row=10,
            home_col=10,
            scatter_tile=(19, 19)
        )
        self.algorithm_name = "Patrol / A*"
        self.ds_name = "MinHeap / Graph"

    def _recalculate_path(self, maze, pacman_pos: tuple):
        start = (self.row, self.col)
        # If Pac-Man is within 6 tiles, retreat to scatter corner, else pursue
        dist = abs(self.row - pacman_pos[0]) + abs(self.col - pacman_pos[1])
        target = self.scatter_tile if (dist < 6 or self.state == 'SCARED') else pacman_pos
        self.target_tile = target

        if start == target or not maze.is_walkable(target[0], target[1]):
            return

        result = astar_search(maze.graph, start, target, forbidden_first=self.prev_tile)
        if result['path']:
            self.current_path = result['path']
            self.visited_frontier = result['visited']
            self.nodes_expanded = result['nodes_expanded']
            self.max_ds_size = result['max_ds_size']
            self.search_time_ms = result['execution_time_ms']
