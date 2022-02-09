from re import M
import pygame
import os
from constantes import BORDER_SIZE, CASE_SIZE, DAMAGE_ZOMBIE_PER_TICK, DEFAULT_HEALTH_BAR_SIZE, FPS, PLAYER_SPEED, \
    SHOW_HITBOX, TOURS, WIDTH, HEIGHT, SIZE_PLAYER, PLAYER_MAX_HP
from lib.animated import Animated
from lib.lib import *
from lib.player import dir_to_angle
from managers.events_const import COLLECT_POTATOE, DIG
from managers.fx_manager import DAMAGE_EVENT
from .autre_element.health_bar import HealthBar
import managers.sound_manager as sound_manager
from managers.sound_manager import PLAYER_DEAD_EVENT

directions = ["up", "down", "left", "right"]
keys = [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d]


class Player(Animated):
    def __init__(self):
        super().__init__("player", (SIZE_PLAYER, SIZE_PLAYER))
        self.inventory = []

        self._current_animation = "walk"

        self.potatoe_mini = load_image(
            "/player/autre/potatoemini.png", (20, 20))

        self.size = (SIZE_PLAYER, SIZE_PLAYER)
        self.coords = (WIDTH / 2, HEIGHT / 2)

        self._speed = PLAYER_SPEED
        self.direction = []
        self.pending_direction = []
        self.__alive = True

        self.time_since_dig = 0
        self._digging = False
        self._paused_animation = ""

        self.time_since_move = 0
        self.__old_angle = 0
        hp = PLAYER_MAX_HP
        new_health_bar = HealthBar(
            (50, 10), max=hp, value=hp, color=(159, 3, 1))
        self.__health_bar = new_health_bar
        self.__health = hp

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, hp) -> None:

        if hp < self.__health and self.__health > 0:
            queue_event(DAMAGE_EVENT)
        if hp <= 0:  # and self.__alive:
            # TODO: faire que le son de mort se joue qu'une fois
            self.__health = 0
            self.__alive = False
            self.current_animation = "dead"
            queue_event(PLAYER_DEAD_EVENT)

        elif hp >= PLAYER_MAX_HP:
            self.__health = PLAYER_MAX_HP
        else:
            self.__health = hp

        self.__health_bar.health = self.__health

    @property
    def alive(self) -> bool:
        return self.__alive

    @property
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.coords, self.size)

    @property
    def center_coords(self) -> tuple:
        return self.coords[0] + self.size[0] / 2, self.coords[1] + self.size[1] / 2

    @property
    def digging(self) -> bool:
        return self._digging

    @property
    def speed(self) -> int:
        valeur = self._speed
        if len(self.direction) == 2:
            valeur *= 0.8

        if self.time_since_move < 7:
            valeur *= (self.time_since_move + 1) / 7

        return valeur

    @digging.setter
    def digging(self, value: bool) -> None:
        self._digging = value
        if value:
            self._paused_animation = self.current_animation
            self.current_animation = "dig"
        else:
            self.current_animation = self._paused_animation

    def add_direction(self, direction: str) -> bool:
        if direction == "up":
            if not "down" in self.direction and not "up" in self.direction:
                self.direction.append("up")
                return True
        elif direction == "down":
            if not "up" in self.direction and not "down" in self.direction:
                self.direction.append("down")
                return True
        elif direction == "left":
            if not "right" in self.direction and not "left" in self.direction:
                self.direction.append("left")
                return True
        elif direction == "right":
            if not "left" in self.direction and not "right" in self.direction:
                self.direction.append("right")
                return True
        return False

    def dig(self, terrain):
        self.digging = True
        queue_event(DIG)
        if terrain.harvrest(self.center_coords) and len(self.inventory) < 5:
            self.inventory.append("potatoe")
            queue_event(COLLECT_POTATOE)
            # Heal 5hp if full inventory
            if len(self.inventory) == 5:
                self.health += 5

    def move(self, event: pygame.event.Event, elements) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in keys:
                dirrection = directions[keys.index(event.key)]
                if not len(self.direction) >= 2:
                    self.add_direction(dirrection)
                    if len(self.direction) > 0:
                        self.current_animation = "walk"

            for i in range(len(directions)):
                if event.key == keys[i] and not directions[i] in self.direction:
                    self.pending_direction.append(directions[i])

            if event.key == pygame.K_SPACE:
                # Si il est a proximitée d'un pig
                feeded = False
                if self.hitbox.collidelist([element.hitbox_feed for element in elements["pigs"]]) != -1:
                    if len(self.inventory) > 0:
                        for pig in elements["pigs"]:
                            if pig.hitbox_feed.colliderect(self.hitbox):
                                pig.feed()
                                self.inventory.pop()
                                feeded = True
                                break

                # si il est dans la hitbox d'une potatoe
                if not feeded:
                    self.digging = True
                    queue_event(DIG)
                    if elements["terrain"][0].harvrest(self.center_coords) and len(self.inventory) < 5:
                        self.inventory.append("potatoe")
                        queue_event(COLLECT_POTATOE)
                        # Heal 5hp if full inventory
                        if len(self.inventory) == 5:
                            self.health += 5
                    self.dig(elements["terrain"][0])

        elif event.type == pygame.KEYUP:
            for i in range(4):
                if event.key == keys[i]:
                    if directions[i] in self.direction:
                        self.direction.remove(directions[i])
                    elif directions[i] in self.pending_direction:
                        self.pending_direction.remove(directions[i])

            # Ajoute les directions en attente
            if len(self.pending_direction) > 0 and len(self.direction) < 2:
                self.add_direction(self.pending_direction.pop(0))

            if len(self.direction) == 0:
                self.current_animation = "idle"
                self.time_since_move = 0

    def tick_update_100(self, elements) -> None:
        self.current_frame += 1
        if self.digging:
            self.time_since_dig += 1
            if self.time_since_dig > len(self._animation["dig"]):
                self.digging = False
                self.time_since_dig = 0

        if len(self.direction) > 0:
            self.time_since_move += 1

    def update(self, elements: dict) -> None:
        # Effectue les deplacement

        zombies_hitboxs = [
            element.hitbox_degats for element in elements["zombies"]]

        if self.hitbox.collidelist(zombies_hitboxs) != -1:
            self.health -= DAMAGE_ZOMBIE_PER_TICK

        if self._digging or self.health <= 0:
            return

        for direction in self.direction:
            originels = self.coords
            if direction == "up":
                self.coords = (self.coords[0], self.coords[1] - self.speed)
            if direction == "down":
                self.coords = (self.coords[0], self.coords[1] + self.speed)
            if direction == "left":
                self.coords = (self.coords[0] - self.speed, self.coords[1])
            if direction == "right":
                self.coords = (self.coords[0] + self.speed, self.coords[1])
            # Verifie les collisions avec les autres elements ( pigs ) (!!! A mieux optimiser !!!)
            if self.coords != originels:
                if self.hitbox.collidelist([element.hitbox for element in elements["pigs"]]) != -1:
                    self.coords = originels

        # Verifie les collisions avec les bords

        if self.coords[0] < BORDER_SIZE:
            self.coords = (BORDER_SIZE, self.coords[1])
        if self.coords[0] > WIDTH - BORDER_SIZE - self.size[0]:
            self.coords = (WIDTH - BORDER_SIZE - self.size[0], self.coords[1])
        if self.coords[1] < BORDER_SIZE:
            self.coords = (self.coords[0], BORDER_SIZE)
        if self.coords[1] > HEIGHT - BORDER_SIZE - self.size[1]:
            self.coords = (self.coords[0], HEIGHT - BORDER_SIZE - self.size[1])

    def display(self, screen, angle=None) -> None:
        if angle is None:
            angle = dir_to_angle(self.direction)

        rotated_image = pygame.transform.rotate(self.sprite, angle)
        new_rect = rotated_image.get_rect(
            center=self.sprite.get_rect(topleft=self.coords).center)
        screen.blit(rotated_image, new_rect)

        if SHOW_HITBOX:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        for i in range(len(self.inventory)):
            screen.blit(
                self.potatoe_mini, (self.coords[0] + i * 20, self.coords[1] - 20))

        self.__health_bar.display(screen)


class AutoPlayer(Player):
    def __init__(self, coords: tuple = (0, 0), max_angle: int = 10):
        super().__init__()
        self.__nearest_zombie = None
        self.__nearest_potatoe = None
        self.__max_angle = max_angle
        self.__moving_vector = (1, 1)
        self.update_moving_vector()
        self.__safe_distance = 200

    @property
    def speed(self):
        return 6

    @property
    def moving_vector(self):
        return self.__moving_vector

    def update_moving_vector(self):
        old_vector = self.__moving_vector
        if self.__nearest_zombie is None or \
                self.__nearest_zombie.health <= 0 or \
                distance_between(self.__nearest_zombie.coords, self.coords) > self.__safe_distance:

            target_coords = (WIDTH/2, HEIGHT/2)
            if self.__nearest_potatoe is not None:
                target_coords = self.__nearest_potatoe.coords
            v = vector_to_target(target_coords, self.center_coords, self.speed)
            self.__moving_vector = v

        else:
            # Runnaway from the nearest zombie
            to_zombie_vector = vector_to_target(
                self.__nearest_zombie.center_coords, self.center_coords, self.speed)
            np_array = np.array(to_zombie_vector)
            away_from_zombie_array = np_array * -1
            self.__moving_vector = np_to_tuple(away_from_zombie_array)

        self.__moving_vector = intermediate_vector(
            old_vector, self.__moving_vector, max_angle=self.__max_angle)

    def update(self, elements):
        terrain = elements["terrain"][0]
        self.__nearest_zombie = nearest_zombie(
            elements["zombies"], self.center_coords)
        self.__nearest_potatoe = nearest_zombie(
            terrain.potatoes, self.center_coords)
        if (self.__nearest_zombie is None or
           distance_between(self.center_coords, self.__nearest_zombie.center_coords) > self.__safe_distance) and \
                self.__nearest_potatoe is not None and distance_between(self.__nearest_potatoe.coords, self.center_coords) < CASE_SIZE:
            self.dig(terrain)

        self.coords = (self.coords[0] + self.moving_vector[0],
                       self.coords[1] + self.moving_vector[1])
        super().update(elements)

    def tick_update_100(self, elements):
        super().tick_update_100(elements)
        self.update_moving_vector()

    def display(self, screen):
        angle = g_angle(self.moving_vector, (0, 1))
        if self.moving_vector[0] <= 0:
            angle = -angle
        super().display(screen, angle)
