import pygame as pg
import random
import time

import settings as S
from Code.Funcs_data.helper_functions import Animation

import Code.Funcs_data.asset_data as asset_data

ASTEROID_SIZE = asset_data.ASTEROID_SIZE
DAMAGE_AMOUNT = 25

asset_data.collision_sfx.set_volume(0.5)

class Asteroids:
    def __init__(self):
        self.assets = {
            name: {
                "image": Animation(cfg["paths"], cfg.get("speed", 0.1), cfg["size"]).get_current_frame(),
                "hitbox_offset": cfg["hitbox_offset"],
            }
            for name, cfg in asset_data.ASTEROID_CONFIG.items()
        }
        self.asteroid_list = []
        self.spawn_timer = 0
        self.spawn_interval = S.SCREEN_HEIGHT // 6
        self.is_inv = False
        self.inv_duration = 3.5  # Invincibility lasts 5 seconds
        self.is_inv_start = None  # When invincibility started
        self.can_spawn = True

        # New attributes for center spawning
        self.spawn_center = False
        self.center_spawn_amt = S.SCREEN_HEIGHT // 60  # Number of asteroids to spawn in center
        self.center_spawned = False

    def calc_right(self):
        """Return the rightmost off-screen spawn position for asteroids."""
        return S.SCREEN_WIDTH + ASTEROID_SIZE[0]

    def spawn_rand(self, amount=1):
        """Spawn a random number of asteroids off-screen to the right."""
        for _ in range(amount):
            name, data = random.choice(list(self.assets.items()))
            img = data["image"]
            offset = data["hitbox_offset"]

            x = self.calc_right()
            y = random.randint(0, S.SCREEN_HEIGHT - img.get_height())
            speed = random.uniform(7, 15)

            self.asteroid_list.append({
                "image": img,
                "pos": [x, y],
                "speed": speed,
                "hitbox_offset": offset,
            })

    def calculate_hitbox(pos, offset):
        """Return a pygame.Rect for the asteroid's hitbox based on offset."""
        ox, oy, w, h = offset
        return pg.Rect(int(pos[0] + ox), int(pos[1] + oy), int(w), int(h))

    def update(self, dt):
        """Advance spawn timer and generate new asteroids as needed."""
        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and self.can_spawn:
            self.spawn_timer += self.spawn_interval
            self.spawn_rand(1)
        
    def update_and_draw(self, screen, ship, dt_ms):
        """
        Move asteroids, check collisions with the ship, draw them,
        and clean up those that go off-screen or collide.
        """
        if pg.display.get_surface() is None:
            return

        # Check if the invincibility period is over.
        if self.is_inv:
            if self.is_inv_start is None:
                # Lazy initialization in case it hasn't been set
                self.is_inv_start = time.time()
            elapsed_time = time.time() - self.is_inv_start
            if elapsed_time >= self.inv_duration:
                self.is_inv = False
                self.is_inv_start = None

        # One-time spawn of center asteroids if enabled
        if self.spawn_center and not self.center_spawned:
            self.center_spawned = True
            safe_rect = pg.Rect(150, 300, 50, 50)  # Safe area around player

            for _ in range(self.center_spawn_amt):
                name, data = random.choice(list(self.assets.items()))
                img = data["image"]
                offset = data["hitbox_offset"]

                while True:
                    x = random.randint(600, S.SCREEN_WIDTH - img.get_width())
                    y = random.randint(0, S.SCREEN_HEIGHT - img.get_height())
                    asteroid_rect = pg.Rect(x, y, img.get_width(), img.get_height())
                    if not asteroid_rect.colliderect(safe_rect):
                        break
                self.spawn_center = False

                speed = random.uniform(3, 5)
                self.asteroid_list.append({
                    "image": img,
                    "pos": [x, y],
                    "speed": speed,
                    "hitbox_offset": offset,
                })

        to_remove = []

        for a in self.asteroid_list:
            # Move the asteroid left; speed up if the ship is boosting
            self.speed_factor = 1.5 if getattr(ship, 'is_boosting', False) else 1.0
            a["pos"][0] -= a["speed"] * self.speed_factor

            asteroid_mask = pg.mask.from_surface(a["image"])
            asteroid_rect = a["image"].get_rect(topleft=(int(a["pos"][0]), int(a["pos"][1])))

            # Calculate offset for collision detection
            offset = (
                asteroid_rect.left - ship.rect.left,
                asteroid_rect.top - ship.rect.top
            )

            # Check collision with the ship
            if ship.mask.overlap(asteroid_mask, offset):
                if not self.is_inv:
                    self.is_inv = True
                    self.is_inv_start = time.time()  # Record when invincibility starts
                    # Damage the ship only on first collision that triggers invincibility
                    ship.take_damage(DAMAGE_AMOUNT)
                    ship.is_boosting = False
                    asset_data.ship_boost_sfx.stop()
                    ship.is_damaged = True
                    ship.damage_timer = 0.5
                    asset_data.collision_sfx.play()
                to_remove.append(a)
                continue

            # Check if the asteroid has moved completely off-screen to the left.
            if a["pos"][0] + a["image"].get_width() < 0:
                to_remove.append(a)
                continue

            screen.blit(a["image"], (int(a["pos"][0]), int(a["pos"][1])))

        # Remove asteroids that collided or moved off-screen.
        for a in to_remove:
            if a in self.asteroid_list:
                self.asteroid_list.remove(a)
