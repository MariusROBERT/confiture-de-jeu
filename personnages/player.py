from re import M
import pygame
import os
from constantes import BORDER_SIZE, CASE_SIZE, DAMAGE_ZOMBIE_PER_TICK, DEFAULT_HEALTH_BAR_SIZE, FPS, PLAYER_SPEED, \
    DEBUG_MODE, TOURS, WIDTH, HEIGHT, SIZE_PLAYER, PLAYER_MAX_HP
from lib.animated import Animated
from lib.lib import *
from lib.player import dir_to_angle
from managers.events_const import COLLECT_POTATOE, DIG, INVALID_ACTION, PLAYER_WALKING, USE_ZONE_DAMAGE
from managers.fx_manager import DAMAGE_EVENT
from personnages.potatoes import POTATO_ZONE_DAMAGE, PotatoesCode
from personnages.terrain import Terrain
from .autre_element.health_bar import HealthBar
import managers.sound_manager as sound_manager
from managers.sound_manager import PLAYER_DEAD_EVENT

directions = ["up", "down", "left", "right", "up", "down", "left", "right"]
keys = [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d,
        pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
mini_potatoes_images = []


def init_mini_potatoes_images():
    global mini_potatoes_images
    for i in range(4):
        mini_potatoes_images.append(load_image(
            "/player/autre/potatoemini{}.png".format(i), (20, 20)))
        if DEBUG_MODE:
            print(i)


class Player(Animated):
    def __init__(self):
        super().__init__("player", (SIZE_PLAYER, SIZE_PLAYER))
        self.inventory_potatoes = []
        self.inventory_power_ups = []

        self._current_animation = "walk"

        if len(mini_potatoes_images) == 0:
            init_mini_potatoes_images()

        self.size = (SIZE_PLAYER, SIZE_PLAYER)
        self.coords = (WIDTH / 2, HEIGHT / 2)

        self._speed = PLAYER_SPEED
        self.direction = []
        self.pending_direction = []
        self.__alive = True

        self.time_since_dig = 0
        self._digging = False
        self._paused_animation = ""
        self._latest_movement_vector = (0, 0)
        self.time_since_move = 0
        self.__old_angle = 0
        hp = PLAYER_MAX_HP
        new_health_bar = HealthBar(
            (50, 10), max=hp, value=hp, color=(159, 3, 1))
        self._health_bar = new_health_bar
        self.__health = hp

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, hp) -> None:
        if not self.alive:
            self.current_animation = "dead"
            return
        if hp < self.__health and self.__health > 0:
            queue_event(DAMAGE_EVENT)
        if hp <= 0:  # and self.__alive:
            self.__health = 0
            self.__alive = False
            self.current_animation = "dead"
            queue_event(PLAYER_DEAD_EVENT)

        elif hp >= PLAYER_MAX_HP:
            self.__health = PLAYER_MAX_HP
        else:
            self.__health = hp

        self._health_bar.health = self.__health
        self._health_bar.update()

    @property
    def latest_movement_vector(self):
        return self._latest_movement_vector

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

    def dig(self, terrain: Terrain):
        self.digging = True
        queue_event(DIG)
        found = terrain.harvrest(self.center_coords)
        if found >= 0 and len(self.inventory_potatoes) < 5:
            # self.inventory_potatoes.append(found)
            queue_event(COLLECT_POTATOE)
            # Heal 5hp if full inventory
            if found != PotatoesCode.POTATO_ZONE_DAMAGE.value:
                if len(self.inventory_potatoes) >= 5:
                    self.health += 5
                else:
                    self.inventory_potatoes.append(found)

            elif found == PotatoesCode.POTATO_ZONE_DAMAGE.value:
                if DEBUG_MODE:
                    print("wesh")
                if len(self.inventory_power_ups) < 3:
                    self.inventory_power_ups.append(found)

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
                    if len(self.inventory_potatoes) > 0:
                        for pig in elements["pigs"]:
                            if pig.hitbox_feed.colliderect(self.hitbox):
                                pig.feed(food=self.inventory_potatoes.pop())
                                feeded = True
                                break

                # si il est dans la hitbox d'une potatoe
                if not feeded:
                    self.dig(elements["terrain"][0])
            if event.key == pygame.K_b:
                if len(self.inventory_power_ups) > 0:
                    queue_event(USE_ZONE_DAMAGE, {
                                "center_coords": self.center_coords})
                    for zombie in elements["zombies"]:
                        size_zone_damage = SIZE_PLAYER * 2
                        zone_damage = pygame.Rect(self.center_coords[0] - size_zone_damage,
                                                  self.center_coords[1] -
                                                  size_zone_damage,
                                                  size_zone_damage * 2 + 1, size_zone_damage * 2 + 1)

                        if zone_damage.colliderect(zombie.hitbox_degats):
                            zombie.health = -1
                    self.inventory_power_ups.pop()
                else:
                    queue_event(INVALID_ACTION)

        elif event.type == pygame.KEYUP:
            for i in range(len(directions)):
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

        if len(self.direction) > 0:
            queue_event(PLAYER_WALKING, {"coords": self.coords})

    def update(self, elements: dict) -> None:
        # Effectue les deplacement
        old_coords = self.coords
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
        self._latest_movement_vector = self.coords[0] - \
            old_coords[0], self.coords[1]-old_coords[1]

    def display(self, screen, angle=None, night=False) -> None:
        if angle is None:
            angle = dir_to_angle(self.direction)

        rotated_image = pygame.transform.rotate(self.sprite, angle)
        new_rect = rotated_image.get_rect(
            center=self.sprite.get_rect(topleft=self.coords).center)
        screen.blit(rotated_image, new_rect)

        if DEBUG_MODE:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
        i = 0
        for potato_code in self.inventory_potatoes:
            screen.blit(mini_potatoes_images[potato_code],
                        (self.coords[0] + i * 20, self.coords[1] - 20))
            i += 1

        for i in range(len(self.inventory_power_ups)):
            screen.blit(
                mini_potatoes_images[PotatoesCode.POTATO_ZONE_DAMAGE.value], (self.coords[0] + i * 20, self.coords[1] - (20 * 2) - 5))

        self._health_bar.display(screen)


MODE_Z_ESCAPE = 0
MODE_POTATOES = 1
MODE_MIDDLE = 3


class AutoPlayer(Player):
    def __init__(self, coords: tuple = (0, 0), max_angle: int = 23):
        super().__init__()
        self.__nearest_zombie = None
        self.__nearest_potatoe = None
        self.__max_angle = max_angle
        self.__moving_vector = (1, 1)
        self.__wanted_moving_vector = (1, 1)
        self.__vision = 250
        self.__safe_distance = 100
        self.__mode = MODE_MIDDLE
        self._health_bar.hide()
        self.update_moving_vector()

    @ property
    def speed(self):
        return 5

    @ property
    def moving_vector(self):
        return self.__moving_vector

    def update_mode(self):

        if self.__nearest_zombie is None or \
                self.__nearest_zombie.health <= 0 or \
                distance_between(self.__nearest_zombie.coords, self.coords) > self.__safe_distance:

            if self.__nearest_potatoe is not None:
                self.__mode = MODE_POTATOES

            else:
                self.__mode = MODE_MIDDLE
        else:
            self.__mode = MODE_Z_ESCAPE

    def update_moving_vector(self):
        old_vector = self.__moving_vector
        correction_vector = self.__moving_vector

        if correction_vector[0]*50 + self.coords[0] + self.size[0] >= WIDTH \
                or correction_vector[0]*50 + self.coords[0] <= 0 \
                or correction_vector[1]*50 + self.coords[1] + self.size[1] >= HEIGHT \
                or correction_vector[1]*50 + self.coords[1] <= 0:
            self.__mode = MODE_MIDDLE
        new_vector = None
        if self.__mode == MODE_Z_ESCAPE:
            if self.__nearest_zombie is None or self.__nearest_zombie.health <= 0:
                self.update_mode()
                self.update_moving_vector()
            else:
                new_vector = vector_to_target(
                    self.__nearest_zombie.coords, self.coords, -self.speed)
        elif self.__mode == MODE_POTATOES:
            if self.__nearest_potatoe is None:
                self.update_mode()
                self.update_moving_vector()
            else:
                target_coords = (
                    self.__nearest_potatoe.coords[0] + CASE_SIZE / 2,
                    self.__nearest_potatoe.coords[1] + CASE_SIZE / 2)
                new_vector = vector_to_target(
                    target_coords, self.center_coords, self.speed)

        else:
            target_coords = (WIDTH/2, HEIGHT/2)
            new_vector = vector_to_target(
                target_coords, self.center_coords, self.speed)

        if new_vector is None:
            new_vector = (0.0000001, 0.00000001)
        self.__wanted_moving_vector = new_vector
        # self.__moving_vector = new_vector
        self.__moving_vector = intermediate_vector(
            old_vector, new_vector, max_angle=self.__max_angle, norm=self.speed)

    def update(self, elements):
        terrain = elements["terrain"][0]

        if (self.__nearest_zombie is None or
           distance_between(self.center_coords, self.__nearest_zombie.coords) > self.__safe_distance) and \
                self.__nearest_potatoe is not None and distance_between(self.__nearest_potatoe.coords, self.center_coords) < CASE_SIZE:
            self.dig(terrain)
        self.__nearest_zombie = nearest_zombie(
            elements["zombies"], self.center_coords)
        self.__nearest_potatoe = nearest_zombie(
            terrain.potatoes, self.center_coords)

        if self.__moving_vector is not None:
            self.coords = (self.coords[0] + self.moving_vector[0],
                           self.coords[1] + self.moving_vector[1])
        terrain = elements["terrain"][0]

    def tick_update_100(self, elements):
        super().tick_update_100(elements)
        self.update_moving_vector()

    def display(self, screen):
        angle = 0
        if self.__moving_vector is not None:
            angle = g_angle(self.moving_vector, (0, 1))
            if self.moving_vector[0] <= 0:
                angle = -angle
        if DEBUG_MODE:
            rect = pygame.Rect(self.center_coords[0] + self.moving_vector[0]
                               * 50, self.center_coords[1] + self.moving_vector[1]*50, 20, 20)
            pygame.draw.rect(screen, (0, 0, 255), rect, 1)
            rect = pygame.Rect(self.center_coords[0] + self.__wanted_moving_vector[0]
                               * 50, self.center_coords[1] + self.__wanted_moving_vector[1]*50, 15, 15)
            pygame.draw.rect(screen, (0, 255, 255), rect, 1)
        super().display(screen, angle)

    def tick_update(self, elements):
        terrain = elements["terrain"][0]
        self.update_mode()

    def tick_update_fast(self, elements):
        terrain = elements["terrain"][0]
