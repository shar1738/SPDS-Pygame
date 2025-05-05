import pygame as pg
import sys
import time
from Entities.spaceman import Spaceman
from Entities.holes import Holes
from funcs_data.data import EXT_UI_ELEMENTS
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from sfx import fail_sfx

def load_scaled_image(path, size):
    """Safely loads and scales an image."""
    try:
        return pg.transform.scale(pg.image.load(path).convert_alpha(), size)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return pg.Surface(size)  # Returns a blank surface if loading fails

class Interior:
    def __init__(self, game_state):
        self.screen = pg.display.get_surface()
        self.game_state = game_state

        # --- Load background and interior images ---
        self.space_bg = load_scaled_image("Assets/images/Background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.interior_image = load_scaled_image("Assets/images/interior.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.interior_rect = self.interior_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        # Inflating the interior_rect to define an interactive area
        self.interior_rect = self.interior_rect.inflate(-400, -300)
        self.interior_rect.y -= 95  
        self.interior_rect.x += 30  

        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont(None, 50)
        
        # Save the starting tick time for countdowns
        self.timer_start = time.time()

        self.esc_info = EXT_UI_ELEMENTS["esc_interior"]
        self.esc_ship_img = load_scaled_image(self.esc_info["paths"][0], self.esc_info["size"])
        self.esc_ship_rect = self.esc_ship_img.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        self.health = self.game_state.ex_health
        
        self.space_info = EXT_UI_ELEMENTS["space"]
        self.spacebar_img = load_scaled_image(self.space_info["paths"][0], self.space_info["size"])
        self.spacebar_rect = self.spacebar_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # --- Load Spaceman and Holes ---
        self.spaceman = Spaceman(SCREEN_WIDTH - 350, SCREEN_HEIGHT // 2, boundary_rect=self.interior_rect)
        
        # IMPORTANT: Load the exact health from game_state and calculate holes accordingly.
        self.player_health = self.game_state.ex_health
        self.hole_count = (150 - self.player_health) // 25  
        self.holes_manager = Holes(amount=self.hole_count, interior_rect=self.interior_rect)
        print(f"Initial holes: {self.hole_count}")

        # --- Load Time and Distance ---
        # Save the initial time and distance from the global state so subsequent updates subtract elapsed time.
        self.initial_time = self.game_state.ex_remaining_time
        # Ensure that ex_remaining_dist exists; otherwise assign a default distance
        self.initial_distance = self.game_state.ex_remaining_dist if self.game_state.ex_remaining_dist is not None else 500

        # These variables will be updated each frame.
        self.remaining_time = self.initial_time
        self.remaining_distance = self.initial_distance

        # ------------------
        # Add Health UI initialization.
        self.health_info = EXT_UI_ELEMENTS["health"]
        # Calculate the current health index using the initial ship health.
        step = 25
        self.health_index = min(len(self.health_info["paths"]) - 1, (150 - self.player_health) // step)
        self.ui_health_img = load_scaled_image(self.health_info["paths"][self.health_index],
                                               self.health_info["size"])
        # Define a rectangle to blit the health UI image.
        self.ui_health_rect = self.ui_health_img.get_rect(bottomright=(SCREEN_WIDTH // 13.5, SCREEN_HEIGHT - 10))
        # ------------------

        self.update_state()  # Initialize any other states

    def update_ui(self):
        """Dynamically update the health UI based on the current player health."""
        max_health = 150
        step = 25
        # Use the current health from the global state (or from the ship if you prefer)
        self.player_health = self.game_state.ex_health
        self.health_index = min(len(self.health_info["paths"]) - 1,
                                (max_health - self.player_health) // step)
        self.ui_health_img = load_scaled_image(self.health_info["paths"][self.health_index],
                                               self.health_info["size"])
        # Store the updated values in the global game state
        self.game_state.ex_health_index = self.health_index
        self.game_state.ex_health_frame = self.health_info["paths"][self.health_index]

    def update_state(self):
        """Update the player state, countdown timers and holes dynamically."""
        # Health is loaded directly from the global state.
        self.player_health = self.game_state.ex_health

        # Update the health UI dynamically
        self.update_ui()

        # Calculate elapsed time since the start of the Interior scene.
        elapsed = time.time() - self.timer_start

        # Update remaining time and distance by subtracting elapsed time.
        self.remaining_time = max(0, self.initial_time - elapsed)
        # For simplicity we assume a rate of 1 unit per second.
        self.remaining_distance = max(0, self.initial_distance - elapsed)

        # Optionally, update the global game state so next scene receives the updated values:
        self.game_state.ex_remaining_time = self.remaining_time
        self.game_state.ex_remaining_dist = self.remaining_distance

        # Update holes if necessary, based on health changes.
        self.update_holes()

    def update_holes(self):
        """Recalculate holes if player's health has changed."""
        new_hole_count = (150 - self.player_health) // 25
        if new_hole_count != self.hole_count:
            self.hole_count = new_hole_count
            self.holes_manager = Holes(amount=self.hole_count, interior_rect=self.interior_rect)
    
    def game_over(self, path, delay=2000):
        game_over_img = pg.image.load(path).convert_alpha()
        rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_img, rect.topleft)
        pg.display.flip()
        pg.time.delay(delay)
        pg.quit()
        sys.exit()

    def run(self):
        """Main game loop for the Interior scene."""
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        self.game_state.has_interior_ran = True
                        self.game_state.current_level = "Exterior"
                        return self.game_state.current_level
                    if e.key == pg.K_SPACE:
                        # When space is pressed, check if the spaceman is colliding with any hole.
                        for hole, hole_rect in self.holes_manager.holes:
                            if hole_rect.colliderect(self.spaceman.rect):
                                self.game_state.current_level = "MiniGame"
                                return self.game_state.current_level
            
            keys = pg.key.get_pressed()
            self.spaceman.update(keys)
            
            # Blit background and UI elements.
            self.screen.blit(self.space_bg, (0, 0))
            self.screen.blit(self.esc_ship_img, self.esc_ship_rect)
            self.screen.blit(self.interior_image, (0, 0))
            self.holes_manager.draw(self.screen)
            self.spaceman.draw(self.screen)
            
            # Optionally, if a hole collides with the spaceman display the spacebar graphic.
            for hole, hole_rect in self.holes_manager.holes:
                if hole_rect.colliderect(self.spaceman.rect):
                    self.screen.blit(self.spacebar_img, self.spacebar_rect)
            
            # Call update_state() every frame so that time, distance, and health UI update.
            self.update_state()

            if self.remaining_time == 0:
                fail_sfx.play()
                self.game_over("Assets/images/ui/cold_lose.png", 8000)
                
            # Render the remaining time, remaining distance, and (for debugging) health value.
            time_text = self.font.render(f"Time: {int(self.remaining_time)}", True, (255, 255, 255))
            dist_text = self.font.render(f"Dist: {int(self.remaining_distance)}", True, (255, 255, 255))
            health_text = self.font.render(f"Health: {int(self.player_health)}", True, (255, 255, 255))
            self.screen.blit(time_text, (10, 90))
            self.screen.blit(dist_text, (10, 50))
            self.screen.blit(health_text, (10, 130))
            
            # *** Blit the dynamic health UI image (the hearts) ***
            self.screen.blit(self.ui_health_img, self.ui_health_rect)
            
            pg.display.flip()
            self.clock.tick(60)
