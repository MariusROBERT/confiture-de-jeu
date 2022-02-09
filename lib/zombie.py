from math import sqrt
from random import randrange

from constantes import CASE_SIZE, HEIGHT, WIDTH, TOURS


def randomCoords():
    side = randrange(4)
    if side == 0:
        res = (randrange(0, WIDTH), 0)
    elif side == 1:
        res = (WIDTH - CASE_SIZE, randrange(0, HEIGHT))
    elif side == 2:
        res = (randrange(0, WIDTH), HEIGHT - CASE_SIZE)
    elif side == 3:
        res = (0, randrange(0, HEIGHT))
    else:
        raise Exception(
            "Error in Zombie.__init__() : side = " + str(side))
    return res


def get_distance(coords_a: tuple[int, int], coords_b: tuple[int, int]) -> float:
    return sqrt((coords_a[0] - coords_b[0]) ** 2 + (coords_a[1] - coords_b[1]) ** 2)


def get_target(coords_zombie: tuple[int, int], coords_player: tuple[int, int]) -> tuple[int, int]:
    distance = sqrt((coords_player[0] - coords_zombie[0])
                    ** 2 + (coords_player[1] - coords_zombie[1]) ** 2)
    target = coords_player
    # KEEP COMMENT TO FOLLOW PLAYER ONLY
    # for pig in TOURS:
    #     dist_temp = get_distance(coords_zombie, pig)
    #     print(dist_temp)
    #     print(distance)
    #     if dist_temp < distance:
    #         distance = dist_temp
    #         target = pig
    return target


def get_direction(coords_zombie, target: tuple[int, int]) -> tuple[int, int]:
    return target[0] - coords_zombie[0], target[1] - coords_zombie[1]


def get_direction_vector(coords_zombie, target: tuple[int, int]) -> tuple[float, float]:
    dir = get_direction(coords_zombie, target)
    dist = get_distance(coords_zombie, target)
    return dir[0] / dist, \
           dir[
               1] / dist
