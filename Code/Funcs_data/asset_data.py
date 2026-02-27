import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
ASTEROID_SIZE = (SCREEN_WIDTH // 30 , SCREEN_HEIGHT // 30)
IS_DAMAGED = False

DAMAGE_ANIMATION = {
    "paths": [
        "Assets/images/ship/ship_damage.png"
    ],
    "size": (SCREEN_WIDTH // 18, SCREEN_HEIGHT // 12.5),
    "speed": 0.01,
}

BASIC_ANIMATION = {
    "paths": [
        "Assets/images/ship/fire_mini.png",
        "Assets/images/ship/fire_small.png",
        "Assets/images/ship/fire_medium.png",
        "Assets/images/ship/fire_large.png",
        "Assets/images/ship/fire_colossal.png",
    ],
    "size":  (SCREEN_WIDTH // 18, SCREEN_HEIGHT // 12.5),
    "speed": 0.1,}

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
    "size":  (SCREEN_WIDTH // 18, SCREEN_HEIGHT // 12.5),
    "speed": 0.5,
}

ASTEROID_CONFIG = {
    f"asteroid{i}": {
        "paths": [f"Assets/images/asteroid{i}.png"],
        "size": ASTEROID_SIZE,
        "hitbox_offset": (12.5, 12.5, 25, 25),
    }
    for i in range(1, 5)
}

EXT_UI_ELEMENTS = {
    "customers": {
        "paths": [f"Assets/images/ui/costumer{i}.png" for i in range(1, 7)],
        "size": (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10)
    },
    "pizza_timer": {
        "paths": [
            "Assets/images/ui/full_time.png",
            *[f"Assets/images/ui/pt{i}.png" for i in range(1, 12)],
            "Assets/images/ui/run_out.png"
        ],
        "size": (128, 128)
    },
    "health": {
        "paths": [f"Assets/images/ui/a_{i}h.png" for i in range(1, 8)],
        "size": (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10)
    },
    "nitro": {
        "paths": [
            "Assets/images/ui/nitro_locked.png",
            "Assets/images/ui/nitro_unlocked.png"
        ],
        "size": (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10)
    },
    "costumer_label": {
        "paths": ["Assets/images/ui/costumer_label.png"],
        "size": (SCREEN_WIDTH // 8, SCREEN_HEIGHT // 8)
    },
    "esc_ship": {
        "paths": ["Assets/images/ship/escape_interior.png"],
        "size": (SCREEN_WIDTH * 1.54/10, SCREEN_HEIGHT * 1.54/10)
    },
    "hole": {
        "paths": ["Assets/images/ui/hole_found.png"],
        'size': (SCREEN_WIDTH * 1.2/10, SCREEN_HEIGHT * 1.2/10)
    },
    "fix_hole": {
        'paths': ["Assets/images/ui/press_space.png"],
        'size': (SCREEN_WIDTH * 1.54/10, SCREEN_HEIGHT * 1.54/10)
    },
    'esc_interior': {
        'paths': ['Assets/images/ui/escape_exterior.png'],
        'size': (SCREEN_WIDTH * 1.54/10, SCREEN_HEIGHT * 1.54/10)
    },
    'space': {
        'paths': ['Assets/images/ui/press_space.png'],
        'size': (SCREEN_WIDTH * 2.54/10, SCREEN_HEIGHT * 2.6/10)
    }

}

collision_sfx = pg.mixer.Sound("Assets/sfx/explosion.mp3") 
ship_basic_sfx = pg.mixer.Sound("Assets/sfx/ship_basic.mp3") 
ship_boost_sfx = pg.mixer.Sound("Assets/sfx/ship_boost.wav")
yay_sfx = pg.mixer.Sound("Assets/sfx/YAY.mp3")
fail_sfx = pg.mixer.Sound("Assets/sfx/failed.mp3")
alarm_sfx = pg.mixer.Sound("Assets/sfx/alarm.mp3")
gooing_sfx = pg.mixer.Sound("Assets/sfx/gooing.mp3")
song = pg.mixer.Sound("Assets/sfx/song.mp3")
pickup_sfx = pg.mixer.Sound("Assets/sfx/powerUP.wav")