import random
import pygame
from lib.lib import create_transparent_animation, load_animation, load_image

from personnages.potatoes import Potatoes
from constantes import NB_ELEM_X, NB_ELEM_Y, SHOW_HITBOX, SIZE, CASE_SIZE, AGE_MAX_TROU, CHANCE_POTATO


class Terrain:
    def __init__(self) -> None:

        self.base_terrains = load_animation(
            "terrain/sol", (CASE_SIZE, CASE_SIZE))
        self.pousse = load_image(
            "terrain/pousse3.png", (CASE_SIZE, CASE_SIZE))
        trous_images = load_animation(
            "terrain/trou", (CASE_SIZE, CASE_SIZE))

        self.trous_images_t = [
            create_transparent_animation(x) for x in trous_images]

        self.potatoes = []
        self.trous = []

        self.nbcase = (NB_ELEM_X + 1) * (NB_ELEM_Y + 1)

        self.terrain_texture_index = [random.randint(
            0, len(self.base_terrains) - 1) for i in range(self.nbcase+100)]

        for x in range(3):
            self.potatoes.append(Potatoes())

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

    @ property
    def potatoes_hitbox(self) -> list:
        pos_patates = [x.get_pos_patate() for x in self.potatoes]

    def harvrest(self, coords: tuple) -> bool:
        coordsbase = (coords[0] // CASE_SIZE * CASE_SIZE,
                      coords[1] // CASE_SIZE * CASE_SIZE)
        self.trous.append(
            {"coords": coordsbase, "old": 0, "imgIndex": random.randint(1, len(self.trous_images_t))})
        for patate in self.potatoes:
            pos_patate = patate.get_pos_patate()
            if coords[0] - CASE_SIZE < pos_patate[0] < coords[0] + CASE_SIZE:
                if coords[1] - CASE_SIZE < pos_patate[1] < coords[1] + CASE_SIZE:
                    self.potatoes.remove(patate)
                    return "potato"

        return "rien"

    def update(self, elements) -> None:
        pass

    def display(self, screen: pygame.Surface) -> None:
        a = 0
        for i in range(0, SIZE[0], CASE_SIZE):
            for j in range(0, SIZE[1], CASE_SIZE):

                screen.blit(
                    self.base_terrains[self.terrain_texture_index[a]], (i, j))
                trou = list(
                    filter(lambda x: x["coords"] == (i, j), self.trous))
                if len(trou) > 0:
                    indexImage = trou[0]["imgIndex"] - 1
                    image = self.trous_images_t[indexImage]
                    transparence = 255 - (trou[0]["old"] * 255 // AGE_MAX_TROU)

                    screen.blit(image[transparence], (i, j))

                if (i, j) in [x.pos_pousse for x in self.potatoes]:
                    screen.blit(self.pousse, (i, j))

                if SHOW_HITBOX:
                    if (i, j) in [x.get_pos_patate() for x in self.potatoes]:
                        rect = pygame.Rect(i + 15, j + 15, 20, 20)
                        pygame.draw.rect(screen, (255, 0, 0), rect, 1)

                a += 1
