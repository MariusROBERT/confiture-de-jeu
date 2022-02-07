import pygame

class patate():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/patate.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen

def spawn_patate(screen):
    patate = patate(screen)
    return patate