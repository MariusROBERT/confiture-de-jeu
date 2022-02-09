import pygame
from constantes import OPACITY_NIGHT, SIZE_PLAYER, WIDTH, HEIGHT
from lib.lib import load_animation, load_image
from managers.events_const import CHANGE_NIGHT, DAMAGE_EVENT
from managers.sound_manager import COLLECT_POTATOE


# EVENT DE 20 A 30 reservés


DAMAGE_DURATION = 8


class Fx_manager:
    def __init__(self):
        self.damage_screen = load_image("red.png", (WIDTH, HEIGHT))
        self.damage_screen_old = 0
        self.damage_screen_on = False

        self.nuit_screen = load_image("nuit.png", (WIDTH, HEIGHT))
        self.nuit_screen.fill((255, 255, 255, OPACITY_NIGHT),
                              special_flags=pygame.BLEND_RGBA_MULT)
        self.nuit_screen_on = False

        self.explosion_screen = load_animation(
            "particle/explosion", (SIZE_PLAYER*2, SIZE_PLAYER*2))
        self.explosion_on = False
        self.explosion_old = 0
        self.pos_explosion = (0, 0)

    def event_manager(self, event: pygame.event.Event, elements):
        if event.type == DAMAGE_EVENT:
            self.damage_screen_on = True
        elif event.type == CHANGE_NIGHT:
            self.nuit_screen_on = not self.nuit_screen_on
        elif event.type == COLLECT_POTATOE:
            self.explosion_on = True
            self.pos_explosion = elements["player"][0].coords

    def tick_update_100(self, elements):
        if self.damage_screen_on:
            self.damage_screen_old += 1
            if self.damage_screen_old > DAMAGE_DURATION:
                self.damage_screen_on = False
                self.damage_screen_old = 0
        if self.explosion_old:
            self.explosion_old += 1
            if self.explosion_old > len(self.explosion_screen):
                self.explosion_on = False
                self.explosion_old = 0

    def update(self, elements):
        pass

    def display(self, screen: pygame.Surface):
        if self.damage_screen_on:
            # ( A optimiser !!! ) (( si besoin mdr ))
            dm_screen = self.damage_screen.copy()

            transparence = 255 - \
                (self.damage_screen_old * 255 // DAMAGE_DURATION)
            dm_screen.fill((255, 255, 255, transparence),
                           special_flags=pygame.BLEND_RGBA_MULT)

            screen.blit(dm_screen, (0, 0))

        if self.nuit_screen_on:
            screen.blit(self.nuit_screen, (0, 0))

        if self.explosion_on:
            self.explosion_screen.tick(screen, self.pos_explosion)
            self.explosion_old += 1
