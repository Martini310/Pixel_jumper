from os import walk
import pygame
from settings import *


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


def set_scroll_speed(score):
    if score > 175:
        return scroll_speed[175]
    elif score > 150:
        return scroll_speed[150]
    elif score > 125:
        return scroll_speed[125]
    elif score > 100:
        return scroll_speed[100]
    elif score > 75:
        return scroll_speed[75]
    elif score > 50:
        return scroll_speed[50]
    elif score > 20:
        return scroll_speed[20]
    else:
        return [0, 0]
