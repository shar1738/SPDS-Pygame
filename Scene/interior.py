# Scene/interior.py
import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Interior:
    def __init__(self, screen):
        self.screen = screen
        self.clock  = pg.time.Clock()
        self.font   = pg.font.SysFont(None, 50)

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    return None
                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    from Scene.exterior import Exterior
                    return Exterior(self.screen)

            self.screen.fill((30, 5, 5))
            text = self.font.render(
                "INTERIOR — Press ESC to go back", True, (220, 220, 220)
            )
            rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            self.screen.blit(text, rect)
            pg.display.flip()
            self.clock.tick(60)


