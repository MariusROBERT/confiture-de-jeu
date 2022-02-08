import pygame
import os
from constantes import BORDER_SIZE, CASE_SIZE, DEFAULT_HEALTH_BAR_SIZE, FPS, PLAYER_SPEED, SHOW_HITBOX, TOURS, WIDTH, HEIGHT, SIZE_PLAYER
from lib.animated import Animated
from lib.lib import load_animation, load_image
from lib.player import dir_to_angle
from .autre_element.health_bar import HealthBar


class Player(Animated):
    def __init__(self):
        super().__init__("player", (SIZE_PLAYER, SIZE_PLAYER))
        self.inventory = []

        self._current_animation = "walk"

        self.potatoe_mini = load_image(
            "./images/player/autre/potatoemini.png", (20, 20))

        self.size = (SIZE_PLAYER, SIZE_PLAYER)
        self.coords = (20, 20)

        self._speed = PLAYER_SPEED
        self.direction = []
        self.__alive = True

        self.time_since_dig = 0
        self._digging = False
        self._paused_animation = ""

        self.time_since_move = 0

        hp=100
        self.health_bar_size=(self.size[0],self.size[1]+5)
        new_health_bar= HealthBar((-1000,-1000),size=self.health_bar_size,max=hp,value=hp,color=(255,30,255),auto_hide=True)
        self.__health_bar=new_health_bar
        self.__health=hp

    @property
    def health(self)->int:
        return self.__health

    @health.setter
    def health(self,hp)->None:
        if hp<=0:
            self.__health=0
            self.__alive=False
            self.current_animation="dead"
        else:
            self.__health=hp
        self.__health_bar.health=self.__health

    @property
    def alive(self) -> bool:
        return self.__alive

    @property
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.coords, self.size)

    @property
    def center_coords(self) -> tuple:
        return self.coords[0] + self.size[0] / 2, self.coords[1] + self.size[1] / 2

    @property
    def digging(self) -> bool:
        return self._digging

    @property
    def speed(self) -> int:
        valeur = self._speed
        if len(self.direction) == 2:
            valeur *= 0.8

        if self.time_since_move < 7:
            valeur *= (self.time_since_move + 1) / 7

        return valeur

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
            if not len(self.direction) >= 2:
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
                self.time_since_move = 0

    def tick_update_100(self, elements) -> None:
        self.current_frame += 1
        if self.digging:
            self.time_since_dig += 1
            if self.time_since_dig > len(self._animation["dig"]):
                self.digging = False
                self.time_since_dig = 0

        if len(self.direction) > 0:
            self.time_since_move += 1

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

        if self.coords[0] < BORDER_SIZE:
            self.coords = (BORDER_SIZE, self.coords[1])
        if self.coords[0] > WIDTH - BORDER_SIZE - self.size[0]:
            self.coords = (WIDTH - BORDER_SIZE - self.size[0], self.coords[1])
        if self.coords[1] < BORDER_SIZE:
            self.coords = (self.coords[0], BORDER_SIZE)
        if self.coords[1] > HEIGHT - BORDER_SIZE - self.size[1]:
            self.coords = (self.coords[0], HEIGHT - BORDER_SIZE - self.size[1])
        
        healt_bar_x = self.coords[0] + self.size[0] / 2 - self.__health_bar.size[0] / 2
        healt_bar_y = self.coords[1] - self.__health_bar.size[1] - 10
        self.__health_bar.coords = (healt_bar_x, healt_bar_y)
        self.__health_bar.move_to(self.__health_bar.coords)

    def display(self, screen) -> None:

        angle = dir_to_angle(self.direction)
        # rotated = pygame.transform.rotate(self.sprite, angle)

        rotated_image = pygame.transform.rotate(self.sprite, angle)
        new_rect = rotated_image.get_rect(
            center=self.sprite.get_rect(topleft=self.coords).center)

        screen.blit(rotated_image, new_rect)

        if SHOW_HITBOX:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        for i in range(len(self.inventory)):
            screen.blit(
                self.potatoe_mini, (self.coords[0] + i * 20, self.coords[1] - 20))
        
        self.__health_bar.display(screen)
