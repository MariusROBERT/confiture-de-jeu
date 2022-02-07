import random
import pygame
from lib.lib import load_image

from personnages.potatoes import Potatoes
from constantes import SIZE, CASE_SIZE


class Terrain:
    def __init__(self) -> None:
        self.base_terrain = pygame.image.load("images/grass.png").convert()
        self.pousse = load_image("images/pousse2.png", (CASE_SIZE, CASE_SIZE))

        self.potatoes = []

    def tick_update(self) -> None:
        chance = 2
        if random.randint(0, chance) == 0:
            self.potatoes.append(Potatoes())

        for potato in self.potatoes:
            potato.tick_update()
            if potato.alive is False:
                self.potatoes.remove(potato)

    @property
    def potatoes_hitbox(self) -> list:
        pos_patates = [x.get_pos_patate() for x in self.potatoes]
        return [pygame.Rect(x[0], x[1], 20, 20) for x in pos_patates]

    def update(self, elements) -> None:
        pass

    def display(self, screen: pygame.Surface) -> None:
        for i in range(0, SIZE[0], CASE_SIZE):
            for j in range(0, SIZE[1], CASE_SIZE):
                screen.blit(self.base_terrain, (i, j))

                if (i, j) in [x.get_pos_pousse() for x in self.potatoes]:
                    screen.blit(self.pousse, (i, j))

                if (i, j) in [x.get_pos_patate() for x in self.potatoes]:
                    potatosize = 20
                    rect = pygame.Rect(i, j, 20, 20)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
