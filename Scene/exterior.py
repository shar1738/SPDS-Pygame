# =================== IMPORTS ===================
import pygame as pg
import random
import json
import sys
import time

from Entities.ship import Ship
from Entities.asteroids import Asteroids
from funcs_data.data import EXT_UI_ELEMENTS
from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, FONT
from sfx import ship_basic_sfx, ship_boost_sfx, yay_sfx, fail_sfx, song
from game_state import GameState


# =================== CONFIGURATION & CONSTANTS ===================
DISTANCE_RATE = 5
INI_DISTANCE = 0
START_TIME = random.randint(100, 180)
PIZZA_SPEED = 200

ship_boost_sfx.set_volume(0.008)
fail_sfx.set_volume(0.5)
ship_basic_sfx.set_volume(0.3)
song.set_volume(0.15)


# =================== HELPER FUNCTIONS ===================
def load_scaled_image(path, size):
    return pg.transform.scale(pg.image.load(path).convert_alpha(), size)


# =================== EXTERIOR SCENE ===================
class Exterior:
    def __init__(self, game_state):
        # Init Pygame and Mixer
        pg.init()
        pg.mixer.init()
        self.ship_basic_sfx = ship_basic_sfx
        self.clock = pg.time.Clock()
        self.game_state = game_state
        self.player_ship = Ship(150, 300)
        self.override_img = load_scaled_image("Assets/images/ship/basic_ship.png", (200, 200))
        
        # --- CUSTOMER SELECTION & TIMER SETUP ---
        if self.game_state.has_interior_ran:
            # Use values carried over from Interior:
            self.player_health = self.game_state.ex_health
            self.player_ship.player_health = self.game_state.ex_health  # Preserve the damaged health
            self.distance = self.game_state.ex_remaining_dist
            self.rand_time = self.game_state.ex_remaining_time  # Remaining time from previous scene
            self.timer_start = time.time()  # Reset timer start for this scene
            self.game_state.timer_start = self.timer_start
            self.health_index = self.game_state.ex_health_index
            # Load customer image using stored file path:
            customer_path = self.game_state.current_customer
        else:
            # First-run (or no Interior update): assign default values.
            self.player_health = self.player_ship.player_health
            self.distance = random.randint(600, 1000)
            self.game_state.ex_health = self.player_health
            self.game_state.ex_distance = self.distance
            self.health_info = EXT_UI_ELEMENTS["health"]
            self.health_index = min(len(self.health_info["paths"]) - 1, (150 - self.player_health) // 25)
            self.rand_time = START_TIME
            self.timer_start = time.time()
            self.game_state.timer_start = self.timer_start
            # Randomly select a customer and store its file path:
            customer_path = random.choice(EXT_UI_ELEMENTS["customers"]["paths"])
            self.game_state.current_customer = customer_path
        
        # Save the customer path in an instance variable (for later access)
        self.customer_path = customer_path
        self.customer_img = load_scaled_image(self.customer_path, EXT_UI_ELEMENTS["customers"]["size"])

        # --- SCREEN & BACKGROUND ---
        pg.display.set_caption("S.P.D.S")
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = load_scaled_image("Assets/images/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # --- ASTEROIDS & OTHER GAME ELEMENTS ---
        self.is_inv = False  # Replace IS_INV if defined otherwise.
        self.hole_shown = False
        self.hole_start_time = None
        self.asteroids = Asteroids()
        self.asteroids.spawn_rand(5)
        self.spawn_aster = True

        # --- UI - DELIVERY & PIZZA ---
        self.delivered_img = pg.image.load("Assets/images/ui/garage_(delivered).png").convert_alpha()
        self.delivered_rect = self.delivered_img.get_rect(topright=(SCREEN_WIDTH + 1500, 0))
        self.show_delivery = False
        
        self.raw_pizza = pg.image.load("Assets/images/pizza_box.png").convert_alpha()
        self.pizza_img = pg.transform.scale(self.raw_pizza, (128, 128))
        self.pizza_angle = 0.0
        self.pizza_rot_speed = 180.0
        self.pizza_spawned = False
        self.pizza_rect = None

        # --- UI - DATA FROM EXT_UI_ELEMENTS ---
        self.health_info = EXT_UI_ELEMENTS["health"]
        self.nitro_info = EXT_UI_ELEMENTS["nitro"]
        self.customer_LBL_info = EXT_UI_ELEMENTS["costumer_label"]
        self.esc_info = EXT_UI_ELEMENTS["esc_ship"]
        self.hole_info = EXT_UI_ELEMENTS["hole"]
        self.font = pg.font.Font(FONT, 30)

        # --- UI - STATIC IMAGES ---
        self.ui_health_img = load_scaled_image(self.health_info["paths"][0], self.health_info["size"])
        # DO NOT override customer_img here. We're already using the dynamic one.
        self.customer_LBL_img = load_scaled_image(self.customer_LBL_info["paths"][0], self.customer_LBL_info["size"])
        self.esc_ship_img = load_scaled_image(self.esc_info["paths"][0], self.esc_info["size"])
        self.hole_img = load_scaled_image(self.hole_info["paths"][0], self.hole_info["size"])

        # --- TIMER (If not coming from Interior, ensure timer values are fresh) ---
        if not self.game_state.has_interior_ran:
            self.rand_time = START_TIME
            self.timer_start = time.time()
            self.game_state.timer_start = self.timer_start

        # --- UI - RECTS ---
        self.customer_rect = self.customer_img.get_rect(topright=(SCREEN_WIDTH, 0))
        self.costumer_lbl_rect = self.customer_LBL_img.get_rect(topright=(SCREEN_WIDTH, 100))
        self.esc_ship_rect = self.esc_ship_img.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        self.hole_rect = self.hole_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.ui_health_rect = load_scaled_image(
            self.health_info["paths"][self.health_index],
            self.health_info["size"]
        ).get_rect(bottomleft=(10, SCREEN_HEIGHT - 10))
        self.ui_nitro_rect = self.nitro_img = load_scaled_image(
            self.nitro_info["paths"][0], self.nitro_info["size"]
        ).get_rect(bottomleft=(self.ui_health_rect.right + 10, SCREEN_HEIGHT - 50))

        # --- HOLE STATUS ---
        self.hole_shown = False
        self.hole_start_time = None

    # =================== UI UPDATE ===================
    def update_ui(self):
        # Update health UI based on current health
        self.player_health = self.player_ship.player_health
        max_health = 150
        step = 25
        self.health_index = min(len(self.health_info["paths"]) - 1,
                                (max_health - self.player_health) // step)
        self.ui_health_img = load_scaled_image(self.health_info["paths"][self.health_index],
                                               self.health_info["size"])
        # Store health index info into game_state
        self.game_state.ex_health_index = self.health_index
        self.game_state.ex_health_frame = self.health_info["paths"][self.health_index]
        self.ui_health_img = load_scaled_image(self.game_state.ex_health_frame, self.health_info["size"])
        nitro_index = 1 if self.player_ship.is_boosting else 0
        self.ui_nitro_img = load_scaled_image(self.nitro_info["paths"][nitro_index], self.nitro_info["size"])
        
        # Timer update
        if self.distance > 0:
            elapsed = time.time() - self.timer_start
            self.remaining_time = max(0, self.rand_time - elapsed)
            if self.remaining_time == 0:
                fail_sfx.play()
                self.game_over("Assets/images/ui/cold_lose.png", 8000)

    def game_over(self, path, delay):
        song.stop()
        game_over_img = pg.image.load(path).convert_alpha()
        rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_img, rect.topleft)
        pg.display.flip()
        pg.time.delay(delay)
        pg.quit()
        sys.exit()

    def garage_spawn(self):
        garage_img = pg.image.load("Assets/images/ui/garage_(delivered).png").convert_alpha()
        rect = garage_img.get_rect(topright=(SCREEN_WIDTH - 100, SCREEN_HEIGHT))
        self.screen.blit(garage_img, rect.topleft)
        pg.display.flip()

    def hole_detected(self):
        if self.hole_start_time is None:
            self.hole_start_time = time.time()

    def run(self):
        self.player_health = self.player_ship.player_health
        while True:
            dt_ms = self.clock.tick(FPS)
            dt = dt_ms / 1000.0

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    max_health = 150
                    step = 25
                    self.holes = (max_health - self.player_health) // step
                    elapsed = time.time() - self.timer_start
                    self.remaining_time = max(0, self.rand_time - elapsed)
                    self.game_state.ex_health = self.player_health
                    self.game_state.ex_health_frame = self.health_info["paths"][self.health_index]
                    self.game_state.ex_health_index = self.health_index
                    self.game_state.ex_remaining_time = int(self.remaining_time)
                    self.game_state.ex_remaining_dist = self.distance
                    # Save the customer image file path (persisting the same customer)
                    self.game_state.current_customer = self.customer_path
                    print(self.game_state.current_customer)
                    self.game_state.holes = self.holes
                    self.game_state.current_level = 'Interior'
                    return self.game_state.current_level

            keys = pg.key.get_pressed()
            self.player_ship.update(keys, dt)

            self.asteroids.update(dt_ms)
            if self.player_health <= 0:
                fail_sfx.play()
                self.game_over("Assets/images/ui/game_over.png", 8000)

            if self.player_health == 125:
                self.hole_detected()

            rate = DISTANCE_RATE * (2 if self.player_ship.is_boosting else 1)
            self.distance = max(0, self.distance - rate * dt)

            if self.distance <= 0:
                self.asteroids.can_spawn = False
                if not self.show_delivery:
                    self.show_delivery = True

            self.update_ui()
            self.player_health = self.player_ship.player_health

            # Drawing
            self.screen.blit(self.background, (0, 0))
            self.player_ship.draw(self.screen)
            self.asteroids.update_and_draw(self.screen, self.player_ship)

            self.screen.blit(self.ui_health_img, self.ui_health_rect)
            self.screen.blit(self.ui_nitro_img, self.ui_nitro_rect)
            self.screen.blit(self.customer_img, self.customer_rect)
            self.screen.blit(self.customer_LBL_img, self.costumer_lbl_rect)
            time_text = self.font.render(f"Time: {int(self.remaining_time)}", True, (255, 255, 255))
            self.screen.blit(time_text, (10, 40))
            
            self.screen.blit(self.esc_ship_img, self.esc_ship_rect)

            dist_text = f"Distance to customer: {int(self.distance)}"
            text_surf = self.font.render(dist_text, True, (255, 255, 255))
            self.screen.blit(text_surf, (10, 10))

            if self.player_ship.is_boosting:
                ship_boost_sfx.play()
                
            DELIEVER_SPEED = 200

            if self.show_delivery:
                if self.delivered_rect.right > SCREEN_WIDTH:
                    self.delivered_rect.x -= DELIEVER_SPEED * dt
                else:
                    self.delivered_rect.right = SCREEN_WIDTH
                    self.player_ship.set_override_image(self.override_img)
                    if not self.pizza_spawned:
                        ship_center = self.player_ship.rect.center
                        self.pizza_rect = self.pizza_img.get_rect(center=ship_center)
                        self.pizza_spawned = True

                self.screen.blit(self.delivered_img, self.delivered_rect)

                if self.pizza_spawned:
                    target_x, target_y = SCREEN_WIDTH - 700, SCREEN_HEIGHT - 500
                    self.target_xy = (target_x, target_y)

                    px, py = self.pizza_rect.center
                    dx = target_x - px
                    dy = target_y - py
                    distance = (dx**2 + dy**2) ** 0.5

                    if distance > 5:
                        dx /= distance
                        dy /= distance
                        self.pizza_rect.centerx += int(dx * PIZZA_SPEED * dt)
                        self.pizza_rect.centery += int(dy * PIZZA_SPEED * dt)
                        self.pizza_angle = (self.pizza_angle * dt) % 360
                        self.screen.blit(pg.transform.rotate(self.pizza_img, self.pizza_angle), self.pizza_rect)
                    else:
                        self.pizza_rect.center = self.target_xy
                        self.screen.blit(pg.transform.rotate(self.pizza_img, self.pizza_angle), self.pizza_rect)
                        yay_sfx.play()
                        self.game_over("Assets/images/ui/win_ui.png", 3000)

            if self.player_ship.is_boosting:
                ship_boost_sfx.play()
            
            if self.hole_start_time and time.time() - self.hole_start_time < 3:
                self.screen.blit(self.hole_img, self.hole_rect)
                

            pg.display.flip()



if __name__ == "__main__":
    Exterior().run()# =================== IMPORTS ===================