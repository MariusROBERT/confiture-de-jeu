import string
from random import randrange
import pygame
from math import sqrt
from lib.lib import load_image

from constantes import SHOW_HITBOX, WIDTH, HEIGHT, CASE_SIZE, TOURS


class Zombie:
    def __init__(self, speed: int = 1, name: string = "Zombie",
                 damage: int = 10, hp: int = 100, coords: tuple = None):
        self.__name = name
        self.__health = hp
        self.__damage = damage
        self.__speed = speed
        self.__alive = True
        self.__size = (CASE_SIZE, CASE_SIZE)
        self.__sprite = load_image("./images/zombie.png", self.size)
        self.__hitbox_degats = self.sprite.get_rect()
        if coords is None:
            side = randrange(4)
            if side == 0:
                self.__coords = (randrange(0, WIDTH), 0)
            elif side == 1:
                self.__coords = (WIDTH - CASE_SIZE, randrange(0, HEIGHT))
            elif side == 2:
                self.__coords = (randrange(0, WIDTH), HEIGHT - CASE_SIZE)
            elif side == 3:
                self.__coords = (0, randrange(0, HEIGHT))
            else:
                raise Exception(
                    "Error in Zombie.__init__() : side = " + str(side))
        else:
            self.__coords = coords

    @property
    def damage(self) -> int:
        return self.__damage

    @damage.setter
    def damage(self, damage) -> None:
        self.__damage = damage

    @property
    def speed(self) -> int:
        return self.__speed

    @speed.setter
    def speed(self, speed) -> None:
        self.__speed = speed

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, hp) -> None:
        if hp <= 0:
            self.__health = 0
        else:
            self.__health = hp
        if self.__health <= 0:
            self.__alive = False

    @property
    def latest_vector(self) -> tuple[int, int]:
        return 1, 1  # Place holder

    @property
    def sprite(self) -> pygame.Surface:
        return self.__sprite

    @sprite.setter
    def sprite(self, sprite) -> None:
        self.__sprite = sprite

    @property
    def coords(self) -> tuple[int, int]:
        return self.__coords

    @coords.setter
    def coords(self, coords: tuple[int, int]) -> None:
        self.__coords = coords

    @property
    def alive(self) -> bool:
        return self.__alive

    @property
    def hitbox_degats(self) -> pygame.Rect:
        return pygame.Rect(self.coords, self.size)

    @property
    def size(self) -> tuple[int, int]:
        return self.__size

    def is_attacked(self, damage: int) -> None:
        self.health -= damage

    def attack(self, target) -> None:
        target.is_attacked(self.__damage)

    def get_distance(self, coords: tuple[int, int]) -> float:
        return sqrt((self.coords[0] - coords[0]) ** 2 + (self.coords[1] - coords[1]) ** 2)

    def get_target(self, coords_player: tuple[int, int]) -> tuple[int, int]:
        distance = sqrt((coords_player[0] - self.coords[0])
                        ** 2 + (coords_player[1] - self.coords[1]) ** 2)
        target = coords_player
        # KEEP COMMENT TO FOLLOW PLAYER ONLY
        # for pig in TOURS:
        # 	dist_temp = self.get_distance(pig)
        # 	if dist_temp < distance:
        # 		distance = dist_temp
        # 		target = pig
        return target

    def get_direction(self, target: tuple[int, int]) -> tuple[int, int]:
        return target[0] - self.coords[0], target[1] - self.coords[1]

    def get_direction_vector(self, target: tuple[int, int]) -> tuple[float, float]:
        return self.get_direction(target)[0] / self.get_distance(target), \
            self.get_direction(target)[1] / self.get_distance(target)

    def display(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.__coords)
        if SHOW_HITBOX:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox_degats, 1)

    def update(self, elements: dict) -> None:
        direction = self.get_direction(
            self.get_target(elements["player"][0].coords))
        produit = abs(direction[0]) + abs(direction[1])

        if self.hitbox_degats.collidelist([element.hitbox for element in elements["fries"]]) != -1:
            for i in elements["fries"]:
                if i.hitbox.colliderect(self.hitbox_degats):
                    self.is_attacked(self.__damage)
                    elements["fries"].remove(i)
        if produit != 0:
            direction = (direction[0] / produit, direction[1] / produit)
        else:
            direction = (0, 0)
        self.coords = self.coords[0] + direction[0] * \
            self.speed, self.coords[1] + direction[1] * self.speed
