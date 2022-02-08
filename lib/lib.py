import pygame
import numpy as np
import math
import os


def load_image(path: str, size: tuple) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path), size).convert_alpha()


def load_animation(path: str, size: tuple) -> list:
    folder_content = sorted(os.listdir(path))
    return [load_image(f"{path}/{file}", size) for file in folder_content]


def get_angle_between_vectors(v1: tuple, v2: tuple) -> int:
    dot_product = np.dot(v1, v2)
    angle = np.arccos(dot_product/(np.linalg.norm(v2)*np.linalg.norm(v1)))
    return math.degrees(angle)


def get_vector_angle(v1: tuple) -> int:
    return math.degrees(math.atan2(v1[1], v1[0]))

def vector_from_speed_angle(speed : int, angle : int) -> tuple:
   tan_teta = math.tan(math.radians(angle))
   vector_y = (speed * tan_teta) / (1 + tan_teta)
   vector_x = speed - vector_y
   return (vector_x, vector_y)

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect
