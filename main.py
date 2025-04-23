import pygame as pg
import settings as S
import sys
from constants import load_assets

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")
        self.screen = pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.clock.tick(S.FPS)

        self.assets = load_assets()
        self.ship = self.assets["ship"]

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            POS_CONFIG = {
                ship_pos: (100, 0)


            } 

            ship_pos = POS_CONFIG["ship_pos"]
            self.screen.blit(self.ship["image_size"], ship_pos)
            pg.draw.rect(self.screen, (255, 0, 0), self.ship["hitbox"], 1)  

            

            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

Game().run()
