from random import random
import pygame

from constantes import NIGHT_DURATION, PROB_ZOMBIE_SPAWN
from lib.lib import queue_event
from personnages.autre_element.fx_manager import CHANGE_NIGHT


class Night_manager:
    def __init__(self):
        self.is_night = False
        self.night_duration = NIGHT_DURATION
        self._timer_night = 0

    @property
    def timer_night(self):
        return self._timer_night

    @timer_night.setter
    def timer_night(self, value):
        self._timer_night = value
        if self._timer_night >= self.night_duration:
            self.is_night = not self.is_night
            self._timer_night = 0
            queue_event(CHANGE_NIGHT)

    @property
    def prob_zombie_spawn(self):
        if self.is_night:
            return PROB_ZOMBIE_SPAWN * 1.5

        return PROB_ZOMBIE_SPAWN

    @property
    def speed_zombies(self):
        if self.is_night:
            return (random() * 1.5) + 3

        return(random() * 1.5) + 0.8

    def event_manager(self, event: pygame.event.Event):
        pass

    def tick_update(self, elements):
        self.timer_night += 1

    def update(self, elements):
        pass
