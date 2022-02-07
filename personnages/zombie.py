import string
from random import randrange

from constantes import WIDTH, HEIGHT, CASE_SIZE


class Zombie:
	def __init__(self, speed: int = 1, name: string = "Zombie", damage: int = 10, hp: int = 100):
		self.__name = name
		self.__hp = hp
		self.__damage = damage
		self.__speed = speed
		self.__alive = True
		self.__image = "images/zombie.png"

		side = randrange(0, 3)
		if side == 0:
			self.__pos = (randrange(0, WIDTH), 0)
		elif side == 1:
			self.__pos = (WIDTH - CASE_SIZE, randrange(0, HEIGHT))
		elif side == 2:
			self.__pos = (randrange(0, WIDTH), HEIGHT - CASE_SIZE)
		elif side == 3:
			self.__pos = (0, randrange(0, HEIGHT))
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
	def image(self) -> str:
		return self.__image

	@image.setter
	def image(self, image) -> None:
		self.__image = image

	@property
	def pos(self) -> tuple[int, int]:
		return self.__pos

	@pos.setter
	def pos(self, pos: tuple[int, int]) -> None:
		self.__pos = pos

	@property
	def alive(self) -> bool:
		return self.__alive

	def is_attacked(self, damage: int) -> None:
		self.hp -= damage

	def attack(self, target) -> None:
		target.is_attacked(self.__damage)
