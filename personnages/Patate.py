import pygame
import random
from constantes import TOURS, NB_ELEM_X, NB_ELEM_Y, CASE_SIZE


class Patate():
    def __init__(self):
        self.image = pygame.image.load("../images/patate.png")
        x=random.randint(0,NB_ELEM_X)
        y=random.randint(0,NB_ELEM_Y)
        pos=x*CASE_SIZE,y*CASE_SIZE
        while pos not in TOURS :
            x=random.randint(0,NB_ELEM_X)
            y=random.randint(0,NB_ELEM_Y)
            pos=x*CASE_SIZE,y*CASE_SIZE
        self.set_x(pos[0])
        self.set_y(pos[1])
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_image(self):
        return self.image
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y


    



