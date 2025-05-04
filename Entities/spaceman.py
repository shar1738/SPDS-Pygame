import pygame as pg
from funcs_data.functions import Animation

SPACEMAN_MOVE_ANIMATION = {
    "paths": [
        "Assets/images/spaceman/spaceman1.png",
        "Assets/images/spaceman/spaceman2.png",
        "Assets/images/spaceman/spaceman3.png",
    ],
    "size":  (200, 200),
    "speed": 0.3,
}

MOVE_SPEED = 0.1
FRICTION = 0.96

class Spaceman:
    def __init__(self, x, y, boundary_rect=None):
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.anim = Animation(
            SPACEMAN_MOVE_ANIMATION["paths"],
            size=SPACEMAN_MOVE_ANIMATION["size"],
            speed=SPACEMAN_MOVE_ANIMATION["speed"]
        )
        self.image = self.anim.get_current_frame()
        self.rect = self.image.get_rect(center=self.pos)
        self.boundary_rect = boundary_rect
        self.facing_left = False

    def update(self, keys):
        # Check for movement input
        moving = False

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x -= MOVE_SPEED
            self.facing_left = True
            moving = True
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x += MOVE_SPEED
            self.facing_left = False
            moving = True

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y -= MOVE_SPEED
            moving = True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y += MOVE_SPEED
            moving = True

        # Apply friction and update position
        self.vel *= FRICTION
        self.pos += self.vel

        # Only update animation if movement is detected
        if moving:
            self.anim.update()

        frame = self.anim.get_current_frame()
        if self.facing_left:
            frame = pg.transform.flip(frame, True, False)
        self.image = frame

        # Clamp to screen or boundary
        self.rect = self.image.get_rect(center=self.pos)

        if self.boundary_rect:
            self.rect.clamp_ip(self.boundary_rect)
        else:
            screen_rect = pg.display.get_surface().get_rect()
            self.rect.clamp_ip(screen_rect)

        self.pos = pg.Vector2(self.rect.center)


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
