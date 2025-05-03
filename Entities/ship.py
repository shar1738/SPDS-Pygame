import pygame as pg
import time
from funcs_data.functions import Animation
from funcs_data.data import IS_DAMAGED

# Constants
THRUST_POWER       = 0.3
FRICTION           = 0.97
ROTATION_SPEED     = 3
MAX_ANGLE          = 60  # degrees up and down

SCALE_FACTOR       = 2

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

DAMAGE_ANIMATION = {
    "paths": [
        "Assets/images/ship/ship_damage.png"
    ],
    "size": (100, 100),
    "speed": 0.01,
}


class Ship:
    def __init__(self, x, y):
        pg.init()

        # Position and movement
        self.pos             = pg.Vector2(x, y)
        self.vel             = pg.Vector2(0, 0)
        self.angle           = 0
        self.is_boosting     = False
        self.is_damaged      = IS_DAMAGED
        self.damage_timer    = 0
        self.override_image = None  

        # Custom hitbox size
        self.hitbox_length   = 40  # width
        self.hitbox_height   = 60  # height

        # Ship stats
        self.health = 150

        # Load and scale animations
        basic_size = (
            BASIC_ANIMATION["size"][0] * SCALE_FACTOR,
            BASIC_ANIMATION["size"][1] * SCALE_FACTOR
        )
        boost_size = (
            BOOST_ANIMATION["size"][0] * SCALE_FACTOR,
            BOOST_ANIMATION["size"][1] * SCALE_FACTOR
        )
        damage_size = (
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
        self.damage_anim = Animation(
            DAMAGE_ANIMATION["paths"],
            speed = DAMAGE_ANIMATION["speed"],
            size  = damage_size
        )

        self.image = self.basic_anim.get_current_frame()
        self.rect  = self.image.get_rect(center = self.pos)

        # Boost timers
        self.boost_start_time = 0  
        self.boost_duration = 5  
        self.boost_cooldown_time = 0  
        self.boost_cooldown_duration = 5 

    def set_override_image(self, image: pg.Surface):
        self.override_image = image

    def update(self, keys, dt):
        # Rotation
        if keys[pg.K_LEFT]:
            self.angle -= ROTATION_SPEED
        if keys[pg.K_RIGHT]:
            self.angle += ROTATION_SPEED
        self.angle = max(-MAX_ANGLE, min(MAX_ANGLE, self.angle))

        # Thrust
        if keys[pg.K_UP]:
            forward = pg.Vector2(0, -1).rotate(self.angle)
            self.vel += forward * THRUST_POWER
        if keys[pg.K_DOWN]:
            backward = pg.Vector2(0, 1).rotate(self.angle)
            self.vel += backward * (THRUST_POWER * 0.5)

        # Boost detection
        current_time = time.time()
        if keys[pg.K_SPACE]:
            if not self.is_boosting and (current_time - self.boost_cooldown_time) > self.boost_cooldown_duration:
                self.is_boosting = True
                self.boost_start_time = current_time

        if self.is_boosting:
            if current_time - self.boost_start_time > self.boost_duration:
                self.is_boosting = False
                self.boost_cooldown_time = current_time
        
        if self.is_damaged:
            self.damage_timer -= dt
            if self.damage_timer <= 0:
                self.is_damaged = False

        # Move and apply friction
        self.vel *= FRICTION
        self.pos += self.vel

        # Lock X, clamp Y
        self.pos.x = 150
        w, h = pg.display.get_surface().get_size()
        self.pos.y = max(0, min(h, self.pos.y))

        # Update mask and rect for collision
        current_frame = (
            self.override_image if self.override_image else
            self.damage_anim.get_current_frame() if self.is_damaged else
            self.boost_anim.get_current_frame() if self.is_boosting else
            self.basic_anim.get_current_frame()
        )
        rotated = pg.transform.rotozoom(current_frame, -self.angle, 1)
        self.image = rotated
        self.rect = rotated.get_rect(center=self.pos)

        # Create and rotate hitbox
        hitbox_surface = pg.Surface((self.hitbox_length, self.hitbox_height), pg.SRCALPHA)
        pg.draw.rect(hitbox_surface, (255, 255, 255), (0, 0, self.hitbox_length, self.hitbox_height))
        rotated_hitbox = pg.transform.rotozoom(hitbox_surface, -self.angle, 1)
        offset_vector = pg.Vector2(200, 0).rotate(-self.angle)
        self.mask = pg.mask.from_surface(self.image)
        self.mask_rect = rotated_hitbox.get_rect(center=(self.pos + offset_vector))


    def draw(self, surface):
        # Update animation frame
        if self.override_image:
            frame = self.override_image
        else:
            if self.is_damaged:
                self.damage_anim.update()
                frame = self.damage_anim.get_current_frame()
            elif self.is_boosting:
                self.boost_anim.update()
                frame = self.boost_anim.get_current_frame()
            else:
                self.basic_anim.update()
                frame = self.basic_anim.get_current_frame()

        # Rotate ship image
        rotated = pg.transform.rotozoom(frame, -self.angle, 1)
        self.image = rotated
        self.rect = rotated.get_rect(center=self.pos)

        # Create rectangular hitbox surface
        hitbox_surface = pg.Surface((self.hitbox_length, self.hitbox_height), pg.SRCALPHA)
        pg.draw.rect(hitbox_surface, (255, 255, 255), (0, 0, self.hitbox_length, self.hitbox_height))

        # Draw ship
        surface.blit(self.image, self.rect.topleft)


    def take_damage(self, amount: int):
        if self.health < 0:
            print('you dead')
        else:
            self.health -= amount

    def get_mask(self):
        return self.mask, self.mask_rect.topleft
