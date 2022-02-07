from multiprocessing import Event
import pygame
import sys
from pig import Pig

from constantes import HEIGHT, SIZE, WIDTH


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
            elements.append(Pig())
            

def draw_loop():
    for element in elements:
        element.draw(screen)
    
    

while 1:
    clear_screen(screen)
    for event in pygame.event.get():
        event_loop(event)
    logic_loop()
    draw_loop()
    pygame.display.update()
