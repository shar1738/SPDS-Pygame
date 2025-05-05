import pygame as pg
import sys
import time
import random
from Entities.spaceman import Spaceman
from Entities.holes import Holes
from funcs_data.data import EXT_UI_ELEMENTS
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT, FPS
from sfx import fail_sfx, song

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

        self.customer_LBL_info = EXT_UI_ELEMENTS["costumer_label"]
        self.customer_LBL_img = load_scaled_image(self.customer_LBL_info["paths"][0], self.customer_LBL_info["size"])
        self.costumer_lbl_rect = self.customer_LBL_img.get_rect(topright=(SCREEN_WIDTH, 100))
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(FONT, 30)
        
        # Save the starting tick time for countdowns
        if self.game_state.has_interior_ran:
            # When reentering, use the saved remaining time as the new "initial_time"
            self.initial_time = self.game_state.ex_remaining_time  
            # Reset the timer start - pause the old countdown and restart from now.
            self.timer_start = time.time() 
            self.game_state.timer_start = self.timer_start  
        else:
            self.initial_time = self.game_state.ex_remaining_time  
            self.timer_start = time.time()
            self.game_state.timer_start = self.timer_start

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
        # Health UI Initialization.
        self.health_info = EXT_UI_ELEMENTS["health"]
        step = 25
        self.health_index = min(len(self.health_info["paths"]) - 1, (150 - self.player_health) // step)
        self.ui_health_img = load_scaled_image(self.health_info["paths"][self.health_index],
                                               self.health_info["size"])
        self.ui_health_rect = self.ui_health_img.get_rect(bottomright=(SCREEN_WIDTH // 13.5, SCREEN_HEIGHT - 10))
        # ------------------

        # --- Customer Order UI (Persistent) ---
        # Ensure that game_state.current_customer is set as a valid file path.
        if self.game_state.current_customer:
            self.customer_img = load_scaled_image(self.game_state.current_customer,
                                                  EXT_UI_ELEMENTS["customers"]["size"])
        else:
            self.game_state.current_customer = random.choice(EXT_UI_ELEMENTS["customers"]["paths"])
            self.customer_img = load_scaled_image(self.game_state.current_customer,
                                                  EXT_UI_ELEMENTS["customers"]["size"])
        # Save the customer path locally for easy reference
        self.customer_path = self.game_state.current_customer
        # Create a rect for the customer image (e.g., at the top-right corner)
        self.customer_rect = self.customer_img.get_rect(topright=(SCREEN_WIDTH, 0))

        self.update_state()  # Initialize any other states

    def update_ui(self):
        """Dynamically update the health UI based on the current player health."""
        max_health = 150
        step = 25
        # Use the current health from the global state.
        self.player_health = self.game_state.ex_health
        self.health_index = min(len(self.health_info["paths"]) - 1,
                                (max_health - self.player_health) // step)
        self.ui_health_img = load_scaled_image(self.health_info["paths"][self.health_index],
                                               self.health_info["size"])
        # Store health index in global game state.
        self.game_state.ex_health_index = self.health_index
        self.game_state.ex_health_frame = self.health_info["paths"][self.health_index]

    def update_state(self):
        """Update the player state, countdown timers and holes dynamically."""
        self.player_health = self.game_state.ex_health
        self.update_ui()
        # Calculate elapsed time since the start of the Interior scene.
        elapsed = time.time() - self.timer_start
        self.remaining_time = max(0, self.initial_time - elapsed)
        self.remaining_distance = max(0, self.initial_distance - elapsed)
        self.game_state.ex_remaining_time = self.remaining_time
        self.game_state.ex_remaining_dist = self.remaining_distance
        self.update_holes()

    def update_holes(self):
        """Recalculate holes if player's health has changed."""
        new_hole_count = (150 - self.player_health) // 25
        if new_hole_count != self.hole_count:
            self.hole_count = new_hole_count
            self.holes_manager = Holes(amount=self.hole_count, interior_rect=self.interior_rect)
    
    def game_over(self, path, delay=2000):
        song.stop()
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
                        # Check if the spaceman collides with any hole.
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
            
            # Optionally, display the spacebar graphic if needed.
            for hole, hole_rect in self.holes_manager.holes:
                if hole_rect.colliderect(self.spaceman.rect):
                    self.screen.blit(self.spacebar_img, self.spacebar_rect)
            
            self.update_state()
            if self.remaining_time == 0:
                fail_sfx.play()
                self.game_over("Assets/images/ui/cold_lose.png", 8000)
                
            # Render debugging texts (time, distance, health).
            time_text = self.font.render(f"Time: {int(self.remaining_time)}", True, (255, 255, 255))
            dist_text = self.font.render(f"Dist: {int(self.remaining_distance)}", True, (255, 255, 255))
            health_text = self.font.render(f"Health: {int(self.player_health)}", True, (255, 255, 255))
            self.screen.blit(time_text, (10, 90))
            self.screen.blit(dist_text, (10, 50))
            self.screen.blit(health_text, (10, 130))
            # Blit the health UI (the hearts).
            self.screen.blit(self.ui_health_img, self.ui_health_rect)
            # Blit the customer image (persistent order) at its designated location.
            self.screen.blit(self.customer_LBL_img, self.costumer_lbl_rect)
            self.screen.blit(self.customer_img, self.customer_rect)
    
            pg.display.flip()
            self.clock.tick(FPS)
