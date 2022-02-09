import pygame
import random
from random import randrange
from constantes import CASE_SIZE, SIZE, NB_ELEM_Y, TOURS, NB_ELEM_X
from constantes import POTATO_LIFESPAN


class Potatoes:
    def __init__(self):

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

    def get_pos_pousse(self):
        return self.__pos_pousse

    def get_pos_patate(self):
        return self.__pos_patate

    def position(self):
        x_patate = self.x_pousse
        y_patate = self.y_pousse
        pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE
        return pos_patate
