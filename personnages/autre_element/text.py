import pygame
from lib.lib import load_font
from lib.text import rect_size_floating
class Text ():
    def __init__(self, coords : tuple,
                 text : str = "Sample", 
                 font_path : str = "default.ttf",
                 size : int = 2000,
                 color : tuple = (0,0,0),
                 centerd_around_coords : bool = False,
                 floating_effect_speed : int = 1,
                 max_grow :float = 1.02):
        self.__coords = coords
        self.__text = text
        self.__font = load_font(font_path, size)
        self.__color = color
        self.__center_around_coords = centerd_around_coords
        self.__floating_effect_speed = floating_effect_speed
        self.__curent_frame_counter = 0
        self.__max_grow = max_grow
        self.__nb_frame = 40
        self.__font_path = font_path
        self.__size = size
        self.__curent_dimensions = (0,0)

    @property
    def coords(self) -> tuple:
        if self.__center_around_coords:
            return (
                self.__coords[0] - self.__current_dimensions[0]/2,
                self.__coords[1] - self.__current_dimensions[1]/2
            )
        else:
            return self.__coords
    
    @property
    def sprite(self):
        surface = self.font.render(self.__text, False, self.__color)
        print(surface.get_size())
        if self.__floating_effect_speed > 0:
            new_dimension = rect_size_floating(surface.get_size(), self.__max_grow, self.__curent_frame_counter, self.__nb_frame)
            self.__current_dimensions = new_dimension
            surface = pygame.transform.scale(surface, new_dimension)
        return surface
    @property
    def font(self):
        return load_font(self.__font_path, self.__size)
    
    def tick_event_100(self):
        self.__curent_frame_counter += 1 * self.__floating_effect_speed
        if self.__curent_frame_counter >= self.__nb_frame:
            self.__curent_frame_counter = 0

    
    def update(self):
        pass
    
    def display(self, screen: pygame.Surface):
        
        screen.blit( self.sprite, self.coords)