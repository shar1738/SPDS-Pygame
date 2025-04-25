import pygame as pg
from functions import load_assets

THRUST_POWER = 0.3
FRICTION = 0.97

ASSET_CONFIG = {
    "ship": {
        "path": "Assets/images/ship.png",
        "size": (256, 256),
        "hitbox_offset": (64, 64, 128, 128),
    },
}

class Ship:
    def __init__(self, x, y):
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)

        self.assets = load_assets(ASSET_CONFIG)
        self.ship_data = self.assets["ship"]

        self.image = self.ship_data["image"]
        self.original_image = self.image
        self.hitbox_offset = self.ship_data["hitbox_offset"]

        self.image_rect = self.image.get_rect(center=self.pos)

    def update(self, keys):
        # Allow vertical movement only
        if keys[pg.K_UP]:
            self.vel.y -= THRUST_POWER
        if keys[pg.K_DOWN]:
            self.vel.y += THRUST_POWER

        self.vel *= FRICTION
        self.pos += self.vel

        # Keep the ship within screen bounds (optional)
        screen_height = pg.display.get_surface().get_height()
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = 0
        if self.pos.y > screen_height:
            self.pos.y = screen_height
            self.vel.y = 0

    def draw(self, surface):
        # No rotation needed
        self.image_rect = self.original_image.get_rect(center=self.pos)
        surface.blit(self.original_image, self.image_rect.topleft)

    def get_hitbox(self):
        hit_x, hit_y, width, height = self.hitbox_offset
        return pg.Rect(
            self.image_rect.left + hit_x,
            self.image_rect.top + hit_y,
            width,
            height
        )
