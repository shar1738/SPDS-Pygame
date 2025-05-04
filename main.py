import pygame as pg
import settings as S
from funcs_data.scene_manager import SCENES
from game_state import GameState


class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")
        self.screen = pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.game_state = GameState()  # Shared state object

    def run(self):
        # Pass game_state to each scene
        menu = SCENES["MainMenu"](self.game_state)
        menu.run()

        exterior = SCENES["Exterior"](self.game_state)
        interior = SCENES["Interior"](self.game_state)
        mini_game = SCENES["MiniGame"](self.game_state)

        exterior.run()

        if self.game_state.current_level == 'Exterior':
            exterior.run()

        if self.game_state.current_level == 'Interior':
            interior.run()
        
        if self.game_state.current_level == 'MiniGame':
            mini_game.run()
    
if __name__ == "__main__":
    Main().run()