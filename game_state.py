import pygame as pg
import time
import random

from Code.Scenes.exterior import Exterior
from Code.Scenes.interior import Interior
from Code.Scenes.main_menu import MainMenu
from Code.Scenes.mini_game import MiniGame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT

import Code.Funcs_data.asset_data as asset_data

SCENES = {
    "Exterior": Exterior,
    "MainMenu": MainMenu,
    "Interior": Interior,
    "MiniGame": MiniGame,
}

DISTANCE_RATE = 5
INI_DISTANCE = 0
START_TIME = random.randint(240, 285)

class GameState:
    def __init__(self):

         # Scene tracking
        self.current_level = "Exterior"  # "Exterior", "Interior", or "MiniGame"

        self.player_health = 150
        self.health_info = asset_data.EXT_UI_ELEMENTS["health"]
        self.health_index = 0    # Default index (full health)
        self.health_frame = asset_data.EXT_UI_ELEMENTS["health"]["paths"][self.health_index] 
        
        self.distance = random.randint(500, 2500)

        self.rand_time = START_TIME
        self.time = time.time()
        self.clock = pg.time.Clock()
        self.dt_ms = self.clock.tick(60)

        self.customer_path = random.choice(asset_data.EXT_UI_ELEMENTS["customers"]["paths"])

        # Customer persistence (store image path instead of object reference)
        self.holes = None
        self.hole_positions = None
        self.spaceman_position = None

    def game_over(self, path, delay):
        asset_data.song.stop()
        game_over_img = pg.image.load(path).convert_alpha()
        rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_img, rect.topleft)
        pg.display.flip()
        pg.time.delay(delay)
        pg.quit()
        sys.exit()