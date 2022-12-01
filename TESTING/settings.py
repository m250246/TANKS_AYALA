import pygame
class Settings:
    """A class to store all settings for Tank War."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.bg = pygame.image.load('images/background.png')
        self.rect = self.bg.get_rect()
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.bg = pygame.transform.scale(self.bg, (self.screen_width, self.screen_height))

        # Tank settings
        self.tank_speed = 1.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3