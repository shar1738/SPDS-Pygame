import pygame as pg
import sys
from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from constants import load_assets
from Entities.ship import Ship 

DEFAULT_POSITIONS = {
    "ship": (100, 0),
    "aster1": (500, 0),
}

class Exterior:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.assets = load_assets()
        self.aster1 = self.assets["aster1"]

        self.player_ship = Ship(100, 300) 
    

    def render(self):
        self.screen.fill((0, 0, 0))

        self.player_ship.draw(self.screen)
        pg.draw.rect(self.screen, (255, 0, 0), self.player_ship.get_hitbox(), 1)

        aster1_pos = DEFAULT_POSITIONS["aster1"]
        self.screen.blit(self.aster1["image"], aster1_pos)
        hitbox_aster = self.calculate_hitbox(aster1_pos, self.aster1["hitbox_offset"])
        pg.draw.rect(self.screen, (255, 0, 0), hitbox_aster, 1)

        pg.display.update()


    def calculate_hitbox(self, pos, offset):
        x, y = pos
        offset_x, offset_y, width, height = offset
        return pg.Rect(x + offset_x, y + offset_y, width, height)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.clock.tick(FPS)
            keys = pg.key.get_pressed()
            self.player_ship.update(keys)  
            self.render()
            self.handle_events()

