import pygame
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, path):
        super().__init__()

        self.display_surface = surface
        self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
        self.jump_sound.set_volume(2)

        # player animation variables
        self.character_path = path
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.1

        # Player image
        self.image = self.animations['idle'][self.frame_index]
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(midbottom=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 1
        self.jump_speed = -30

        # player status
        self.status = 'idle'
        self.on_ground = False
        self.on_ceiling = False
        self.facing_right = True

    def import_character_assets(self):
        self.animations = {'idle': [], 'idle2': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = self.character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        # flipping image
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y <= -1:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
