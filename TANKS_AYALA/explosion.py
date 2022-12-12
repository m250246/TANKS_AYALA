import pygame, random, math, time
from pygame.locals import *
from background import update_screen
from load_save import *
from settings import *


def explosion(exp_x, exp_y, Game):
    Game.sound.play("explosion_ground")

    Game.screen.lock()
    for i in range(1, 17):
        for angles in range(0, 360, 3):
            x = int(exp_x + math.sin(math.radians(angles)) * i)
            y = int(exp_y + math.cos(math.radians(angles)) * i)
            if y > 590: y = 590
            if x <= 1:
                x = 0
            elif x >= 798:
                x = 799
            color = Game.screen.get_at((x, y))
            if color != (120, 80, 50, 255):
                Game.screen.set_at((x, y), (120, 80, 50))
                if (exp_x - x) == 0:
                    speed_x = (random.random() * 4) - 2
                else:
                    speed_x = (3 / (exp_x - x) * random.random())
                if (exp_y - y) == 0:
                    speed_y = (random.random() * 2) - 1.2
                else:
                    speed_y = (3 / (exp_y - y) * random.random() * 2) - 1
                if y >= (600 - Game.ground[x]):
                    Game.ground[x] = 599 - y

    Game.screen.unlock()

    for i in range(-15, -25, -1):
        Game.ground[exp_x + i - 1] = Game.ground[exp_x + i] + int(
            (Game.ground[exp_x + i - 1] - Game.ground[exp_x + i]) * 0.35)
    for i in range(15, 25):
        Game.ground[exp_x + i + 1] = Game.ground[exp_x + i] + int(
            (Game.ground[exp_x + i + 1] - Game.ground[exp_x + i]) * 0.35)

    Game.background = update_screen(Game)


def gravity(speed_y, weight):
    adjustment = weight / GRAVITY
    speed_y = speed_y + adjustment
    if speed_y > 8.0:
        speed_y = 8.0
    return speed_y
