import pygame
from pygame.locals import *
from lib.animated import Animated
from lib.lib import load_image
from constantes import AUTO_DAMAGE_SPEED, CASE_SIZE, FRIES_SPEED, SHOW_HITBOX, DEFAULT_HEALTH_BAR_BOTTOM_MARGIN, OVERRIDE_TEA_TIME_ALGORITHM, NO_DIRECT_SHOT, DEFAULT_PIG_HEALTH, PIG_MAX_HEALTH
from managers.events_const import FEEDED, OUT_OF_FOOD
from .autre_element.health_bar import HealthBar
from lib.lib import *
from .autre_element.fries import Fries, Frissile
import numpy as np
import managers.sound_manager as sound_manager

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


class Pig(Animated):
    def __init__(self, x: int, y: int, size=(CASE_SIZE, CASE_SIZE), max_health=PIG_MAX_HEALTH, health=DEFAULT_PIG_HEALTH):
        super().__init__("pig", size)
        self.coords = (x, y)

        self.size = size
        oversize = 10
        health_bar_size = (size[0] + oversize*2, 10)
        self.health_bar = HealthBar(
            (
                self.coords[0] - oversize + 2,  # 2 fix due to texture offset
                self.coords[1] - (DEFAULT_HEALTH_BAR_BOTTOM_MARGIN + health_bar_size[1])),
            value=DEFAULT_PIG_HEALTH,
            size=health_bar_size,
            border_size=2,
            color=(203, 219, 11))

        self.__health = health
        self.__hitbox = pygame.Rect(self.coords, self.size)
        self.__max_health = max_health
        feed_space = 20
        self.__hitbox_feed = pygame.Rect(
            (self.coords[0] - feed_space, self.coords[1] - feed_space),
            (self.size[0] + feed_space * 2, self.size[1] + feed_space * 2))
        self.center_coords = (
            self.coords[0] + self.size[0] / 2, self.coords[1] + self.size[1] / 2)

        self._current_animation = "fire"
        self.target = None

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, value: int) -> None:
        min_value = -10

        if value > self.__health:
            queue_event(FEEDED)
        self.__health = value
        if self.__health <= min_value:
            self.__health = min_value
        if self.__health > self.__max_health:
            self.__health = self.__max_health
        if self.__health <= 0 and self.current_animation != "idle":
            self.current_animation = "idle"
            queue_event(OUT_OF_FOOD)

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

    def feed(self, nourish_value: int = 20) -> None:
        self.health += nourish_value
        if self.health > 0:
            self._current_animation = "fire"

    def tick_update(self):
        self.health -= 9

    def tick_update_100(self, elements) -> None:
        self.current_frame += 1

    def get_fries(self):
        intersection_box = None
        fries_vector = None
        if self.target and self.target.alive and self.health > 0:
            try:
                fries_vector, t = vector_to_target_tea_time_algorithm(
                    self.target.center_coords,
                    self.target.latest_movement_vector,
                    self.center_coords,
                    FRIES_SPEED
                )
                intersection_coords = (
                    self.target.center_coords[0] +
                    self.target.latest_movement_vector[0] * t,
                    self.target.center_coords[1] + self.target.latest_movement_vector[1] * t)
                size = (20, 20)
                intersection_box = pygame.Rect(
                    intersection_coords[0] - size[0]//2,
                    intersection_coords[1] - size[1]//2,
                    size[0],
                    size[1])
            except TypeError:
                pass
            if fries_vector is None or OVERRIDE_TEA_TIME_ALGORITHM:
                if NO_DIRECT_SHOT:
                    return []
                vector_to_target = np.array((
                    self.target.coords[0] - self.coords[0],
                    self.target.coords[1] - self.coords[1]))

                normalized_vector = vector_to_target / \
                    np.sqrt(np.sum(vector_to_target ** 2))
                fries_vector = normalized_vector * FRIES_SPEED
            self.health -= AUTO_DAMAGE_SPEED
            return [Frissile(self.center_coords, fries_vector, intersection_box=intersection_box, target=self.target)]
        else:
            return []

    def tick_update(self):
        #self.health -= AUTO_DAMAGE_SPEED
        pass

    def tick_update_2(self, elements) -> None:
        self.current_frame += 1

    def update(self, elements: dict) -> None:
        self.health_bar.update()
        self.target = nearest_zombie(
            [zombie for zombie in elements["zombies"] if not zombie.dead], self.coords)

    def display(self, screen: pygame.Surface) -> None:
        self.health_bar.display(screen)
        screen.blit(self.sprite, self.coords)
        if SHOW_HITBOX:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
            pygame.draw.rect(screen, (255, 0, 0), self.__hitbox_feed, 1)
