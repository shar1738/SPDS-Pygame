import pygame as pg
from constants import ASSET_CONFIG, load_assets
import math

ROTATION_SPEED = 3
THRUST_POWER = 0.3
FRICTION = 0.97

class Ship:
    def __init__(self, x, y):
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.angle = 0

        self.assets = load_assets()
        self.ship_data = self.assets["ship"]

        self.image = self.ship_data["image"]
        self.original_image = self.image
        self.hitbox_offset = self.ship_data["hitbox_offset"]

        self.image_rect = self.image.get_rect(center=self.pos)

    def update(self, keys):
        if keys[pg.K_LEFT]:
            self.angle += ROTATION_SPEED
        if keys[pg.K_RIGHT]:
            self.angle -= ROTATION_SPEED

        if keys[pg.K_UP]:
            radians = math.radians(self.angle)
            thrust = pg.Vector2(math.cos(radians), -math.sin(radians)) * THRUST_POWER
            self.vel += thrust

        self.vel *= FRICTION
        self.pos += self.vel

    def draw(self, surface):
        rotated_image = pg.transform.rotate(self.original_image, self.angle)
        self.image_rect = rotated_image.get_rect(center=self.pos)  
        surface.blit(rotated_image, self.image_rect.topleft)

    def get_hitbox(self):
        radians = math.radians(self.angle)
        hit_x, hit_y, width, height = self.hitbox_offset
        
        # Adjust hitbox based on rotation
        rotated_hitbox_x = hit_x * math.cos(radians) - hit_y * math.sin(radians)
        rotated_hitbox_y = hit_x * math.sin(radians) + hit_y * math.cos(radians)
        
        return pg.Rect(
            self.image_rect.centerx + rotated_hitbox_x - width // 2,
            self.image_rect.centery + rotated_hitbox_y - height // 2,
            width,
            height
        )

