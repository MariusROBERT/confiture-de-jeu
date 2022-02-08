from lib.lib import load_animation
import os
import pygame


class Animated:
    def __init__(self, name: str, size: tuple):
        self.animation = {}

        animations_names = os.listdir("./images/{}/" .format(name))
        for animation_name in animations_names:
            self.animation[animation_name] = load_animation(
                f"./images/{name}/{animation_name}", size
            )

        self._current_frame = 0

    @property
    def current_animation(self) -> str:
        return self._current_animation

    @current_animation.setter
    def current_animation(self, animation: str) -> None:
        self._current_animation = animation
        self._current_frame = 0

    @property
    def current_frame(self) -> int:
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value: int) -> None:
        self._current_frame = value
        if value >= len(self.animation[self.current_animation]):
            self._current_frame = 0

    @property
    def sprite(self) -> pygame.Surface:
        current_frame = self.current_frame
        return self.animation[self.current_animation][self.current_frame]
