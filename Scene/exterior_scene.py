import pygame as pg
import sys
from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from Entities.ship      import Ship
from Entities.asteroids import Asteroids


class Exterior:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.background = pg.image.load("Assets/images/background.png").convert()
        self.background = pg.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock  = pg.time.Clock()

        self.player_ship = Ship(150, 300)
        self.asteroids   = Asteroids()

        # (optional) seed a few to start
        self.asteroids.spawn_rand(5)

    def run(self):
        while True:
            dt = self.clock.tick(FPS)  # dt in milliseconds
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            keys = pg.key.get_pressed()
            self.asteroids.is_boosting = self.player_ship.is_boosting
            self.player_ship.update(keys)

            # spawn new asteroids over time
            self.asteroids.update(dt)

            # render everything
            self.screen.blit(self.background, (0, 0))
            self.player_ship.draw(self.screen)

            self.asteroids.update_and_draw(self.screen, 
                                           self.player_ship.rect, 
                                           self.player_ship.get_mask(),
                                           self.player_ship.is_boosting)

            pg.display.flip()

if __name__=="__main__":
    Exterior().run()
