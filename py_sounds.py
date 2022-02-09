import pygame

from constantes import DATAPACK
pygame.init()

base_path_sounds = "./datapacks/"+DATAPACK+"/sounds/"
# EVENT DE 10 A 20 reservés
COLLECT_POTATOE = pygame.USEREVENT + 10
# collect_sound = pygame.mixer.Sound("sounds/collect.wav")
collect_sound = pygame.mixer.Sound(base_path_sounds+"grass1.ogg")


DEAD_ZOMBIE = pygame.USEREVENT + 11
dead_sound = pygame.mixer.Sound(base_path_sounds+"dead_zombie3.wav")

FEEDED = pygame.USEREVENT + 12
feed_sound = pygame.mixer.Sound(base_path_sounds+"feeded.wav")

OUT_OF_FOOD = pygame.USEREVENT + 13
out_of_food_sound = pygame.mixer.Sound(base_path_sounds+"out_of_food.wav")

DIG = pygame.USEREVENT + 14
# dig_sound = pygame.mixer.Sound("sounds/dig.wav")
dig_sound = pygame.mixer.Sound(base_path_sounds+"till1.ogg")


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
