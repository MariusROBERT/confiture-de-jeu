import pygame
import numpy as np
import math
import os

from constantes import DATAPACK, DEBUG_MODE


def load_image(path: str, size: tuple) -> pygame.Surface:
    path2 = "./datapacks/" + DATAPACK + "/images/" + path
    if DEBUG_MODE:
        print("loading image:", path2)
    return pygame.transform.scale(pygame.image.load(path2).convert_alpha(), size)


def load_animation(path: str, size: tuple) -> list:
    path2 = "./datapacks/" + DATAPACK + "/images/" + path
    folder_content = sorted(os.listdir(path2))
    filtered_folder_content = list(
        filter(lambda x: x.endswith(".png"), folder_content))
    if DEBUG_MODE:
       print(filtered_folder_content)

    # image format = image:number:.png
    if len(filtered_folder_content) >= 9:
        filtered_folder_content.sort(
            key=lambda x: int(x.split(".")[0].split(":")[1]))

    return [load_image(f"{path}/{file}", size) for file in filtered_folder_content]


def angle_from_coordinates(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Calculate the angle between two coordinates
    :param x1: x coordinate of the first point
    :param y1: y coordinate of the first point
    :param x2: x coordinate of the second point
    :param y2: y coordinate of the second point
    :return: angle in degrees
    """
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def get_angle_between_vectors(v1: tuple, v2: tuple) -> float:
    return angle_from_coordinates(v1[0], v1[1], v2[0], v2[1])


def get_vector_angle(v1: tuple) -> float:
    return math.degrees(math.atan2(v1[1], v1[0]))


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


def queue_event(id: int, data: dict = {}):
    pygame.event.post(pygame.event.Event(id, data))


def quadratic_equation_roots(a: int, b: int, c: int) -> tuple:
    delta = b**2 - 4*a*c
    if delta < 0 or a + b == 0:
        return None
    else:
        return (-b + math.sqrt(delta)) / (2*a), (-b - math.sqrt(delta)) / (2*a)


def vector_to_target_tea_time_algorithm(
        moving_object_coords: tuple,
        moving_object_vector: tuple,
        interceptor_origin_coords: tuple,
        interceptor_vector_norm: int) -> tuple:
    """[summary]

    Args:
        moving_object_coords (tuple): t0 coordinates of the moving object targeted
        moving_object_vector (tuple): t0 movement vector of the moving object (acceleration is null)
        interceptor_origin_coords (tuple): t0 coordinates of the interceptor
        interceptor_vector_norm (int): norm of the interceptor vector (speed)

    Returns:
        tuple: vector to intercept the moving target None if no interception possible

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
    a = moving_object_vector[0]**2 + \
        moving_object_vector[1]**2 - interceptor_vector_norm**2
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
        u = (moving_object_coords[0] - interceptor_origin_coords[0]
             ) / holly_tea + moving_object_vector[0]
        v = (moving_object_coords[1] - interceptor_origin_coords[1]
             ) / holly_tea + moving_object_vector[1]
        return (u, v), holly_tea


def np_to_tuple(a):
    try:
        return tuple(np_to_tuple(i) for i in a)
    except TypeError:
        return a


def normalize_vector(vector: tuple) -> tuple:
    norm = math.sqrt(vector[0]**2 + vector[1]**2)
    if norm == 0:
        return 0, 0
    return vector[0]/norm, vector[1]/norm


def load_font(path: str, size: int) -> pygame.font.Font:
    path2 = "./datapacks/" + DATAPACK + "/fonts/" + path
    return pygame.font.Font(path2, size)


def vector_to_target(
        moving_object_coords: tuple,
        interceptor_origin_coords: tuple,
        interceptor_vector_norm: int) -> tuple:
    """[summary]
    Direct vector to target algorithm
    Args:
        moving_object_coords (tuple): [description]
        interceptor_origin_coords (tuple): [description]
        interceptor_vector_norm (int): [description]

    Returns:
        tuple: [description]
    """
    raw_vector = (moving_object_coords[0] - interceptor_origin_coords[0],
                  moving_object_coords[1] - interceptor_origin_coords[1])

    normalized_vector = normalize_vector(raw_vector)
    np_array = np.array(normalized_vector)
    normed_array = np_array * interceptor_vector_norm
    return np_to_tuple(normed_array)


def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def g_angle(v1, v2):
    cos = dotproduct(v1, v2) / (length(v1) * length(v2))
    if cos >= 1.0:
        cos = 0.99999999999999999
    if cos <= -1.0:
        cos = -0.9999999999999999
    try:
        return math.degrees(
            math.acos(
                cos))
    except ValueError:
        if DEBUG_MODE:
            print(cos)
        raise ValueError


def vector_from_angle_magnitude(angle: int, magnitude: float) -> tuple:
    u = np.cos(np.radians(angle))
    v = np.sin(np.radians(angle))

    arr = np.array((u, v))*magnitude

    return np_to_tuple(arr)


def rotate_vector(vector, angle):
    """Rotate the vector by the given angle in degrees"""
    x = vector[0]
    y = vector[1]
    rad = math.radians(angle)
    cos = math.cos(rad)
    sin = math.sin(rad)
    return x * cos - y * sin, x * sin + y * cos


def intermediate_vector(v1: tuple, v2: tuple, max_angle: int = 90, norm: int = None):

    angle = get_angle_between_vectors((0, 1), v1)
    init_angle_2 = get_angle_between_vectors((0, 1), v2)
    init_angle = angle
    init_tilt = init_angle_2 - init_angle
    tilt = init_tilt

    if tilt < 0 :
        if tilt < -max_angle:
            tilt = -max_angle

    else:
        if tilt > max_angle:
            tilt = max_angle
    if 180 < angle < 360-max_angle:
        tilt = -max_angle
    if abs(init_tilt) < abs(tilt):
        tilt = init_tilt
    angle += tilt
    v3 = rotate_vector(v1, tilt)
    
    #init_tilt = round(init_tilt, 2)
    #tilt = round(tilt, 2)
    #init_angle = round(init_angle, 2)
    #angle = round(angle, 2)
    #v3 = vector_from_angle_magnitude(angle, norm)
    
    #effective_angle = round(get_angle_between_vectors(v1, v3), 2)
    #print("ANG init_tilt:{}  tilt:{} init_angle_2:{} init_angle:{} -> angle:{} -> effective_angle:{}".format(init_tilt, tilt, init_angle_2, init_angle, angle, effective_angle) )

    return v3[0], v3[1]


def distance_between(coord1: tuple, coords2: tuple) -> float:
    return math.sqrt((coord1[0] - coords2[0])**2 + (coord1[1] - coords2[1])**2)


def create_transparent_animation(image: pygame.Surface):
    result = []
    for i in range(0, 256):
        t_image = image.copy()
        t_image.fill((255, 255, 255, i),
                     special_flags=pygame.BLEND_RGBA_MULT)
        result.append(t_image.convert_alpha())
    return result


def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf
