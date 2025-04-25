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
    
}


def load_assets(asset_config):
    assets = {}
    for name, config in asset_config.items():
        image = pg.image.load(config["path"]).convert_alpha()
        image_scaled = pg.transform.scale(image, config["size"])

        assets[name] = {
            "image": image_scaled,
            "hitbox_offset": config["hitbox_offset"],  # store relative values
        }
    return assets
