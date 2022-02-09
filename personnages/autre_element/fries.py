import pygame
from constantes import CASE_SIZE, FPS, TOURS, WIDTH, HEIGHT, SHOW_HITBOX
from constantes import FRIES_SIZE, FRIES_DAMAGE, HITBOX_FRIES, FRIES_SPEED
from lib.lib import *


class Fries:
    def __init__(self, coords: tuple, movement_vector: tuple = (1, 0), size: tuple = FRIES_SIZE, intersection_box=None):
        self.coords = coords
        self.size = size
        self.__damage = FRIES_DAMAGE
        self.__intersection_box = intersection_box
        self.__movement_vector = movement_vector
        sprite = pygame.image.load("./images/frite.png")
        sprite = pygame.transform.scale(sprite, size)
        fries_angle = get_angle_between_vectors((0, 1), movement_vector)
        if movement_vector[0] < 0:
            fries_angle = 180 - fries_angle
        self.sprite, rect = rot_center(
            sprite, fries_angle, self.coords[0], self.coords[1])
        self.__hitbox = self.sprite.get_rect(center=rect.center)
        # self.sprite = rot_center(sprite, fries_angle)
        self.direction = []
        self.__alive = True
        self.angle = fries_angle

    @property
    def movement_vector(self) -> tuple:
        return self.__movement_vector

    @property
    def damage(self) -> int:
        return self.__damage

    @damage.setter
    def damage(self, value: int):
        self.__damage = value

    @property
    def alive(self) -> bool:
        return self.__alive

    @property
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.coords, HITBOX_FRIES)

    def kill(self):
        self.__alive = False

    def update(self, elements: dict):
        self.coords = self.coords[0] + \
            self.movement_vector[0], self.coords[1] + self.movement_vector[1]
        self.__alive = self.__alive and 0 < self.coords[0] < WIDTH and 0 < self.coords[1] < HEIGHT

    def display(self, screen):
        screen.blit(self.sprite,
                    (self.coords[0] - self.sprite.get_width() / 2, self.coords[1] - self.sprite.get_height() / 2))
        if SHOW_HITBOX:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
            if self.__intersection_box is not None:
                pygame.draw.rect(screen, (0, 255, 0),
                                 self.__intersection_box, 1)
