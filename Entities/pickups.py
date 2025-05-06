import pygame as pg
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from sfx import pickup_sfx

def load_scaled_image(path, size):
    try:
        return pg.transform.scale(pg.image.load(path).convert_alpha(), size)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return pg.Surface(size)

class Pickups:
    def __init__(self, move_speed, effect, amount):
        """
        Initializes the pickups manager.
        
        Parameters:
          move_speed (float): The horizontal speed at which pickups move left.
          effect (str): 'increase' or 'decrease'; defines the effect on the player.
          amount (number): The base amount to adjust the player's stat upon pickup.
        """
        self.move_speed = move_speed
        self.effect = effect
        self.amount = amount

        # List that will contain each pickup dictionary.
        self.pickup_list = []

        # Load the pickup asset (for example, a pizza boost image).
        self.asset = load_scaled_image("Assets/images/pizza_box.png", (75, 75))
        
        # Spawn timing, in milliseconds.
        self.spawn_timer = 15000  # Force immediate spawn (for debugging)
        self.spawn_interval = 15000  # Spawn every 2000 ms (2 seconds)
        self.can_spawn = True

    def spawn(self, count=1):
        """Spawn `count` new pickups off-screen."""
        for _ in range(count):
            x = SCREEN_WIDTH + 50  # Spawn just off the right side.
            y = random.randint(0, SCREEN_HEIGHT - 50)
            speed = self.move_speed  # Use the provided speed.
            self.pickup_list.append({
                "pos": [x, y],
                "speed": speed,
                "collected": False
            })

    def update(self, dt):
        """
        Update pickup positions and spawn new ones.
        
        dt: Delta time (in seconds) from the main loop.
        """
        self.spawn_timer -= dt * 1000  # Convert dt to milliseconds.
        if self.spawn_timer <= 0 and self.can_spawn:
            self.spawn_timer += self.spawn_interval
            self.spawn(1)
        
        for pickup in self.pickup_list:
            pickup["pos"][0] -= pickup["speed"]
        
        # Remove pickups that have gone off-screen.
        self.pickup_list = [p for p in self.pickup_list if (p["pos"][0] + 50) > 0]

    def draw(self, screen):
        """Draw each active pickup on the given screen."""
        for pickup in self.pickup_list:
            screen.blit(self.asset, pickup["pos"])

    def check_collision(self, player):
        """
        Checks collision between the player and pickups.
        On collision:
            - Plays a pickup sound effect.
            - If the pickup effect is "increase", increases the ship's boosting speed.
            - If the pickup effect is "decrease", decreases the player's health.
            - Removes the pickup upon collision.
        Assumes that the player has a 'rect' attribute and a 'boost_speed' attribute.
        """
        collided = []
        for pickup in self.pickup_list:
            pickup_rect = pg.Rect(pickup["pos"][0], pickup["pos"][1], 50, 50)
            if player.rect.colliderect(pickup_rect):
                collided.append(pickup)
                pickup_sfx.play()
                if self.effect == "increase":
                    # Increase the ship's boosting speed by self.amount.
                    # Make sure your Ship class has a boost_speed attribute.
                    player.boost_speed = getattr(player, "boost_speed", 0) + self.amount
                elif self.effect == "decrease":
                    player.health -= self.amount

        for p in collided:
            if p in self.pickup_list:
                self.pickup_list.remove(p)

    def set_amount(self, new_amount):
        """
        Updates the pickup's amount parameter dynamically.
        Use this method if you want to change how much the pickup affects the ship.
        """
        self.amount = new_amount
