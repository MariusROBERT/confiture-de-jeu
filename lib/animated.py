from constantes import DATAPACK
from lib.lib import load_animation
import os
import pygame


class Animated:
    def __init__(self, name: str, size: tuple):
        self._animation = {}

        animations_names = os.listdir(
            "datapacks/{}/images/{}/" .format(DATAPACK, name))
        filtered_folder_content = [
            animation for animation in animations_names if animation != ".DS_Store"]
        for animation_name in filtered_folder_content:
            self._animation[animation_name] = load_animation(
                f"{name}/{animation_name}", size
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
        if value >= len(self._animation[self.current_animation]):
            self._current_frame = 0

    @property
    def sprite(self) -> pygame.Surface:
        return self._animation[self.current_animation][int(self.current_frame)]
