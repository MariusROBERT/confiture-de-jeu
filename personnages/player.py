from turtle import update
import pygame


class Player ():
    def __init__(self):
        self.inventory = []
        self.sprite = pygame.image.load("./images/zombie.jpg")
        self.coords = (20, 20)
        self.speed = 2
        self.direction = []

    def move(self, event: pygame.event.Event):
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

    def update(self):
        for direction in self.direction:
            if direction == "up":
                self.coords = (self.coords[0], self.coords[1] - self.speed)
            if direction == "down":
                self.coords = (self.coords[0], self.coords[1] + self.speed)
            if direction == "left":
                self.coords = (self.coords[0] - self.speed, self.coords[1])
            if direction == "right":
                self.coords = (self.coords[0] + self.speed, self.coords[1])

    def display(self, screen):
        self.update()
        screen.blit(self.sprite, self.coords)
