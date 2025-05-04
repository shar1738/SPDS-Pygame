
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
import sys

class SealantMinigame:
    def __init__(self, screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        pygame.init()

        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Seal the Hole")
        self.clock = pygame.time.Clock()

        # Load images (ensure these are in your working directory or provide full paths)
        self.background = pygame.Surface(screen_size)
        self.background.fill((30, 30, 30))

        self.hole_image = pygame.image.load("hole.png").convert_alpha()  # transparent PNG
        self.sealant_brush = pygame.image.load("sealant.png").convert_alpha()  # sealant dot

        # Get rect for hole placement and size
        self.hole_rect = self.hole_image.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

        # Surface to accumulate sealant drawing
        self.sealant_surface = pygame.Surface(screen_size, pygame.SRCALPHA)

        # Store screen size
        self.screen_width, self.screen_height = screen_size

        self.mouse_down = False
        self.hole_filled = False
        self.threshold_fill_percent = 0.9
        self.font = pygame.font.SysFont(None, 48)

    def get_fill_percentage(self):
        """
        Compare how many visible hole pixels have been covered by sealant using alpha channel comparison.
        """
        hole_alpha = pygame.surfarray.pixels_alpha(self.hole_image)
        seal_alpha = pygame.surfarray.pixels_alpha(self.sealant_surface)

        filled = 0
        total = 0

        for y in range(self.hole_rect.height):
            for x in range(self.hole_rect.width):
                screen_x = self.hole_rect.left + x
                screen_y = self.hole_rect.top + y

                if 0 <= screen_x < self.screen_width and 0 <= screen_y < self.screen_height:
                    # Only check pixels where hole image is visible (alpha > 0)
                    if hole_alpha[x][y] > 0:
                        total += 1
                        if seal_alpha[screen_x][screen_y] > 0:
                            filled += 1

        return filled / total if total > 0 else 0

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False

            # Draw the hole image
            self.screen.blit(self.hole_image, self.hole_rect)

            # Draw accumulated sealant on top
            self.screen.blit(self.sealant_surface, (0, 0))

            # Handle brush painting
            if self.mouse_down and not self.hole_filled:
                mouse_pos = pygame.mouse.get_pos()
                if self.hole_rect.collidepoint(mouse_pos):
                    # Draw sealant image centered at mouse
                    brush_rect = self.sealant_brush.get_rect(center=mouse_pos)
                    self.sealant_surface.blit(self.sealant_brush, brush_rect)

            # Check fill status
            if not self.hole_filled:
                fill_pct = self.get_fill_percentage()
                if fill_pct >= self.threshold_fill_percent:
                    self.hole_filled = True
                    print("Hole sealed!")

            # Display win text
            if self.hole_filled:
                text = self.font.render("HOLE SEALED!", True, (0, 255, 0))
                self.screen.blit(text, (self.screen_width // 2 - 120, 100))

            pygame.display.flip()
            self.clock.tick(FPS)

