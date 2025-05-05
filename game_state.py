import pygame as pg
from funcs_data.data import EXT_UI_ELEMENTS
import random 

class GameState:
    def __init__(self):
        # Exterior related
        self.ex_health = 150
        self.ex_health_index = None    # Initialize with a default index
        self.ex_health_frame = None   # You could store either a path or an image reference

        # Time/distance related for the exterior scene.
        self.ex_remaining_time = None
        self.ex_remaining_dist = None
        self.ex_time_frame = None   
           

        # Customer and obstacles
        self.current_customer = random.choice(list(EXT_UI_ELEMENTS["customers"].values()))  # Should be set to a valid image path or identifier
        self.holes = None

        # Current level: now stored as a single string.
        self.current_level = "Exterior"  # can be "Exterior", "Interior", or "MiniGame"
        self.has_interior_ran = False

    # Example setter method for health:
    def update_health(self, new_health):
        self.ex_health = new_health

    # Example setter method for current scene:
    def set_current_level(self, level: str):
        if level in {"Exterior", "Interior", "MiniGame"}:
            self.current_level = level
        else:
            raise ValueError("Invalid level")

    # You could add additional methods to update your animation indices:
    def update_health_index(self, index: int):
        self.ex_health_index = index

    def update_time_frame(self, frame: int):
        self.ex_time_frame = frame

    # And similar methods for other persistent variables...
