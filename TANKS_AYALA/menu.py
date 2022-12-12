import pygame, os, time
from settings import *
from load_save import load_image


class Menu:

    def __init__(self, Game):
        # Import screen, game_started value, don't update screen
        self.screen = Game.screen
        self.game_started = Game.game_started
        self.update_screen = False

        # RECTANGLES sizes for menu boxes for each screen
        # 1st SCREEN
        self.new_game_rect = pygame.Rect(100, 200, 250, 50)
        self.quit_rect = pygame.Rect(450, 200, 250, 50)
        # 2nd SCREEN
        self.player1_rect = pygame.Rect(150, 250, 200, 50)
        self.player2_rect = pygame.Rect(450, 250, 200, 50)
        # 3rd SCREEN
        self.easy_rect = pygame.Rect(300, 200, 200, 50)
        self.medium_rect = pygame.Rect(300, 350, 200, 50)
        self.hard_rect = pygame.Rect(300, 500, 200, 50)
        # IDK
        self.update_buttons_rect = pygame.Rect(0, 150, 800, 400)

        # VALUES FOR THE SELECTED MENU SETTINGS (START AT NONE)
        self.new_game_selected = False
        self.players_selected = False
        self.difficulty_selected = False

        # FONT SETTINGS FOR THE MENU OPTIONS
        self.title_font = pygame.font.SysFont("Comic Sans", 50)
        self.font = pygame.font.SysFont("Comic Sans", 30)

    def draw(self):
        # DRAW MAIN MENU SCREEN: 1ST SCREEN: NEW GAME OR QUIT
        self.screen.fill((0, 0, 0))
        title = self.title_font.render(GAME_NAME, True, (0, 180, 180))
        self.screen.blit(title, ((self.screen.get_width() / 2) - (title.get_width() / 2), 80))
        # CHECK IF SELECTED: NEW GAME
        if self.new_game_selected:
            # CHECK IF SELECTED: PLAYER
            if self.players_selected:
                # DRAW DIFFICULTY LEVELS
                pygame.draw.rect(self.screen, (0, 180, 180), self.easy_rect, 3)
                pygame.draw.rect(self.screen, (0, 180, 180), self.medium_rect, 3)
                pygame.draw.rect(self.screen, (0, 180, 180), self.hard_rect, 3)
                text = self.font.render("Easy", True, (0, 200, 0))
                self.screen.blit(text, (self.easy_rect.centerx - (text.get_width() / 2),
                                        self.easy_rect.centery - (text.get_height() / 2)))
                text = self.font.render("Medium", True, (0, 200, 0))
                self.screen.blit(text, (self.medium_rect.centerx - (text.get_width() / 2),
                                        self.medium_rect.centery - (text.get_height() / 2)))
                text = self.font.render("Hard", True, (0, 200, 0))
                self.screen.blit(text, (self.hard_rect.centerx - (text.get_width() / 2),
                                        self.hard_rect.centery - (text.get_height() / 2)))
            else:
                # IF PLAYER 1/2 NOT SELECTED: DRAW PLAYER OPTIONS 1 OR 2
                pygame.draw.rect(self.screen, (180, 180, 0), self.player1_rect, 3)
                pygame.draw.rect(self.screen, (180, 180, 0), self.player2_rect, 3)
                text = self.font.render("1 player", True, (0, 200, 0))
                self.screen.blit(text, (self.player1_rect.centerx - (text.get_width() / 2),
                                        self.player1_rect.centery - (text.get_height() / 2)))
                text = self.font.render("2 players", True, (0, 200, 0))
                self.screen.blit(text, (self.player2_rect.centerx - (text.get_width() / 2),
                                        self.player2_rect.centery - (text.get_height() / 2)))
        else:
            # IF NO GAME OPTION SELECTED, DRAW THE GAME/QUIT OPTIONS
            pygame.draw.rect(self.screen, (180, 180, 0), self.new_game_rect, 3)
            pygame.draw.rect(self.screen, (180, 180, 0), self.quit_rect, 3)
            if self.game_started:
                text = self.font.render("Return to game", True, (0, 200, 0))
            else:
                text = self.font.render("New game", True, (0, 200, 0))
            self.screen.blit(text, (
                self.new_game_rect.centerx - (text.get_width() / 2),
                self.new_game_rect.centery - (text.get_height() / 2)))
            text = self.font.render("Quit", True, (0, 200, 0))
            self.screen.blit(text, (
                self.quit_rect.centerx - (text.get_width() / 2), self.quit_rect.centery - (text.get_height() / 2)))
            instruction = self.font.render("INSTRUCTIONS:", True, (255, 20, 0))
            self.screen.blit(instruction, (50, 300))
            instruction = self.font.render("- Use MOUSE on screen for Angle, Power, and Fire", True, (255, 20, 0))
            self.screen.blit(instruction, (50, 350))
            instruction = self.font.render("                OR", True, (255, 20, 0))
            self.screen.blit(instruction, (50, 400))
            instruction = self.font.render("- Use LEFT + RIGHT for Angle", True, (255, 20, 0))
            self.screen.blit(instruction, (50, 450))
            instruction = self.font.render("- Use UP + DOWN for Power", True, (255, 20, 0))
            self.screen.blit(instruction, (50, 500))
            instruction = self.font.render("- Use SPACEBAR to Fire", True, (255, 20, 0))
            self.screen.blit(instruction, (50, 550))

    def check_mouse_event(self, Game, pos):
        # START OF THE GAME : select NEW GAME OR QUIT
        if not self.new_game_selected:
            if self.new_game_rect.collidepoint(pos):
                self.new_game_selected = True
                self.update_screen = True
            elif self.quit_rect.collidepoint(pos):
                Game.state = STATE_QUIT
        # 2nd SCREEN PLAYERS: select 1 OR 2 PLAYERS
        else:
            if not self.players_selected:
                # CHECK IF MOUSE COLLIDES IN PLAYER1 BOX
                if self.player1_rect.collidepoint(pos):
                    self.players_selected = True
                    Game.number_players = 1
                    self.update_screen = True
                # CHECK IF MOUSE COLLIDES IN PLAYER2 BOX
                elif self.player2_rect.collidepoint(pos):
                    self.players_selected = True
                    Game.number_players = 2
                    self.update_screen = True
            # 3rd SCREEN DIFFICULTY: select 1, 2, OR 3 (PRIV, CAPT, COL)
            else:
                if not self.difficulty_selected:
                    if self.easy_rect.collidepoint(pos):
                        self.difficulty_selected = True
                        Game.difficulty = 1
                        Game.start_game = True
                    elif self.medium_rect.collidepoint(pos):
                        self.difficulty_selected = True
                        Game.difficulty = 2
                        Game.start_game = True
                    elif self.hard_rect.collidepoint(pos):
                        self.difficulty_selected = True
                        Game.difficulty = 3
                        Game.start_game = True
                else:
                    pass
        # ONCE GAME MENU SELECTED--> start_game == TRUEEEEEEEEEE
        if Game.start_game:
            self.new_game_selected = False
            self.players_selected = False
            self.difficulty_selected = False
