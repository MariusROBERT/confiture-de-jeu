import random
import pygame
from lib.lib import load_animation, load_image

from personnages.potatoes import Potatoes
from constantes import NB_ELEM_X, NB_ELEM_Y, SIZE, CASE_SIZE, AGE_MAX_TROU, CHANCE_POTATO


class Terrain:
    def __init__(self) -> None:
        self.base_terrain = load_image(
            "images/terrain/soltest3.png", (CASE_SIZE, CASE_SIZE))
        self.pousse = load_image(
            "images/terrain/pousse3.png", (CASE_SIZE, CASE_SIZE))
        self.trous_images = load_animation(
            "images/terrain/trou",  (CASE_SIZE, CASE_SIZE))

        self.potatoes = []
        self.trous = []

        self.nbcase = NB_ELEM_X * NB_ELEM_Y

    def tick_update(self) -> None:
        if random.randint(0, CHANCE_POTATO) == 0:
            self.potatoes.append(Potatoes())

        for potato in self.potatoes:
            potato.tick_update()
            if potato.alive is False:
                self.potatoes.remove(potato)

        for trou in self.trous:
            trou["old"] += 1
            if trou["old"] > AGE_MAX_TROU:
                self.trous.remove(trou)
                pass

    @property
    def potatoes_hitbox(self) -> list:
        pos_patates = [x.get_pos_patate() for x in self.potatoes]

    def harvrest(self, coords: tuple) -> bool:
        coordsbase = (coords[0] // CASE_SIZE * CASE_SIZE,
                      coords[1] // CASE_SIZE * CASE_SIZE)
        self.trous.append(
            {"coords": coordsbase, "old": 0, "imgIndex": random.randint(1, len(self.trous_images))})
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

                screen.blit(self.base_terrain, (i, j))
                trou = list(
                    filter(lambda x: x["coords"] == (i, j), self.trous))
                if len(trou) > 0:
                    indexImage = trou[0]["imgIndex"] - 1
                    # ( A optimiser !!! ) (( si besoin mdr ))
                    image = self.trous_images[indexImage].copy()

                    transparence = 255 - (trou[0]["old"] * 255 // AGE_MAX_TROU)
                    image.fill((255, 255, 255, transparence),
                               special_flags=pygame.BLEND_RGBA_MULT)

                    screen.blit(image, (i, j))

                if (i, j) in [x.get_pos_pousse() for x in self.potatoes]:
                    screen.blit(self.pousse, (i, j))

                if (i, j) in [x.get_pos_patate() for x in self.potatoes]:
                    rect = pygame.Rect(i+15, j+15, 20, 20)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
