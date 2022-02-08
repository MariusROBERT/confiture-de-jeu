from random import randrange

from constantes import CASE_SIZE, HEIGHT, WIDTH


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
