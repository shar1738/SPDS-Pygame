import pygame as pg
import sys
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT
from game_state import GameState
import time 
from sfx import gooing_sfx, song, fail_sfx
from funcs_data.data import EXT_UI_ELEMENTS  # Make sure EXT_UI_ELEMENTS is imported

def load_scaled_image(path, size):
    """Safely loads and scales an image."""
    try:
        return pg.transform.scale(pg.image.load(path).convert_alpha(), size)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return pg.Surface(size)  # Returns a blank surface if loading fails

class MiniGame:
    def __init__(self, game_state: GameState):
        pg.init()
        pg.mixer.init()
        self.game_state = game_state
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen_width, self.screen_height = screen_size

        self.screen = pg.display.set_mode(screen_size)
        pg.display.set_caption("Seal the Hole")
        self.clock = pg.time.Clock()
        self.timer_start = time.time()   

        # Load and scale background image
        bg_img = pg.image.load("Assets/images/minigame/cockpit_wall.png").convert_alpha()
        self.background = pg.transform.scale(bg_img, screen_size)

        sealed_img = pg.image.load("Assets/images/minigame/hole_sealed.png").convert_alpha()
        self.sealed_img = pg.transform.scale(sealed_img, (254, 254))
        self.sealed_rect = self.sealed_img.get_rect(center=(self.screen_width // 2, int(self.screen_height // 2)))

        sealer_img = pg.image.load("Assets/images/minigame/goon_sealant.png").convert_alpha()
        self.sealer_img = pg.transform.scale(sealer_img, (254, 254))
        self.sealer_rect = self.sealer_img.get_rect()

        self.hole_paths = ['Assets/images/minigame/hole1.png',
                           'Assets/images/minigame/hole2.png',
                           'Assets/images/minigame/hole3.png',
                           'Assets/images/minigame/hole4.png']
        # Load and scale random hole image
        random_hole_path = random.choice(self.hole_paths)
        original_hole = pg.image.load(random_hole_path).convert_alpha()
        self.hole = pg.transform.scale(original_hole, (254, 254))
        self.hole_rect = self.hole.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        # Surface to accumulate green circle drawing (sealant)
        self.sealant_surface = pg.Surface(screen_size, pg.SRCALPHA)

        # Sealant brush settings
        self.brush_radius = 35
        self.brush_color = (165, 227, 141)

        self.mouse_down = False
        self.hole_filled = False
        self.threshold_fill_percent = 0.99
        self.font = pg.font.Font(FONT, 48)

    def get_fill_percentage(self):
        hole_alpha = pg.surfarray.pixels_alpha(self.hole)
        seal_alpha = pg.surfarray.pixels_alpha(self.sealant_surface)

        filled = 0
        total = 0

        for y in range(self.hole_rect.height):
            for x in range(self.hole_rect.width):
                screen_x = self.hole_rect.left + x
                screen_y = self.hole_rect.top + y

                if 0 <= screen_x < self.screen_width and 0 <= screen_y < self.screen_height:
                    if hole_alpha[x][y] > 0:
                        total += 1
                        if seal_alpha[screen_x][screen_y] > 0:
                            filled += 1

        return filled / total if total > 0 else 0
    
    def update_state(self):
        """Update player state variables and holes dynamically."""
        self.time = self.game_state.ex_remaining_time
        self.player_health = self.game_state.ex_health
        self.holes = self.game_state.holes
        elapsed = time.time() - self.timer_start
        self.remaining_time = max(0, self.time - elapsed)
    
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
        while True:
            # Update state at the beginning of each loop iteration
            self.update_state()

            self.screen.blit(self.background, (0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                    gooing_sfx.set_volume(0.1)
                    gooing_sfx.play(-1)
                elif event.type == pg.MOUSEBUTTONUP:
                    gooing_sfx.set_volume(0)
                    self.mouse_down = False

            mouse_x, mouse_y = pg.mouse.get_pos()
            self.sealer_rect.center = (mouse_x, mouse_y)
            self.screen.blit(self.hole, self.hole_rect)
            self.screen.blit(self.sealant_surface, (0, 0))

            offset_x = 97  # Adjust this value to move it right
            offset_y = 48  # Adjust this value to move it down
            blit_x = mouse_x + offset_x - self.sealer_rect.width // 2
            blit_y = mouse_y + offset_y - self.sealer_rect.height // 2
            self.screen.blit(self.sealer_img, (blit_x, blit_y))  # Blit at the offset position

            if self.mouse_down and not self.hole_filled:
                mouse_pos = pg.mouse.get_pos()
                if self.hole_rect.collidepoint(mouse_pos):
                    pg.draw.circle(self.sealant_surface, self.brush_color, mouse_pos, self.brush_radius)

            if not self.hole_filled:
                fill_pct = self.get_fill_percentage()
                if fill_pct >= self.threshold_fill_percent:
                    self.hole_filled = True

            # Render the UI Health and Timer in the MiniGame
            # Health UI rendered based on the global game_state health index.
            health_img = load_scaled_image(EXT_UI_ELEMENTS["health"]["paths"][self.game_state.ex_health_index],
                                        EXT_UI_ELEMENTS["health"]["size"])
            health_rect = health_img.get_rect(bottomright=(SCREEN_WIDTH // 13.5, SCREEN_HEIGHT - 10))
            self.screen.blit(health_img, health_rect)
            
            # Render timer text using the updated self.remaining_time value.
            timer_text = self.font.render(f"Time: {int(self.remaining_time)}", True, (0,0,0))
            self.screen.blit(timer_text, (10, 50))

            if self.remaining_time == 0:
                fail_sfx.play()
                self.game_over("Assets/images/ui/cold_lose.png", 8000)

            if self.hole_filled:
                self.screen.blit(self.sealed_img, self.sealed_rect)
                pg.display.flip()
                
                # SYNC HEALTH: Add 25 to global ex_health and recalc the health index.
                self.game_state.ex_health += 25
                max_health = 150
                step = 25
                new_index = min(len(EXT_UI_ELEMENTS["health"]["paths"]) - 1,
                                (max_health - self.game_state.ex_health) // step)
                self.game_state.ex_health_index = new_index
                self.game_state.ex_health_frame = EXT_UI_ELEMENTS["health"]["paths"][new_index]
                print("Global ex_health:", self.game_state.ex_health)
                self.game_state.holes -= 1

                # SYNC TIME: Update the global remaining time based on the mini-game countdown.
                self.game_state.ex_remaining_time = int(self.remaining_time)

                gooing_sfx.set_volume(0)
                pg.time.delay(1000)
                
                self.game_state.current_level = 'Interior'
                return self.game_state.current_level

            pg.display.flip()
            self.clock.tick(FPS)
