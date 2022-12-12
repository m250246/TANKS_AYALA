import pygame
import time
from pygame.locals import *
from tank import Shell
from background import update_screen
from settings import *
from tank import Tank


class Control_panel(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.display = True
        self.font = pygame.font.SysFont("Roboto", 36)
        # TIMER
        self.font_timer = pygame.font.SysFont("Roboto", 45)
        self.player_timer = time.time()
        self.button_timer = time.time()
        self.timer_rect = pygame.Rect(670, 80, 40, 30)

        # PLAYER
        self.player_rect = {"left": pygame.Rect(100, 22, 110, 34), "right": pygame.Rect(100, 22, 110, 34)}
        # ANGLE TURRET
        self.button_up_barrel_rect = pygame.Rect(195, 60, 34, 34)
        self.button_down_barrel_rect = pygame.Rect(70, 60, 34, 34)
        self.barrel_rect = pygame.Rect(122, 60, 66, 34)
        # POWER OF BULLET
        self.button_up_powder_rect = pygame.Rect(205, 94, 34, 34)
        self.button_down_powder_rect = pygame.Rect(60, 94, 34, 34)
        self.powder_rect = pygame.Rect(122, 94, 66, 34)
        # FIRE BUTTON
        self.button_fire_rect = pygame.Rect(660, 40, 60, 30)
        self.fire_rect = pygame.Rect(655, 35, 70, 35)

    def update(self, Game):
        # SET UP WHICH TANK'S TURN
        tanks = {}
        for tank in Game.tanks:
            tanks[tank.position] = tank
        tank = tanks[Game.turn]

        # ANGLE OF ATTACK
        text = self.font.render(f"Angle: {tank.gun.angle}", True, (138, 11, 17))
        self.screen.blit(text, (self.barrel_rect.centerx - (text.get_width() / 2),
                                self.barrel_rect.centery - (text.get_height() / 2) - 3))
        self.screen.blit(self.font.render("<", True, (138, 11, 17)), (self.button_down_barrel_rect.centerx,
                                                                      self.button_down_barrel_rect.top))
        self.screen.blit(self.font.render(">", True, (138, 11, 17)), (self.button_up_barrel_rect.centerx,
                                                                      self.button_up_barrel_rect.top))

        # POWER OF BULLET
        text = self.font.render(f"Power: {tank.gun.powder}", True, (138, 11, 17))
        self.screen.blit(text, (self.powder_rect.centerx - (text.get_width() / 2),
                                self.powder_rect.centery - (text.get_height() / 2) - 3))
        self.screen.blit(self.font.render("<", True, (138, 11, 17)), (self.button_down_powder_rect.centerx,
                                                                      self.button_down_powder_rect.top))
        self.screen.blit(self.font.render(">", True, (138, 11, 17)), (self.button_up_powder_rect.centerx,
                                                                      self.button_up_powder_rect.top))

        # FIRE BUTTON
        text = self.font.render("FIRE!", True, (138, 11, 17))
        self.screen.blit(text, (self.button_fire_rect.centerx - (text.get_width() / 2),
                                self.button_fire_rect.centery - (text.get_height() / 2) - 3))
        pygame.draw.rect(self.screen, (138, 11, 17), self.fire_rect, 2)

        # PLAYER OF TURN
        rect = self.player_rect[tank.position]
        self.screen.fill((0, 0, 0), rect)
        if tank.position == "left":
            text = self.font.render("Player 1", True, (205, 205, 205))
        else:
            text = self.font.render("Player 2", True, (205, 205, 205))
        self.screen.blit(text, (rect.centerx - (text.get_width() / 2), rect.centery - (text.get_height() / 2) - 2))

        # TIME LEFT
        seconds_past = time.time() - self.player_timer
        text_timer = self.font_timer.render(str(tank.time_to_fire), True, (30, 30, 30))
        if int(seconds_past) >= 1:
            self.player_timer = time.time()
            tank.time_to_fire -= 1
            if tank.time_to_fire == -1:
                tank.time_to_fire = 15
                fire_shell(self, Game, tank)
                return
        if tank.time_to_fire > 9:
            self.screen.blit(text_timer, self.timer_rect.topleft)
        else:
            self.screen.blit(text_timer, self.timer_rect.midtop)
        pygame.draw.rect(self.screen, (0, 0, 0), self.timer_rect, 2)

    def check_type_event(self, Game, event):
        button1, button2, button3 = pygame.mouse.get_pressed()
        if (button1, button2, button3) == (0, 0, 0):
            pygame.mixer.music.stop()
        pos = pygame.mouse.get_pos()
        for tank in Game.tanks:
            if (tank.position == Game.turn):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        tank.gun.turn(1)
                        return
                    elif event.key == pygame.K_LEFT:
                        tank.gun.turn(-1)
                        return
                    elif event.key == pygame.K_UP:
                        Game.sound.play("powder")
                        tank.gun.powder += 1
                        if tank.gun.powder > 99:
                            tank.gun.powder = 99
                        return
                    elif event.key == pygame.K_DOWN:
                        Game.sound.play("powder")
                        tank.gun.powder -= 1
                        if tank.gun.powder < 10:
                            tank.gun.powder = 10
                        return
                    pygame.mixer.music.stop()
                    if event.key == pygame.K_SPACE:
                        fire_shell(self, Game, tank)
                    break
                else:
                    if button1:
                        if (time.time() - self.button_timer) > 0.07:
                            self.button_timer = time.time()
                            if self.button_up_barrel_rect.collidepoint(pos):
                                tank.gun.turn(1)
                                return
                            elif self.button_down_barrel_rect.collidepoint(pos):
                                tank.gun.turn(-1)
                                return

                            if self.button_up_powder_rect.collidepoint(pos):
                                Game.sound.play("powder")
                                tank.gun.powder += 1
                                if tank.gun.powder > 99:
                                    tank.gun.powder = 99
                                return
                            elif self.button_down_powder_rect.collidepoint(pos):
                                Game.sound.play("powder")
                                tank.gun.powder -= 1
                                if tank.gun.powder < 10:
                                    tank.gun.powder = 10
                                return
                            pygame.mixer.music.stop()

                        if self.button_fire_rect.collidepoint(pos):
                            fire_shell(self, Game, tank)

                        break
                    else:
                        continue


def fire_shell(panel, Game, tank):
    pygame.mixer.music.stop()
    Game.sound.play("gun")
    Game.shell_fired = True
    panel.display = False
    Game.sprites.add(Shell(tank, Game.ground))
    Game.background = update_screen(Game)
    pygame.display.update()
