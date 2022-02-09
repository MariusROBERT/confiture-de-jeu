import pygame

from constantes import DATAPACK

pygame.init()

base_path_sounds = "./datapacks/" + DATAPACK + "/sounds/"
# EVENT DE 10 A 20 reservés
COLLECT_POTATOE = pygame.USEREVENT + 10
try:
    collect_sound = pygame.mixer.Sound(base_path_sounds + "collect.ogg")
except FileNotFoundError:
    collect_sound = pygame.mixer.Sound(base_path_sounds + "collect.wav")

DEAD_ZOMBIE = pygame.USEREVENT + 11
try:
    dead_sound = pygame.mixer.Sound(base_path_sounds + "dead_zombie.wav")
except FileNotFoundError:
    dead_sound = pygame.mixer.Sound(base_path_sounds + "dead_zombie.ogg")

FEEDED = pygame.USEREVENT + 12
try:
    feed_sound = pygame.mixer.Sound(base_path_sounds + "feeded.wav")
except FileNotFoundError:
    feed_sound = pygame.mixer.Sound(base_path_sounds + "feeded.ogg")

OUT_OF_FOOD = pygame.USEREVENT + 13
try:
    out_of_food_sound = pygame.mixer.Sound(base_path_sounds + "out_of_food.wav")
except FileNotFoundError:
    out_of_food_sound = pygame.mixer.Sound(base_path_sounds + "out_of_food.ogg")

DIG = pygame.USEREVENT + 14
try:
    dig_sound = pygame.mixer.Sound(base_path_sounds + "dig.wav")
except FileNotFoundError:
    dig_sound = pygame.mixer.Sound(base_path_sounds + "dig.ogg")


def sound_manager(pygame, event: pygame.event.Event):
    try:
        if event.type == COLLECT_POTATOE:
            collect_sound.play().set_volume(0.3)
        if event.type == DEAD_ZOMBIE:
            dead_sound.play().set_volume(0.06)
        if event.type == FEEDED:
            feed_sound.play().set_volume(0.3)
        if event.type == OUT_OF_FOOD:
            out_of_food_sound.play().set_volume(0.3)
        if event.type == DIG:
            dig_sound.play().set_volume(0.3)

    except Exception as e:
        print(e)
