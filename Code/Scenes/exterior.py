# =================== IMPORTS ===================
import pygame as pg
import random
import sys
import time

from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, FONT

from Code.Entities.ship import Ship
from Code.Entities.asteroids import Asteroids
from Code.Entities.pickups import Pickups 

import Code.Funcs_data.asset_data as asset_data
from Code.Funcs_data.helper_functions import load_scaled_image

# =================== CONFIGURATION & CONSTANTS ===================
PIZZA_SPEED = 200
DISTANCE_RATE = 5

asset_data.ship_boost_sfx.set_volume(0.05)
asset_data.fail_sfx.set_volume(0.5)
asset_data.ship_basic_sfx.set_volume(0.3)
asset_data.song.set_volume(0.15)

# =================== EXTERIOR SCENE ===================
class Exterior:
    def __init__(self, game_state, screen):
        self.game_state = game_state
        self.screen = screen

        pg.mixer.init()

        # **TIME INIT**
        self.time = self.game_state.time
        self.clock = self.game_state.clock

        self.distance = self.game_state.distance

        self.background = load_scaled_image("Assets/images/exterior/background.png",
                                            (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.ship_basic_sfx = asset_data.ship_basic_sfx

        self.player_ship = Ship(150, 300, game_state)
        self.asteroids = Asteroids()

        self.override_img = load_scaled_image("Assets/images/objects/ship/basic_ship.png", 
                                              (SCREEN_WIDTH // 18, SCREEN_HEIGHT // 12.5))
        
        self.override_img2 = load_scaled_image("Assets/images/objects/ship/hyper_plasma_extreme.png", 
                                               (SCREEN_WIDTH // 18, SCREEN_HEIGHT // 12.5))

        self.customer_img = load_scaled_image(self.game_state.customer_path, asset_data.EXT_UI_ELEMENTS["customers"]["size"])
        
        # --- ASTEROIDS & GAME ELEMENTS ---
        self.hole_shown = False
        self.hole_start_time = None
        self.asteroids.spawn_rand(5)

        # --- PICKUPS (pizza boost) ---
        self.pickups = Pickups(move_speed=12, effect="increase", amount=0)
        self.pickup_active = False
        self.pickup_start = 0
        self.pickup_duration = 5.0

        self.pizza_box_init()

        # Initializes 
        self.ui_init()
        self.font = pg.font.Font(FONT, 30)

    # =================== UI UPDATE ===================
    def update_ui(self):

        self.ui_nitro_img = self.nitro_imgs[1 if self.player_ship.is_boosting else 0]

        # Timer update
        if self.distance > 0:
            elapsed = time.time() - self.time
            if self.time == 0:
                asset_data.fail_sfx.play()
                self.game_state.game_over("Assets/images/win_lose/cold_lose.png", 8000)

    def run(self):
        self.player_health = self.player_ship.player_health
        while True:
            # --- DRAW SCENE ---
            self.draw_scene()
            
            # Chech for Scene
            self.end_scene()

            dt_ms = self.clock.tick(FPS)
            dt = dt_ms / 1000.0

            self.update_ui()
            self.player_ship.update(pg.key.get_pressed(), dt)

            self.pickups.update(dt)
            before = len(self.pickups.pickup_list)
            self.pickups.check_collision(self.player_ship)
            after = len(self.pickups.pickup_list)

            if after < before:
                self.pickup_active = True
                self.pickup_start = time.time()
            
            # --- DISTANCE RATE & BOOST LOGIC ---
            base_rate = DISTANCE_RATE * (2 if self.player_ship.is_boosting else 1)
            boost = self.pickup_active and (time.time() - self.pickup_start) < self.pickup_duration
            if boost:
                self.asteroids.is_inv = True
                rate = base_rate * 4
                self.player_ship.set_override_image(self.override_img2, 0.70)
                self.player_ship.is_boosting
            else:
                rate = base_rate
                if self.pickup_active:
                    self.pickup_active = False

            self.distance = max(0, self.distance - rate * dt)

            if self.distance <= 0:
                self.asteroids.can_spawn = False
                if not self.show_delivery:
                    self.show_delivery = True
            
            if self.player_health == 0:
                asset_data.fail_sfx.play()
                self.game_over("Assets/images/win_lose/game_over.png", 8000)
            
            if boost:
                # extra movement for 5× speed
                for a in self.asteroids.asteroid_list:
                    a["pos"][0] -= a["speed"] * 5
                self.asteroids.update(dt_ms)
            else:
                self.asteroids.update(dt_ms)

            pg.display.flip()

    def ui_init(self):

        # **HEALTH**
        self.health_info = asset_data.EXT_UI_ELEMENTS["health"]

        self.health_imgs = [
            load_scaled_image(path, self.health_info["size"])
            for path in self.health_info["paths"]
        ]

        self.ui_health_img = self.health_imgs[self.game_state.health_index]
        self.ui_health_rect = self.ui_health_img.get_rect(bottomleft=
                                                        (asset_data.EXT_UI_ELEMENTS["health"]["position"]))

        # **NITRO**
        self.nitro_info = asset_data.EXT_UI_ELEMENTS["nitro"]
        self.nitro_imgs = [
            load_scaled_image(path, self.nitro_info["size"])
            for path in self.nitro_info["paths"]]

        self.ui_nitro_img = self.nitro_imgs[0]
        self.ui_nitro_rect = self.ui_nitro_img.get_rect(bottomleft=(asset_data.EXT_UI_ELEMENTS["nitro"]["position"]))

        # **CUSTOMER**
        self.customer_LBL_info = asset_data.EXT_UI_ELEMENTS["costumer_label"]
        self.customer_LBL_img = load_scaled_image(self.customer_LBL_info["paths"][0], self.customer_LBL_info["size"])
        self.customer_rect = self.customer_img.get_rect(topright=(SCREEN_WIDTH, 0))
        self.customer_lbl_rect = self.customer_LBL_img.get_rect(topright=(SCREEN_WIDTH * 1.014, SCREEN_HEIGHT // 12))
        self.customer_LBL_info = asset_data.EXT_UI_ELEMENTS["costumer_label"]

        # **ESCAPE INFO**
        self.esc_info = asset_data.EXT_UI_ELEMENTS["esc_ship"]
        self.esc_ship_img = load_scaled_image(self.esc_info["paths"][0], self.esc_info["size"])
        self.esc_ship_rect = self.esc_ship_img.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))

        # **HOLE IN INTERIOR IMAGE**
        self.hole_info = asset_data.EXT_UI_ELEMENTS["hole"]
        self.hole_img = load_scaled_image(self.hole_info["paths"][0], self.hole_info["size"])
        self.hole_rect = self.hole_img.get_rect(center=(SCREEN_WIDTH // 2,SCREEN_HEIGHT // 2))

    def pizza_box_init(self):
        self.delivered_img = pg.image.load("Assets/images/exterior/ui/loading_bay.png").convert_alpha()
        self.delivered_img = pg.transform.scale(self.delivered_img, (SCREEN_WIDTH * 8/10, SCREEN_HEIGHT * 8/10))
        self.delivered_rect = self.delivered_img.get_rect(topleft=(SCREEN_WIDTH - 200, 0))
        self.show_delivery = False
        self.raw_pizza = pg.image.load("Assets/images/objects/pizza_box.png").convert_alpha()
        self.pizza_img = pg.transform.scale(self.raw_pizza, (128, 128))
        self.pizza_angle = 0.0
        self.pizza_rot_speed = 180.0
        self.pizza_spawned = False
        self.pizza_rect = None

    def draw_scene(self):

        self.screen.blit(self.background, (0, 0))
        self.player_ship.draw(self.screen)
        self.pickups.draw(self.screen)
        self.asteroids.update_and_draw(self.screen, self.player_ship, self.game_state.dt_ms)

        self.screen.blit(self.ui_health_img, self.ui_health_rect)
        self.screen.blit(self.ui_nitro_img, self.ui_nitro_rect)
        self.screen.blit(self.customer_img, self.customer_rect)
        self.screen.blit(self.customer_LBL_img, self.customer_lbl_rect)
        self.screen.blit(self.esc_ship_img, self.esc_ship_rect)
        time_text = self.font.render(f"Time: {int(self.game_state.time)}", True, (255, 255, 255))
        target_w = SCREEN_WIDTH  // 15
        target_h = SCREEN_HEIGHT // 35
        scaled_time_text = pg.transform.smoothscale(time_text, (target_w, target_h))
        self.screen.blit(scaled_time_text, (10, 40))

        # 1) Create the raw text surface
        dist_surf = self.font.render(
            f"Distance to customer: {int(self.distance)}", True, (255, 255, 255))
        target_w = SCREEN_WIDTH  // 4
        target_h = SCREEN_HEIGHT // 35

        scaled_dist_surf = pg.transform.smoothscale(dist_surf, (target_w, target_h))

        self.screen.blit(scaled_dist_surf, (10, 10))

    def end_scene(self):
        if self.show_delivery:
            # door slide
            if self.delivered_rect.right > SCREEN_WIDTH:
                self.delivered_rect.x -= 200*dt
            self.screen.blit(self.delivered_img,self.delivered_rect)
            # pizza fly
            if not self.pizza_spawned and self.delivered_rect.right<=SCREEN_WIDTH:
                ship_c=self.player_ship.rect.center
                self.pizza_rect=self.pizza_img.get_rect(center=ship_c)
                self.pizza_spawned=True
            if self.pizza_spawned:
                tx,ty=SCREEN_WIDTH * 6/10,SCREEN_HEIGHT * 7/10
                px,py=self.pizza_rect.center; dx,dy=tx-px,ty-py
                dist=(dx*dx)**0.5
                if dist>5:
                    dx,dy=dx/dist,dy/dist
                    self.pizza_rect.centerx+=int(dx*PIZZA_SPEED*dt)
                    self.pizza_rect.centery+=int(dy*PIZZA_SPEED*dt)
                    self.pizza_angle=(self.pizza_angle+self.pizza_rot_speed*dt)%360
                    self.screen.blit(pg.transform.rotate(self.pizza_img,self.pizza_angle),self.pizza_rect)
                else:
                    self.screen.blit(pg.transform.rotate(self.pizza_img,self.pizza_angle),self.pizza_rect)
                    asset_data.yay_sfx.play()
                    self.game_over("Assets/images/win_lose/win_ui.png",3000)