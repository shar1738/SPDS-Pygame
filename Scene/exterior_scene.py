import pygame as pg
import sys
from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from functions import load_assets, ASSET_CONFIG
from Entities.ship import Ship
from Entities.asteroids import Asteroids  # Make sure this path is correct

class Exterior:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.assets = load_assets(ASSET_CONFIG)
        self.player_ship = Ship(150, 300)

        # Initialize asteroid handler and spawn 5 random ones
        self.asteroids = Asteroids()
        self.asteroids.spawn_rand(25)

    def render(self):
        self.screen.fill((0, 0, 0))

        # Draw ship
        self.player_ship.draw(self.screen)
        pg.draw.rect(self.screen, (255, 0, 0), self.player_ship.get_hitbox(), 1)

        # Draw asteroids
        self.asteroids.update_and_draw(self.screen)

        pg.display.update()

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
