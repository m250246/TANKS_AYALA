import os
import pygame
from pygame.locals import *

def load_image(imageN, path, colorKey=None):
    full = os.path.join("resources", str(path), imageN)
    image = pygame.image.load(full)
    if colorKey is not None:
        if colorKey == -1:
            colorKey = image.get_at((0,0))
        image.set_colorkey(colorKey, RLEACCEL)
    return image.convert()

def load_image_alpha(imageN, path):
    full = os.path.join("resources", str(path), imageN)
    image = pygame.image.load(full)
    return image

def load_sound(soundN):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    full = os.path.join("resources", "sound", soundN)
    sound = pygame.mixer.Sound(full)
    return sound

def load_music(soundN):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    full = os.path.join("resources", "sound", soundN)
    music = pygame.mixer.music.load(full)
    return music