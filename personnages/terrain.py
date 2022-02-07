import pygame

from constantes import SIZE, CASE_SIZE


class Terrain:
    def __init__(self) -> None:
        self.base_terrain = pygame.image.load("images/grass.png").convert()

    def update(self, elements) -> None:
        pass

    def display(self, screen: pygame.Surface) -> None:
        for i in range(0, SIZE[0], CASE_SIZE):
            for j in range(0, SIZE[1], CASE_SIZE):
                screen.blit(self.base_terrain, (i, j))
