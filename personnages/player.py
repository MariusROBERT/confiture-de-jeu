import pygame

from constantes import CASE_SIZE, FPS, TOURS, WIDTH, HEIGHT


class Player:
	def __init__(self):
		self.inventory = []
		self.sprite = pygame.image.load("./images/player.png")
		self.size = self.sprite.get_size()
		self.coords = (20, 20)
		self.speed = 300 / FPS
		self.direction = []
		self.__alive = True

	@property
	def alive(self) -> bool:
		return self.__alive

	@property
	def hitbox(self) -> pygame.Rect:
		return pygame.Rect(self.coords, self.size)

	def move(self, event: pygame.event.Event) -> None:
		if event.type == pygame.KEYDOWN:
			if len(self.direction) >= 2:
				return
			if event.key == pygame.K_z:
				if not "down" in self.direction and not "up" in self.direction:
					self.direction.append("up")
			if event.key == pygame.K_s:
				if not "up" in self.direction and not "down" in self.direction:
					self.direction.append("down")
			if event.key == pygame.K_q:
				if not "right" in self.direction and not "left" in self.direction:
					self.direction.append("left")
			if event.key == pygame.K_d:
				if not "left" in self.direction and not "right" in self.direction:
					self.direction.append("right")
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_z and "up" in self.direction:
				self.direction.remove("up")
			if event.key == pygame.K_s and "down" in self.direction:
				self.direction.remove("down")
			if event.key == pygame.K_q and "left" in self.direction:
				self.direction.remove("left")
			if event.key == pygame.K_d and "right" in self.direction:
				self.direction.remove("right")

	def update(self, elements: dict) -> None:

		# Effectue les deplacement
		for direction in self.direction:
			originels = self.coords

			if direction == "up":
				self.coords = (self.coords[0], self.coords[1] - self.speed)
			if direction == "down":
				self.coords = (self.coords[0], self.coords[1] + self.speed)
			if direction == "left":
				self.coords = (self.coords[0] - self.speed, self.coords[1])
			if direction == "right":
				self.coords = (self.coords[0] + self.speed, self.coords[1])

			# Verifie les collisions avec les autres elements ( pigs ) (!!! A mieux optimiser !!!)
			if self.coords != originels:
				if self.hitbox.collidelist([element.hitbox for element in elements["pigs"]]) != -1:
					self.coords = originels

		# Verifie les collisions avec les bords
		bordure = 5
		if self.coords[0] < bordure:
			self.coords = (bordure, self.coords[1])
		if self.coords[0] > WIDTH - bordure - self.size[0]:
			self.coords = (WIDTH - bordure - self.size[0], self.coords[1])
		if self.coords[1] < bordure:
			self.coords = (self.coords[0], bordure)
		if self.coords[1] > HEIGHT - bordure - self.size[1]:
			self.coords = (self.coords[0], HEIGHT - bordure - self.size[1])

	def display(self, screen) -> None:
		# self.update()
		screen.blit(self.sprite, self.coords)