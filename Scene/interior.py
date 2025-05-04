import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from funcs_data.functions import Animation
import time
from Entities.spaceman import Spaceman
from Entities.holes import Holes
from funcs_data.data import EXT_UI_ELEMENTS

def load_scaled_image(path, size):
    return pg.transform.scale(pg.image.load(path).convert_alpha(), size)

class Interior:
    def __init__(self, game_state):
        self.screen = pg.display.get_surface()

        # Background images
        self.space_bg = load_scaled_image("Assets/images/Background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.interior_image = load_scaled_image("Assets/images/interior.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.interior_rect = self.interior_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.interior_rect = self.interior_rect.inflate(-400, -300)  # Shrinks the rect
        self.interior_rect.y -= 95  
        self.interior_rect.x += 30  

        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont(None, 50)
        self.game_state = game_state
        
        # Initialize timer variables correctly
        self.timer_start = time.time()
        self.rand_time = 60  # Default time

        # Extract game state variables safely
        self.player_health = self.game_state.ex_health
        self.holes = self.game_state.holes
        self.time_index = self.game_state.ex_time_frame
        self.remaining_time = self.game_state.ex_remaining_time
        self.health_index = self.game_state.ex_health_index
        
        # **Ensure `self.health_info` is initialized**
        self.health_info = {"paths": []}  # Default empty list to avoid crashes
        self.health_info = self.game_state.ex_health_frame

        # **Consolidate save state logic into a method**
        self.update_state()

        # Spaceman
        self.spaceman = Spaceman(SCREEN_WIDTH - 350, SCREEN_HEIGHT // 2, boundary_rect=self.interior_rect)

        # **NEW: Initialize holes randomly at interior boundaries**
        self.holes_manager = Holes(amount=self.holes, interior_rect=self.interior_rect)

    def update_state(self):
        """Update player state variables"""
        max_health = 150
        step = 25
        self.holes = (max_health - self.player_health) // step
        elapsed = time.time() - self.timer_start
        self.remaining_time = max(0, self.rand_time - elapsed)

        # **Reinitialize holes_manager to reflect updated hole count**
        self.holes_manager = Holes(amount=self.holes, interior_rect=self.interior_rect)


    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    return None
                
                if e.type == pg.KEYDOWN and e.key in [pg.K_ESCAPE, pg.K_SPACE]:
                    self.update_state()  # Call the method instead of duplicating logic
                    
                    self.game_state.ex_health = self.player_health
                    self.game_state.ex_health_frame = self.health_info["paths"][self.health_index]
                    self.game_state.ex_health_index = self.health_index
                    self.game_state.ex_remaining_time = int(self.remaining_time)
                    self.game_state.ex_time_frame = self.time_index
                    self.game_state.holes = self.holes
                    
                    self.game_state.current_level = "MiniGame" if e.key == pg.K_SPACE else "Exterior"
                    return self.game_state.current_level
            
            keys = pg.key.get_pressed()
            self.spaceman.update(keys)

            # **Check for hole count changes in GameState**
            if self.holes != self.game_state.holes:
                self.holes = self.game_state.holes
                self.holes_manager = Holes(amount=self.holes, interior_rect=self.interior_rect)  # Refresh holes

            # Render scene
            self.screen.blit(self.space_bg, (0, 0))            # Layer 1: Space background
            self.screen.blit(self.interior_image, (0, 0))      # Layer 2: Interior overlay
            self.holes_manager.draw(self.screen)              # Layer 3: Holes
            self.spaceman.draw(self.screen)                   # Layer 4: Spaceman

            pg.display.flip()
            self.clock.tick(60)


