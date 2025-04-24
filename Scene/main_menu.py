import pygame as pg
import Scene.settings as S
import sys

class MainMenu:
    def __init__(self):
        pg.init()
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

        self.screen = pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        pg.display.set_caption("Main Menu")

  
        self.font = pg.font.Font(None, 74)

      
        self.button_width = 200
        self.button_height = 80
        self.button_x = (S.SCREEN_WIDTH - self.button_width) // 2
        self.button_y = (S.SCREEN_HEIGHT - self.button_height) // 2

    def draw_button(self):
        pg.draw.rect(self.screen, self.GRAY, (self.button_x, self.button_y, self.button_width, self.button_height))
        text = self.font.render("Start", True, self.BLACK)
        text_rect = text.get_rect(center=(self.button_x + self.button_width // 2, self.button_y + self.button_height // 2))
        self.screen.blit(text, text_rect)

    def run(self): 
        while True: #run a continous loop until one button is pressed than break the loop causing the main_menu to stop running 
            self.screen.fill(self.WHITE)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        mouse_x, mouse_y = event.pos #Mouse Position
                        if self.button_x <= mouse_x <= self.button_x + self.button_width and self.button_y <= mouse_y <= self.button_y + self.button_height: #if the click happens within these bounds, return
                            print("Start button clicked!")
                            return  

            
            self.draw_button()

            
            pg.display.flip()