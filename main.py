import pygame as pg
import settings as S
from funcs_data.scene_manager import SCENES


class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")

        # Use the instance to access screen dimensions
        self.screen = pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

    def run(self):
        menu = SCENES["MainMenu"]()
        menu.run() 

        mini_game = SCENES["MiniGame"]()
        mini_game.run()

        #exterior = SCENES["Exterior"]()
        #exterior.run()

        #interior = SCENES["Interior"]()
        #inerior.run
    
if __name__ == "__main__":
    Main().run()