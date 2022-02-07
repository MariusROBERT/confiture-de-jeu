import pygame


class Player ():
    def __init__(self):
        self.inventory = []
        self.sprite = pygame.Rect(0, 0, 32, 32)
        self.coords = (20, 20)
        self.speed = 1

    def move(self, direction: str):

        if direction == "up":
            self.sprite.y -= 32
            self.coords = (self.coords[0], self.coords[1] - self.speed)
        elif direction == "down":
            self.sprite.y += 32
            self.coords = (self.coords[0], self.coords[1] + self.speed)
        elif direction == "left":
            self.sprite.x -= 32
            self.coords = (self.coords[0] - self.speed, self.coords[1])
        elif direction == "right":
            self.sprite.x += 32
            self.coords = (self.coords[0] + self.speed, self.coords[1])
        else:
            print("Error: direction not recognized")

    def display(self, screen):
        screen.blit(self.sprite, self.coords)
