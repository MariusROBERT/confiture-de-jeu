class zombie:
	def __init__(self, speed = 1, name = "Zombie", damage = 10, hp = 100):
		self.__name = name
		self.__hp = hp
		self.__damage = damage
		self.__speed = speed
		self.__alive = True


	# Getters
	def get_damage(self):
		return self.__damage
	def get_speed(self):
		return self.__speed
	def get_name(self):
		return self.__name
	def get_hp(self):
		return self.__hp

	# Setters
	def set_damage(self, damage):
		self.__damage = damage
	def set_speed(self, speed):
		self.__speed = speed
	def set_name(self, name):
		self.__name = name
	def set_hp(self, hp):
		self.__hp = hp
		if self.__hp <= 0:
			self.__alive = False




