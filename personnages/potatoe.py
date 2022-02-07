import pygame
import random
from random import randrange
from constantes import TOURS, NB_ELEM_X, NB_ELEM_Y, CASE_SIZE, SIZE


class Potatoe:
    def __init__(self):
        x_pousse = random.randint(0, NB_ELEM_X)
        y_pousse = random.randint(0, NB_ELEM_Y)

        self.__coords_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

        while self.__coords_pousse not in TOURS:
            x_pousse = random.randint(0, NB_ELEM_X)
            y_pousse = random.randint(0, NB_ELEM_Y)
            self.__coords_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

        x_patate = randrange(x_pousse - 1, x_pousse + 2)
        y_patate = randrange(y_pousse - 1, y_pousse + 2)
        self.__coords_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE

        while self.__coords_patate not in TOURS and self.__coords_patate[1] < SIZE[1] and self.__coords_patate[2] < \
                SIZE[2]:
            x_patate = randrange(x_pousse - 1, x_pousse + 2)
            y_patate = randrange(y_pousse - 1, y_pousse + 2)
            self.__coords_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE

    @property
    def coords_patate(self) -> tuple[int, int]:
        return self.__coords_patate

    @property
    def coords_pousse(self) -> tuple[int, int]:
        return self.__coords_pousse
