from tkinter import N
from constantes import HEIGHT, SIZE, WIDTH, TOURS
from constantes import FPS, HEIGHT, SIZE, WIDTH
import pygame
import sys
from personnages.pig import Pig
from personnages.player import Player
from personnages.zombie import Zombie
from personnages.terrain import Terrain

pygame.init()


screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


player = Player()
# patate=Potatoe()
terrain = Terrain()

elements = {
    "terrain": [terrain],
    "player": [player],
    "pigs": [Pig(x, y) for (x, y) in TOURS],
    "zombies": [Zombie(coords=(0,0)) for i in range(1)],
    "frites": [],

}


TICKEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TICKEVENT, 1000)

TICKEVENT500 = pygame.USEREVENT + 2
pygame.time.set_timer(TICKEVENT500, 400 )

def clear_screen(screen: pygame.Surface):
    screen.fill((70, 166, 0))


def event_loop(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        sys.exit()
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        player.move(event, elements)

    # Every seconds
    if event.type == TICKEVENT:
        terrain.tick_update()
        for pig in elements["pigs"]:
            pig.tick_update()
    if event.type == TICKEVENT500:
        for pig in elements["pigs"]:
            new_fries = pig.get_fries()
            if new_fries is not None:
                elements["frites"].append(new_fries)
                
def logic_loop():
    for key in elements.keys():
        for element in elements[key]:
            element.update(elements)
        

def display_loop():
    for key in elements.keys():
        for element in elements[key]:
            element.display(screen)


while 1:
    clear_screen(screen)
    for event in pygame.event.get():
        event_loop(event)
    logic_loop()
    display_loop()

    clock.tick(FPS)
    pygame.display.flip()
