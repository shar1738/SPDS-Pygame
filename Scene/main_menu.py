import pygame as pg
import sys

# Configuration for UI assets
UI_CONFIG = {
    "buttons": {
        "title": "Assets/images/ui/title.png",
        "start": "Assets/images/ui/start.png"
    }
}

class MainMenu:
    SPACING = 20  # spacing between buttons
    UI_AREA_RATIO = 9.5 / 10  # UI takes up one-third of the window

    def __init__(self):
        pg.init()
        # Detect system display resolution
        info = pg.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h

        # Create a resizable window at full display size
        self.screen = pg.display.set_mode(
            (self.screen_width, self.screen_height), pg.RESIZABLE
        )
        pg.display.set_caption("Main Menu")

        # Load original background and button images
        self.bg_image_orig = pg.image.load("Assets/images/background.png").convert()
        self.button_images_orig = {}
        for name, path in UI_CONFIG["buttons"].items():
            img = pg.image.load(path).convert_alpha()
            self.button_images_orig[name] = img

        # Initial layout
        self.update_layout()

    def update_layout(self):
        # Scale background to current window size
        self.background = pg.transform.scale(
            self.bg_image_orig, (self.screen_width, self.screen_height)
        )

        # Define UI container area (centered)
        ui_width = self.screen_width * self.UI_AREA_RATIO
        ui_height = self.screen_height * self.UI_AREA_RATIO
        container_x = (self.screen_width - ui_width) // 2
        container_y = (self.screen_height - ui_height) // 2

        # Prepare scaled button images to fit within UI container
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

        # Position buttons evenly within the container
        current_y = container_y
        self.buttons = {}
        for name, img in scaled_images.items():
            rect = img.get_rect(
                center=(
                    self.screen_width // 2,
                    int(current_y + img.get_height() // 2)
                )
            )
            self.buttons[name] = {'image': img, 'rect': rect}
            current_y += img.get_height() + self.SPACING

    def draw(self):
        # Draw background then buttons
        self.screen.blit(self.background, (0, 0))
        for btn in self.buttons.values():
            self.screen.blit(btn['image'], btn['rect'].topleft)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.VIDEORESIZE:
                    # Update window size and re-layout
                    self.screen_width, self.screen_height = event.w, event.h
                    self.screen = pg.display.set_mode(
                        (self.screen_width, self.screen_height), pg.RESIZABLE
                    )
                    self.update_layout()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    for name, btn in self.buttons.items():
                        if btn['rect'].collidepoint(mouse_pos):
                            print(f"{name.capitalize()} button clicked!")
                            return name

            self.draw()
            pg.display.flip()

if __name__ == "__main__":
    menu = MainMenu()
    action = menu.run()
    print(f"Action returned: {action}")