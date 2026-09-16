"""
Pac-Man Lite: Data Structures & Algorithms Group Project
Course: ECE 2103 / ECE 2104
Main Game Loop & State Management
"""

import sys
import os
import pygame

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MAZE_WIDTH, MAZE_HEIGHT, HEADER_HEIGHT, FPS,
    COLOR_BG, COLOR_TEXT_WHITE, COLOR_TEXT_HIGHLIGHT, COLOR_TEXT_MUTED,
    COLOR_ACCENT_GREEN, COLOR_ACCENT_RED, COLOR_ACCENT_BLUE,
    POINTS_GHOST
)
from world.maze import Maze
from world.visualizer import DSAVisualizer
from entities.pacman import Pacman
from entities.ghost import PinkyBFS, BlinkyDFS, InkyAStar, ClydePatrol
from dsa.bst import BinarySearchTree
from algorithms.sorting import quick_sort

# Game States
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3
STATE_WIN = 4


class PacmanGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pac-Man Lite | ECE 2103 DSA Group Project")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Fonts
        self.font_large = pygame.font.SysFont('consolas', 32, bold=True)
        self.font_medium = pygame.font.SysFont('consolas', 20, bold=True)
        self.font_small = pygame.font.SysFont('consolas', 14)

        # High Score BST Leaderboard
        self.leaderboard_bst = BinarySearchTree()
        # Seed some initial high scores
        initial_scores = [(1200, "Inky_Bot"), (850, "Blinky_Bot"), (600, "Pinky_Bot"), (300, "Novice")]
        for s, name in initial_scores:
            self.leaderboard_bst.insert(s, name)

        # Game Entities & Systems
        self.maze = Maze()
        self.pacman = Pacman(start_row=16, start_col=10)
        self.ghosts = [
            PinkyBFS(),     # BFS
            BlinkyDFS(),    # DFS
            InkyAStar(),    # A*
            ClydePatrol()   # Patrol
        ]
        self.visualizer = DSAVisualizer()
        self.current_state = STATE_MENU

    def reset_game(self):
        """Reset game world for a new match."""
        self.maze.reset_pellets()
        self.pacman.reset_position()
        self.pacman.lives = 3
        self.pacman.score = 0
        for g in self.ghosts:
            g.reset_position()
        self.current_state = STATE_PLAYING

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return

            if event.type == pygame.KEYDOWN:
                # Global Hotkeys
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == STATE_PLAYING:
                        self.current_state = STATE_MENU
                    else:
                        self.is_running = False

                if event.key == pygame.K_v:
                    self.visualizer.toggle()

                if event.key == pygame.K_1:
                    self.visualizer.set_focus(0)
                elif event.key == pygame.K_2:
                    self.visualizer.set_focus(1)
                elif event.key == pygame.K_3:
                    self.visualizer.set_focus(2)
                elif event.key == pygame.K_4:
                    self.visualizer.set_focus(3)

                # State-specific inputs
                if self.current_state == STATE_MENU:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()

                elif self.current_state == STATE_PLAYING:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.pacman.set_next_direction('UP')
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.pacman.set_next_direction('DOWN')
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.pacman.set_next_direction('LEFT')
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.pacman.set_next_direction('RIGHT')
                    elif event.key == pygame.K_p:
                        self.current_state = STATE_PAUSED
                    elif event.key == pygame.K_r:
                        self.reset_game()

                elif self.current_state == STATE_PAUSED:
                    if event.key == pygame.K_p:
                        self.current_state = STATE_PLAYING

                elif self.current_state in (STATE_GAME_OVER, STATE_WIN):
                    if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_m:
                        self.current_state = STATE_MENU

    def update(self, dt: float):
        if self.current_state != STATE_PLAYING:
            return

        # 1. Update Pac-Man
        ate_power_pellet = self.pacman.update(self.maze)
        if ate_power_pellet:
            for g in self.ghosts:
                g.set_scared()

        pacman_tile = (self.pacman.row, self.pacman.col)

        # 2. Update Ghosts
        for g in self.ghosts:
            g.update(dt, self.maze, pacman_tile)

            # Check collision between Pac-Man and Ghost
            dist = pygame.math.Vector2(self.pacman.x - g.x, self.pacman.y - g.y).length()
            if dist < 14:
                if g.state == 'SCARED':
                    # Pac-Man eats ghost
                    g.state = 'EATEN'
                    g.reset_position()
                    self.pacman.score += POINTS_GHOST
                elif g.state == 'NORMAL':
                    # Ghost catches Pac-Man
                    self.pacman.lives -= 1
                    if self.pacman.lives <= 0:
                        self.leaderboard_bst.insert(self.pacman.score, "Player 1")
                        self.current_state = STATE_GAME_OVER
                    else:
                        # Soft reset positions
                        self.pacman.reset_position()
                        for other in self.ghosts:
                            other.reset_position()
                    break

        # 3. Check Win Condition
        if self.maze.pellets_remaining <= 0:
            self.leaderboard_bst.insert(self.pacman.score, "Player 1")
            self.current_state = STATE_WIN

    def render(self):
        self.screen.fill(COLOR_BG)

        if self.current_state == STATE_MENU:
            self._render_menu()
        else:
            # Render Maze and Pellets
            self.maze.render(self.screen, offset_y=HEADER_HEIGHT)

            # Render Visualizer Overlay (Frontiers & Path lines)
            self.visualizer.render_overlay(self.screen, self.ghosts)

            # Render Pac-Man & Ghosts
            self.pacman.render(self.screen)
            for g in self.ghosts:
                g.render(self.screen)

            # Render Top Banner & Sidebar HUD
            self.visualizer.render_header(self.screen, self.pacman, self.maze)
            self.visualizer.render_sidebar(self.screen, self.ghosts, self.pacman, self.maze)

            # Render Overlays for Pause, Game Over, Win
            if self.current_state == STATE_PAUSED:
                self._render_modal("PAUSED", "Press 'P' to Resume Gameplay", COLOR_TEXT_HIGHLIGHT)
            elif self.current_state == STATE_GAME_OVER:
                self._render_modal("GAME OVER", f"Final Score: {self.pacman.score} | Press 'R' to Restart", COLOR_ACCENT_RED)
            elif self.current_state == STATE_WIN:
                self._render_modal("STAGE CLEARED!", f"Score: {self.pacman.score} | Press 'R' to Play Again", COLOR_ACCENT_GREEN)

        pygame.display.flip()

    def _render_modal(self, title: str, subtitle: str, color: tuple):
        """Draw translucent centered dialog overlay."""
        overlay = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, HEADER_HEIGHT))

        t_surf = self.font_large.render(title, True, color)
        s_surf = self.font_medium.render(subtitle, True, COLOR_TEXT_WHITE)

        cx = MAZE_WIDTH // 2
        cy = HEADER_HEIGHT + MAZE_HEIGHT // 2

        self.screen.blit(t_surf, (cx - t_surf.get_width() // 2, cy - 35))
        self.screen.blit(s_surf, (cx - s_surf.get_width() // 2, cy + 15))

    def _render_menu(self):
        """Render Title Screen with Course Info, DSA Summary, and BST Leaderboard."""
        cx = SCREEN_WIDTH // 2

        # Title Banner
        title_surf = self.font_large.render("PAC-MAN LITE: DSA EDITION", True, COLOR_TEXT_HIGHLIGHT)
        self.screen.blit(title_surf, (cx - title_surf.get_width() // 2, 40))

        sub_surf = self.font_medium.render("ECE 2103: Data Structures & Algorithms Project", True, COLOR_ACCENT_BLUE)
        self.screen.blit(sub_surf, (cx - sub_surf.get_width() // 2, 85))

        # Project Features Box
        features = [
            ("Pinky Ghost (Pink)", "BFS Algorithm via CircularQueue (FIFO) -> Shortest Path"),
            ("Blinky Ghost (Red)", "DFS Algorithm via ArrayStack (LIFO) -> Deep Exploration"),
            ("Inky Ghost (Cyan)", "A* Search via Min-Heap Priority Queue -> Heuristic Search"),
            ("Clyde Ghost (Orange)", "Patrol & Scatter AI via Graph Adjacency List"),
            ("Maze Representation", "2D Linear Array matrix mapped to Mathematical Graph G=(V,E)"),
            ("Leaderboard", "High scores sorted with Binary Search Tree (BST) & QuickSort")
        ]

        card_rect = pygame.Rect(cx - 380, 130, 760, 220)
        pygame.draw.rect(self.screen, (22, 25, 40), card_rect, border_radius=8)
        pygame.draw.rect(self.screen, (50, 60, 95), card_rect, 2, border_radius=8)

        fy = 145
        for title, desc in features:
            t_s = self.font_small.render(title, True, COLOR_TEXT_HIGHLIGHT)
            d_s = self.font_small.render(f": {desc}", True, COLOR_TEXT_WHITE)
            self.screen.blit(t_s, (cx - 360, fy))
            self.screen.blit(d_s, (cx - 360 + t_s.get_width(), fy))
            fy += 32

        # Leaderboard Preview from BST (Sorted using BST In-Order Traversal)
        lb_y = 370
        lb_title = self.font_medium.render("TOP SCORES (Stored in Binary Search Tree):", True, COLOR_ACCENT_GREEN)
        self.screen.blit(lb_title, (cx - lb_title.get_width() // 2, lb_y))
        lb_y += 30

        top_scores = self.leaderboard_bst.get_top_n(4)
        for idx, (score, name) in enumerate(top_scores):
            entry_txt = f"#{idx + 1}  {name:12s} -  {score:5d} PTS"
            entry_surf = self.font_small.render(entry_txt, True, COLOR_TEXT_WHITE)
            self.screen.blit(entry_surf, (cx - entry_surf.get_width() // 2, lb_y))
            lb_y += 22

        # Start prompt
        prompt_surf = self.font_medium.render("PRESS [SPACE] TO START GAME", True, (255, 255, 0))
        self.screen.blit(prompt_surf, (cx - prompt_surf.get_width() // 2, 540))

        inst_surf = self.font_small.render("Controls: Arrow Keys to Move | [V] Toggle DSA Visualizer | [P] Pause | [ESC] Exit", True, COLOR_TEXT_MUTED)
        self.screen.blit(inst_surf, (cx - inst_surf.get_width() // 2, 580))

    def run(self):
        """Main game loop."""
        while self.is_running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()


if __name__ == "__main__":
    game = PacmanGame()
    game.run()
