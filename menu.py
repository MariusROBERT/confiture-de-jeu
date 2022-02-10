import pygame, sys
from pygame.locals import *
from lib.lib import *
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
from personnages.autre_element.text import Text
from constantes import WIDTH, HEIGHT, FPS
from personnages.terrain import Terrain
from personnages.player import AutoPlayer
from personnages.zombie import Zombie
FAST_TICK = pygame.USEREVENT + 5
pygame.time.set_timer(FAST_TICK, 20)
def menu_event_loop(screen : pygame.display, clock, elements, user_events):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if event.type == pygame.quit():
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return "Play"
            if event.type == user_events[1]:
                for key in elements.keys():
                    for element in elements[key]:
                        try:
                            element.tick_update_100(elements)
                        except AttributeError:
                            pass
            if event.type == user_events[len(user_events) - 1]:
                for key in elements.keys():
                    for element in elements[key]:
                        try:
                            element.tick_update()
                        except AttributeError:
                            pass
                        except TypeError:
                            element.tick_update(elements)
            if event.type == FAST_TICK:
                for key in elements.keys():
                    for element in elements[key]:
                        try:
                            element.tick_update_fast()
                        except AttributeError:
                            pass
                        except TypeError:
                            element.tick_update_fast(elements)
def menu_display_loop(screen : pygame.display, elements):
    for key in elements.keys():
        for element in elements[key]:
            element.display(screen)
def init_menu_elements():
    menu_elements = {}
    terrain = Terrain()
    menu_elements["terrain"] = [terrain]
    player = AutoPlayer()
    menu_elements["player"] = [player]
    menu_elements["text"] = []
    menu_elements["fries"] = []
    menu_elements["pigs"] = []
    menu_elements["zombies"] = [Zombie() for i in range(3)]
    main_title = Text(
        (WIDTH//2, 100),
        "FRIES NIGHT AT PIGGIES",
        "menu.ttf",
        size=40,
        centerd_around_coords=True,
        floating_effect=True
    )
    menu_elements["text"].append(main_title)
    
    hint = Text((WIDTH//2, 180),"Appuyez sur Entree pour lancer une partie", "menu.ttf", size=15, centerd_around_coords=True, color=(255, 255,255))
    menu_elements["text"].append(hint)
    
    return menu_elements

def menu_logic_loop(elements):
    for key in elements.keys():
        for element in elements[key]:
            element.update(elements)
    
        
def main_menu(screen : pygame.display, clock, user_events):
    pygame.font.init()
    
    menu_elements = init_menu_elements()
    code = None
    while code is None:
        screen.fill((70, 166, 0))
        code = menu_event_loop(screen, clock, menu_elements, user_events)
        menu_logic_loop(menu_elements)
        menu_display_loop(screen, menu_elements)
        clock.tick(60)
        pygame.display.flip()
    return code