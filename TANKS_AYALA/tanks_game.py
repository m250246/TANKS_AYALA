from menu import Menu
from background import *
from tank import *
from control_panel import Control_panel
from sound import Sound
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0, COLOR_DEPTH)
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.timer = time.time() - 5
        self.game_started = False
        self.menu = Menu(self)
        self.sound = Sound()
        self.sprites = pygame.sprite.OrderedUpdates()
        self.font = pygame.font.SysFont('Comic Sans', 28)
        self.initialize_game()

    def main_loop(self):
        # WHERE TO STARTTTTTTT
        while True:
            self.clock.tick(FRAME_SPEED)
            if FULL_SCREEN == False:
                pygame.display.set_caption(GAME_NAME)

            rectlist = []
            if self.state == STATE_MENU:
                self.eventCheckMenu()

            elif self.state == STATE_INTRO:
                self.play_intro()

            elif self.state == STATE_DAMAGE:
                rectlist = self.draw_update_ground()
                if ((time.time() - self.timer) > 4) and self.check_damage:
                    self.check_damage = False
                    self.timer = time.time()
                    defeated_tank = self.show_damage()
                    if defeated_tank != None:
                        self.timer = time.time()
                        exploded = False
                        showing_score = False
                elif ((time.time() - self.timer) > 5) and (self.check_damage == False):
                    self.state = STATE_GAME
                self.eventCheckWaiting()

            elif self.state == STATE_GAME:
                rectlist = self.draw_update_ground()
                if ((time.time() - self.timer) > 5) and (self.shell_fired == False):
                    self.control_panel.update(self)
                    rectlist.append(self.panel_rect)
                self.eventCheckGame()

            elif self.state == STATE_END:
                if not showing_score:
                    if (time.time() - self.timer) > 8:
                        showing_score = True
                        self.show_score()
                        self.timer = time.time()
                    if not exploded:
                        explosion_timer = time.time()
                        exploded = True
                        self.sound.play("explosion_tank")

                    if ((time.time() - explosion_timer) > 0.5) and (exploded == True):
                        explosion_timer = time.time()
                else:
                    if (time.time() - self.timer) > 7:
                        self.start_new_game()
                rectlist = self.draw_update_ground()
                self.eventCheckWaiting()

            else:
                pygame.quit()
                exit(0)
            pygame.display.update(rectlist)
            self.sprites.clear(self.screen, self.background)

    def draw_update_ground(self):
        if (time.time() - self.update_ground_timer) > 0.5:
            self.background = update_screen(self)
        self.sprites.update(self)
        rectlist = self.sprites.draw(self.screen)
        if (time.time() - self.update_ground_timer) > 0.5:
            rectlist.append(self.ground_rect)
            self.update_ground_timer = time.time()
        return rectlist

    def eventCheckMenu(self):
        """ Check input in the menu """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.state = STATE_QUIT
                break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.menu.new_game_selected:
                        if self.menu.players_selected:
                            self.menu.players_selected = False
                            self.menu.update_screen = True
                            break
                        else:
                            self.menu.new_game_selected = False
                            self.menu.update_screen = True
                            break
                    else:
                        if self.game_started:
                            self.state = STATE_GAME
                            self.background = update_screen(self)
                            pygame.display.update()
                            self.menu.new_game_selected = False
                            self.menu.players_selected = False
                            break
                        else:
                            self.state = STATE_QUIT
                            break

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == LEFT_BUTTON:
                    self.menu.check_mouse_event(self, event.pos)

        if self.start_game:
            self.score = [0, 0]
            self.start_new_game()
            return

        if self.menu.update_screen:
            self.menu.draw()
            self.menu.update_screen = False
            pygame.display.update()

    def eventCheckGame(self):
        """ Check input in the game """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.state = STATE_QUIT
                break
            elif (event.type == KEYDOWN) and (self.shell_fired == False):
                if event.key == K_ESCAPE:
                    self.state = STATE_MENU
                    self.menu.draw()
                    pygame.display.update()
                    self.background = self.screen.copy()
                    break
            if ((time.time() - self.timer) > 5) and (self.shell_fired == False):
                self.control_panel.check_type_event(self, event)

    def eventCheckWaiting(self):
        """ Check input while waiting, showing damage, ending, etc. """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.state = STATE_QUIT
                break

    def start_new_game(self):
        self.sprites.empty()
        self.start_game = False
        self.game_started = True
        self.check_damage = False
        self.update_ground_timer = time.time()
        self.turn = "left"
        if self.number_players == 1:
            self.player1 = "Player"
            self.player2 = "CPU"
        else:
            self.player1 = "Player"
            self.player2 = "Player"

        self.ground, self.max_height = new_ground()
        self.ground_rect = pygame.Rect(0, 549 - self.max_height, 800, self.max_height + 50)

        self.tanks = []
        self.guns = []
        Tank_left = Tank("left", self)
        Gun_left = Gun("left", self)
        Tank_left.gun = Gun_left
        self.tanks.append(Tank_left)
        self.guns.append(Gun_left)
        Tank_right = Tank("right", self)
        Gun_right = Gun("right", self)
        Tank_right.gun = Gun_right
        self.tanks.append(Tank_right)
        self.guns.append(Gun_right)
        self.sprites.add(self.tanks)
        self.sprites.add(self.guns)
        self.shell_fired = False
        Tank_right.enemy = Tank_left
        Tank_left.enemy = Tank_right

        self.background = update_screen(self)

        pygame.display.update()

        self.control_panel = Control_panel()
        self.panel_rect = pygame.Rect(0, 0, 800, 180)
        self.state = STATE_INTRO

    def change_turn(self):
        for tank in self.tanks:
            tank.time_to_fire = int(((float(100 - tank.damage) / 100) * 20))
        self.state = STATE_DAMAGE
        self.check_damage = True
        if self.turn == "left":
            self.turn = "right"
        else:
            self.turn = "left"
        self.shell_fired = False
        self.control_panel.display = True
        self.timer = time.time()

    def initialize_game(self):
        self.start_game = False
        self.game_started = False
        self.state = STATE_MENU
        self.menu.draw()
        pygame.display.update()
        self.background = self.screen.copy()

    def show_damage(self):
        show_damage = False
        for tank in self.tanks:
            if tank.damaged == True:
                if tank.damage >= 100:
                    self.state = STATE_END
                    if tank.position == "left":
                        self.score[1] += 1
                    else:
                        self.score[0] += 1
                    return tank
                show_damage = True
                tank.damaged = False
                damage = self.font.render(str(tank.damage) + "% DAMAGED", True, (0, 0, 0))
                if tank.position == "left":
                    self.screen.blit(damage, (15, 550))
                    self.background.blit(damage, (15, 550))
                elif tank.position == "right":
                    self.screen.blit(damage, (615, 550))
                    self.background.blit(damage, (615, 550))

        if not show_damage:
            return None
        pygame.display.update()
        self.sound.play("warning")
        return None

    def show_score(self):
        draw_ground(self)
        score1 = self.font.render("PLAYER 1: " + str(self.score[0]), True, (0, 0, 0))
        score2 = self.font.render("PLAYER 2: " + str(self.score[1]), True, (0, 0, 0))
        self.screen.blit(score1, (110, 550))
        self.screen.blit(score2, (550, 550))
        pygame.display.update()
        self.background = self.screen.copy()

    def play_intro(self):
        self.state = STATE_GAME

if __name__ == "__main__":
    artillery = Game()
    artillery.main_loop()
