import pygame as pg
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_manager import GameState
from sfx import gooing_sfx

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

        # Load and scale background image
        bg_img = pg.image.load("Assets/images/minigame/cockpit_wall.png").convert_alpha() 
        self.background = pg.transform.scale(bg_img, screen_size)

        # Load and scale "hole sealed" image
        sealed_img = pg.image.load("Assets/images/minigame/hole_sealed.png").convert_alpha() 
        self.sealed_img = pg.transform.scale(sealed_img, (254, 254)) 
        self.sealed_rect = self.sealed_img.get_rect(center=(self.screen_width // 2, 125))

        # Load and scale hole image
        original_hole = pg.image.load("Assets/images/minigame/hole1.png").convert_alpha()
        self.hole = pg.transform.scale(original_hole, (254, 254))
        self.hole_rect = self.hole.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        # Surface to accumulate green circle drawing (sealant)
        self.sealant_surface = pg.Surface(screen_size, pg.SRCALPHA)

        # Sealant brush settings
        self.brush_radius = 17
        self.brush_color = (165, 227, 141)

        self.mouse_down = False
        self.hole_filled = False
        self.threshold_fill_percent = 1
        self.font = pg.font.SysFont(None, 48)

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

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                    gooing_sfx.set_volume(0.1)
                    gooing_sfx.play()
                elif event.type == pg.MOUSEBUTTONUP:
                    gooing_sfx.set_volume(0)
                    self.mouse_down = False


            # Draw the hole
            self.screen.blit(self.hole, self.hole_rect)

            # Draw accumulated green sealant
            self.screen.blit(self.sealant_surface, (0, 0))

            # Handle drawing with brush
            if self.mouse_down and not self.hole_filled:
                mouse_pos = pg.mouse.get_pos()
                if self.hole_rect.collidepoint(mouse_pos):
                    pg.draw.circle(self.sealant_surface, self.brush_color, mouse_pos, self.brush_radius)

            # Check fill completion
            if not self.hole_filled:
                fill_pct = self.get_fill_percentage()
                if fill_pct >= self.threshold_fill_percent:
                    self.hole_filled = True
                    print("Hole sealed!")

            # Show sealed indicator
            if self.hole_filled:
                self.screen.blit(self.sealed_img, self.sealed_rect)

            pg.display.flip()
            self.clock.tick(FPS)
