from constantes import HEIGHT, SIZE, WIDTH, TOURS
from constantes import FPS, HEIGHT, SIZE, WIDTH
import pygame
import sys
from personnages.pig import Pig
from personnages.Player import Player

<< << << < HEAD
== == == =
>>>>>> > 254837d1cf2e10b4c3cf2bb708358244f3883382


pygame.init()


screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


player = Player()
elements = {
    "player": [player],
    "pigs": [Pig() for i in range(4)],
    "zombies": [],
    "potatoes": [],
    "frites": [],
}


def clear_screen(screen: pygame.Surface):
    screen.fill((0, 0, 0))


def event_loop(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        sys.exit()
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        player.move(event)


def logic_loop():
    for key in elements.keys():
        for element in elements[key]:
            element.update(elements)


def draw_loop():
    for key in elements.keys():
        for element in elements[key]:
            element.update()


while 1:
    clear_screen(screen)
    for event in pygame.event.get():
        event_loop(event)
    logic_loop()
    display_loop()

    clock.tick(FPS)
    pygame.display.flip()
