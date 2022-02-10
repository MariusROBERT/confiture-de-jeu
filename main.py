from threading import Thread
import time
from datetime import datetime, timedelta
from random import random
from re import M
from constantes import PROB_ZOMBIE_SPAWN, SPAWN_DELAY, TOURS, POINTS_PER_ZOMBIE_HIT, POINTS_PER_ZOMBIE_DEAD
from constantes import FPS, HEIGHT, SIZE, WIDTH, CASE_SIZE
from constantes import ZOMBIE_SPAWN
import pygame

import sys





from managers.events_const import DAMAGED_ZOMBIE, DEAD_ZOMBIE
from multiprocessing import Process, Pool


pygame.init()

screen = pygame.display.set_mode(SIZE)
from menu import *
import managers.sound_manager as sound_manager
from personnages.terrain import Terrain
from managers.fx_manager import Fx_manager
from managers.night_manager import Night_manager
from personnages.pig import Pig
from personnages.golden_pig import GoldenPig
from personnages.player import Player, AutoPlayer
from personnages.zombie import Zombie
from personnages.autre_element.fries import Fries

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
elements = {}
counter = 0
score = 0
night_manager = None
score_surface = None
r_code = ""

TICKEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TICKEVENT, 1000)

FIREFRIE = pygame.USEREVENT + 2
pygame.time.set_timer(FIREFRIE, SPAWN_DELAY)

TICKEVENT100 = pygame.USEREVENT + 3
pygame.time.set_timer(TICKEVENT100, 100)

TICKEVENT50 = pygame.USEREVENT + 5
pygame.time.set_timer(TICKEVENT50, 50)

TICKEVENT10 = pygame.USEREVENT + 4
pygame.time.set_timer(TICKEVENT10, 5)

user_events = [
    TICKEVENT10,
    TICKEVENT100,
    TICKEVENT
]
# FPS STUFF


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def init_game():
    player = Player()
# patate=Potatoe()
    terrain = Terrain()

    fx_manager = Fx_manager()
    night_manager = Night_manager()

    elements = {
        "terrain": [terrain],
        "pigs": [Pig(x, y) for (x, y) in TOURS],
        "zombies": [Zombie() for i in range(ZOMBIE_SPAWN)],
        "player": [player],
        "fries": [],
        "fx_manager": [fx_manager]
    }
    score_surface = pygame.Surface((30, 20))

    # elements["pigs"].append(GoldenPig(1000,200, size=(CASE_SIZE*2, CASE_SIZE*2)))
    screen = pygame.display.set_mode(SIZE)
    return elements, night_manager, score_surface

#code = main_menu(screen, clock, user_events)
# ininiting all startup element
#elements = init_game()


def clear_screen(screen: pygame.Surface):
    screen.fill((70, 166, 0))


def add_score(points):
    global score_surface, score
    score += POINTS_PER_ZOMBIE_HIT
    score_surface = refresh_score("SCORE : {}".format(score))


def refresh_score(score):
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(score, True, (255, 255, 255))
    return text


def display_score(screen):
    screen.blit(score_surface, (650, 10))


def event_loop(event: pygame.event.Event, elements, night_manager, score_surface):
    player = elements["player"][0]
    terrain = elements["terrain"][0]
    fx_manager = elements["fx_manager"][0]

    if event.type == pygame.QUIT:
        sys.exit()
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        player.move(event, elements)

    sound_manager.sound_manager(pygame, event)  # Check si il faut jouer un son
    sound_manager.sound_base(pygame, event)
    fx_manager.event_manager(event, elements)
    terrain.event_manager(event, elements)

    # Every seconds
    if event.type == TICKEVENT:
        terrain.tick_update()
        night_manager.tick_update(elements)
        for frite in elements["fries"]:
            if not frite.alive:
                elements["fries"].remove(frite)

        for zombie in elements["zombies"]:
            zombie.tick_update(elements)
            if not zombie.alive:
                elements["zombies"].remove(zombie)
        for pig in elements["pigs"]:
            pig.tick_update()
        """
        if player.alive:
            global counter
            tt = datetime.fromtimestamp(counter)
            time = tt.strftime("%M:%S")
            global score_surface
            score_surface = refresh_score(time)
            counter += 1
        """
    if event.type == DAMAGED_ZOMBIE:
        # Update score when a zombie is hit
        add_score(POINTS_PER_ZOMBIE_HIT)

    if event.type == DEAD_ZOMBIE:
        # Update score when a zombie is dead
        add_score(POINTS_PER_ZOMBIE_DEAD)

    if event.type == FIREFRIE:
        for pig in elements["pigs"]:
            new_fries = pig.get_fries()
            for fries in new_fries:
                elements["fries"].append(fries)
    if event.type == TICKEVENT50:
        pass
    # 100 miliseconds
    if event.type == TICKEVENT100:
        player.tick_update_100(elements)
        fx_manager.tick_update_100(elements)
        
        for pig in elements["pigs"]:
            pig.tick_update_100(elements)

        for zombie in elements["zombies"]:
            zombie.tick_update_100(elements)

        if random() < night_manager.prob_zombie_spawn:
            elements["zombies"].append(
                Zombie(speed=night_manager.speed_zombies, size=night_manager.size_zombie))
        for frie in elements["fries"]:
            frie.tick_update_100(elements)

    if event.type == TICKEVENT50:
        fx_manager.tick_update_50(elements)
        terrain.tick_update_50(elements)


def logic_loop(elements):
    for key in elements.keys():
        for element in elements[key]:
            element.update(elements)


def display_loop(elements):
    for key in elements.keys():
        for element in elements[key]:
            if key != "fx_manager":
                element.display(screen)
            else:
                element.display(screen, elements)
    display_score(screen)
    screen.blit(update_fps(), (10, 0))


#worker_main_menu = Thread(target=main_menu)

# worker_main_menu.start()
elements, night_manager, score_surface = init_game()
# worker_main_menu.join()
r_code = main_menu()
if True:

    while 1:
        clear_screen(screen)
        for event in pygame.event.get():
            event_loop(event, elements, night_manager, score_surface)
        logic_loop(elements)
        display_loop(elements)

        clock.tick(FPS)
        pygame.display.flip()
