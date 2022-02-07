from operator import ne
import pygame
from pygame.locals import *

class Pig:
    def __init__(self, x : int, y : int, size = (80, 80)):
        self.coords = (x,y)
        self.image = pygame.image.load("images/pig.png")
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.health = 50
        self.nb_frames = 240
        self.__animation_frame = 1
    @property
    def health(self) -> int:
        return self.__health
    
    @health.setter
    def health(self, value : int) -> None:
        self.__health = value

    @property
    def aura_frame(self) -> int:
        if self.__animation_frame < 40:
            return 1
        elif self.__animation_frame < 80:
            return 2
        elif self.__animation_frame < 120:
            return 3
        elif self.__animation_frame < 160:
            return 2
        elif self.__animation_frame < 200:
            return 1
        else:
            return 1
    
    def next_frame(self) -> None:
        self.__animation_frame += 1
        if self.__animation_frame > self.nb_frames:
            self.__animation_frame = 1


    def feed(self, nourish_value : int = 20) -> None:
        self.health += 20
    
    
    def display(self, surface : pygame.Surface) -> None:
        
        #display aura
        aura_image = pygame.image.load("images/pig_aura/frame" + str(self.aura_frame) + ".png")
        surface.blit(aura_image, self.coords)
        
        surface.blit(self.image, self.coords)
        self.next_frame()