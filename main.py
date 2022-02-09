from random import random
from re import M
from constantes import HEIGHT, PROB_ZOMBIE_SPAWN, SIZE, WIDTH, TOURS, CASE_SIZE
from constantes import FPS, HEIGHT, SIZE, WIDTH
from constantes import ZOMBIE_SPAWN
import pygame
import sys
from personnages.autre_element.fx_manager import Fx_manager
from personnages.pig import Pig
from personnages.golden_pig import GoldenPig
from personnages.player import Player
from personnages.zombie import Zombie
from personnages.terrain import Terrain
from personnages.autre_element.fries import Fries
import py_sounds
from menu import *
pygame.init()

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

player = Player()
# patate=Potatoe()
terrain = Terrain()

fx_manager = Fx_manager()

elements = {
    "terrain": [terrain],
    "pigs": [Pig(x, y) for (x, y) in TOURS],
    "zombies": [Zombie() for i in range(ZOMBIE_SPAWN)],
    "player": [player],
    "fries": [],
    "fx_manager": [fx_manager]

}

# elements["pigs"].append(GoldenPig(1000,200, size=(CASE_SIZE*2, CASE_SIZE*2)))

TICKEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TICKEVENT, 1000)

TICKEVENT500 = pygame.USEREVENT + 2
pygame.time.set_timer(TICKEVENT500, 370)

TICKEVENT100 = pygame.USEREVENT + 3
pygame.time.set_timer(TICKEVENT100, 100)

TICKEVENT10 = pygame.USEREVENT + 4
pygame.time.set_timer(TICKEVENT10, 40)

def clear_screen(screen: pygame.Surface):
    screen.fill((70, 166, 0))


def event_loop(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        sys.exit()
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        player.move(event, elements)

    py_sounds.sound_manager(pygame, event)  # Check si il faut jouer un son
    fx_manager.event_manager(event)

    # Every seconds
    if event.type == TICKEVENT:
        terrain.tick_update()
        for frite in elements["fries"]:
            if not frite.alive:
                elements["fries"].remove(frite)

        for zombie in elements["zombies"]:
            zombie.tick_update(elements)
            if not zombie.alive:
                elements["zombies"].remove(zombie)
        for pig in elements["pigs"]:
            pig.tick_update()

    # 500 miliseconds
    if event.type == TICKEVENT500:
        for pig in elements["pigs"]:
            new_fries = pig.get_fries()
            for fries in new_fries:
                elements["fries"].append(fries)

    # 100 miliseconds
    if event.type == TICKEVENT100:
        player.tick_update_100(elements)
        fx_manager.tick_update_100(elements)

        for pig in elements["pigs"]:
            pig.tick_update_100(elements)

        for zombie in elements["zombies"]:
            zombie.tick_update_100(elements)

        if random() < PROB_ZOMBIE_SPAWN:
            elements["zombies"].append(Zombie(speed=random() * 1.5 + 0.8))


def logic_loop():
    for key in elements.keys():
        for element in elements[key]:
            element.update(elements)


def display_loop():
    for key in elements.keys():
        for element in elements[key]:
            element.display(screen)

user_events = [
    TICKEVENT10,
    TICKEVENT100,
    TICKEVENT500,
    TICKEVENT
]

code = main_menu(screen, clock, user_events)
print(code)
if code == "Play":

    while 1:
        clear_screen(screen)
        for event in pygame.event.get():
            event_loop(event)
        logic_loop()
        display_loop()

        clock.tick(FPS)
        pygame.display.flip()
