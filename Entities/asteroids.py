import pygame as pg
import random
from functions import load_assets
import settings as S


ASSET_CONFIG = {
    f"asteroid{i}": {
        "path": f"Assets/images/asteroid{i}.png",
        "size": (50, 50),
        "hitbox_offset": (12.5, 12.5, 25, 25),
    }
    for i in range(1, 5)
}

class Asteroids:
    def __init__(self):
        self.assets = load_assets(ASSET_CONFIG)
        self.asteroid_list = []

        self.is_boosting = False


        # spawn‐timer in milliseconds
        self.spawn_timer = 0
        self.spawn_interval = 200

    def calc_right(self):
        return S.SCREEN_WIDTH + 50

    def spawn_rand(self, amount=1):
        for _ in range(amount):
            name, data = random.choice(list(self.assets.items()))
            img    = data["image"]
            offset = data["hitbox_offset"]

            x = self.calc_right()
            y = random.randint(0, S.SCREEN_HEIGHT - img.get_height())
            speed = random.uniform(3,5)


            self.asteroid_list.append({
                "name":          name,
                "image":         img,
                "pos":           [x, y],
                "speed":         speed,
                "hitbox_offset": offset,
            })

    def calculate_hitbox(self, pos, offset):
        ox, oy, w, h = offset
        return pg.Rect(pos[0] + ox, pos[1] + oy, w, h)

    def update(self, dt):
        """
        Call every frame with the elapsed milliseconds since last frame.
        Spawns one new asteroid whenever spawn_timer ≤ 0.
        """
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer += self.spawn_interval
            self.spawn_rand(1)

    def update_and_draw(self, screen, ship_rect: pg.Rect, ship_mask: pg.Mask, is_boosting: bool):
        to_remove = []
        for a in self.asteroid_list:
            speed_factor = 1.5 if is_boosting else 1.0
            a["pos"][0] -= a["speed"] * speed_factor

            ast_box = self.calculate_hitbox(a["pos"], a["hitbox_offset"])

            # Create asteroid mask
            asteroid_mask = pg.mask.from_surface(a["image"])
            offset = (int(ast_box.left - ship_rect.left), int(ast_box.top - ship_rect.top))

            if ship_mask.overlap(asteroid_mask, offset):
                print(f"Collision with {a['name']}")
                to_remove.append(a)
                continue

            if ast_box.right < 0:
                to_remove.append(a)
                continue

            screen.blit(a["image"], a["pos"])
            #pg.draw.rect(screen, (0, 255, 0), ast_box, 1)

        for a in to_remove:
            self.asteroid_list.remove(a)

