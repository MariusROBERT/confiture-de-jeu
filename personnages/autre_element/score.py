import pygame

class Score:
    def __init__(self,coords,max:int=100,value=0,size=(50,20),color=(0,255,0),border_size=4):
        self.coords=coords
        self.value=value
        self.size=size
        self.max=max
        self.border_size=border_size
        self.color=color
        self.colored_rect = None
        self.move_to(coords)
        self.update()
        
    
    @property
    def score(self)->int:
        return self.value

    def update(self):
        self.colored_rect = pygame.Rect(
            self.colored_rect_coords,
            (self.value / self.max * self.colored_rect_max_size[0], self.colored_rect_max_size[1]))
        self.main_rect = pygame.Rect(self.coords, self.size)

    def move_to(self, coords):

        self.colored_rect_coords = (
            coords[0] + self.border_size,
            coords[1] + self.border_size
        )
        self.colored_rect_max_size = (
            self.size[0] - 2*self.border_size,
            self.size[1] - 2*self.border_size
        )
        self.coords = coords
        self.update()

    def display(self,screen:pygame.Surface):
        pygame.draw.rect(screen, (0, 0, 0), self.main_rect)
        pygame.draw.rect(screen, self.color, self.colored_rect)
