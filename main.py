from multiprocessing import Event
import pygame
import sys
from personnages.pig import Pig

from constantes import HEIGHT, SIZE, WIDTH, TOURS


pygame.init()


screen = pygame.display.set_mode(SIZE)
elements = []

def clear_screen(screen: pygame.Surface):
    screen.fill((0, 0, 0))

def event_loop(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        sys.exit()

def logic_loop():
    if len(elements) == 0:
        for i in range(4):
            elements.append(Pig(TOURS[i][0], TOURS[i][1]))
            

def display_loop():
    for element in elements:
        element.display(screen)
    
    

while 1:
    clear_screen(screen)
    for event in pygame.event.get():
        event_loop(event)
    logic_loop()
    display_loop()
    pygame.display.update()
