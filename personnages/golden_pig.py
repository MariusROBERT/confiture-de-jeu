from .pig import Pig
import numpy as np
from .autre_element.fries import Fries
from constantes import CASE_SIZE, FRIES_SPEED


class GoldenPig(Pig):
    def __init__(self, x: int, y: int, size=(CASE_SIZE * 2, CASE_SIZE * 2)):
        super().__init__(x, y, size)
        health = 300
        self.health_bar.color = (218, 165, 32)
        self.health_bar.max = health
        self.health_bar.health = health
        self.health_bar.size = (size[0], 30)
        self.health_bar.move_to((x, y - 40))
        self.health = health

    def get_fries(self):
        if self.target and self.target.alive and self.health > 0:
            f_list = []
            vector_to_target = np.array((
                self.target.coords[0] - self.coords[0],
                self.target.coords[1] - self.coords[1]))

            normalized_vector = vector_to_target / \
                                np.sqrt(np.sum(vector_to_target ** 2))
            for i in range(2):
                f_list.append(Fries((self.center_coords[0] + 20 * i, self.center_coords[1]),
                                    normalized_vector * FRIES_SPEED * 1.6, size=(10, 70)))
            return f_list
        else:
            return []
