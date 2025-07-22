import pygame
from player import Player
from tile import Tile
from settings import *
import random
from support import set_scroll_speed, highscores

import pathlib, sys, os

BASE_DIR = pathlib.Path(__file__).parent
if sys.platform == "emscripten":          # działa w przeglądarce
    os.chdir(BASE_DIR)                    # ← aby względne ścieżki działały

def load_background_music(stem: str, volume=0.4):
    """
    Ładuje plik 'sounds/<stem>.ogg' ➜ fallback '.mp3' ➜ brak muzyki.
    Zwraca True, jeśli któryś format się wczytał.
    """
    snd_path = BASE_DIR / "sounds"
    for ext in (".ogg", ".mp3"):          # kolejne próby
        file = snd_path / f"{stem}{ext}"
        if file.exists():
            try:
                print(f'file {file}')
                pygame.mixer.music.load(str(file))
                pygame.mixer.music.set_volume(volume)
                return True
            except pygame.error:
                continue                  # dekoder w przeglądarce nie obsługuje
    print("⚠️  Muzyka w tle wyłączona – brak kompatybilnego formatu")
    return False

class Level:
    def __init__(self, surface):

        # level setup
        self.display_surface = surface
        self.platform_group = pygame.sprite.Group()
        self.world_shift = 0
        self.score = 0
        self.game_over = False
        self.highscores = None

        # Sounds
        # Load music but do not play it yet. Use .ogg for better browser compatibility.
        self.bg_music = pygame.mixer.Sound("sounds/music.ogg")
        self.bg_music.set_volume(0.4)
        self.music_started = False
        self.dead_sound = pygame.mixer.Sound("sounds/death.wav")
        self.end_game_sound = pygame.mixer.Sound("sounds/round_end.wav")
        self.end_game_sound.set_volume(0.4)

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
        self.platform = Tile(-70, screen_height - 32, screen_width + 140)
        self.platform.moving_left = None
        self.platform_group.add(self.platform)

        # Create player
        self.player_path = 'graphics/player/'
        self.player = pygame.sprite.GroupSingle()
        self.player_sprite = Player((screen_width // 2, screen_height - 200), self.display_surface, self.player_path)
        self.player.add(self.player_sprite)

    def start_music(self):
        if not self.music_started:
            self.bg_music.play(loops=-1)
            self.music_started = True

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y < 250 and direction_y < 0:
            self.world_shift = -direction_y
            player.rect.centery = 250
            self.bg_scroll -= direction_y // 2
            if self.bg_scroll > screen_height:
                self.bg_scroll = 0
        else:
            scroll = set_scroll_speed(int(self.score / 100))
            self.world_shift = scroll[0]
            self.bg_scroll += scroll[0]
            if self.bg_scroll > screen_height:
                self.bg_scroll = 0

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
            if self.score > 100:
                sprite.platform_speed = 2
            if sprite.rect.colliderect(player.rect.x, player.rect.y, 60, 70):
                if player.rect.bottom < sprite.rect.centery:
                    if player.direction.y >= 0:
                        # player stand on platform
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                        # player move with platform
                        if sprite.moving_left == True:
                            player.rect.x -= sprite.platform_speed
                        if sprite.moving_left == False:
                            player.rect.x += sprite.platform_speed

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def draw_bg(self, screen):
        screen.blit(self.bg_image, (0, 0 + self.bg_scroll))
        screen.blit(self.bg_image, (0, -screen_height + self.bg_scroll))

    def run(self):

        if not self.game_over:
            self.draw_bg(self.display_surface)
            # Generate platforms
            if len(self.platform_group) < max_platforms:
                p_w = random.randint(100, 160)
                p_x = random.randint(0, screen_width - p_w)
                p_y = self.platform.rect.y - random.randint(180, 230)
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

            # player fall off the screen
            if self.player.sprite.rect.top > screen_height:
                self.game_over = True
                self.highscores = highscores(int(self.score / 100))
                self.dead_sound.play()
        else:  # GAME OVER
            self.draw_bg(self.display_surface)
            self.platform_group.draw(self.display_surface)
            # Fade effect
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
            if self.fade_counter == 200:
                self.end_game_sound.play()
            # Credits
            if self.fade_counter >= screen_width:
                self.display_surface.fill('black')
                self.draw_text('GAME OVER!', self.font_big, 'white', 240, 100)
                self.draw_text(f'SCORE: {int(self.score / 100)}', self.font_big, 'white', 260, 180)
                self.draw_text('HIGHSCORES', self.font_small, 'white', 300, 310)
                self.draw_text(f'{"Pts".ljust(25)}{"Date".ljust(19)}Time', self.font_small, 'white', 120, 380)

                y = 430
                for score in self.highscores:
                    self.draw_text(f"{str(score[1]).ljust(22, '.')}{score[0]}", self.font_small, 'white', 100, y)
                    y += 50

                self.draw_text('Press R to play again', self.font_small, 'white', 200, 730)

            # Restart GAME
            if pygame.key.get_pressed()[pygame.K_r]:
                # restart game variables
                self.game_over = False
                self.score = 0
                self.fade_counter = 0
                # reset platforms
                self.platform_group.empty()
                # reposition player
                self.player.sprite.rect.centery = 800
                # set ground
                self.platform = Tile(-70, screen_height - 32, screen_width + 140)
                self.platform.moving_left = None
                self.platform_group.add(self.platform)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.display_surface.blit(img, (x, y))

    def display_score(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.display_surface.blit(img, (x, y))
