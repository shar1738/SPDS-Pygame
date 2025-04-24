import pygame as pg 
from settings import S

class Asteroid:
    def __init__(self, image, start_x, start_y, speed):
        self.image = image
        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def spawn_asteroid(self):
        """Spawn a new asteroid on the right side of the screen."""
        start_x = S.SCREEN_WIDTH
        start_y = pg.rand.randint(0, S.SCREEN_HEIGHT - self.asteroid_image.get_height())  # Random Y position
        speed = pg.rand.randint(5, 10)  # Random speed
        asteroid = Asteroid(self.asteroid_image, start_x, start_y, speed)
        self.asteroids.append(asteroid)

    def update_asteroids(self):
        """Update asteroid positions and remove off-screen ones."""
        for asteroid in self.asteroids[:]:
            asteroid.update()
            if asteroid.rect.right < 0:  # Remove asteroids that are off-screen
                self.asteroids.remove(asteroid)

    def render_asteroids(self):
        """Render all asteroids."""
        for asteroid in self.asteroids:
            asteroid.render(self.screen)