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

def load_assets(asset_config_dic):
    assets = {}  # Initialize a dictionary to store processed assets

    for name, config in asset_config_dic.items():  # Iterate through each asset's configuration
        
        # Load the image from the specified path and enable transparency
        image = pg.image.load(config["path"]).convert_alpha()
        
        # Scale the image to the size defined in the configuration
        image_scaled = pg.transform.scale(image, config["size"])

        # Store the processed image and metadata (like hitbox offset) in the assets dictionary
        assets[name] = {
            "image": image_scaled,  # The resized image
            "hitbox_offset": config["hitbox_offset"],  # Metadata for collision detection
        }
    return assets  # Return the dictionary containing all loaded and processed assets

