import pygame
pygame.init()

COLLECT_POTATOE = pygame.USEREVENT + 10
collect_sound = pygame.mixer.Sound("sounds/collect.wav")

DEAD_ZOMBIE = pygame.USEREVENT + 11
dead_sound = pygame.mixer.Sound("sounds/dead_zombie3.wav")


def sound_manager(pygame, event: pygame.event.Event):
    if event.type == COLLECT_POTATOE:
        collect_sound.play().set_volume(0.3)
    if event.type == DEAD_ZOMBIE:
        dead_sound.play().set_volume(0.06)
