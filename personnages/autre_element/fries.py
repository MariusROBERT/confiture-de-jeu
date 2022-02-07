import pygame
from constantes import CASE_SIZE, FPS, TOURS, WIDTH, HEIGHT
from lib.lib import get_angle_between_vectors

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Fries:
    def __init__(self, coords : tuple, movement_vector : tuple = (1,0), size : tuple = (10,80)):
        self.coords = coords
        self.movement_vector = movement_vector
        sprite = pygame.image.load("./images/frite.png")
        sprite = pygame.transform.scale(sprite, size)
        fries_angle = get_angle_between_vectors((0,-1), movement_vector)
        self.sprite = pygame.transform.rotate(sprite, -fries_angle)
        #self.sprite = rot_center(sprite, fries_angle)
        
        self.speed = 300/FPS
        self.direction = []
        self.__alive = True

    
    
    def update(self, elements : dict):
        self.coords = self.coords[0] + self.movement_vector[0], self.coords[1] + self.movement_vector[1]
        self.__alive = self.__alive and self.coords[0] > 0 and self.coords[0] < WIDTH and self.coords[1] > 0 and self.coords[1] < HEIGHT
        
    def display(self, screen):
        screen.blit(self.sprite, self.coords)