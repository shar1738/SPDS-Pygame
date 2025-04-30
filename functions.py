import pygame as pg
import time

class Animation:
    def __init__(self, image_paths, speed, size=None):
        # Load each frame from the provided paths,
        # scaling each image to the specified size when given.
        self.frames = [
            pg.transform.scale(pg.image.load(path).convert_alpha(), size)
            if size else pg.image.load(path).convert_alpha()
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
