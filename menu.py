import pygame
from player import Player
from settings import *


class Menu:
    def __init__(self, surface):

        self.display_surface = surface

        # Fonts
        self.font_big = pygame.font.Font('fonts/Pixeltype.ttf', 100)
        self.font_small = pygame.font.Font('fonts/Pixeltype.ttf', 60)

        # Green Player
        self.player_1 = pygame.sprite.GroupSingle()
        player_sprite = Player((screen_width // 3, 500), self.display_surface, 'graphics/player/')
        self.player_1.add(player_sprite)

        # Pink Player
        self.player_2 = pygame.sprite.GroupSingle()
        player_sprite = Player((screen_width // 1.5, 500), self.display_surface, 'graphics/player_pink/')
        self.player_2.add(player_sprite)

        self.left_player = None
        self.player_graph = 'graphics/player/'
        self.active = True

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, False, text_col)
        self.display_surface.blit(img, (x, y))

    def run(self):
        # Welcome text and instructions
        self.draw_text("Hello in PIXEL JUMPER!", self.font_big, 'white', 100, 100)
        self.draw_text("Select your player", self.font_small, 'white', 220, 220)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.active = False
        if keys[pygame.K_LEFT]:
            self.left_player = True
            self.draw_text("X", self.font_big, "white", 250, 350)
            self.draw_text("X", self.font_big, "black", 520, 350)
            self.player_graph = 'graphics/player/'
        if keys[pygame.K_RIGHT]:
            self.left_player = False
            self.draw_text("X", self.font_big, "black", 250, 350)
            self.draw_text("X", self.font_big, "white", 520, 350)
            self.player_graph = 'graphics/player_pink/'

        self.player_1.update()
        self.player_1.draw(self.display_surface)

        self.player_2.update()
        self.player_2.draw(self.display_surface)

        if self.left_player is not None:
            self.draw_text("Press Space to start game", self.font_small, "white", 170, 600)
