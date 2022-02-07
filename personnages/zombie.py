import string
from random import randrange
import pygame

from constantes import WIDTH, HEIGHT, CASE_SIZE


class Zombie:
	def __init__(self, speed: int = 1, name: string = "Zombie", damage: int = 10, hp: int = 100):
		self.__name = name
		self.__hp = hp
		self.__damage = damage
		self.__speed = speed
		self.__alive = True
		self.__sprite = pygame.image.load("./images/zombie.png")

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

	def is_attacked(self, damage: int) -> None:
		self.hp -= damage

	def attack(self, target) -> None:
		target.is_attacked(self.__damage)

	def display(self, screen: pygame.Surface) -> None:
		screen.blit(self.sprite, self.__coords)

	def update(self, elements : dict) -> None:
		pass