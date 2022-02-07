from multiprocessing import Event
import pygame
import sys

from constantes import SIZE


pygame.init()


screen = pygame.display.set_mode(SIZE)


def event_loop(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        sys.exit()


while 1:
    for event in pygame.event.get():
        event_loop(event)

    # pygame.display.flip()
