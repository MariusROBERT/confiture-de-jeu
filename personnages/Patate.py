import pygame
import random
from random import randrange
from constantes import TOURS, NB_ELEM_X, NB_ELEM_Y, CASE_SIZE, SIZE


class Patate:
	def __init__(self):
		self.image_patate = pygame.image.load("../images/patate.png")
		self.image_pousse = pygame.image.load("../images/pousse_patate.png")
		self.size = CASE_SIZE

		x_pousse = random.randint(0, NB_ELEM_X)
		y_pousse = random.randint(0, NB_ELEM_Y)
		pos_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

		while pos_pousse not in TOURS:
			x_pousse = random.randint(0, NB_ELEM_X)
			y_pousse = random.randint(0, NB_ELEM_Y)
			pos_pousse = x_pousse * CASE_SIZE, y_pousse * CASE_SIZE

		x_patate = randrange(x_pousse - 1, x_pousse + 2)
		y_patate = randrange(y_pousse - 1, y_pousse + 2)
		pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE

		while pos_patate not in TOURS and pos_patate[1] < SIZE[1] and pos_patate[2] < SIZE[2]:
			x_patate = randrange(x_pousse - 1, x_pousse + 2)
			y_patate = randrange(y_pousse - 1, y_pousse + 2)
			pos_patate = x_patate * CASE_SIZE, y_patate * CASE_SIZE

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y
