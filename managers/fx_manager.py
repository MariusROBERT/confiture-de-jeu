import pygame
from constantes import OPACITY_NIGHT, POINTS_PER_ZOMBIE_DEAD, SIZE_PLAYER, SIZE_ZOMBIE, WIDTH, HEIGHT
from constantes import POINTS_PER_ZOMBIE_HIT
from lib.lib import circle_surf, load_animation, load_image
from lib.lib import create_transparent_animation, load_animation, load_image
from managers.events_const import CHANGE_NIGHT, DAMAGE_EVENT, DAMAGED_ZOMBIE, DEAD_ZOMBIE, PLAYER_WALKING
from managers.sound_manager import COLLECT_POTATOE

# EVENT DE 20 A 30 reservés


DAMAGE_DURATION = 8

SIZE_EXPLOSION = (SIZE_PLAYER * 3, SIZE_PLAYER * 3)
EXPLOSION_ANIMATION = load_animation(
    "particle/explosion", SIZE_EXPLOSION)

SIZE_BLOOD = (SIZE_ZOMBIE, SIZE_ZOMBIE)
BLOOD_ANIMATION = load_animation(
    "particle/blood", SIZE_BLOOD)

SIZE_DUST = (SIZE_PLAYER, SIZE_PLAYER)
DUST_ANIMATION = load_animation(
    "particle/dust", SIZE_BLOOD)


font = pygame.font.SysFont("Arial", 20)
DEAD_ZOMBIE_POINTS = [font.render("+{}".format(POINTS_PER_ZOMBIE_DEAD),
                                  True, pygame.Color(255, 75, 75, a=255-int(i * 51))) for i in range(5)]
# TODO: Faire marcher la transparence


class Particle:
    def __init__(self, animation, coords, lifespan=None):
        self.animation = animation
        self.coords = coords
        self.on = True
        self._frame_number = 0
        self.old = 0

        if lifespan is not None:
            self.lifespan = lifespan
        else:
            self.lifespan = len(animation)

    @property
    def frame_number(self):
        return self._frame_number

    @frame_number.setter
    def frame_number(self, value):
        self.old += 1
        if value >= len(self.animation):
            self._frame_number = len(self.animation) - 1
        else:
            self._frame_number = value

        if self.old > self.lifespan:
            self.on = False

    @property
    def frame(self):
        return self.animation[self._frame_number]


class Fx_manager:
    def __init__(self):
        self.damage_screen = create_transparent_animation(
            load_image("red.png", (WIDTH, HEIGHT)))
        self.damage_screen_old = 0
        self.damage_screen_on = False

        #self.nuit_screen = load_image("nuit.png", (WIDTH, HEIGHT))
        self.nuit_screen = pygame.Surface((WIDTH, HEIGHT))
        self.nuit_screen.fill((0, 0, 0))
        self.nuit_screen.set_alpha(OPACITY_NIGHT)
        self.nuit_screen_on = False

        # Explosion
        self.particles = []

    def event_manager(self, event: pygame.event.Event, elements):
        if event.type == DAMAGE_EVENT:
            # return
            self.damage_screen_on = True
        elif event.type == CHANGE_NIGHT:
            self.nuit_screen_on = not self.nuit_screen_on
        elif event.type == "never":
            pos = (elements["player"][0].center_coords[0] -
                   SIZE_EXPLOSION[0] / 2, elements["player"][0].center_coords[1] - SIZE_EXPLOSION[1] / 2)
            self.particles.append(
                Particle(EXPLOSION_ANIMATION, pos))
        elif event.type == DAMAGED_ZOMBIE:
            self.particles.append(Particle(BLOOD_ANIMATION, event.coords))

        elif event.type == DEAD_ZOMBIE:
            self.particles.append(Particle(
                DEAD_ZOMBIE_POINTS, (event.coords[0], event.coords[1] - SIZE_ZOMBIE / 2)))
        # if event.type == PLAYER_WALKING:  ( deplacé dans terrain)
        #     self.particles.append(Particle(DUST_ANIMATION, event.coords))

    def tick_update_50(self, elements):

        for particle in self.particles:
            particle.frame_number += 1
            if not particle.on:
                self.particles.remove(particle)

    def tick_update_100(self, elements):
        if self.damage_screen_on:
            self.damage_screen_old += 1
            if self.damage_screen_old > DAMAGE_DURATION:
                self.damage_screen_on = False
                self.damage_screen_old = 0

    def update(self, elements):
        pass

    def display(self, screen: pygame.Surface, elements):

        if self.damage_screen_on:

            transparence = 255 - \
                (self.damage_screen_old * 255 // DAMAGE_DURATION)

            screen.blit(self.damage_screen[transparence], (0, 0))

        for particle in self.particles:
            screen.blit(particle.frame, particle.coords)

        if self.nuit_screen_on:
            screen.blit(self.nuit_screen, (0, 0))

        player = elements["player"][0]
        radius = player.size[0] * 5

        if self.nuit_screen_on:
            screen.blit(circle_surf(radius, (20, 20, 60)),
                        (player.center_coords[0] - radius, player.center_coords[1] - radius), special_flags=pygame.BLEND_RGB_ADD)
