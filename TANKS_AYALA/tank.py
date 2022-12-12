from explosion import *
from pygame.sprite import Sprite


class Tank(Sprite):
    """ The tank object """

    def __init__(self, position, Game):
        Sprite.__init__(self)
        self.image = load_image('tank.png', 'sprites', -1)
        self.image = pygame.transform.scale(self.image, (45, 30))
        self.rect = self.image.get_rect()
        self.ground = Game.ground
        self.position = position
        self.time_to_fire = 20
        self.damage = 0
        self.damaged = False

        if self.position == "left":
            self.rect.bottomleft = (71, 600 - self.ground[81])
        elif self.position == "right":
            self.rect.bottomleft = (671, 600 - self.ground[681])
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.base_image = self.image


    def stain_black(self, shell_x, shell_y):
        x = int(shell_x) - self.rect.left
        y = int(shell_y) - self.rect.top
        pixel_count = 0
        self.image.lock()
        for i in range(1, 20):
            for angles in range(0, 360, 6):
                pixel_x = int(x + math.sin(math.radians(angles)) * i)
                pixel_y = int(y + math.cos(math.radians(angles)) * i)
                if pixel_x > (self.rect.width - 1): continue
                if pixel_x < 0: continue
                if pixel_y > (self.rect.height - 1): continue
                if pixel_y < 0: continue
                color = self.image.get_at((pixel_x, pixel_y))
                if color != (255, 125, 255):
                    self.image.set_at((pixel_x, pixel_y),
                                      (int(color[0] * 0.6), int(color[1] * 0.6), int(color[2] * 0.6)))
                    pixel_count += 1
        self.image.unlock()
        self.damage += int(pixel_count / 10)
        self.damaged = True

class Gun(pygame.sprite.Sprite):
    image = None

    def __init__(self, position, Game):
        pygame.sprite.Sprite.__init__(self)
        if Gun.image is None:
            Gun.image = load_image('gun.png', 'sprites', -1)
        self.image = Gun.image
        self.rect = self.image.get_rect()
        self.position = position
        self.ground = Game.ground
        self.angle = 00
        self.powder = 40
        if self.position == "left":
            self.rect.center = (108, 584 - self.ground[80])
        elif self.position == "right":
            self.rect.center = (680, 584 - self.ground[680])
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.base_image = self.image

    def turn(self, adjustment):
        self.angle += adjustment
        if self.angle > 90:
            self.angle = 90
        elif self.angle < 0:
            self.angle = 0

        if self.position == "left":
            old_rect = self.rect.bottomleft
            self.image = pygame.transform.rotate(self.base_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = old_rect
        elif self.position == "right":
            old_rect = self.rect.bottomright
            self.image = pygame.transform.rotate(self.base_image, 0 - self.angle)
            self.rect = self.image.get_rect()
            self.rect.bottomright = old_rect


class Shell(pygame.sprite.Sprite):
    image = None

    def __init__(self, tank, ground):
        pygame.sprite.Sprite.__init__(self)
        if Shell.image is None:
            Shell.image = load_image('shell.png', 'sprites', -1)
        self.image = Shell.image
        self.rect = self.image.get_rect()
        self.from_tank = tank
        self.target = tank.enemy
        if tank.position == "left":
            self.rect.center = tank.gun.rect.topright
            self.speed_x = math.sin(math.radians(90 - tank.gun.angle)) * (float(tank.gun.powder + 5) / 9)
            self.speed_y = (0 - math.cos(math.radians(90 - tank.gun.angle))) * (float(tank.gun.powder + 5) / 9)
        elif tank.position == "right":
            self.rect.center = tank.gun.rect.topleft
            self.speed_x = (0 - math.sin(math.radians(90 - tank.gun.angle))) * (float(tank.gun.powder + 5) / 9)
            self.speed_y = (0 - math.cos(math.radians(90 - tank.gun.angle))) * (float(tank.gun.powder + 5) / 9)
        self.pos_x = self.rect.centerx
        self.pos_y = self.rect.centery
        self.weight = 55

    def update(self, Game):
        self.pos_x += self.speed_x
        if (self.pos_x >= 779) or (self.pos_x <= 21):
            Game.sprites.remove(self)
            Game.change_turn()
        self.pos_y += self.speed_y
        if (self.pos_y >= 590):
            Game.sprites.remove(self)
            Game.change_turn()
        self.rect.centerx, self.rect.centery = int(self.pos_x), int(self.pos_y)
        self.speed_y = gravity(self.speed_y, self.weight)

        for collide in pygame.sprite.spritecollide(self, Game.sprites, 0):
            if collide in (self.from_tank, self.target):
                if self.confirm_collision(collide):
                    self.explode(Game, collide)
                    break

        if int(self.pos_y) >= (598 - Game.ground[int(self.pos_x)]):
            self.explode(Game)

    def explode(self, Game, collide=None):
        if collide != None:
            collide.stain_black(self.pos_x, self.pos_y)
            Game.screen.blit(collide.image, collide.rect)
        explosion(int(self.pos_x), int(self.pos_y), Game)
        Game.sprites.remove(self)
        Game.change_turn()

    def confirm_collision(self, target):
        if target.rect.collidepoint(int(self.pos_x), int(self.pos_y)):
            adjusted_x = int(self.pos_x) - target.rect.left
            adjusted_y = int(self.pos_y) - target.rect.top
            if target.image.get_at((adjusted_x, adjusted_y)) != target.image.get_colorkey():
                return True
            else:
                return False
        else:
            return False
