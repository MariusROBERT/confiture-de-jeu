import pygame
import os
from constantes import CASE_SIZE, FPS, TOURS, WIDTH, HEIGHT
from lib.animated import Animated
from lib.lib import load_animation, load_image
from lib.player import dir_to_angle


class Player(Animated):
    def __init__(self):
        super().__init__("player", (CASE_SIZE, CASE_SIZE))
        self.inventory = []

        self._current_animation = "walk"

        self.potatoe_mini = load_image(
            "./images/player/autre/potatoemini.png", (15, 15))
        self.size = (70, 70)
        self.coords = (20, 20)
        self.speed = 350 / FPS
        self.direction = []
        self.__alive = True

        self.time_since_dig = 0
        self._digging = False
        self._paused_animation = ""

    @property
    def alive(self) -> bool:
        return self.__alive

    @property
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.coords, self.size)

    @property
    def center_coords(self) -> tuple:
        return (self.coords[0] + self.size[0] / 2, self.coords[1] + self.size[1] / 2)

    @property
    def digging(self) -> bool:
        return self._digging

    @digging.setter
    def digging(self, value: bool) -> None:
        self._digging = value
        if value:
            self._paused_animation = self.current_animation
            self.current_animation = "dig"
        else:
            self.current_animation = self._paused_animation

    def move(self, event: pygame.event.Event, elements) -> None:
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
            if len(self.direction) > 0:
                self.current_animation = "walk"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z and "up" in self.direction:
                self.direction.remove("up")
            if event.key == pygame.K_s and "down" in self.direction:
                self.direction.remove("down")
            if event.key == pygame.K_q and "left" in self.direction:
                self.direction.remove("left")
            if event.key == pygame.K_d and "right" in self.direction:
                self.direction.remove("right")

            if len(self.direction) == 0:
                self.current_animation = "idle"

            if event.key == pygame.K_SPACE:
                # Si il est a proximitée d'un pig
                feeded = False
                if self.hitbox.collidelist([element.hitbox_feed for element in elements["pigs"]]) != -1:
                    if len(self.inventory) > 0:
                        for pig in elements["pigs"]:
                            if pig.hitbox_feed.colliderect(self.hitbox):
                                pig.feed()
                                self.inventory.pop()
                                feeded = True
                                break

                # si il est dans la hitbox d'une potatoe
                if not feeded:
                    self.digging = True
                    if elements["terrain"][0].harvrest(self.center_coords) and len(self.inventory) < 5:
                        self.inventory.append("potatoe")

    def tick_update(self, elements) -> None:
        self.current_frame += 1
        if self.digging:
            self.time_since_dig += 1
            if self.time_since_dig > len(self.animation["dig"]):
                self.digging = False
                self.time_since_dig = 0

    def update(self, elements: dict) -> None:
        # Effectue les deplacement
        if self._digging:
            return

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
        angle = dir_to_angle(self.direction)
        rotated = pygame.transform.rotate(self.sprite, angle)
        screen.blit(rotated, self.coords)

        for i in range(len(self.inventory)):
            screen.blit(
                self.potatoe_mini, (self.coords[0] + i*15, self.coords[1] - 15))
