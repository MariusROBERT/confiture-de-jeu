from operator import ne
import pygame
from pygame.locals import *
from lib.lib import get_angle_between_vectors, vector_from_speed_angle, load_image
from constantes import CASE_SIZE, FRIES_SPEED
from .autre_element.health_bar import HealthBar
from lib.lib import *
from .autre_element.fries import Fries
"""
               ,-,------,
              _ \(\(_,--'
         <`--'\>/(/(__
         /. .  `'` '  \
        (`')  ,        @
         `-._,        /
            )-)_/--( >  Piggie the pig
           ''''  ''''
"""


class Pig:
    def __init__(self, x: int, y: int, size=(80, 80)):
        self.coords = (x, y)

        self.image = load_image("images/cochonwtf.png", (CASE_SIZE, CASE_SIZE))

        self.nb_frames = 240
        self.size = size
        self.__animation_frame = 1

        self.health_bar = HealthBar(
            (self.coords[0]+11, self.coords[1] - 30), value=50, size=(65, 10), border_size=2, color=(203, 219, 11))
        self.health = 50
        self.__hitbox = pygame.Rect(self.coords, self.size)

        feed_space = 20
        self.__hitbox_feed = pygame.Rect(
            (self.coords[0] - feed_space, self.coords[1]-feed_space), (self.size[0]+feed_space*2, self.size[1] + feed_space*2))

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, value: int) -> None:
        min_value = -10
        self.__health = value
        if (self.__health <= min_value):
            self.__health = min_value

        self.health_bar.health = value

    @property
    def aura_frame(self) -> int:
        pass

    @property
    def hitbox(self) -> pygame.Rect:
        return self.__hitbox

    @property
    def hitbox_feed(self) -> pygame.Rect:
        return self.__hitbox_feed

    def next_frame(self) -> None:
        self.__animation_frame += 1
        if self.__animation_frame > self.nb_frames:
            self.__animation_frame = 1

    def feed(self, nourish_value: int = 20) -> None:
        self.health += 20

    def tick_update(self):
        self.health -= 1

    def update(self, elements: dict) -> None:
        self.health_bar.update()
        self.target=elements["zombies"][0]
        

    def display(self, surface: pygame.Surface) -> None:
        self.health_bar.display(surface)
        surface.blit(self.image, self.coords)

        self.next_frame()

    def get_fries(self):
        if self.target and self.target.alive and self.health > 0:
            vector_from_target = self.target.coords[0] - self.coords[0], self.target.coords[1] - self.coords[1]
            angle = get_angle_between_vectors(
                self.target.latest_vector, vector_from_target)
            
            #print(vector_from_speed_angle(FRIES_SPEED, angle))
            return (Fries(self.coords, vector_from_speed_angle(FRIES_SPEED, angle)))