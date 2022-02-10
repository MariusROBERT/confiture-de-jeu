import pygame
import random
from random import randrange
from constantes import CASE_SIZE, SIZE, NB_ELEM_Y, TOURS, NB_ELEM_X
from constantes import POTATO_LIFESPAN
from lib.lib import load_image

default_pousse = None
lockheed_martin_image = None
power_up = None


def init_terrain_textures():
    global default_pousse
    default_pousse = load_image("terrain/pousse3.png", (CASE_SIZE, CASE_SIZE))
    global lockheed_martin_image
    lockheed_martin_image = default_pousse
    global power_up
    power_up = load_image("player/autre/power_up.png", (CASE_SIZE, CASE_SIZE))
    #lockheed_martin_image = load_image("terrain/pousse_locheed_martin.png", (CASE_SIZE, CASE_SIZE))


BASE_POTATOE = 0
POTATO_LOCKHEED_MARTIN = 1
POTATO_ZONE_DAMAGE = 2


class Potatoes:
    def __init__(self, type=BASE_POTATOE):

        self.__x_pousse = random.randint(0, NB_ELEM_X)
        self.__y_pousse = random.randint(0, NB_ELEM_Y)
        self.__pos_pousse = self.__x_pousse * CASE_SIZE, self.__y_pousse * CASE_SIZE

        for i in TOURS:
            while (self.pos_pousse[0] == i[0] and self.pos_pousse[1] == i[1]) or (
                    self.pos_pousse[0] > (SIZE[0] - CASE_SIZE) or self.pos_pousse[0] < 0) or (
                    self.pos_pousse[1] > (SIZE[1] - CASE_SIZE) or self.pos_pousse[1] < 0):
                self.__x_pousse = random.randint(0, NB_ELEM_X)
                self.__y_pousse = random.randint(0, NB_ELEM_Y)
                self.__pos_pousse = self.__x_pousse * CASE_SIZE, self.__y_pousse * CASE_SIZE

        self.__pos_patate = self.position()

        for i in TOURS:
            while (self.pos_patate[0] == i[0] and self.pos_patate[1] == i[1]) or (
                    self.pos_patate[0] > (SIZE[0] - CASE_SIZE) or self.pos_patate[0] < 0) or (
                    self.pos_patate[1] > (SIZE[1] - CASE_SIZE) or self.pos_patate[1] < 0):
                self.__pos_patate = self.position()

        self.age = 0
        self.lifespan = POTATO_LIFESPAN
        if default_pousse is None:
            init_terrain_textures()

        self.type = type

    @property
    def alive(self):
        return random.randint(0, self.lifespan - 7) + self.age < self.lifespan

    @property
    def x_pousse(self):
        return self.__x_pousse

    @property
    def y_pousse(self):
        return self.__y_pousse

    def tick_update(self):
        self.age += 1

    @property
    def pos_pousse(self):
        return self.__pos_pousse

    @property
    def pos_patate(self):
        return self.__pos_patate

    @property
    def coords(self) -> tuple:
        return self.pos_pousse

    def get_pos_pousse(self):
        return self.__pos_pousse

    def get_pos_patate(self):
        return self.__pos_patate

    def position(self):
        x_patate = self.x_pousse
        y_patate = self.y_pousse
        pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE
        return pos_patate

    def display(self, screen):

        if self.type == POTATO_LOCKHEED_MARTIN:
            screen.blit(lockheed_martin_image, self.pos_pousse)
        elif self.type == BASE_POTATOE:
            screen.blit(default_pousse, self.pos_pousse)
        elif self.type == POTATO_ZONE_DAMAGE:
            screen.blit(power_up, self.pos_pousse)
