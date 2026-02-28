import pygame as pg
import random


class Holes:
    # Class‐level storage to persist hole positions across instances
    hole_positions = []

    def __init__(self, amount, interior_rect):
        self.interior_rect = interior_rect
        self.amount = amount  # Number of holes desired
        self.hole_paths = [
            "Assets/images/interior/minigame/hole1.png",
            "Assets/images/interior/minigame/hole2.png",
            "Assets/images/interior/minigame/hole3.png",
            "Assets/images/interior/minigame/hole4.png",
        ]

        # Instance lists
        self.holes = []  # List of (surface, rect)
        self.hole_positions = []  # List of (x, y) tuples

        # Recreate at stored positions if matching count, else fresh spawn
        if Holes.hole_positions and len(Holes.hole_positions) == self.amount:
            for x, y in Holes.hole_positions:
                self._create_hole_at(x, y)
        else:
            for _ in range(self.amount):
                self.spawn_hole()

        # Update cache with current positions
        Holes.hole_positions = list(self.hole_positions)

    def _create_hole_at(self, x, y):
        """Helper: create hole image/rect at specific coords and record it."""
        path = random.choice(self.hole_paths)
        img = pg.image.load(path).convert_alpha()
        hole = pg.transform.scale(img, (80, 80))
        rect = hole.get_rect(topleft=(x, y))
        self.holes.append((hole, rect))
        self.hole_positions.append((x, y))

    def spawn_hole(self):
        """Randomly place one hole and record its position."""
        path = random.choice(self.hole_paths)
        original = pg.image.load(path).convert_alpha()
        hole = pg.transform.scale(original, (80, 80))

        if random.choice([True, False]):
            # Top area
            x = random.randint(
                self.interior_rect.left, self.interior_rect.right - hole.get_width()
            )
            y = self.interior_rect.top + 40
        else:
            # Center area
            x = random.randint(
                self.interior_rect.left, self.interior_rect.right - hole.get_width()
            )
            y = random.randint(
                self.interior_rect.top + self.interior_rect.height // 3,
                self.interior_rect.bottom - self.interior_rect.height // 3,
            )

        rect = hole.get_rect(topleft=(x, y))
        self.holes.append((hole, rect))
        self.hole_positions.append((x, y))

    def draw(self, surface):
        """Render all holes on the given surface."""
        for hole, rect in self.holes:
            surface.blit(hole, rect.topleft)
