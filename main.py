import pygame as pg
import settings as S
import sys
from constants import load_assets

POS_CONFIG = {
    "ship_pos": (100, 0)
}

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")
        self.screen = pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.assets = load_assets()
        self.ship = self.assets["ship"]

    def run(self):
        while True:
            self.clock.tick(S.FPS)
            self.screen.fill((0, 0, 0))

            ship_pos = POS_CONFIG["ship_pos"]
            self.screen.blit(self.ship["image"], ship_pos)

            # Calculate dynamic hitbox position
            x, y = ship_pos
            offset_x, offset_y, width, height = self.ship["hitbox_offset"]
            hitbox = pg.Rect(x + offset_x, y + offset_y, width, height)
            pg.draw.rect(self.screen, (255, 0, 0), hitbox, 1)

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

Game().run()
