import pygame
from managers.events_const import COLLECT_POTATOE, DEAD_ZOMBIE, DIG, FEEDED, OUT_OF_FOOD, PLAYER_DEAD_EVENT
from managers.fx_manager import DAMAGE_EVENT
from constantes import DATAPACK, SHOW_HITBOX

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
collect_sound = get_sound("collect")
dead_sound = get_sound("dead_zombie")
feed_sound = get_sound("feeded")
out_of_food_sound = get_sound("out_of_food")
dig_sound = get_sound("dig")
hurt_sound = get_sound("hurt")
player_dead_sound = get_sound("player_dead")


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
        elif event.type == PLAYER_DEAD_EVENT:
            player_dead_sound.play().set_volume(3)

    except Exception as e:
        if SHOW_HITBOX:
            print("{} : {}".format(event.type, e))
        pass