"""
Real-Time DSA Visualizer & Educational HUD
Renders search frontiers, chosen paths, data structure telemetry,
and comparative complexity benchmarks.
"""

import pygame
from config import (
    TILE_SIZE, MAZE_WIDTH, MAZE_HEIGHT, HEADER_HEIGHT,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_PANEL_BG, COLOR_PANEL_BORDER, COLOR_TEXT_WHITE,
    COLOR_TEXT_MUTED, COLOR_TEXT_HIGHLIGHT, COLOR_ACCENT_GREEN,
    COLOR_ACCENT_RED, COLOR_ACCENT_BLUE,
    COLOR_VIS_BFS_FRONTIER, COLOR_VIS_BFS_PATH,
    COLOR_VIS_DFS_FRONTIER, COLOR_VIS_DFS_PATH,
    COLOR_VIS_ASTAR_FRONTIER, COLOR_VIS_ASTAR_PATH,
    COLOR_PINKY, COLOR_BLINKY, COLOR_INKY
)

class DSAVisualizer:
    def __init__(self):
        self.enabled = True
        self.focused_ghost_idx = 0  # 0=Pinky(BFS), 1=Blinky(DFS), 2=Inky(A*), 3=All
        
        # Initialize fonts safely
        pygame.font.init()
        self.font_title = pygame.font.SysFont('consolas', 18, bold=True)
        self.font_bold = pygame.font.SysFont('consolas', 14, bold=True)
        self.font_regular = pygame.font.SysFont('consolas', 13)
        self.font_small = pygame.font.SysFont('consolas', 11)

        # Translucent surface for drawing search frontiers without blending slowdowns
        self.alpha_surface = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT), pygame.SRCALPHA)

    def toggle(self):
        self.enabled = not self.enabled

    def set_focus(self, idx: int):
        self.focused_ghost_idx = idx % 4

    def render_overlay(self, surface: pygame.Surface, ghosts: list):
        """
        Draw transparent explored node frontiers and path lines on the maze.
        """
        if not self.enabled:
            return

        self.alpha_surface.fill((0, 0, 0, 0))

        # Determine which ghosts to draw
        active_ghosts = ghosts if self.focused_ghost_idx == 3 else [ghosts[self.focused_ghost_idx]]

        for g in active_ghosts:
            if not g.current_path and not g.visited_frontier:
                continue

            # Pick frontier and path colors
            if g.algorithm_name == "BFS":
                frontier_color = (255, 105, 180, 55)
                path_color = (255, 105, 180)
            elif g.algorithm_name == "DFS":
                frontier_color = (255, 60, 60, 55)
                path_color = (255, 60, 60)
            elif g.algorithm_name == "A*":
                frontier_color = (0, 220, 255, 55)
                path_color = (0, 220, 255)
            else:
                frontier_color = (255, 165, 0, 45)
                path_color = (255, 165, 0)

            # Draw explored frontier tiles
            for r, c in g.visited_frontier:
                px = c * TILE_SIZE
                py = r * TILE_SIZE
                pygame.draw.rect(
                    self.alpha_surface,
                    frontier_color,
                    pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
                )

            # Draw path line
            if len(g.current_path) >= 2:
                points = []
                for r, c in g.current_path:
                    px = c * TILE_SIZE + TILE_SIZE // 2
                    py = r * TILE_SIZE + TILE_SIZE // 2
                    points.append((px, py))
                pygame.draw.lines(self.alpha_surface, path_color, False, points, 3)

        # Blit transparent overlay onto maze area
        surface.blit(self.alpha_surface, (0, HEADER_HEIGHT))

    def render_sidebar(self, surface: pygame.Surface, ghosts: list, pacman, maze):
        """
        Draw detailed DSA Telemetry & Comparative Analysis sidebar.
        """
        sidebar_x = MAZE_WIDTH
        sidebar_w = SCREEN_WIDTH - MAZE_WIDTH
        sidebar_h = SCREEN_HEIGHT

        # Background panel
        pygame.draw.rect(surface, COLOR_PANEL_BG, pygame.Rect(sidebar_x, 0, sidebar_w, sidebar_h))
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (sidebar_x, 0), (sidebar_x, sidebar_h), 2)

        y = 15
        x = sidebar_x + 15

        # 1. Header Section
        title_surf = self.font_title.render("DSA ALGORITHM HUD", True, COLOR_TEXT_HIGHLIGHT)
        surface.blit(title_surf, (x, y))
        y += 22
        sub_surf = self.font_small.render("ECE 2103: Data Structures & Algorithms", True, COLOR_TEXT_MUTED)
        surface.blit(sub_surf, (x, y))
        y += 28

        # Status badge
        vis_status = "ENABLED [ON]" if self.enabled else "DISABLED [OFF]"
        badge_color = COLOR_ACCENT_GREEN if self.enabled else COLOR_ACCENT_RED
        badge_surf = self.font_small.render(f"Visualizer Overlay: {vis_status} (Press 'V')", True, badge_color)
        surface.blit(badge_surf, (x, y))
        y += 24

        pygame.draw.line(surface, COLOR_PANEL_BORDER, (x, y), (sidebar_x + sidebar_w - 15, y), 1)
        y += 12

        # 2. Selected Ghost Detailed Telemetry Card
        focus_names = ["1: Pinky (BFS)", "2: Blinky (DFS)", "3: Inky (A*)", "4: All Algorithms"]
        filter_text = f"FOCUSED VIEW: {focus_names[self.focused_ghost_idx]}"
        filter_surf = self.font_bold.render(filter_text, True, COLOR_TEXT_WHITE)
        surface.blit(filter_surf, (x, y))
        y += 22

        # Current focused ghost object
        active_ghost = ghosts[min(self.focused_ghost_idx, len(ghosts) - 1)]

        # Telemetry Card box
        card_rect = pygame.Rect(x, y, sidebar_w - 30, 160)
        pygame.draw.rect(surface, (25, 28, 44), card_rect, border_radius=6)
        pygame.draw.rect(surface, active_ghost.base_color, card_rect, 2, border_radius=6)

        cy = y + 10
        cx = x + 12

        # Ghost name & algorithm
        name_surf = self.font_bold.render(f"Ghost: {active_ghost.name}", True, active_ghost.base_color)
        surface.blit(name_surf, (cx, cy))
        cy += 20

        # DS & Asymptotic Complexity
        ds_surf = self.font_regular.render(f"Data Structure: {active_ghost.ds_name}", True, COLOR_TEXT_WHITE)
        surface.blit(ds_surf, (cx, cy))
        cy += 18

        complexity_str = {
            "BFS": "Complexity: Time O(V+E) | Space O(V)",
            "DFS": "Complexity: Time O(V+E) | Space O(V)",
            "A*":  "Complexity: Time O(b^d) | Space O(b^d)"
        }.get(active_ghost.algorithm_name, "Complexity: O(V+E)")
        comp_surf = self.font_small.render(complexity_str, True, COLOR_TEXT_MUTED)
        surface.blit(comp_surf, (cx, cy))
        cy += 24

        # Live Real-Time Benchmark Numbers
        p_len = max(0, len(active_ghost.current_path) - 1)
        stats_line1 = f"Path Length:     {p_len:2d} tiles"
        stats_line2 = f"Nodes Expanded:  {active_ghost.nodes_expanded:2d} nodes"
        stats_line3 = f"Peak DS Memory:  {active_ghost.max_ds_size:2d} elements"
        stats_line4 = f"Compute Time:    {active_ghost.search_time_ms:0.3f} ms"

        surface.blit(self.font_regular.render(stats_line1, True, COLOR_TEXT_HIGHLIGHT), (cx, cy))
        cy += 18
        surface.blit(self.font_regular.render(stats_line2, True, COLOR_TEXT_WHITE), (cx, cy))
        cy += 18
        surface.blit(self.font_regular.render(stats_line3, True, COLOR_TEXT_WHITE), (cx, cy))
        cy += 18
        surface.blit(self.font_regular.render(stats_line4, True, COLOR_ACCENT_GREEN), (cx, cy))

        y += 175

        # 3. Side-by-Side Algorithm Comparison Table
        table_title = self.font_bold.render("REAL-TIME ALGORITHM COMPARISON", True, COLOR_TEXT_HIGHLIGHT)
        surface.blit(table_title, (x, y))
        y += 22

        # Table Header
        headers = ["Algorithm", "DS", "Nodes", "Len", "Time"]
        col_x = [x, x + 85, x + 160, x + 230, x + 285]

        for i, h in enumerate(headers):
            surface.blit(self.font_small.render(h, True, COLOR_TEXT_MUTED), (col_x[i], y))
        y += 18
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (x, y), (sidebar_x + sidebar_w - 15, y), 1)
        y += 6

        # Populate rows for BFS, DFS, A*
        for g in ghosts[:3]:
            row_color = g.base_color
            short_ds = "Queue" if "Queue" in g.ds_name else ("Stack" if "Stack" in g.ds_name else "MinHeap")
            p_len = max(0, len(g.current_path) - 1)

            surface.blit(self.font_small.render(g.algorithm_name, True, row_color), (col_x[0], y))
            surface.blit(self.font_small.render(short_ds, True, COLOR_TEXT_WHITE), (col_x[1], y))
            surface.blit(self.font_small.render(str(g.nodes_expanded), True, COLOR_TEXT_WHITE), (col_x[2], y))
            surface.blit(self.font_small.render(str(p_len), True, COLOR_TEXT_WHITE), (col_x[3], y))
            surface.blit(self.font_small.render(f"{g.search_time_ms:0.2f}ms", True, COLOR_ACCENT_GREEN), (col_x[4], y))
            y += 20

        y += 10
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (x, y), (sidebar_x + sidebar_w - 15, y), 1)
        y += 15

        # 4. Controls & Shortcut Guide
        guide_title = self.font_bold.render("CONTROLS & SHORTCUTS", True, COLOR_TEXT_HIGHLIGHT)
        surface.blit(guide_title, (x, y))
        y += 20

        shortcuts = [
            ("ARROWS / WASD", "Move Pac-Man"),
            ("[V]", "Toggle DSA Path Overlay"),
            ("[1, 2, 3, 4]", "Switch Focused Algorithm"),
            ("[P]", "Pause / Resume"),
            ("[R]", "Restart Game")
        ]
        for key, desc in shortcuts:
            surface.blit(self.font_small.render(key, True, COLOR_ACCENT_BLUE), (x, y))
            surface.blit(self.font_small.render(desc, True, COLOR_TEXT_WHITE), (x + 120, y))
            y += 17

    def render_header(self, surface: pygame.Surface, pacman, maze):
        """Draw top banner with Score, Pellets remaining, and Lives."""
        header_rect = pygame.Rect(0, 0, MAZE_WIDTH, HEADER_HEIGHT)
        pygame.draw.rect(surface, (12, 14, 24), header_rect)
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (0, HEADER_HEIGHT - 1), (MAZE_WIDTH, HEADER_HEIGHT - 1), 2)

        # Score
        score_text = f"SCORE: {pacman.score}"
        surface.blit(self.font_title.render(score_text, True, COLOR_TEXT_WHITE), (20, 14))

        # Pellets
        pellet_text = f"PELLETS: {maze.pellets_remaining}/{maze.total_pellets}"
        surface.blit(self.font_regular.render(pellet_text, True, COLOR_TEXT_MUTED), (200, 18))

        # Lives (draw mini Pac-Man icons)
        lives_x = MAZE_WIDTH - 120
        surface.blit(self.font_regular.render("LIVES:", True, COLOR_TEXT_WHITE), (lives_x - 55, 18))
        for i in range(pacman.lives):
            pygame.draw.circle(surface, (255, 255, 0), (lives_x + i * 22, 25), 7)
