import pygame as pg
import Main.settings as S
import sys
from Main.constants import load_assets

# Default positions configuration
DEFAULT_POSITIONS = {
    "ship": (100, 0),
    "aster1": (500, 0),
}


class Exterior:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")

        # Screen setup
        self.screen = pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        # Load assets
        self.assets = load_assets()
        self.ship = self.assets["ship"]
        self.aster1 = self.assets["aster1"]

    def calculate_hitbox(self, pos, offset):
        """Calculate the hitbox for an object."""
        x, y = pos
        offset_x, offset_y, width, height = offset
        return pg.Rect(x + offset_x, y + offset_y, width, height)

    def render(self):
        """Render the scene."""
        self.screen.fill((0, 0, 0))

        # Render the ship
        ship_pos = DEFAULT_POSITIONS["ship"]
        self.screen.blit(self.ship["image"], ship_pos)
        hitbox_ship = self.calculate_hitbox(ship_pos, self.ship["hitbox_offset"])
        pg.draw.rect(self.screen, (255, 0, 0), hitbox_ship, 1)

        # Render the asteroid
        aster1_pos = DEFAULT_POSITIONS["aster1"]
        self.screen.blit(self.aster1["image"], aster1_pos)
        hitbox_aster = self.calculate_hitbox(aster1_pos, self.aster1["hitbox_offset"])
        pg.draw.rect(self.screen, (255, 0, 0), hitbox_aster, 1)

        pg.display.update()

    def handle_events(self):
        """Handle events for the scene."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        """Run the exterior scene loop."""
        while True:
            self.clock.tick(S.FPS)
            self.render()
            self.handle_events()


if __name__ == "__main__":
    from settings import Settings
    settings = Settings()
    Exterior(settings).run()