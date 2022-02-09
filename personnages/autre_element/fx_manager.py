import pygame
from constantes import WIDTH, HEIGHT
from lib.lib import load_image


# EVENT DE 20 A 30 reservés

DAMAGE_EVENT = pygame.USEREVENT + 20


DAMAGE_DURATION = 8


class Fx_manager:
    def __init__(self):
        self.damage_screen = load_image("./images/red4.png", (WIDTH, HEIGHT))
        self.damage_screen_old = 0
        self.damage_screen_on = False

    def event_manager(self, event: pygame.event.Event):
        if event.type == DAMAGE_EVENT:
            self.damage_screen_on = True

    def tick_update_100(self, elements):
        if self.damage_screen_on:
            self.damage_screen_old += 1
            if self.damage_screen_old > DAMAGE_DURATION:
                self.damage_screen_on = False
                self.damage_screen_old = 0

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
