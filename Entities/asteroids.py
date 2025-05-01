import pygame as pg
import random
import sys
from functions import Animation
import settings as S

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
        self.spawn_interval = 200    # spawn every 200 ms

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
        if self.spawn_timer <= 0:
            self.spawn_timer += self.spawn_interval
            self.spawn_rand(1)

    def update_and_draw(self, screen, ship):
        """
        Move asteroids, test collisions with `ship`, draw them,
        handle game over, and remove any that collided or went off-screen.
        """
        # If display is closed, do nothing
        if pg.display.get_surface() is None:
            return

        to_remove = []

        for a in self.asteroid_list:
            # Move left; speed up if ship is boosting
            speed_factor = 1.5 if getattr(ship, 'is_boosting', False) else 1.0
            a["pos"][0] -= a["speed"] * speed_factor

            # Collision test
            ast_box       = self.calculate_hitbox(a["pos"], a["hitbox_offset"])
            asteroid_mask = pg.mask.from_surface(a["image"])
            offset        = (
                ast_box.left - ship.rect.left,
                ast_box.top  - ship.rect.top
            )

            if ship.mask.overlap(asteroid_mask, offset):
                ship.take_damage(25)

                # Game over if health depleted
                if ship.health <= 0:
                    # Load and blit game over image at center
                    game_over_img = pg.image.load(
                        "Assets/images/ui/game_over.png"
                    ).convert_alpha()
                    rect = game_over_img.get_rect(
                        center=(S.SCREEN_WIDTH // 2, S.SCREEN_HEIGHT // 2)
                    )
                    screen.blit(game_over_img, rect.topleft)
                    pg.display.flip()
                    pg.time.delay(2000)
                    pg.quit()
                    sys.exit()

                to_remove.append(a)
                continue

            # Off-screen cleanup
            if ast_box.right < 0:
                to_remove.append(a)
                continue

            # Draw asteroid
            screen.blit(
                a["image"],
                (int(a["pos"][0]), int(a["pos"][1]))
            )

        # Remove collided/off-screen asteroids
        for a in to_remove:
            if a in self.asteroid_list:
                self.asteroid_list.remove(a)
