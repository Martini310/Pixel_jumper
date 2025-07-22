import sys
from os import walk
import pygame
from settings import *
from datetime import datetime
import json


def import_folder(path):

    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            if image.endswith('.png'):
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                image_surf = pygame.transform.scale(image_surf, (60, 60))
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


def highscores(score):
    if sys.platform == "emscripten":
        print("[Pygbag] Highscores are not available in browser mode.")
        # Return a default empty highscore list
        return [["N/A", 0] for _ in range(5)]
    try:
        with open("highscores.json", "r") as hs:
            scores = json.load(hs)
            scores_list = [[k, v] for k, v in scores.items()]
            scores_list.sort(key=lambda x: x[1], reverse=True)

            if len(scores_list) == 5:
                if score > scores_list[-1][1]:
                    scores_list[4] = [datetime.now().strftime("%d-%m-%y    %H:%M.%S"), score]
            else:
                scores_list.append([datetime.now().strftime("%d-%m-%y    %H:%M.%S"), score])

            scores_dict = {}
            for e in scores_list:
                scores_dict[e[0]] = e[1]

            with open("highscores.json", "w") as hs:
                hs.write(json.dumps(scores_dict))

            return sorted(scores_list, key=lambda x: x[1], reverse=True)
    except Exception as e:
        print(f"[Error] Could not read/write highscores.json: {e}")
        return [["N/A", 0] for _ in range(5)]
