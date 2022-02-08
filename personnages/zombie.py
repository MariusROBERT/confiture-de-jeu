import string
from random import randrange
import pygame
from math import sqrt
from lib.lib import load_image
from .autre_element.health_bar import HealthBar
from constantes import WIDTH, HEIGHT, CASE_SIZE, TOURS, DEFAULT_HEALTH_BAR_SIZE


class Zombie:
    def __init__(self, speed: int = 1, name: string = "Zombie",
                 damage: int = 10, hp: int = 100, coords: tuple = None, size : tuple = (CASE_SIZE, CASE_SIZE)):
        self.__name = name
        self.__hp = hp
        self.__damage = damage
        self.__speed = speed
        self.__alive = True
        self.__sprite = load_image("./images/zombie.png", size)
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
                raise Exception("Error in Zombie.__init__() : side = " + str(side))
        else:
            self.__coords = coords
        
        #generating health bar for zombie
        center_x 			= coords[0] - size[0] / 2
        center_y 			= coords[1] - size[1] / 2
        health_bar_size 	= (size[0], DEFAULT_HEALTH_BAR_SIZE[1])
        health_bar_x 		= center_x - health_bar_size[0] / 2
        health_bar_y 		= center_y - health_bar_size[1] / 2
        health_bar_coords 	= (health_bar_x, health_bar_y)
        new_health_bar = HealthBar(health_bar_coords, size=health_bar_size, max=hp, value=hp-10, color=(255,30,255), auto_hide=True)
        

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
    def hp(self) -> int:
        return self.__hp

    @hp.setter
    def hp(self, hp) -> None:
        if hp <= 0:
            self.__hp = 0
        else:
            self.__hp = hp
        if self.__hp <= 0:
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
    def health(self) -> int:
        return self.hp

    @health.setter
    def health(self, health) -> None:
        self.hp = health

    def is_attacked(self, damage: int) -> None:
        self.hp -= damage

    def attack(self, target) -> None:
        target.is_attacked(self.__damage)

    def display(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.__coords)

    def update(self, elements: dict) -> None:
        direction = self.get_direction(self.get_target(elements["player"][0].coords))
        produit = abs(direction[0]) + abs(direction[1])
        if produit != 0:
            direction = (direction[0] / produit, direction[1] / produit)
        else:
            direction = (0, 0)
        self.coords = self.coords[0] + direction[0] * self.speed, self.coords[1] + direction[1] * self.speed

    def get_distance(self, coords: tuple[int, int]) -> float:
        return sqrt((self.coords[0] - coords[0]) ** 2 + (self.coords[1] - coords[1]) ** 2)

    def get_target(self, coords_player: tuple[int, int]) -> tuple[int, int]:
        distance = sqrt((coords_player[0] - self.coords[0]) ** 2 + (coords_player[1] - self.coords[1]) ** 2)
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

# def move(self, target) -> None:
# 	direction = self.get_direction(self.get_target(self.coords))
# 	self.coords = self.coords[0] + direction[0] * self.speed, self.coords[1] + direction[1] * self.speed
