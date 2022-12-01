import pygame
from pygame.sprite import Sprite
 
class Bullet(Sprite):
    """A class to manage bullets fired from the tank"""

    def __init__(self, tw_game):
        """Create a bullet object at the tank's current position."""
        super().__init__()
        self.screen = tw_game.screen
        self.settings = tw_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_height,
            self.settings.bullet_width)
        self.rect.midright = tw_game.tank.rect.midright
        
        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.x += self.settings.bullet_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
