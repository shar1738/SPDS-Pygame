import pygame as pg
import sys
import time
import random
from Entities.spaceman import Spaceman
from Entities.holes import Holes
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT, FPS
import Code.Funcs_data.asset_data as asset_data

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
        self.interior_rect = self.interior_rect.inflate(SCREEN_WIDTH * -1/4, SCREEN_HEIGHT * -1/3)
        self.interior_rect.y -= SCREEN_HEIGHT * 0.07
        self.interior_rect.x += SCREEN_WIDTH * 0.04

        self.customer_LBL_info = asset_data.EXT_UI_ELEMENTS["costumer_label"]
        self.customer_LBL_img = load_scaled_image(
            self.customer_LBL_info["paths"][0], self.customer_LBL_info["size"])
        
        self.customer_lbl_rect = self.customer_LBL_img.get_rect(
            topright=(SCREEN_WIDTH * 1.014, SCREEN_HEIGHT // 12))

        self.clock = pg.time.Clock()
        self.font = pg.font.Font(FONT, 30)

        # Timer setup
        self.initial_time = self.game_state.ex_remaining_time
        self.timer_start = time.time()
        self.game_state.timer_start = self.timer_start

        self.esc_info = asset_data.EXT_UI_ELEMENTS["esc_interior"]
        self.esc_ship_img = load_scaled_image(
            self.esc_info["paths"][0], self.esc_info["size"])
        
        self.esc_ship_rect = self.esc_ship_img.get_rect(
            bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))

        self.health = self.game_state.ex_health

        self.space_info = asset_data.EXT_UI_ELEMENTS["space"]
        self.spacebar_img = load_scaled_image(
            self.space_info["paths"][0], self.space_info["size"])
        
        self.spacebar_rect = self.spacebar_img.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        

        # --- Load Spaceman and Holes ---
        # Restore spaceman position if saved
        if hasattr(self.game_state, 'spaceman_pos'):
            x, y = self.game_state.spaceman_pos
        else:
            x, y = SCREEN_WIDTH - 350, SCREEN_HEIGHT // 2
        self.spaceman = Spaceman(x, y, boundary_rect=self.interior_rect)

        # Calculate holes based on health
        self.player_health = self.game_state.ex_health
        self.hole_count = (150 - self.player_health) // 25

        # Restore hole positions cache if saved
        if hasattr(self.game_state, 'hole_positions'):
            Holes.hole_positions = self.game_state.hole_positions
        self.holes_manager = Holes(
            amount=self.hole_count,
            interior_rect=self.interior_rect)
        
        # Persist hole positions
        self.game_state.hole_positions = list(self.holes_manager.hole_positions)

        # Time & distance initialization
        self.initial_distance = (
            self.game_state.ex_remaining_dist
            if self.game_state.ex_remaining_dist is not None else 500)
        
        self.remaining_time = self.initial_time
        self.remaining_distance = self.initial_distance

        # Health UI
        self.health_info = asset_data.EXT_UI_ELEMENTS["health"]
        step = 25
        self.health_index = min(
            len(self.health_info["paths"]) - 1,
            (150 - self.player_health) // step)
        
        self.ui_health_img = load_scaled_image(
            self.health_info["paths"][self.health_index],
            self.health_info["size"])
        
        self.ui_health_rect = self.ui_health_img.get_rect(
            bottomright=(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.9999))

        # Customer UI
        if self.game_state.current_customer:
            path = self.game_state.current_customer
        else:
            path = random.choice(asset_data.EXT_UI_ELEMENTS["customers"]["paths"])
            self.game_state.current_customer = path
        self.customer_img = load_scaled_image(path, asset_data.EXT_UI_ELEMENTS["customers"]["size"])
        self.customer_path = path
        self.customer_rect = self.customer_img.get_rect(topright=(SCREEN_WIDTH, 0))

        self.update_state()

    def update_ui(self):
        max_health, step = 150, 25
        self.player_health = self.game_state.ex_health
        self.health_index = min(
            len(self.health_info["paths"]) - 1,
            (max_health - self.player_health) // step)
        
        self.ui_health_img = load_scaled_image(
            self.health_info["paths"][self.health_index],
            self.health_info["size"])
        
        self.game_state.ex_health_index = self.health_index
        self.game_state.ex_health_frame = self.health_info["paths"][self.health_index]

    def update_state(self):
        self.player_health = self.game_state.ex_health
        self.update_ui()
        self.remaining_time = max(
            0,
            self.initial_time - (time.time() - self.timer_start))
        
        self.game_state.ex_remaining_time = self.remaining_time
        self.game_state.ex_remaining_dist = self.remaining_distance
        self.update_holes()

    def update_holes(self):
        new_count = (150 - self.player_health) // 25
        if new_count > self.hole_count:
            for _ in range(new_count - self.hole_count):
                self.holes_manager.spawn_hole()
        elif new_count < self.hole_count:
            diff = self.hole_count - new_count
            for _ in range(diff):
                self.holes_manager.holes.pop()
                if hasattr(self.holes_manager, 'hole_positions'):
                    self.holes_manager.hole_positions.pop()
        self.hole_count = new_count
        self.game_state.hole_positions = list(self.holes_manager.hole_positions)

    def game_over(self, path, delay=2000):
        asset_data.song.stop()
        img = pg.image.load(path).convert_alpha()
        rect = img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(img, rect.topleft)
        pg.display.flip()
        pg.time.delay(delay)
        pg.quit()
        sys.exit()

    def run(self):
        while True:
            for e in pg.event.get():

                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif e.type == pg.KEYDOWN:

                    if e.key == pg.K_ESCAPE:
                        self.game_state.has_interior_ran = True
                        self.game_state.current_level = "Exterior"
                        return "Exterior"

                    elif e.key == pg.K_SPACE:
                        if any(
                            hole_rect.colliderect(self.spaceman.rect)
                            for _, hole_rect in self.holes_manager.holes):
                            
                            self.game_state.spaceman_pos = (
                                self.spaceman.rect.x,
                                self.spaceman.rect.y,)
                            
                            self.game_state.current_level = "MiniGame"
                            return "MiniGame"

            keys = pg.key.get_pressed()
            self.spaceman.update(keys)

            self.screen.blit(self.space_bg, (0, 0))
            self.screen.blit(self.esc_ship_img, self.esc_ship_rect)
            self.screen.blit(self.interior_image, (0, 0))
            self.holes_manager.draw(self.screen)
            self.spaceman.draw(self.screen)

            for hole, hole_rect in self.holes_manager.holes:
                if hole_rect.colliderect(self.spaceman.rect):
                    self.screen.blit(self.spacebar_img, self.spacebar_rect)

            self.update_state()
            if self.remaining_time == 0:
                asset_data.fail_sfx.play()
                self.game_over("Assets/images/ui/cold_lose.png", 8000)

            time_text = self.font.render(
                f"Time: {int(self.remaining_time)}", True, (255, 255, 255))
            
            target_w = SCREEN_WIDTH // 15
            target_h = SCREEN_HEIGHT // 35
            scaled_time_text = pg.transform.smoothscale(
                time_text, (target_w, target_h))
            
            self.screen.blit(scaled_time_text, (10, 40))

            dist_surf = self.font.render(
                f"Distance to customer: {int(self.remaining_distance)}", True, (255, 255, 255))
            
            target_w = SCREEN_WIDTH  // 5
            target_h = SCREEN_HEIGHT // 35
            scaled_dist_surf = pg.transform.smoothscale(
                dist_surf, (target_w, target_h))
            
            self.screen.blit(scaled_dist_surf, (10, 10))

            self.screen.blit(self.ui_health_img, self.ui_health_rect)
            self.screen.blit(self.customer_LBL_img, self.customer_lbl_rect)
            self.screen.blit(self.customer_img, self.customer_rect)

            pg.display.flip()
            self.clock.tick(FPS)