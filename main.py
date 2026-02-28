import pygame as pg

import settings as S
import game_state as game_state

from Code.Funcs_data.asset_data import song 

class Main:
    def __init__(self):
        
        pg.init()
        pg.mixer.init()
        song.set_volume(0.05)

        pg.display.set_caption("S.P.D.S")
        self.screen = pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.game_state = game_state()  # Shared state object
        # Ensure the game state has a valid starting level:
        self.game_state.current_level = "Exterior"

    def run(self):
        # Run the main menu first
        menu = game_state.SCENES["MainMenu"](self.game_state)
        menu.run()

        # Main loop for dynamic scene transitions.
        while True:
            current_level = self.game_state.current_level

            if current_level == 'Exterior':
                scene = game_state.SCENES["Exterior"](self.game_state)
            elif current_level == 'Interior':
                scene = game_state.SCENES["Interior"](self.game_state)
            elif current_level == 'MiniGame':
                scene = game_state.SCENES["MiniGame"](self.game_state)
            else:
                print("Unknown scene. Exiting the game loop.")
                break

            # Run the current scene; its run() method should ideally return a new level or update game_state.
            next_scene = scene.run()
            if next_scene:
                self.game_state.current_level = next_scene

if __name__ == "__main__":
    song.play(-1)
    Main().run()
