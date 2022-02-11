import pygame
from managers.events_const import COLLECT_POTATOE, DEAD_ZOMBIE, DIG, FEEDED, OUT_OF_FOOD, PLAYER_DEAD_EVENT, CHANGE_NIGHT
from managers.fx_manager import DAMAGE_EVENT
from constantes import DATAPACK, DEBUG_MODE, NB_ELEM_X, NB_ELEM_Y, SIZE

pygame.init()

game_over_size = (100, 20)
#gameover_surface=pygame.Surface((NB_ELEM_X/2)-game_over_size[0], (NB_ELEM_Y/2)-game_over_size[1])
screen = pygame.display.set_mode(SIZE)


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
base_sound = get_sound("base")
base_sound_night = get_sound("base_night")
menu_sound = get_sound("menu")

i = 1


def sound_base(pygame, event: pygame.event.Event):
    global i
    menu_sound.stop()
    if i == 1:
        try:
            base_sound.play(-1).set_volume(0.3)
        except Exception as e:
            if DEBUG_MODE:
                print("{} : {}".format(event.type, e))
        i = 2
        if DEBUG_MODE:
            print("jour")
    if event.type == CHANGE_NIGHT:
        if i == 2:
            try:
                base_sound.stop()
            except Exception as e:
                if DEBUG_MODE:
                    print("{} : {}".format(event.type, e))
            try:
                base_sound_night.play().set_volume(0.3)
            except Exception as e:
                if DEBUG_MODE:
                    print("{} : {}".format(event.type, e))
            i += 1
            if DEBUG_MODE:
                print("night if")
        else:
            base_sound_night.stop()
            base_sound.play(-1).set_volume(0.3)
            i = 2
            if DEBUG_MODE:
                print("night else")


def sound_menu(pygame):
    menu_sound.play(-1)


def sound_manager(pygame, event: pygame.event.Event):
    try:
        if event.type == COLLECT_POTATOE:
            collect_sound.play().set_volume(0.4)
        elif event.type == DEAD_ZOMBIE:
            dead_sound.play().set_volume(0.09)
        elif event.type == FEEDED:
            feed_sound.play().set_volume(0.4)
        elif event.type == OUT_OF_FOOD:
            out_of_food_sound.play().set_volume(0.4)
        elif event.type == DIG:
            dig_sound.play().set_volume(0.4)
        elif event.type == DAMAGE_EVENT:
            hurt_sound.play().set_volume(0.4)
            # print("DAMAGE_EVENT")
        # elif event.type == PLAYER_DEAD_EVENT:
         #   player_dead_sound.play().set_volume(2)

    except Exception as e:
        if DEBUG_MODE:
            print("{} : {}".format(event.type, e))
        pass


def player_dead(pygame, event: pygame.event.Event):
    player_dead_sound.play()
    font = pygame.font.SysFont("Arial", 20)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (100, 20))
