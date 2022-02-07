import pygame
import random
from random import randrange
from constantes import TOURS, NB_ELEM_X, NB_ELEM_Y, CASE_SIZE, SIZE


class Potatoe:
	def __init__(self):
		self.image_patate = pygame.image.load("../images/patate.png")
		self.image_pousse = pygame.image.load("../images/pousse_patate.png")
		self.size = CASE_SIZE

		x_pousse = random.randint(0, NB_ELEM_X)
		y_pousse = random.randint(0, NB_ELEM_Y)
		self.__pos_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

		while self.__pos_pousse not in TOURS:
			x_pousse = random.randint(0, NB_ELEM_X)
			y_pousse = random.randint(0, NB_ELEM_Y)
			self.__pos_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

		x_patate = randrange(x_pousse - 1, x_pousse + 2)
		y_patate = randrange(y_pousse - 1, y_pousse + 2)
		self.__pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE

		while self.__pos_patate not in TOURS and self.__pos_patate[1] < SIZE[1] and self.__pos_patate[2] < SIZE[2]:
			x_patate = randrange(x_pousse - 1, x_pousse + 2)
			y_patate = randrange(y_pousse - 1, y_pousse + 2)
			self.__pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE

	def get_pos_patate(self):
		return self.__pos_patate

	def get_pos_pousse(self):
		return self.__pos_pousse