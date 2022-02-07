import pygame


class HealthBar:

    def __init__(self, coords : tuple, max : int = 100, value : int = 0, size : tuple = (100, 20)):
        self.coords = coords
        self.max = max
        self.value = value
        self.size = size
        self.main_rect = pygame.Rect(self.coords, (self.cords[0] + self.size[0], self.coords[1] + self.size[1]))
        
        
    def display(self, screen : pygame.Surface):
        screen.blit(self.main_rect, self.coords)