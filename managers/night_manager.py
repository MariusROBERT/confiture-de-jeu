from random import random
import pygame

from constantes import BABY_ZOMBIE_SIZE, BABY_ZOMBIE_SPAWN_CHANCE, NIGHT_DURATION, PLAYER_SPEED, PROB_ZOMBIE_SPAWN, SIZE_ZOMBIE
from constantes import SHOW_HITBOX
from lib.lib import queue_event
from managers.fx_manager import CHANGE_NIGHT


class Night_manager:
    def __init__(self):
        self.is_night = False
        self.night_duration = NIGHT_DURATION
        self._timer_night = 0

        self.night_count = 0

    @property
    def timer_night(self):
        return self._timer_night

    @timer_night.setter
    def timer_night(self, value):
        self._timer_night = value
        if self._timer_night >= self.night_duration:
            self.is_night = not self.is_night
            if self.is_night:
                self.night_count += 1
            self._timer_night = 0
            queue_event(CHANGE_NIGHT)

    @property
    def prob_zombie_spawn(self):
        value = PROB_ZOMBIE_SPAWN
        if self.is_night:
            maxadd = 1
            add = (self.night_count / 25)
            if add > maxadd:
                add = maxadd
                if SHOW_HITBOX:
                    print("max difficulty prob spwan")
            value = PROB_ZOMBIE_SPAWN * 1.4 + add

        return value

    @property
    def speed_zombies(self):
        if self.is_night:
            maxadd = (PLAYER_SPEED - (1.5 + 1.3)) - 0.5
            add = (self.night_count / 25)
            if add > maxadd:
                add = maxadd
                if SHOW_HITBOX:
                    print("max difficluty speed")
            return (random() * 1.5) + 1.3 + (self.night_count / 6)

        return(random() * 1.5) + 0.7

    @property
    def size_zombie(self):
        if self.is_night:
            if random() < BABY_ZOMBIE_SPAWN_CHANCE:
                return (BABY_ZOMBIE_SIZE, BABY_ZOMBIE_SIZE)
            return (SIZE_ZOMBIE, SIZE_ZOMBIE)

        return (SIZE_ZOMBIE, SIZE_ZOMBIE)

    def event_manager(self, event: pygame.event.Event):
        pass

    def tick_update(self, elements):
        self.timer_night += 1

    def update(self, elements):
        pass
