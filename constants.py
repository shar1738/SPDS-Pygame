import pygame as pg

ASSET_CONFIG = {
    "spaceman": {
        "path": "Assets/images/spaceman.png",
        "size": (128, 128),
        "hitbox_offset": (32, 32, 64, 64),  
    },
    "aster1": {
        "path": "Assets/images/asteroid1.png",
        "size": (128, 128),
        "hitbox_offset": (32, 32, 64, 64),
    },
    "ship": {
        "path": "Assets/images/ship.png",
        "size": (256, 256),
        "hitbox_offset": (0, 0, 128, 128),
    },
}


def load_assets():
    assets = {}
    for name, config in ASSET_CONFIG.items():
        image = pg.image.load(config["path"]).convert_alpha()
        image_scaled = pg.transform.scale(image, config["size"])

        assets[name] = {
            "image": image_scaled,
            "hitbox_offset": config["hitbox_offset"],  # store relative values
        }
    return assets
