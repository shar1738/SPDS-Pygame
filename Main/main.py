import pygame as pg
import settings as S
from Scene.main_menu import MainMenu
from Scene.exterior_scene import Exterior


class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("S.P.D.S")

        # Use the instance to access screen dimensions
        self.screen = pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

    def run(self):
        menu = MainMenu()  
        menu.run() 

        exterior = Exterior()
        exterior.run()


if __name__ == "__main__":
    Main().run()