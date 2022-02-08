import pygame


class HealthBar:

    def __init__(self, 
                 coords : tuple, 
                 max : int = 100, 
                 value : int = 100, 
                 size : tuple = (100, 20), 
                 color : tuple = (0, 255, 0),
                 border_size : int = 4,
                 auto_hide : bool = False):
        """Init HealthBar object

        Args:
            coords (tuple): top left coordinates of the health bar
            max (int, optional): max_health. Defaults to 100.
            value (int, optional): initial health. Defaults to 0.
            size (tuple, optional): main size. Defaults to (100, 20).
            color (tuple, optional): color of the colored part of the health bar. Defaults to (0, 255, 0) GREEN.
        """
        self.coords = coords
        self.max = max
        self.value = value
        self.size = size
        self.main_rect = pygame.Rect(self.coords, self.size)
        self.color = color
        self.colored_rect = None
        self.colored_rect_coords = (
            coords[0] + border_size,
            coords[1] + border_size
        )
        self.colored_rect_max_size = (
            size[0] - 2*border_size,
            size[1] - 2*border_size
        )
        self.update()
        self.__auto_hide = auto_hide
    @property
    def health(self) -> int:
        return self.value

    @health.setter
    def health(self, value) -> None:
        if value > self.max:
            value = self.max
        elif value < 0:
            value = 0
        self.value = value
        self.update()
    
    def update(self):
        self.colored_rect = pygame.Rect(
            self.colored_rect_coords, 
            (self.value / self.max * self.colored_rect_max_size[0], self.colored_rect_max_size[1]) )
    
    def display(self, screen : pygame.Surface):
        if not (self.__auto_hide and self.health < 100):
            pygame.draw.rect(screen, (0,0,0), self.main_rect)
            pygame.draw.rect(screen, self.color, self.colored_rect)