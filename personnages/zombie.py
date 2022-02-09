import string
import pygame
from lib.lib import get_angle_between_vectors, np_to_tuple, queue_event, normalize_vector
from lib.zombie import get_direction, get_target, randomCoords
from .autre_element.health_bar import HealthBar
from constantes import DEAD_BODY_LIFESPAN, WIDTH, HEIGHT, CASE_SIZE, TOURS, DEFAULT_HEALTH_BAR_SIZE, DEFAULT_HEALTH_BAR_BOTTOM_MARGIN
from lib.animated import Animated
import numpy
from constantes import SHOW_HITBOX, WIDTH, HEIGHT, CASE_SIZE, TOURS
from constantes import ZOMBIE_SPEED, COLLIDBOX_SIZE, SIZE_ZOMBIE, ZOMBIE_DAMAGE, ZOMBIE_HEALTH
import py_sounds


class Zombie(Animated):
    def __init__(self, speed: int = ZOMBIE_SPEED, name: string = "Zombie",
                 damage: int = ZOMBIE_DAMAGE, hp: int = ZOMBIE_HEALTH, coords: tuple = None,
                 size: tuple = (CASE_SIZE, CASE_SIZE)):
        self.health_bar_size = (size[0], DEFAULT_HEALTH_BAR_SIZE[1])
        new_health_bar = HealthBar(
            (-1000, -1000),
            size=self.health_bar_size,
            max=hp,
            value=hp,
            color=(255, 30, 255),
            auto_hide=True)
        self.__health_bar = new_health_bar

        super().__init__("zombie", (SIZE_ZOMBIE, SIZE_ZOMBIE))

        self.__name = name
        self.__health = hp
        self.damage = damage
        self.speed = speed
        self.alive = True
        self.size = size
        self.dead = False
        self._time_since_dead = 0
        self.angle = 0
        self.__latest_movement_vector = (0, 0)
        self.current_animation = "walk"

        if coords is None:
            self.__coords = randomCoords()
        else:
            self.__coords = coords

        # generating health bar for zombie

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, hp) -> None:
        if hp <= 0:
            self.__health = 0
            self.dead = True
            self.current_animation = "dead"

            queue_event(py_sounds.DEAD_ZOMBIE)
        else:
            self.__health = hp
        self.__health_bar.health = self.__health

    @property
    def time_since_dead(self) -> int:
        return self._time_since_dead

    @time_since_dead.setter
    def time_since_dead(self, value: int) -> None:
        self._time_since_dead = value
        if (self._time_since_dead) > DEAD_BODY_LIFESPAN:
            self.alive = False

    @property
    def latest_movement_vector(self) -> tuple[int, int]:
        return self.__latest_movement_vector

    @property
    def coords(self) -> tuple[int, int]:
        return self.__coords

    @property
    def center_coords(self) -> tuple[int, int]:
        return (self.coords[0] + self.size[0] // 2, self.coords[1] + self.size[1] // 2)

    @coords.setter
    def coords(self, coords: tuple[int, int]) -> None:

        self.__coords = coords
        center_x = coords[0] + self.size[0] / 2
        health_bar_x = center_x - self.health_bar_size[0] / 2
        health_bar_y = coords[1] - self.health_bar_size[1] - \
            DEFAULT_HEALTH_BAR_BOTTOM_MARGIN
        health_bar_coords = (health_bar_x, health_bar_y)
        self.__health_bar.move_to(health_bar_coords)

    @property
    def hitbox_degats(self) -> pygame.Rect:
        if not self.dead:
            return pygame.Rect(self.coords, self.size)
        else:
            return pygame.Rect((0, 0), (0, 0))

    @property
    def hitbox_collision(self) -> pygame.Rect:
        if not self.dead:
            return pygame.Rect((self.coords[0] + COLLIDBOX_SIZE, self.coords[1] + COLLIDBOX_SIZE),
                               (self.size[0] - 2 * COLLIDBOX_SIZE, self.size[1] - 2 * COLLIDBOX_SIZE))
        else:
            return pygame.Rect((0, 0), (0, 0))

    def is_attacked(self, damage: int) -> None:
        self.health -= damage

    def attack(self, target) -> None:
        target.is_attacked(self.__damage)

    def tick_update(self, elements: tuple) -> None:
        if self.dead:
            self.time_since_dead += 1

    def tick_update_100(self, elements: tuple) -> None:
        self.current_frame += 1

    def display(self, screen: pygame.Surface) -> None:
        # ( A optimiser !!! ) (( si besoin mdr ))
        if self.dead:
            image = self.sprite
            transparence = 255 - (self.time_since_dead *
                                  255 // DEAD_BODY_LIFESPAN)
            image.fill((255, 255, 255, transparence),
                       special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(image, self.__coords)
        else:

            angle = self.angle + 90
            rotated_image = pygame.transform.rotate(self.sprite, angle)
            new_rect = rotated_image.get_rect(
                center=self.sprite.get_rect(topleft=self.coords).center)
            screen.blit(rotated_image, new_rect)

        if not self.dead:
            self.__health_bar.display(screen)
        if SHOW_HITBOX:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox_degats, 1)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox_collision, 1)

    def update(self, elements: dict) -> None:
        if self.dead:
            return

        olds = self.coords
        # Dirrection du player
        direction = get_direction(
            self.coords, get_target(self.coords, elements["player"][0].coords))
        produit = abs(direction[0]) + abs(direction[1])

        # Si le zombie est en colision avec une frite
        if self.hitbox_degats.collidelist([element.hitbox for element in elements["fries"]]) != -1:
            for i in elements["fries"]:
                if i.hitbox.colliderect(self.hitbox_degats):
                    self.is_attacked(self.damage)
                    elements["fries"].remove(i)

        # Direction du zombie
        olds = self.coords
        direction = get_direction(
            self.coords, get_target(self.coords, elements["player"][0].coords))
        produit = abs(direction[0]) + abs(direction[1])

        self.angle = get_angle_between_vectors(direction, (0, 1))
        if direction[0] < 0:
            self.angle = - self.angle
        self.angle -= 90

        if produit != 0:
            direction = (direction[0] / produit, direction[1] / produit)
        else:
            direction = (0, 0)
        direction = numpy.array(direction)
        normalized_vector = normalize_vector(direction)
        movement_vector = np_to_tuple(
            numpy.array(normalized_vector) * self.speed)
        self.__latest_movement_vector = movement_vector
        self.coords = (self.coords[0] + movement_vector[0],
                       self.coords[1] + movement_vector[1])

        zombie_except_me = [
            zombie for zombie in elements["zombies"] if zombie != self]

        if self.hitbox_collision.collidelist([element.hitbox_collision for element in zombie_except_me]) != -1:
            self.coords = olds
