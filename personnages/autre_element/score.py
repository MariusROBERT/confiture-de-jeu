"""import pygame
pygame.font.init()
my_font=pygame.font.SysFont('Comic Sans MS',30)

class Score:
    def __init__(self,coords,value=0,size=(50,20),text:str(text),color(200,0,0)):
        self.coords=coords
        self.value=value
        self.size=size
        self.text=text
        self.color=color
        self.update()    
    
    @property
    def score(self)->int:
        return self.value

    def update(self):
        text=my_font.render(str(self.value),True,(255,255,255))

    def display(self,screen:pygame.Surface):
        screen.blit(text,self.coords)"""