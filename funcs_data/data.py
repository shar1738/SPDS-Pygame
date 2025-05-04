ASTEROID_SIZE = (50,50)
IS_DAMAGED = False

DAMAGE_ANIMATION = {
    "paths": [
        "Assets/images/ship/ship_damage.png"
    ],
    "size": (100, 100),
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

ASTEROID_CONFIG = {
    f"asteroid{i}": {
        "paths": [f"Assets/images/asteroid{i}.png"],
        "size": ASTEROID_SIZE,
        "hitbox_offset": (12.5, 12.5, 25, 25),
    }
    for i in range(1, 5)
}

EXT_UI_ELEMENTS = {
    "costumers": {
        "paths": [f"Assets/images/ui/costumer{i}.png" for i in range(1, 6)],
        "size": (256, 256)
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
        "size": (128, 128)
    },
    "nitro": {
        "paths": [
            "Assets/images/ui/nitro_locked.png",
            "Assets/images/ui/nitro_unlocked.png"
        ],
        "size": (128, 128)
    },
    "costumer_label": {
        "paths": ["Assets/images/ui/costumer_label.png"],
        "size": (128, 128)
    },
    "esc_ship": {
        "paths": ["Assets/images/ship/escape_interior.png"],
        "size": (200, 200)
    },
    "hole": {
        "paths": ["Assets/images/ui/hole_found.png"],
        'size': (256, 256)
    }

}