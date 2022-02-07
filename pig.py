import pygame
from pygame.locals import *

class Pig:
    def __init__(self, name : str = "Porcinet", hp : int =100):
        self.name = name
        self.hp = hp
    
    def draw(self, surface : pygame.Surface):
        self.rect = pygame.draw.rect(surface, (255, 0, 0), (0, 0, 20, 20))