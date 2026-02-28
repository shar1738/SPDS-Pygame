import sys
import pygame as pg

from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Configuration for UI assets
UI_CONFIG = {
    "buttons": {
        "title": "Assets/images/main_menu/title.png",
        "start": "Assets/images/main_menu/start.png"
    }
}

class MainMenu:
    SPACING = 20
    UI_AREA_RATIO = 9.5 / 10

    def __init__(self, game_state, screen):
        self.game_state = game_state
        
        self.screen_width, self.screen_height = SCREEN_WIDTH, SCREEN_HEIGHT

        self.screen = screen

        self.bg_image_orig = pg.image.load("Assets/images/exterior/background.png").convert()
        self.button_images_orig = {
            name: pg.image.load(path).convert_alpha()
            for name, path in UI_CONFIG["buttons"].items()
        }

        self.update_layout()

    def update_layout(self):
        self.background = pg.transform.scale(
            self.bg_image_orig, (self.screen_width, self.screen_height)
        )

        ui_width = self.screen_width * self.UI_AREA_RATIO
        ui_height = self.screen_height * self.UI_AREA_RATIO
        container_x = (self.screen_width - ui_width) // 2
        container_y = (self.screen_height - ui_height) // 2

        n_buttons = len(self.button_images_orig)
        available_height = ui_height - self.SPACING * (n_buttons - 1)
        max_button_height = available_height / n_buttons
        max_button_width = ui_width

        scaled_images = {}
        for name, orig in self.button_images_orig.items():
            orig_w, orig_h = orig.get_size()
            scale_factor = min(1, max_button_width / orig_w, max_button_height / orig_h)
            new_size = (int(orig_w * scale_factor), int(orig_h * scale_factor))
            img = pg.transform.scale(orig, new_size)
            scaled_images[name] = img
        

        current_y = container_y
        self.buttons = {}
        for name, img in scaled_images.items():
            rect = img.get_rect(center=(self.screen_width // 2, int(current_y + img.get_height() // 2)))
            self.buttons[name] = {'image': img, 'rect': rect}
            current_y += img.get_height() + self.SPACING

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for btn in self.buttons.values():
            self.screen.blit(btn['image'], btn['rect'].topleft)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    self.update_layout()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    for name, btn in self.buttons.items():
                        if btn['rect'].collidepoint(mouse_pos):
                            print(f"{name.capitalize()} button clicked!")
                            if name == "start":
                                return "start"
            
            self.draw()
            pg.display.flip()