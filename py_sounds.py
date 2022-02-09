import pygame
from personnages.autre_element.fx_manager import DAMAGE_EVENT
from constantes import DATAPACK

pygame.init()

def get_sound(sound_name: str) -> pygame.mixer.Sound:
    try:
        sound = pygame.mixer.Sound(base_path_sounds + sound_name + ".ogg")
    except FileNotFoundError:
        try:
            sound = pygame.mixer.Sound(base_path_sounds + sound_name + ".wav")
        except FileNotFoundError:
            return None
    return sound

base_path_sounds = "./datapacks/" + DATAPACK + "/sounds/"
# EVENT DE 10 A 20 reservés
COLLECT_POTATOE = pygame.USEREVENT + 10
collect_sound = get_sound("collect")

DEAD_ZOMBIE = pygame.USEREVENT + 11
dead_sound = get_sound("dead_zombie")

FEEDED = pygame.USEREVENT + 12
feed_sound = get_sound("feeded")

OUT_OF_FOOD = pygame.USEREVENT + 13
out_of_food_sound = get_sound("out_of_food")

DIG = pygame.USEREVENT + 14
dig_sound = get_sound("dig")

hurt_sound = get_sound("hurt")

def sound_manager(pygame, event: pygame.event.Event):
    try:
        if event.type == COLLECT_POTATOE:
            collect_sound.play().set_volume(0.3)
        elif event.type == DEAD_ZOMBIE:
            dead_sound.play().set_volume(0.06)
        elif event.type == FEEDED:
            feed_sound.play().set_volume(0.3)
        elif event.type == OUT_OF_FOOD:
            out_of_food_sound.play().set_volume(0.3)
        elif event.type == DIG:
            dig_sound.play().set_volume(0.3)
        elif event.type == DAMAGE_EVENT:
            hurt_sound.play().set_volume(0.3)
            # print("DAMAGE_EVENT")

    except Exception as e:
        print(e)
