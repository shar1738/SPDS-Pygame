import pygame as pg
import random
from functions import Animation
import settings as S

ASSET_CONFIG = {
    f"asteroid{i}": {
        "paths": [f"Assets/images/asteroid{i}.png"],
        "size": (50, 50),
        "hitbox_offset": (12.5, 12.5, 25, 25),
    }
    for i in range(1, 5)
}

class Asteroids:
    def __init__(self):
        # Instead of using load_assets, we manually load each asset using the Animation class.
        self.assets = {}
        for name, cfg in ASSET_CONFIG.items():
            # Use a default animation speed (0.1 seconds per frame) if not specified.
            speed = cfg.get("speed", 0.1)
            anim = Animation(cfg["paths"], speed, cfg.get("size"))
            self.assets[name] = {
                "image": anim.get_current_frame(),
                "hitbox_offset": cfg["hitbox_offset"],
            }
        self.asteroid_list = []
        self.is_boosting = False

        # Spawn timer in milliseconds.
        self.spawn_timer = 0
        self.spawn_interval = 200

    def calc_right(self):
        return S.SCREEN_WIDTH + 50

    def spawn_rand(self, amount=1):
        for _ in range(amount):
            # Randomly choose one of the asteroid assets.
            name, data = random.choice(list(self.assets.items()))
            img = data["image"]
            offset = data["hitbox_offset"]

            x = self.calc_right()
            # Ensure the asteroid stays within the vertical limits of the screen.
            y = random.randint(0, S.SCREEN_HEIGHT - img.get_height())
            speed = random.uniform(3, 5)

            self.asteroid_list.append({
                "name": name,
                "image": img,
                "pos": [x, y],  # Using a mutable list to represent [x, y] position.
                "speed": speed,
                "hitbox_offset": offset,
            })

    def calculate_hitbox(self, pos, offset):
        # Unpack the offset, converting any fractional values to integers.
        ox, oy, w, h = offset
        return pg.Rect(int(pos[0] + ox), int(pos[1] + oy), int(w), int(h))

    def update(self, dt):
        """
        Called every frame with the elapsed time (in ms) since the last frame.
        Spawns a new asteroid whenever the spawn timer reaches 0.
        """
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer += self.spawn_interval
            self.spawn_rand(1)

    def update_and_draw(self, screen, ship_rect: pg.Rect, ship_mask: pg.Mask, is_boosting: bool):
        to_remove = []
        for a in self.asteroid_list:
            # Move the asteroid left; if the ship is boosting, increase its speed.
            speed_factor = 1.5 if is_boosting else 1.0
            a["pos"][0] -= a["speed"] * speed_factor

            ast_box = self.calculate_hitbox(a["pos"], a["hitbox_offset"])
            asteroid_mask = pg.mask.from_surface(a["image"])
            # Calculate the offset between the asteroid and ship for mask collision.
            offset = (int(ast_box.left - ship_rect.left), int(ast_box.top - ship_rect.top))

            if ship_mask.overlap(asteroid_mask, offset):
                print(f"Collision with {a['name']}")
                to_remove.append(a)
                continue

            # Remove the asteroid if it has moved off the left side of the screen.
            if ast_box.right < 0:
                to_remove.append(a)
                continue

            # Blit the asteroid image; ensure the position is an integer tuple.
            screen.blit(a["image"], (int(a["pos"][0]), int(a["pos"][1])))
            # Optionally, draw the hitbox for debugging:
            # pg.draw.rect(screen, (0, 255, 0), ast_box, 1)

        # Remove asteroids that have either collided or gone offscreen.
        for a in to_remove:
            if a in self.asteroid_list:
                self.asteroid_list.remove(a)
