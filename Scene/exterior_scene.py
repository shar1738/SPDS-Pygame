import pygame as pg
import sys
import random
import time
from data import EXT_UI_ELEMENTS
from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from Entities.ship import Ship
from Entities.asteroids import Asteroids  # Your asteroid module


def load_scaled_image(path, size):
    return pg.transform.scale(pg.image.load(path).convert_alpha(), size)


class Exterior:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.background = pg.image.load("Assets/images/background.png").convert()
        self.background = pg.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.player_ship = Ship(150, 300)
        self.asteroids = Asteroids()
        self.asteroids.spawn_rand(5)

        # Load and scale UI images
        self.health_info = EXT_UI_ELEMENTS["health"]
        self.nitro_info = EXT_UI_ELEMENTS["nitro"]
        self.costumer_info = EXT_UI_ELEMENTS["costumers"]
        self.costumer_lbl_info = EXT_UI_ELEMENTS["costumer_label"]
        self.pizza_timer_info = EXT_UI_ELEMENTS["pizza_timer"]

        self.ui_health_img = load_scaled_image(self.health_info["paths"][0], self.health_info["size"])
        self.ui_nitro_img = load_scaled_image(self.nitro_info["paths"][0], self.nitro_info["size"])
        self.costumer_lbl_img = load_scaled_image(self.costumer_lbl_info["paths"][0], self.costumer_lbl_info["size"])

        # Preload pizza timer frames
        self.pizza_timer_frames = [
            load_scaled_image(path, self.pizza_timer_info["size"])
            for path in self.pizza_timer_info["paths"]
        ]
        self.current_pizza_timer_img = self.pizza_timer_frames[0]
        self.pizza_timer_total = random.randint(30, 120)  # 30s to 2 minutes
        self.pizza_timer_start = time.time()
        self.pizza_timer_rect = self.pizza_timer_frames[0].get_rect(topright=(SCREEN_WIDTH - 150, 0))

        # Load random customer image and scale it
        self.ui_costumer_img = load_scaled_image(
            self.costumer_info["paths"][random.randint(0, len(self.costumer_info["paths"]) - 1)],
            self.nitro_info["size"]
        )

        # Position customer at the top-right corner
        self.ui_costumer_rect = self.ui_costumer_img.get_rect(topright=(SCREEN_WIDTH, 0))
        self.costumer_lbl_rect = self.costumer_lbl_img.get_rect(topright=(SCREEN_WIDTH, 100))

        # Position health bottom-left and nitro just to the right
        self.ui_health_rect = self.ui_health_img.get_rect(bottomleft=(10, SCREEN_HEIGHT - 10))
        self.ui_nitro_rect = self.ui_nitro_img.get_rect(bottomleft=(self.ui_health_rect.right + 10, SCREEN_HEIGHT - 50))

    def update_ui(self):
        max_health = 150
        step = 25
        index = min(len(self.health_info["paths"]) - 1, (max_health - self.player_ship.health) // step)
        self.ui_health_img = load_scaled_image(self.health_info["paths"][index], self.health_info["size"])

        # Nitro boost status
        nitro_index = 1 if self.player_ship.is_boosting else 0
        self.ui_nitro_img = load_scaled_image(self.nitro_info["paths"][nitro_index], self.nitro_info["size"])

        # Pizza timer countdown
        elapsed = time.time() - self.pizza_timer_start
        remaining = max(0, self.pizza_timer_total - elapsed)

        num_progress_frames = len(self.pizza_timer_frames) - 2

        if remaining > 0:
            percent_complete = 1 - (remaining / self.pizza_timer_total)
            frame_index = int(percent_complete * num_progress_frames)
        else:
            frame_index = len(self.pizza_timer_frames) - 1  # Final frame: run_out.png

        self.current_pizza_timer_img = self.pizza_timer_frames[frame_index]

        # Only reset after fully displaying run_out.png for 1 second
        if frame_index == len(self.pizza_timer_frames) - 1:
            if not hasattr(self, "run_out_time"):
                self.run_out_time = time.time()
            elif time.time() - self.run_out_time > 1.0:
                self.pizza_timer_total = random.randint(30, 120)
                self.pizza_timer_start = time.time()
                del self.run_out_time
        elif hasattr(self, "run_out_time"):
            del self.run_out_time

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            keys = pg.key.get_pressed()
            self.player_ship.update(keys)
            self.asteroids.update(dt)

            self.update_ui()

            self.screen.blit(self.background, (0, 0))
            self.player_ship.draw(self.screen)
            self.asteroids.update_and_draw(self.screen, self.player_ship)

            self.screen.blit(self.ui_health_img, self.ui_health_rect)
            self.screen.blit(self.ui_nitro_img, self.ui_nitro_rect)
            self.screen.blit(self.ui_costumer_img, self.ui_costumer_rect)
            self.screen.blit(self.costumer_lbl_img, self.costumer_lbl_rect)
            self.screen.blit(self.current_pizza_timer_img, self.pizza_timer_rect)

            pg.display.flip()


if __name__ == "__main__":
    Exterior().run()
