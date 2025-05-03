# Scene/interior.py
import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from functions import Animation
import Entities.pizza_box
import Entities.goo_gun

SPACEMAN_MOVE_ANIMATION = {
    "paths": [
        "Assets/images/spaceman/spaceman1.png",
        "Assets/images/spaceman/spaceman2.png",
        "Assets/images/spaceman/spaceman3.png",
    ],
    "size":  (100, 100),
    "speed": 0.15,
}




class Minigame:
    pass

cockpit_img = pg.image.load('Assets/images/cockpit.png')

class Cockpit:
    pass

cargo_img = pg.image.load('Assets/images/storage.png')

class Cargo:
    pass

class Interior:
    def __init__(self, screen):
        self.screen = screen
        self.clock  = pg.time.Clock()
        self.font   = pg.font.SysFont(None, 50)

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    return None
                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    from Scene.exterior import Exterior
                    return Exterior(self.screen)

            self.screen.fill((30, 5, 5))
            text = self.font.render(
                "INTERIOR — Press ESC to go back", True, (220, 220, 220)
            )
            rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            self.screen.blit(text, rect)
            pg.display.flip()
            self.clock.tick(60)
        



