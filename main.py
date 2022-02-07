from multiprocessing import Event
import pygame
import sys
from pig import Pig

pygame.init()

size = width, height = 320, 240

screen = pygame.display.set_mode(size)


def event_loop(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        sys.exit()

def update_loop():
    test_pig = Pig()
    test_pig.draw(screen)

while 1:
    
    for event in pygame.event.get():
        event_loop(event)
    update_loop()
    pygame.display.update()
