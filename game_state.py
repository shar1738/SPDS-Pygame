import pygame as pg
import time
import random

from Code.Scenes.exterior import Exterior
from Code.Scenes.interior import Interior
from Code.Scenes.main_menu import MainMenu
from Code.Scenes.mini_game import MiniGame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

from Code.Funcs_data.asset_data import EXT_UI_ELEMENTS 

SCENES = {
    "Exterior": Exterior,
    "MainMenu": MainMenu,
    "Interior": Interior,
    "MiniGame": MiniGame,
}

class GameState:
    def __init__(self):

        self.ex_health = 150
        self.ex_health_index = 0    # Default index (full health)
        self.ex_health_frame = EXT_UI_ELEMENTS["health"]["paths"][self.ex_health_index] 
        
        # Time/distance management
        self.ex_remaining_time = None
        self.ex_remaining_dist = None
        self.timer_start = None   # Add global timer tracking

        # Customer persistence (store image path instead of object reference)
        self.current_customer = random.choice(EXT_UI_ELEMENTS["customers"]["paths"])
        self.holes = None
        self.hole_positions = None
        self.spaceman_position = None

        # Scene tracking
        self.current_level = "Exterior"  # "Exterior", "Interior", or "MiniGame"
        self.has_interior_ran = False

    # --- Helper Methods ---
    def update_health(self, new_health):
        self.ex_health = new_health
        self.ex_health_index = min(len(EXT_UI_ELEMENTS["health"]["paths"]) - 1, (150 - self.ex_health) // 25)
        self.ex_health_frame = EXT_UI_ELEMENTS["health"]["paths"][self.ex_health_index]  # Update health frame

    def set_current_level(self, level: str):
        if level in {"Exterior", "Interior", "MiniGame"}:
            self.current_level = level
        else:
            raise ValueError("Invalid level")

    def update_timer_start(self):
        """Save the current start time (for precise tracking across scenes)."""
        self.timer_start = time.time()

    def update_customer(self, new_customer_path):
        """Ensures customer image path is preserved across scenes."""
        self.current_customer = new_customer_path

