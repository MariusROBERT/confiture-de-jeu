from constantes import TOURS, NB_ELEM_X, NB_ELEM_Y, CASE_SIZE, SIZE
import random
from random import randrange

test=(400,160)
for i in range(len(TOURS)):
    while test in TOURS[i]:
        test=(randrange(0,NB_ELEM_X),randrange(0,NB_ELEM_Y))
    print(test)