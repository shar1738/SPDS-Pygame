import pygame as pg
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Configuration for UI assets
UI_CONFIG = {
    "buttons": {
        "title": "Assets/images/ui/title.png",
        "start": "Assets/images/ui/start.png"
    }
}

class MainMenu:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Main Menu")

        # Load background
        self.background = pg.image.load("Assets/images/background.png").convert()

        # Load button images and create rects for hit detection
        self.buttons = {}
        spacing = 20  # spacing between buttons
        total_height = 0
        images = {}
        # First, load all images to calculate total height
        for key, path in UI_CONFIG["buttons"].items():
            img = pg.image.load(path).convert_alpha()
            images[key] = img
            total_height += img.get_height()
        # Add spacing between buttons
        total_height += spacing * (len(images) - 1)

        # Starting y to vertically center all buttons
        current_y = (SCREEN_HEIGHT - total_height) // 2

        # Create rects for each button, centered horizontally
        for name, img in images.items():
            rect = img.get_rect(center=(SCREEN_WIDTH // 2, current_y + img.get_height() // 2))
            self.buttons[name] = {'image': img, 'rect': rect}
            current_y += img.get_height() + spacing

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        # Draw each button
        for btn in self.buttons.values():
            self.screen.blit(btn['image'], btn['rect'].topleft)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    # Check each button for click
                    for name, btn in self.buttons.items():
                        if btn['rect'].collidepoint(mouse_pos):
                            print(f"{name.capitalize()} button clicked!")
                            return name  # return the identifier of clicked button
            # Draw UI
            self.draw()
            pg.display.flip()

if __name__ == "__main__":
    menu = MainMenu()
    action = menu.run()
    print(f"Action returned: {action}")
