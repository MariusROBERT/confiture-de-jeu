from constantes import WIDTH, HEIGHT
from constantes import FRIES_SIZE, FRIES_DAMAGE, HITBOX_FRIES, FRIES_SPEED
from lib.lib import *

FRITE_IMAGE = load_image("frite.png", FRIES_SIZE)
FRISSILE_IMAGE = load_image("frite.png", (FRIES_SIZE[0]*1.4, FRIES_SIZE[1]*1.4))

class Fries:
    def __init__(self, coords: tuple, movement_vector: tuple = (1, 0), size: tuple = FRIES_SIZE, intersection_box=None):
        self.coords = coords
        self.size = size
        self._damage = FRIES_DAMAGE
        self._intersection_box = intersection_box
        self._movement_vector = movement_vector

        if size == FRIES_SIZE:
            sprite = FRITE_IMAGE
        else:
            sprite = load_image("frite.png", size)

        fries_angle = g_angle((0, 1), movement_vector)
        if movement_vector[0] < 0:
            fries_angle = 180 - fries_angle

        self.sprite, rect = rot_center(
            sprite, fries_angle, self.coords[0], self.coords[1])
        self.__hitbox = self.sprite.get_rect(center=rect.center)
        # self.sprite = rot_center(sprite, fries_angle)
        self.direction = []
        self.__alive = True
        self.angle = fries_angle
        self.age = 25
    @property
    def speed(self):
        return FRIES_SPEED
    
    @property
    def movement_vector(self) -> tuple:
        return self._movement_vector

    @property
    def damage(self) -> int:
        value = self._damage + (self.age/1.7)
        return value

    @damage.setter
    def damage(self, value: int):
        self._damage = value

    @property
    def alive(self) -> bool:
        return self.__alive

    @property
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.coords, HITBOX_FRIES)

    @property
    def age(self) -> int:
        return self.__age
    @property
    def center_coords(self):
        return self.coords[0] + self.size[0] / 2, self.coords[1] + self.size[1] / 2
    @age.setter
    def age(self, value: int):
        if value < 0:
            value = 0
        self.__age = value

    def kill(self):
        self.__alive = False

    def tick_update_100(self, elements):
        self.age -= 1

    def update(self, elements: dict):
        self.coords = self.coords[0] + \
            self.movement_vector[0], self.coords[1] + self.movement_vector[1]
        self.__alive = self.__alive and 0 < self.coords[0] < WIDTH and 0 < self.coords[1] < HEIGHT
        
    def display(self, screen, angle =None):
        sprite = self.sprite
        if angle is not None:
            sprite = pygame.transform.rotate(sprite, angle)
        screen.blit(sprite,
                    (self.coords[0] - self.sprite.get_width() / 2, self.coords[1] - self.sprite.get_height() / 2))
        if DEBUG_MODE:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
            if self._intersection_box is not None:
                pygame.draw.rect(screen, (0, 255, 0),
                                 self._intersection_box, 1)

class Frissile(Fries):
    def __init__(self,coords: tuple, movement_vector: tuple = (1, 0), size: tuple = FRIES_SIZE, intersection_box=None, target=None):
        super().__init__(coords, movement_vector, size, intersection_box)
        self.__target = target
        self.tick_update_100(None)
        self.__old_vector = (1,1)
    @property
    def speed(self):
        return FRIES_SPEED / 4
    
    def tick_update_100(self, elements):
        if self.__target is not None and self.__target.health > 0:
            pack = vector_to_target_tea_time_algorithm(self.__target.center_coords, self.__target.latest_movement_vector, self.center_coords,self.speed)
            if pack is not None and False:
                vector = pack[0]
            else:
                vector = vector_to_target(self.__target.center_coords, self.coords, self.speed)
            self.__old_vector = self.movement_vector
            vector = intermediate_vector(self.__old_vector, vector,max_angle=30 ,norm=self.speed)
            self._movement_vector = vector
            angle = g_angle((0, 1),self._movement_vector)
            if vector[0] < 0:
                angle = 180 - angle
            self.angle = angle
            self.sprite = FRISSILE_IMAGE
        elif elements is not None:
            if DEBUG_MODE:
                print("Changing target")
            self.__target = nearest_zombie(elements["zombies"], self.center_coords)
            self.tick_update_100(None)
    def display(self, screen : pygame.Surface):
        super().display(screen, angle=self.angle)
        if DEBUG_MODE:
            intersection_coords = (
                    self.center_coords[0] +
                    self.__old_vector[0] * self.speed,
                    self.center_coords[1] + self.__old_vector[1] * self.speed)
            size = (20, 20)
            intersection_box = pygame.Rect(
                    intersection_coords[0] - size[0]//2,
                    intersection_coords[1] - size[1]//2,
                    size[0],
                    size[1])
            pygame.draw.rect(screen, (255, 0, 255), intersection_box, 1)

    @property
    def damage(self) -> int:
        return super().damage * 1.3