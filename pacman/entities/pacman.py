"""
Pac-Man Player Entity
Handles player movement, direction buffering, grid alignment, and animation.
"""

import math
import pygame
from config import (
    TILE_SIZE, HEADER_HEIGHT, PACMAN_SPEED,
    COLOR_PACMAN, COLOR_PACMAN_MOUTH, DIRECTIONS
)

class Pacman:
    def __init__(self, start_row: int = 16, start_col: int = 10):
        self.start_row = start_row
        self.start_col = start_col
        self.lives = 3
        self.score = 0
        self.mouth_angle = 0.0
        self.mouth_speed = 0.25
        self.mouth_opening = True
        self.reset_position()

    def reset_position(self):
        """Reset coordinates to spawn point."""
        self.row = self.start_row
        self.col = self.start_col
        self.x = self.col * TILE_SIZE + TILE_SIZE // 2
        self.y = HEADER_HEIGHT + self.row * TILE_SIZE + TILE_SIZE // 2
        self.current_dir = 'NONE'
        self.next_dir = 'NONE'
        self.speed = PACMAN_SPEED
        self.is_alive = True

    def set_next_direction(self, dir_name: str):
        """Buffer direction requested by player."""
        if dir_name in DIRECTIONS:
            self.next_dir = dir_name

    def update(self, maze):
        """
        Update Pac-Man's position and handle grid navigation.
        """
        if not self.is_alive:
            return

        # Animate mouth chomp
        if self.current_dir != 'NONE':
            if self.mouth_opening:
                self.mouth_angle += self.mouth_speed
                if self.mouth_angle >= 0.8:
                    self.mouth_opening = False
            else:
                self.mouth_angle -= self.mouth_speed
                if self.mouth_angle <= 0.05:
                    self.mouth_opening = True

        # Compute current tile center in pixels
        curr_r = int((self.y - HEADER_HEIGHT) // TILE_SIZE)
        curr_c = int(self.x // TILE_SIZE)
        tile_center_x = curr_c * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = HEADER_HEIGHT + curr_r * TILE_SIZE + TILE_SIZE // 2

        # Check if next_dir is reverse of current_dir (can turn immediately)
        if self.next_dir != 'NONE' and self.next_dir != self.current_dir:
            cur_dx, cur_dy = DIRECTIONS[self.current_dir]
            nxt_dx, nxt_dy = DIRECTIONS[self.next_dir]
            if cur_dx == -nxt_dx and cur_dy == -nxt_dy:
                self.current_dir = self.next_dir

        # Attempt turn when sufficiently aligned with tile center
        if self.next_dir != 'NONE' and self.next_dir != self.current_dir:
            dist_to_center = math.hypot(self.x - tile_center_x, self.y - tile_center_y)
            if dist_to_center <= self.speed + 1.5:
                nxt_dx, nxt_dy = DIRECTIONS[self.next_dir]
                target_r = curr_r + nxt_dy
                target_c = curr_c + nxt_dx

                if maze.is_walkable(target_r, target_c):
                    # Snap to tile center line to prevent drifting
                    if nxt_dx != 0:
                        self.y = tile_center_y
                    if nxt_dy != 0:
                        self.x = tile_center_x
                    self.current_dir = self.next_dir

        # Move in current direction if path ahead is clear
        if self.current_dir != 'NONE':
            dx, dy = DIRECTIONS[self.current_dir]
            next_x = self.x + dx * self.speed
            next_y = self.y + dy * self.speed

            # Calculate the tile ahead
            front_x = next_x + dx * (TILE_SIZE // 2 - 2)
            front_y = next_y + dy * (TILE_SIZE // 2 - 2)
            check_r = int((front_y - HEADER_HEIGHT) // TILE_SIZE)
            check_c = int(front_x // TILE_SIZE)

            # Handle wrap-around tunnel at row 10
            if curr_r == 10:
                if self.x < 0:
                    self.x = maze.cols * TILE_SIZE
                elif self.x > maze.cols * TILE_SIZE:
                    self.x = 0
                else:
                    self.x = next_x
                    self.y = next_y
            elif maze.is_walkable(check_r, check_c):
                self.x = next_x
                self.y = next_y
            else:
                # Snap right into tile center
                if dx != 0:
                    self.x = tile_center_x
                if dy != 0:
                    self.y = tile_center_y
                self.current_dir = 'NONE'

        # Update current grid indices
        self.row = int((self.y - HEADER_HEIGHT) // TILE_SIZE)
        self.col = int(self.x // TILE_SIZE)

        # Eat pellet on current tile
        points, is_power = maze.eat_pellet(self.row, self.col)
        if points > 0:
            self.score += points
        return is_power

    def render(self, surface: pygame.Surface):
        """Draw animated Pac-Man with wedge mouth opening in movement direction."""
        radius = TILE_SIZE // 2 - 2
        center = (int(self.x), int(self.y))

        # Base rotation angle according to direction
        dir_angles = {
            'RIGHT': 0.0,
            'DOWN': 0.5 * math.pi,
            'LEFT': 1.0 * math.pi,
            'UP': 1.5 * math.pi,
            'NONE': 0.0
        }
        base_angle = dir_angles.get(self.current_dir, 0.0)
        mouth_span = self.mouth_angle

        # If mouth is almost closed, draw full circle
        if mouth_span <= 0.08:
            pygame.draw.circle(surface, COLOR_PACMAN, center, radius)
            return

        # Draw filled pie/wedge using polygon
        points = [center]
        steps = 24
        start_a = base_angle + mouth_span
        end_a = base_angle + 2 * math.pi - mouth_span
        for i in range(steps + 1):
            theta = start_a + (end_a - start_a) * (i / steps)
            px = center[0] + radius * math.cos(theta)
            py = center[1] + radius * math.sin(theta)
            points.append((px, py))

        pygame.draw.polygon(surface, COLOR_PACMAN, points)
