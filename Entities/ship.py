import pygame as pg
from functions import load_assets
from functions import Animation  # Make sure Animation class is available here

THRUST_POWER    = 0.3
FRICTION        = 0.97
ROTATION_SPEED  = 3     

SHIP_CONFIG = {
    "ship": {
        "path":          "Assets/images/ship/Fire_Small.png",
        "size":          (150, 150),
        "hitbox_offset": (25, 25, 100, 75),
    },
}

BOOST_ANIMATION = {
    "paths": [
        "Assets/images/ship/Fire_Small.png",
        "Assets/images/ship/Fire_Medum.png",
        "Assets/images/ship/Fire_Large.png",
    ]
}

BASIC_ANIMATION = {
    "paths": [
        "Assets/images/ship/Hyper_Plasma.png",
        "Assets/images/ship/Hyper_Plasma.png",
    ]
}

class Ship:
    def __init__(self, x, y):
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        data = load_assets(SHIP_CONFIG)["ship"]
        self.original_image = data["image"]
        self.hitbox_offset  = data["hitbox_offset"]

        self.angle = 0
        self.image = self.original_image
        self.rect  = self.image.get_rect(center=self.pos)
        self.mask  = pg.mask.from_surface(self.image)

        self.basic_anim = self.boost_anim = Animation(BASIC_ANIMATION["paths"], speed=0.1, size=(150, 150))

        self.is_boosting = False
        self.boost_anim = Animation(BOOST_ANIMATION["paths"], speed=0.1, size=(150, 150))

    def update(self, keys):
        if keys[pg.K_LEFT]:
            self.angle = (self.angle + ROTATION_SPEED) % 360

        if keys[pg.K_RIGHT]:
            self.angle = (self.angle - ROTATION_SPEED) % 360

        if keys[pg.K_UP]:
            direction = pg.Vector2(0, -1).rotate(self.angle)
            self.vel += direction * THRUST_POWER

        if keys[pg.K_DOWN]:
            direction = pg.Vector2(0, 1).rotate(self.angle)
            self.vel += direction * THRUST_POWER * 0.5

        self.is_boosting = keys[pg.K_SPACE]

        self.vel *= FRICTION
        self.pos.y += self.vel.y
        self.pos.x = 150  # Fixed x position

        # Clamp Y within window bounds
        w, h = pg.display.get_surface().get_size()
        self.pos.y = max(0, min(h, self.pos.y))

    def draw(self, surface):
        # Draw boost flame first if boosting
        if self.is_boosting:
            self.boost_anim.update()
            boost_img = self.boost_anim.get_current_frame()
        else:
            self.basic_anim.update()
            boost_img = self.basic_anim.get_current_frame()

        # Rotate and draw ship
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect  = self.image.get_rect(center=self.pos)
        self.mask  = pg.mask.from_surface(self.image)
        surface.blit(self.image, self.rect.topleft)

    def get_hitbox(self) -> pg.Rect:
        ox, oy, w, h = self.hitbox_offset
        return pg.Rect(self.rect.left + ox, self.rect.top + oy, w, h)

    def get_mask(self):
        return self.mask
