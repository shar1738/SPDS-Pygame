import pygame as pg
import time 


def load_assets(asset_config_dic):
    assets = {}
    for name, cfg in asset_config_dic.items():
        surf = pg.image.load(cfg["path"]).convert_alpha()
        surf = pg.transform.scale(surf, cfg["size"])
        assets[name] = {
            "image": surf,
            "hitbox_offset": cfg["hitbox_offset"],
        }
    return assets

def check_collision(rect1: pg.Rect, rect2: pg.Rect) -> bool:
    """Simple AABB collision between two rects."""
    return rect1.colliderect(rect2)

class Animation:
    def __init__(self, image_paths, speed, size=None):
        self.frames = [
            pg.transform.scale(pg.image.load(path).convert_alpha(), size) if size
            else pg.image.load(path).convert_alpha()
            for path in image_paths
        ]
        self.speed = speed
        self.current_frame = 0
        self.last_update = time.time()

    def update(self):
        now = time.time()
        if now - self.last_update >= self.speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def get_current_frame(self) -> pg.Surface:
        return self.frames[self.current_frame]