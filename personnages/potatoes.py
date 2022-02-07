import pygame
from random import *
from constantes import CASE_SIZE, SIZE, NB_ELEM_Y, TOURS, NB_ELEM_X


class Potatoes:
    def __init__(self):
        self.image_patate = pygame.image.load("./images/patate.png")
        self.image_pousse = pygame.image.load("./images/pousse_patate.png")
        self.size = CASE_SIZE

        x_pousse = random.randint(0, NB_ELEM_X)
        y_pousse = random.randint(0, NB_ELEM_Y)
        self.__pos_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

        for i in TOURS :
            while self.__pos_pousse in i:
                x_pousse = random.randint(0, NB_ELEM_X)
                y_pousse = random.randint(0, NB_ELEM_Y)
                self.__pos_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

        x_patate = randrange(x_pousse - 1, x_pousse + 2)
        y_patate = randrange(y_pousse - 1, y_pousse + 2)
        self.__pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE

        for i in TOURS :
            while self.__pos_patate in TOURS and self.__pos_patate[1] < SIZE[1] and self.__pos_patate[2] < SIZE[2]:
                x_patate = randrange(x_pousse - 1, x_pousse + 2)
                y_patate = randrange(y_pousse - 1, y_pousse + 2)
                self.__pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE
