import pygame as pg
import time
from functions import Animation

# Constants
THRUST_POWER       = 0.3
FRICTION           = 0.97
ROTATION_SPEED     = 3
MAX_ANGLE          = 60  # degrees up and down


SCALE_FACTOR       = 2

HEALTH             = 150

BASIC_ANIMATION = {
    "paths": [
        "Assets/images/ship/fire_mini.png",
        "Assets/images/ship/fire_small.png",
        "Assets/images/ship/fire_medium.png",
        "Assets/images/ship/fire_large.png",
        "Assets/images/ship/fire_colossal.png",
    ],
    "size":  (100, 100),
    "speed": 0.15,
}

BOOST_ANIMATION = {
    "paths": [
        "Assets/images/ship/hyper_plasma.png",
        "Assets/images/ship/hyper_plasma.png",
        "Assets/images/ship/hyper_plasma.png",
        "Assets/images/ship/hyper_plasma_extreme.png",
        "Assets/images/ship/hyper_plasma_extreme.png",
        "Assets/images/ship/hyper_plasma_extreme.png",
        "Assets/images/ship/hyper_plasma_extreme.png",
        "Assets/images/ship/hyper_plasma_extreme.png",
        "Assets/images/ship/hyper_plasma_extreme.png",
        "Assets/images/ship/hyper_plasma_extreme.png",
    ],
    "size":  (100, 100),
    "speed": 0.5,
}

class Ship:
    def __init__(self, x, y):
        pg.init()

        # Position and movement
        self.pos             = pg.Vector2(x, y)
        self.vel             = pg.Vector2(0, 0)
        self.angle           = 0
        self.is_boosting     = False

        # Ship stats
        self.health          = HEALTH

        # Load and scale animations
        basic_size = (
            BASIC_ANIMATION["size"][0] * SCALE_FACTOR,
            BASIC_ANIMATION["size"][1] * SCALE_FACTOR
        )
        boost_size = (
            BOOST_ANIMATION["size"][0] * SCALE_FACTOR,
            BOOST_ANIMATION["size"][1] * SCALE_FACTOR
        )

        self.basic_anim = Animation(
            BASIC_ANIMATION["paths"],
            speed = BASIC_ANIMATION["speed"],
            size  = basic_size
        )

        self.boost_anim = Animation(
            BOOST_ANIMATION["paths"],
            speed = BOOST_ANIMATION["speed"],
            size  = boost_size
        )

        # Initial frame setup
        frame      = self.basic_anim.get_current_frame()
        self.image = frame
        self.rect  = frame.get_rect(center = self.pos)
        self.mask  = pg.mask.from_surface(frame)

        # Boost timers
        self.boost_start_time = 0  # Time when boost started
        self.boost_duration = 5  # Boost lasts 5 seconds
        self.boost_cooldown_time = 0  # Time when cooldown started
        self.boost_cooldown_duration = 5  # 5 second cooldown after boost

    def update(self, keys):
        # Rotation
        if keys[pg.K_LEFT]:
            self.angle -= ROTATION_SPEED
        if keys[pg.K_RIGHT]:
            self.angle += ROTATION_SPEED

        self.angle = max(-MAX_ANGLE, min(MAX_ANGLE, self.angle))

        # Thrust
        if keys[pg.K_UP]:
            forward   = pg.Vector2(0, -1).rotate(self.angle)
            self.vel += forward * THRUST_POWER
        if keys[pg.K_DOWN]:
            backward  = pg.Vector2(0, 1).rotate(self.angle)
            self.vel += backward * (THRUST_POWER * 0.5)

        # Boost detection
        current_time = time.time()

        # Check if boost can be activated (not in cooldown)
        if keys[pg.K_SPACE]:
            if self.is_boosting == False and (current_time - self.boost_cooldown_time) > self.boost_cooldown_duration:
                self.is_boosting = True
                self.boost_start_time = current_time  # Start boost timer

        # Boost duration and cooldown logic
        if self.is_boosting:
            if current_time - self.boost_start_time > self.boost_duration:
                self.is_boosting = False
                self.boost_cooldown_time = current_time  # Start cooldown after boost ends

        # Move and apply friction
        self.vel *= FRICTION
        self.pos += self.vel

        # Lock X, clamp Y
        self.pos.x = 150
        w, h = pg.display.get_surface().get_size()
        self.pos.y = max(0, min(h, self.pos.y))

    def draw(self, surface):
        # Select animation frame
        if self.is_boosting:
            self.boost_anim.update()
            frame = self.boost_anim.get_current_frame()
        else:
            self.basic_anim.update()
            frame = self.basic_anim.get_current_frame()

        # Rotate and render ship
        rotated      = pg.transform.rotozoom(frame, -self.angle, 1)
        self.image   = rotated
        self.rect    = rotated.get_rect(center = self.pos)
        self.mask    = pg.mask.from_surface(rotated)

        surface.blit(self.image, self.rect.topleft)

    def take_damage(self, amount: int):
        # Shield absorbs first, then health
        if self.health < 0:
            print('you dead')
        else:
            self.health -= amount

    def get_mask(self):
        return self.mask
