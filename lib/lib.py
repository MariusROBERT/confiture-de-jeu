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
    angle = np.arccos(dot_product / (np.linalg.norm(v2) * np.linalg.norm(v1)))
    return math.degrees(angle)


def get_vector_angle(v1: tuple) -> int:
    return math.degrees(math.atan2(v1[1], v1[0]))


def vector_from_speed_angle(speed: int, angle: int) -> tuple:
    tan_teta = math.tan(math.radians(angle))
    vector_y = (speed * tan_teta) / (1 + tan_teta)
    vector_x = speed - vector_y
    return vector_x, vector_y


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def nearest_zombie(zombies: 'Zombie', coords: tuple) -> 'Zombie':
    nearest = None
    nearest_distance = float('inf')
    for zombie in zombies:
        distance = math.sqrt(
            (zombie.coords[0] - coords[0]) ** 2 + (zombie.coords[1] - coords[1]) ** 2)
        if distance < nearest_distance:
            nearest = zombie
            nearest_distance = distance
    return nearest


def queue_event(id: int):
    pygame.event.post(pygame.event.Event(id))
    
def quadratic_equation_roots(a : int, b : int, c : int) -> tuple:
    delta = b**2 - 4*a*c
    if delta < 0 or a +b == 0:
        return None
    else:
        return (-b + math.sqrt(delta)) / (2*a), (-b - math.sqrt(delta)) / (2*a)
    
def vector_to_target_tea_time_algorithm(
        moving_object_coords : tuple, 
        moving_object_vector : tuple, 
        interceptor_origin_coords : tuple, 
        interceptor_vector_norm : int) -> tuple:
    """[summary]

    Args:
        moving_object_coords (tuple): [description]
        moving_object_vector (tuple): [description]
        interceptor_origin_coords (tuple): [description]
        interceptor_vector_norm (int): [description]

    Returns:
        tuple: [description]

    TEA TIME ALGORITHM

    (  )   (   )  )
     ) (   )  (  (
     ( )  (    ) )
     _____________
    <_____________> ___
    |             |/ _ \
    |               | | |
    |               |_| |
 ___|             |\___/
/    \___________/    \
\_____________________/
    """
    # solving the quadratic equation
    a = moving_object_vector[0]**2 + moving_object_vector[1]**2 - interceptor_vector_norm**2
    b = 0
    c = moving_object_coords[0]**2 \
        + moving_object_coords[1]**2 \
        - 2*interceptor_origin_coords[0]*moving_object_coords[0] \
        - 2*interceptor_origin_coords[1]*moving_object_coords[1] \
        + interceptor_origin_coords[0]**2 \
        + interceptor_origin_coords[1]**2
    roots = quadratic_equation_roots(a, b, c)
    if roots is None:
        # interception not possible
        return None
    else:
        holly_tea = max(roots)
        if holly_tea == 0:
            # interception not possible
            return None
        u = (moving_object_coords[0] - interceptor_origin_coords[0]) / holly_tea
        v = (moving_object_coords[1] - interceptor_origin_coords[1]) / holly_tea
        return (u, v)