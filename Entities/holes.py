import pygame as pg
import random

class Holes:
    def __init__(self, amount, interior_rect):
        self.interior_rect = interior_rect
        self.amount = amount  # Set the number of holes
        self.hole_paths = [
            'Assets/images/minigame/hole1.png',
            'Assets/images/minigame/hole2.png',
            'Assets/images/minigame/hole3.png',
            'Assets/images/minigame/hole4.png'
        ]

        self.holes = []  # Store all hole objects
        for _ in range(self.amount):
            self.spawn_hole()

    def spawn_hole(self):
        """Randomly places a hole only at the top (with an offset) or in the center."""
        random_hole_path = random.choice(self.hole_paths)
        original_hole = pg.image.load(random_hole_path).convert_alpha()
        hole = pg.transform.scale(original_hole, (80, 80))  # Adjust hole size

        # Choose between top or center spawn
        position_type = random.choice(["top", "center"])

        if position_type == "top":
            hole_x = random.randint(self.interior_rect.left, self.interior_rect.right - hole.get_width())
            hole_y = self.interior_rect.top + 40  # Offset top holes by 20 pixels down
        elif position_type == "center":
            hole_x = random.randint(self.interior_rect.left, self.interior_rect.right - hole.get_width())
            hole_y = random.randint(self.interior_rect.top + self.interior_rect.height // 3, 
                                    self.interior_rect.bottom - self.interior_rect.height // 3)

        hole_rect = hole.get_rect(topleft=(hole_x, hole_y))
        self.holes.append((hole, hole_rect))  # Store hole image & rect


    def draw(self, surface):
        """Render all holes"""
        for hole, hole_rect in self.holes:
            surface.blit(hole, hole_rect.topleft)