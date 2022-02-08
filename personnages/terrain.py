import random
import pygame
from lib.lib import load_image

from personnages.potatoes import Potatoes
from constantes import SIZE, CASE_SIZE


class Terrain:
    def __init__(self) -> None:
        self.base_terrain = load_image(
            "images/terrain/soltest3.png", (CASE_SIZE, CASE_SIZE))
        self.pousse = load_image(
            "images/terrain/pousse2.png", (CASE_SIZE, CASE_SIZE))
        self.trous_image = load_image(
            "images/terrain/trou.png", (CASE_SIZE, CASE_SIZE))

        self.potatoes = []
        self.trous = []

    def tick_update(self) -> None:
        chance = 2
        if random.randint(0, chance) == 0:
            self.potatoes.append(Potatoes())

        for potato in self.potatoes:
            potato.tick_update()
            if potato.alive is False:
                self.potatoes.remove(potato)

        for trou in self.trous:
            trou["old"] += 1
            if trou["old"] > 8:
                self.trous.remove(trou)
                pass

    @property
    def potatoes_hitbox(self) -> list:
        pos_patates = [x.get_pos_patate() for x in self.potatoes]

    def harvrest(self, coords: tuple) -> bool:
        coordsbase = (coords[0] // CASE_SIZE * CASE_SIZE,
                      coords[1] // CASE_SIZE * CASE_SIZE)
        self.trous.append(
            {"coords": coordsbase, "old": 0})
        for patate in self.potatoes:
            pos_patate = patate.get_pos_patate()
            if pos_patate[0] > coords[0] - CASE_SIZE and pos_patate[0] < coords[0] + CASE_SIZE:
                if pos_patate[1] > coords[1] - CASE_SIZE and pos_patate[1] < coords[1] + CASE_SIZE:
                    self.potatoes.remove(patate)
                    return True

        return False

    def update(self, elements) -> None:
        pass

    def display(self, screen: pygame.Surface) -> None:
        for i in range(0, SIZE[0], CASE_SIZE):
            for j in range(0, SIZE[1], CASE_SIZE):

                if (i, j) in [x["coords"] for x in self.trous]:
                    screen.blit(self.trous_image, (i, j))
                else:
                    screen.blit(self.base_terrain, (i, j))

                if (i, j) in [x.get_pos_pousse() for x in self.potatoes]:
                    screen.blit(self.pousse, (i, j))

                if (i, j) in [x.get_pos_patate() for x in self.potatoes]:
                    potatosize = 20
                    rect = pygame.Rect(i+15, j+15, 20, 20)
                    # pygame.draw.rect(screen, (255, 0, 0), rect, 1)
