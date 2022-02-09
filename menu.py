import pygame, sys
from pygame.locals import *
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.

def main_menu(screen : pygame.display, clock):
    while True:
        screen.fill((70, 166, 0))
        pygame.font.init() 
        myfont = pygame.font.SysFont('Arial', 3000)
        textsurface = myfont.render('Some Text', True, (0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if event.type == pygame.quit():
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()