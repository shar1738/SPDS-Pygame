import pygame as pg
import random
from functions import Animation
import settings as S


IS_INV = False

# Configuration for asteroid assets
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
        # Preload one-frame animations for each asteroid type
        self.assets = {}
        for name, cfg in ASSET_CONFIG.items():
            anim = Animation(cfg["paths"], cfg.get("speed", 0.1), cfg.get("size"))
            self.assets[name] = {
                "image": anim.get_current_frame(),
                "hitbox_offset": cfg["hitbox_offset"],
            }

        self.asteroid_list  = []
        self.spawn_timer    = 0      # ms until next spawn
        self.spawn_interval = 150
        self.is_inv = IS_INV
        self.inv_timer = 0
        self.can_spawn = True
        
            
    def calc_right(self):
        return S.SCREEN_WIDTH + 50

    def spawn_rand(self, amount=1):
        for _ in range(amount):
            name, data = random.choice(list(self.assets.items()))
            img         = data["image"]
            offset      = data["hitbox_offset"]

            x = self.calc_right()
            y = random.randint(0, S.SCREEN_HEIGHT - img.get_height())
            speed = random.uniform(3, 5)

            self.asteroid_list.append({
                "image":        img,
                "pos":          [x, y],
                "speed":        speed,
                "hitbox_offset": offset,
            })


    def calculate_hitbox(self, pos, offset):
        ox, oy, w, h = offset
        return pg.Rect(
            int(pos[0] + ox),
            int(pos[1] + oy),
            int(w),
            int(h)
        )

    def update(self, dt):
        """
        Advance spawn timer and generate new asteroids as needed.
        """
        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and self.can_spawn == True:
            self.spawn_timer += self.spawn_interval
            self.spawn_rand(1)


    def update_and_draw(self, screen, ship):
        """
        Move asteroids, test collisions with `ship`, draw them,
        handle game over, and remove any that collided or went off-screen.
        """
        if pg.display.get_surface() is None:
            return

        # Decrease invulnerability timer
        if self.is_inv:
            self.inv_timer -= 1
            if self.inv_timer <= 0:
                self.is_inv = False

        to_remove = []

        for a in self.asteroid_list:
            # Move left; speed up if ship is boosting
            speed_factor = 1.5 if getattr(ship, 'is_boosting', False) else 1.0
            a["pos"][0] -= a["speed"] * speed_factor

            # Collision detection using pixel-perfect masks
            asteroid_mask = pg.mask.from_surface(a["image"])
            asteroid_rect = a["image"].get_rect(topleft=(int(a["pos"][0]), int(a["pos"][1])))

            # Compute the offset between the ship and asteroid for mask overlap
            offset = (
                asteroid_rect.left - ship.rect.left,
                asteroid_rect.top - ship.rect.top
            )

            if ship.mask.overlap(asteroid_mask, offset):
                if not self.is_inv:
                    ship.take_damage(25)
                    ship.is_damaged = True
                    ship.damage_timer = 0.5

                    self.is_inv = True
                    self.inv_timer = 120  # e.g., 2 seconds at 60 FPS

                to_remove.append(a)
                continue

            # Off-screen cleanup
            if asteroid_rect.right < 0:
                to_remove.append(a)
                continue

            # Draw asteroid
            screen.blit(a["image"], (int(a["pos"][0]), int(a["pos"][1])))

        # Cleanup
        for a in to_remove:
            if a in self.asteroid_list:
                self.asteroid_list.remove(a)
