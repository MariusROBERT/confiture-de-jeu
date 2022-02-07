import pygame
import random

from constantes import WIDTH, CASE_SIZE, HEIGHT, TOURS


class Patate():
    def __init__(self, x, y, screen):
        self.screen = screen
        self.image = pygame.image.load("../images/patate.png")
        self.x = x
        self.y = y
    
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

    



