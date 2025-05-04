
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
import sys

class SealantMinigame:
    def __init__(self, screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        pygame.init()

        # Create the main screen window
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Seal the Hole")

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()

        # Hole position and size
        self.hole_pos = (400, 300)
        self.hole_radius = 50

        # Color of the sealant (e.g. brownish orange)
        self.sealant_color = (200, 100, 50)

        # Surface to draw sealant on (independent of the main screen)
        self.sealant_surface = pygame.Surface(screen_size, pygame.SRCALPHA)  # supports transparency

        # Track whether the mouse is pressed
        self.mouse_down = False

        # Flag to track whether the hole has been fully sealed
        self.hole_filled = False

        # How much of the hole must be filled to count as "sealed" (e.g. 90%)
        self.threshold_fill_percent = 0.9

        # Font used to display "HOLE SEALED!" message
        self.font = pygame.font.SysFont(None, 48)

        # Store screen dimensions for bounds checking
        self.screen_width, self.screen_height = screen_size

    def is_in_hole(self, pos):
        """
        Check if a point (pos) is within the circular hole.
        Uses the distance formula.
        """
        x, y = pos
        hx, hy = self.hole_pos
        return (x - hx) ** 2 + (y - hy) ** 2 <= self.hole_radius ** 2

    def get_fill_percentage(self):
        """
        Count the number of pixels inside the hole that have been covered with sealant.
        Return the percentage of the hole that is filled.
        """
        arr = pygame.surfarray.pixels_alpha(self.sealant_surface)  # Get alpha channel (transparency)
        filled = 0
        total = 0
        hx, hy = self.hole_pos

        # Loop over a square bounding box around the hole
        for y in range(hy - self.hole_radius, hy + self.hole_radius):
            for x in range(hx - self.hole_radius, hx + self.hole_radius):
                # Make sure we stay inside screen bounds
                if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                    # Check if the point is inside the circle
                    if self.is_in_hole((x, y)):
                        total += 1
                        if arr[x][y] > 0:  # Alpha > 0 means sealant was drawn here
                            filled += 1

        # Return the ratio of filled to total hole pixels
        return filled / total if total > 0 else 0

    def run(self):
        """
        Main game loop: handles input, drawing, fill logic, and completion detection.
        """
        while True:
            # Fill screen with dark gray background
            self.screen.fill((30, 30, 30))

            # Handle events like quitting or mouse input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False

            # Draw the hole as a black circle on the main screen
            pygame.draw.circle(self.screen, (0, 0, 0), self.hole_pos, self.hole_radius)

            # Draw the sealant surface on top (this accumulates over time)
            self.screen.blit(self.sealant_surface, (0, 0))

            # If mouse is down and hole hasn't been sealed yet
            if self.mouse_down and not self.hole_filled:
                pos = pygame.mouse.get_pos()
                if self.is_in_hole(pos):
                    # Draw a small circle of sealant at the mouse position
                    pygame.draw.circle(self.sealant_surface, self.sealant_color, pos, 5)

            # If the hole hasn't been filled yet, check how much is filled
            if not self.hole_filled:
                fill_pct = self.get_fill_percentage()
                if fill_pct >= self.threshold_fill_percent:
                    self.hole_filled = True
                    print("Hole sealed!")  # Trigger your game logic here

            # If the hole has been filled, show a message on screen
            if self.hole_filled:
                text = self.font.render("HOLE SEALED!", True, (0, 255, 0))
                self.screen.blit(text, (300, 100))

            # Update the display and cap the frame rate at 60 FPS
            pygame.display.flip()
            self.clock.tick(FPS)
