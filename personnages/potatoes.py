import pygame
import random
from random import randrange
from constantes import CASE_SIZE, PROBA_PATATE, SIZE, NB_ELEM_Y, TOURS, NB_ELEM_X


class Potatoes:
    def __init__(self):

        x_pousse = random.randint(0, NB_ELEM_X)
        y_pousse = random.randint(0, NB_ELEM_Y)
        self.__pos_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

        for i in TOURS:
            while (self.__pos_pousse[0] == i[0] and self.__pos_pousse[1] == i[1]) or (self.__pos_pousse[0] > (SIZE[0]-CASE_SIZE) or self.__pos_pousse[0]<0) or (self.__pos_pousse[1] > (SIZE[1]-CASE_SIZE) or self.__pos_pousse[1]<0):
                x_pousse = random.randint(0, NB_ELEM_X)
                y_pousse = random.randint(0, NB_ELEM_Y)
                self.__pos_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

        def position(self):
            #x_patate = randrange(x_pousse - 1, x_pousse + 2)
            #y_patate = randrange(y_pousse - 1, y_pousse + 2)
            if random.randint(0,PROBA_PATATE) == 0:
                x_patate=x_pousse
                y_patate=y_pousse
            else:
                x_patate=random.randint(x_pousse-1,x_pousse+1)
                if x_patate!=0 :
                    y_patate=y_pousse
                else:
                    y_patate=random.randint(y_pousse-1,y_pousse+1)
            self.__pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE
            return self.__pos_patate

        position(self)

        for i in TOURS:
            while (self.__pos_patate[0]== i[0] and self.__pos_patate[1]==i[1]) or (self.__pos_patate[0] > (SIZE[0]-CASE_SIZE) or self.__pos_patate[0]<0) or (self.__pos_patate[1] > (SIZE[1]-CASE_SIZE) or self.__pos_patate[1]<0):
                position(self)

        self.image_patate = pygame.image.load("./images/patate.png")
        self.image_pousse = pygame.image.load("./images/pousse_patate.png")
        self.size = CASE_SIZE
        self.age = 0
        self.lifespan = 26


    @property
    def alive(self):
        return not random.randint(0, self.lifespan-7) + self.age >= self.lifespan

    def tick_update(self):
        self.age += 1

    def get_pos_pousse(self):
        return self.__pos_pousse

    def get_pos_patate(self):
        return self.__pos_patate
