import pygame


def load_image(path: str, size: tuple) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path), size).convert_alpha()
