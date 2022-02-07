from random import randrange

from constantes import NB_ELEM_X


class Zombie:
	def __init__(self, speed: int = 1, name="Zombie", damage: int = 10, hp: int = 100):
		self.__name = name
		self.__hp = hp
		self.__damage = damage
		self.__speed = speed
		self.__alive = True
		self.__image = "images/zombie.jpg"

		side = randrange(0, 3)
		if side == 0:
			self.__x = randrange(0, NB_ELEM_X)
			self.__y = 0
		elif side == 1:
			self.__x = NB_ELEM_X - 1
			self.__y = randrange(0, NB_ELEM_X)
		elif side == 2:
			self.__x = randrange(0, NB_ELEM_X)
			self.__y = NB_ELEM_X - 1
		elif side == 3:
			self.__x = 0
			self.__y = randrange(0, NB_ELEM_X)
		else:
			raise Exception("Error in Zombie.__init__() : side = " + str(side))

	# Getters
	def get_damage(self):
		return self.__damage

	def get_speed(self):
		return self.__speed

	# def get_name(self):
	# 	return self.__name

	def get_hp(self):
		return self.__hp

	def get_image(self):
		return self.__image

	def get_x(self):
		return self.__x

	def get_y(self):
		return self.__y

	def is_alive(self):
		return self.__alive

	# Setters
	def set_damage(self, damage):
		self.__damage = damage

	def set_speed(self, speed):
		self.__speed = speed

	def set_name(self, name):
		self.__name = name

	def take_damage(self, damage):
		if self.__hp - damage <= 0:
			self.__hp = 0
			self.__alive = False
		else:
			self.__hp -= damage

	def move_x(self, x):
		self.__x += x * self.get_speed()

	def move_y(self, y):
		# Move in y
		self.__y += y * self.get_speed()
