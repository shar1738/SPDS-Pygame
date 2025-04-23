import pygame as pg
from main import POS_CONFIG

ship_pos = POS_CONFIG{ship_pos}

ASSET_CONFIG = {
    "spaceman": {
        "path": "Assets/images/spaceman.png",
        "size": (128, 128),
        "hitbox": (32, 32, 64, 64),  
    },
    "asteroid1": {
        "path": "Assets/images/asteroid1.png",
        "size": (256, 256),
        "hitbox": (40, 40, 176, 176),
    },

    "ship": {
        "path": "Assets/images/ship.png",
        "size": (256, 256),
        "hitbox": (ship_pos, 128, 128),
    },
}

def load_assets():
    assets = {}
    for name, config in ASSET_CONFIG.items():
        image_init = pg.image.load(config["path"]).convert_alpha()
        image_scale = pg.transform.scale(image_init, config["size"])
        hitbox_rect = pg.Rect(*config["hitbox"])  # unpack tuple into Rect

        assets[name] = {
            "image": image_init,
            "image_size": image_scale,
            "hitbox": hitbox_rect,
        }
    return assets
