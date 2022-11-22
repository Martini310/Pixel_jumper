import pygame
from settings import *
from random import choice


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.image.load('graphics/1.png')
        self.image = pygame.transform.scale(self.image, (width, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving_left = choice([True, False])
        self.platform_speed = 1

    def update(self, y_shift):
        # update platform's vertical position
        self.rect.y += y_shift

        # moving platforms
        if self.moving_left and self.rect.width < screen_width:
            self.rect.x -= self.platform_speed
            if self.rect.left <= 0:
                self.moving_left = False
        if not self.moving_left and self.rect.width < screen_width:
            self.rect.x += self.platform_speed
            if self.rect.right >= screen_width:
                self.moving_left = True

        # check if platform has gone off the screen
        if self.rect.top > screen_height:
            self.kill()
