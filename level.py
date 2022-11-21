import pygame
from player import Player
from tile import Tile
from settings import *
import random


class Level:
    def __init__(self, surface):

        # level setup
        self.display_surface = surface
        self.platform_group = pygame.sprite.Group()
        self.world_shift = 0
        self.score = 0
        self.game_over = False

        # fade effect
        self.fade_counter = 0

        # import fonts
        self.font_small = pygame.font.Font('fonts/Pixeltype.ttf', 64)
        self.font_big = pygame.font.Font('fonts/Pixeltype.ttf', 100)

        # Background image
        self.bg_image = pygame.image.load('graphics/bg.png').convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (screen_width, screen_height))
        self.bg_scroll = 0

        # Create ground
        self.platform = Tile(0, screen_height - 32, screen_width)
        self.platform_group.add(self.platform)

        # Create player
        self.player = pygame.sprite.GroupSingle()
        player_sprite = Player((screen_width // 2, screen_height - 200), self.display_surface)
        self.player.add(player_sprite)

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y < 200 and direction_y < 0:
            self.world_shift = -direction_y
            player.rect.centery = 200
            self.bg_scroll -= direction_y // 2
            if self.bg_scroll > screen_height:
                self.bg_scroll = 0
        else:
            self.world_shift = 0

    def horizontal_movement(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > screen_width:
            player.rect.right = screen_width

    def vertical_movement(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.platform_group.sprites():
            if sprite.rect.colliderect(player.rect.x, player.rect.y, 80, 80):
                if player.rect.bottom < sprite.rect.centery:
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def draw_bg(self, screen):
        screen.blit(self.bg_image, (0, 0 + self.bg_scroll))
        screen.blit(self.bg_image, (0, -screen_height + self.bg_scroll))

    def run(self):

        if not self.game_over:
            # Generate platforms
            if len(self.platform_group) < max_platforms:
                p_w = random.randint(100, 150)
                p_x = random.randint(0, screen_width - p_w)
                p_y = self.platform.rect.y - random.randint(180, 240)
                self.platform = Tile(p_x, p_y, p_w)
                self.platform_group.add(self.platform)

            # level tiles
            self.platform_group.update(self.world_shift)
            self.platform_group.draw(self.display_surface)
            self.scroll_y()

            # player
            self.player.update()
            self.horizontal_movement()
            self.vertical_movement()
            self.player.draw(self.display_surface)

            # score
            self.display_score(f'SCORE: {int(self.score / 100)}', self.font_small, 'black', 10, 10)
            self.score += self.world_shift

            if self.player.sprite.rect.top > screen_height:
                self.game_over = True
        else:
            self.platform_group.draw(self.display_surface)
            if self.fade_counter < screen_width:
                self.fade_counter += 5
                for y in range(0, 6, 2):
                    pygame.draw.rect(self.display_surface,
                                     'black',
                                     (0, y * (screen_height / 6),
                                      self.fade_counter, screen_height / 6))
                    pygame.draw.rect(self.display_surface,
                                     'black',
                                     (screen_width - self.fade_counter, (y + 1) * (screen_height / 6),
                                      screen_width, screen_height / 6))

            if self.fade_counter >= screen_width:
                self.display_surface.fill('black')
                self.draw_text('GAME OVER!', self.font_big, 'white', 240, 300)
                self.draw_text(f'SCORE: {int(self.score / 100)}', self.font_big, 'white', 270, 380)
                self.draw_text('Press SPACE to play again', self.font_small, 'white', 160, 460)

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                # restart game
                self.game_over = False
                self.score = 0
                self.fade_counter = 0
                # reset platforms
                self.platform_group.empty()
                # reposition player
                self.player.sprite.rect.centery = 800
                # set ground
                self.platform = Tile(0, screen_height - 32, screen_width)
                self.platform_group.add(self.platform)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.display_surface.blit(img, (x, y))

    def display_score(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.display_surface.blit(img, (x, y))
