from os import walk
import pygame


def import_folder(path):

    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            if image.endswith('.png'):
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                image_surf = pygame.transform.scale(image_surf, (80, 80))
                surface_list.append(image_surf)

    return surface_list
