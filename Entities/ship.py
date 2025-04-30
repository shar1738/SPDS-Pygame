import pygame as pg
from functions import Animation

# Constants governing ship motion and rotation.
THRUST_POWER = 0.3
FRICTION = 0.97
ROTATION_SPEED = 3

# Ship visual settings.
HITBOX_OFFSET = (25, 25, 100, 75)
SCALE_FACTOR = 2  # Scale the ship's animation frames up by this factor

# Animation dictionary for the ship's appearance when not boosting.
BASIC_ANIMATION = {
    "paths": [
        "Assets/images/ship/fire_small.png",
        "Assets/images/ship/fire_medium.png",
        "Assets/images/ship/fire_large.png",
    ],
    "size": (100, 100),  # original size; will be scaled up
    "speed": 0.2,
}

# Animation dictionary for the ship's appearance when boosting.
BOOST_ANIMATION = {
    "paths": [
        "Assets/images/ship/hyper_plasma.png",
        "Assets/images/ship/hyper_plasma_extreme.png",
    ],
    "size": (100, 100),
    "speed": 2.5,
}

class Ship:
    def __init__(self, x, y):
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.hitbox_offset = HITBOX_OFFSET
        self.angle = 0
        
        # Scale up the animation frames' sizes.
        basic_size = (BASIC_ANIMATION["size"][0] * SCALE_FACTOR, BASIC_ANIMATION["size"][1] * SCALE_FACTOR)
        boost_size = (BOOST_ANIMATION["size"][0] * SCALE_FACTOR, BOOST_ANIMATION["size"][1] * SCALE_FACTOR)
        
        # Create Animation objects using the scaled-up sizes.
        self.basic_anim = Animation(BASIC_ANIMATION["paths"], speed=BASIC_ANIMATION["speed"], size=basic_size)
        self.boost_anim = Animation(BOOST_ANIMATION["paths"], speed=BOOST_ANIMATION["speed"], size=boost_size)
        self.is_boosting = False
        
        # Start with the basic animation frame as the ship image.
        self.image = self.basic_anim.get_current_frame()
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pg.mask.from_surface(self.image)
        
    def update(self, keys):
        # Rotate the ship.
        if keys[pg.K_RIGHT]:
            self.angle = (self.angle + ROTATION_SPEED) % 360
        if keys[pg.K_LEFT]:
            self.angle = (self.angle - ROTATION_SPEED) % 360

        # Apply thrust forward/backward.
        if keys[pg.K_UP]:
            direction = pg.Vector2(0, -1).rotate(self.angle)
            self.vel += direction * THRUST_POWER
        if keys[pg.K_DOWN]:
            direction = pg.Vector2(0, 1).rotate(self.angle)
            self.vel += direction * THRUST_POWER * 0.5

        self.is_boosting = keys[pg.K_SPACE]

        # Apply friction.
        self.vel *= FRICTION

        # Update position (with fixed X).
        self.pos += self.vel
        self.pos.x = 150

        # Clamp Y to the screen boundaries.
        w, h = pg.display.get_surface().get_size()
        self.pos.y = max(0, min(h, self.pos.y))
    
    def draw(self, surface):
        # Select and update the appropriate animation.
        if self.is_boosting:
            self.boost_anim.update()
            frame = self.boost_anim.get_current_frame()
        else:
            self.basic_anim.update()
            frame = self.basic_anim.get_current_frame()
        
        # Rotate the selected frame using rotozoom (no additional scaling needed since size is already scaled up).
        rotated_frame = pg.transform.rotozoom(frame, -self.angle, 1)
        self.image = rotated_frame
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pg.mask.from_surface(self.image)
        
        # Draw the ship.
        surface.blit(self.image, self.rect.topleft)
    
    def get_hitbox(self) -> pg.Rect:
        ox, oy, w, h = self.hitbox_offset
        return pg.Rect(self.rect.left + ox, self.rect.top + oy, w, h)
    
    def get_mask(self):
        return self.mask
