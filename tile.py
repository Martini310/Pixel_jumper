import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.image.load('graphics/1.png')
        self.image = pygame.transform.scale(self.image, (width, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, y_shift):
        # update platform's vertical position
        self.rect.y += y_shift

        # check if platform has gone off the screen
        if self.rect.top > screen_height:
            self.kill()
