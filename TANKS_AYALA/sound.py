import pygame, time
from load_save import load_sound


class Sound(object):
    """ Sound Mixer """
    def __init__(self):
        self.sounds = {}
        self.sounds["gun"] = load_sound('gun.ogg')
        self.sounds["gun"].set_volume(0.8)
        self.sounds["explosion_ground"] = load_sound('explosion_ground.ogg')
        self.sounds["explosion_tank"] = load_sound('explosion_tank.ogg')
        self.sounds["warning"] = load_sound('warning.ogg')
        self.sounds["warning"].set_volume(0.4)
        self.sounds["powder"] = load_sound('powder.ogg')
        self.sounds["powder"].set_volume(0.5)
        self.powder_sound_timer = time.time()

    def play(self, key):
        sound = self.sounds[key]
        if key != "powder":
            sound.play()
        else:
            if (time.time() - self.powder_sound_timer) > 0.55:
                self.powder_sound_timer = time.time()
                sound.play()
