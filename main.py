import pygame
import sys
from personnages.Player import Player
from pig import Pig

from constantes import HEIGHT, SIZE, WIDTH


pygame.init()


screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

elements = []
player = Player()

elements.append(player)


def clear_screen(screen: pygame.Surface):
    screen.fill((0, 0, 0))


def event_loop(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        sys.exit()
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        player.move(event)


def logic_loop():
    if len(elements) == 0:
        for i in range(4):
            elements.append(Pig())


def draw_loop():
    for element in elements:
        element.display(screen)


while 1:
    clear_screen(screen)
    for event in pygame.event.get():
        event_loop(event)
    logic_loop()
    draw_loop()

    clock.tick(60)
    pygame.display.flip()
