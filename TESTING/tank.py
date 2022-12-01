import pygame
 
class Tank:
    """A class to manage the tank."""
 
    def __init__(self, tw_game):
        """Initialize the tank and set its starting position."""
        self.screen = tw_game.screen
        self.settings = tw_game.settings
        self.screen_rect = tw_game.screen.get_rect()

        # Load the tank image and get its rect.
        self.image = pygame.image.load('images/tank1.png')
        self.image = pygame.transform.scale(self.image, (75,50))

        self.rect = self.image.get_rect()
        # Start each new tank at the bottom left of the screen.
        self.rect.bottomleft = self.screen_rect.bottomleft

        # Store a decimal value for the tank's horizontal position.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        # Movement flags
        self.move_left = False
        self.move_right = False

    def move(self):
        """Update the tank's position based on movement flags."""
        # Update the mtank's x value, not the rect. (down=left)
        if self.move_left and self.rect.left > 0:
            self.x -= self.settings.tank_speed
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.tank_speed

        # Update rect object from self.x.
        self.rect.y = self.y
        self.rect.x = self.x

    def blitme(self):
        """Draw the tank at its current location."""
        self.screen.blit(self.image, self.rect)
