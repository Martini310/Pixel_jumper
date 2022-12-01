import sys
import pygame
from settings import *
from level import Level
from menu import Menu


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Jumper')
        self.clock = pygame.time.Clock()
        self.level = Level(self.screen)
        self.menu = Menu(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.menu.active:
                self.menu.run()
            else:
                self.level.player_sprite.character_path = self.menu.player_graph
                self.level.player_sprite.import_character_assets()
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
