import pygame as pg
import random
from functions import load_assets
import settings as S

ASSET_CONFIG = {
    "asteroid1": {
        "path": "Assets/images/asteroid1.png",
        "size": (128, 128),
        "hitbox_offset": (32, 32, 64, 64)
    },
    "asteroid2": {
        "path": "Assets/images/asteroid2.png",
        "size": (128, 128),
        "hitbox_offset": (32, 32, 64, 64)
    },
    "asteroid3": {
        "path": "Assets/images/asteroid3.png",
        "size": (128, 128),
        "hitbox_offset": (32, 32, 64, 64)
    },
    "asteroid4": {
        "path": "Assets/images/asteroid4.png",
        "size": (128, 128),
        "hitbox_offset": (32, 32, 64, 64)
    },
    "asteroid5": {
        "path": "Assets/images/asteroid5.png",
        "size": (128, 128),
        "hitbox_offset": (32, 32, 64, 64)
    },
}


class Asteroids:
    def __init__(self):
        self.assets = load_assets(ASSET_CONFIG)  # Load assets with images and hitbox data
        self.SCREEN_WIDTH = S.SCREEN_WIDTH
        self.SCREEN_HEIGHT = S.SCREEN_HEIGHT
        self.asteroid_list = []  # List to store active asteroid instances

    def calc_right(self):
        return self.SCREEN_WIDTH + 50  # Spawn just off-screen to the right

    def rand_aster(self):
        return random.choice(list(self.assets.items()))

    def spawn_rand(self, amount):
        for _ in range(amount):
            name, data = self.rand_aster()
            img = data["image"]
            hitbox_offset = data["hitbox_offset"]
            img_width, img_height = img.get_size()

            x = self.calc_right()
            y = random.randint(0, self.SCREEN_HEIGHT - img_height)

            asteroid = {
                "name": name,
                "image": img,
                "pos": [x, y],
                "speed": random.uniform(1.0, 3.0),
                "hitbox_offset": hitbox_offset,
            }

            self.asteroid_list.append(asteroid)

    def update_and_draw(self, screen):
        to_remove = []

        for asteroid in self.asteroid_list:
            asteroid["pos"][0] -= asteroid["speed"]  # Move left

            # Remove if completely off-screen
            if asteroid["pos"][0] + asteroid["image"].get_width() < 0:
                to_remove.append(asteroid)
                continue

            # Draw asteroid
            screen.blit(asteroid["image"], asteroid["pos"])
            # Optional: draw hitbox
            hitbox = self.calculate_hitbox(asteroid["pos"], asteroid["hitbox_offset"])
            pg.draw.rect(screen, (0, 255, 0), hitbox, 1)

        # Clean up off-screen asteroids
        for asteroid in to_remove:
            self.asteroid_list.remove(asteroid)

    def get_hitboxes(self):
        hitboxes = []
        for asteroid in self.asteroid_list:
            x, y = asteroid["pos"]
            offset = asteroid["hitbox_offset"]
            hitbox = pg.Rect(x + offset[0], y + offset[1], offset[2], offset[3])
            hitboxes.append((asteroid["name"], hitbox))
        return hitboxes

    def calculate_hitbox(self, pos, offset):
        x, y = pos
        offset_x, offset_y, width, height = offset
        return pg.Rect(x + offset_x, y + offset_y, width, height)
