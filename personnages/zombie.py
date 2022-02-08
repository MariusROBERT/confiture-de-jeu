import string
from random import randrange
import pygame
from math import sqrt
from lib.lib import load_image
from .autre_element.health_bar import HealthBar
from constantes import WIDTH, HEIGHT, CASE_SIZE, TOURS, DEFAULT_HEALTH_BAR_SIZE
from lib.animated import Animated


from constantes import COLLIDBOX_SIZE, SHOW_HITBOX, SIZE_ZOMBIE, WIDTH, HEIGHT, CASE_SIZE, TOURS


class Zombie(Animated):
    def __init__(self, speed: int = 1, name: string = "Zombie",
                 damage: int = 10, hp: int = 100, coords: tuple = None, size : tuple = (CASE_SIZE, CASE_SIZE)):
        self.health_bar_size 	= (size[0], DEFAULT_HEALTH_BAR_SIZE[1])
        new_health_bar = HealthBar(
            (-1000,-1000),
            size=self.health_bar_size,
            max=hp,
            value=hp,
            color=(255,30,255),
            auto_hide=True)
        self.__health_bar = new_health_bar

        super().__init__("zombie", (SIZE_ZOMBIE, SIZE_ZOMBIE))

        self.__name = name
        self.__health = hp
        self.__damage = damage
        self.__speed = speed
        self.__alive = True
        self.__size = size

        self.current_animation = "walk"

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

        #generating health bar for zombie



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
            self.__alive = False
        else:
            self.__health = hp
        self.__health_bar.health = self.__health

    @property
    def latest_vector(self) -> tuple[int, int]:
        return 1, 1  # Place holder

    @property
    def coords(self) -> tuple[int, int]:
        return self.__coords

    @coords.setter
    def coords(self, coords: tuple[int, int]) -> None:
        self.__coords = coords
        center_x 			= coords[0] + self.size[0] / 2
        health_bar_x 		= center_x - self.health_bar_size[0] / 2
        health_bar_y 		= coords[1] - self.health_bar_size[1] - 5
        health_bar_coords 	= (health_bar_x, health_bar_y)
        self.__health_bar.move_to(health_bar_coords)

    @property
    def alive(self) -> bool:
        return self.__alive

    @property
    def hitbox_degats(self) -> pygame.Rect:
        return pygame.Rect(self.coords, self.size)

    @property
    def hitbox_collision(self) -> pygame.Rect:

        return pygame.Rect((self.coords[0]+COLLIDBOX_SIZE, self.coords[1]+COLLIDBOX_SIZE), (self.size[0]-2*COLLIDBOX_SIZE, self.size[1]-2*COLLIDBOX_SIZE))

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

    def tick_update(self, elements: tuple) -> None:
        self.current_frame += 1

    def display(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.__coords)
        self.__health_bar.display(screen)
        if SHOW_HITBOX:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox_degats, 1)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox_collision, 1)

    def update(self, elements: dict) -> None:

        olds = self.coords
        direction = self.get_direction(
            self.get_target(elements["player"][0].coords))
        produit = abs(direction[0]) + abs(direction[1])

        if self.hitbox_degats.collidelist([element.hitbox for element in elements["fries"]]) != -1:
            for i in elements["fries"]:
                if self.hitbox_degats.colliderect(i.hitbox):
                    # print("collision")
                    self.is_attacked(i.damage)
                    elements["fries"].remove(i)
        if produit != 0:
            direction = (direction[0] / produit, direction[1] / produit)
        else:
            direction = (0, 0)
        self.coords = self.coords[0] + direction[0] * \
            self.speed, self.coords[1] + direction[1] * self.speed

        zombie_except_me = [
            zombie for zombie in elements["zombies"] if zombie != self]

        if self.hitbox_collision.collidelist([element.hitbox_collision for element in zombie_except_me]) != -1:
            self.coords = olds
