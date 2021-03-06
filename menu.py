import sys
from pygame.locals import *
from lib.lib import *

pygame.font.init()
from personnages.autre_element.text import Text
from constantes import WIDTH, HEIGHT, SIZE
from personnages.terrain import Terrain
from personnages.player import AutoPlayer, Player
from personnages.zombie import Zombie
import managers.sound_manager as sound_manager
from personnages.pig import Pig

pygame.init()

screen = pygame.display.set_mode(SIZE, 0, 32)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
button_credits = None

TICKEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TICKEVENT, 1000)

TICKEVENT100 = pygame.USEREVENT + 3
pygame.time.set_timer(TICKEVENT100, 100)

TICKEVENT50 = pygame.USEREVENT + 3
pygame.time.set_timer(TICKEVENT50, 50)

TICKEVENT10 = pygame.USEREVENT + 4
pygame.time.set_timer(TICKEVENT10, 5)

user_events = [
    TICKEVENT10,
    TICKEVENT100,
    TICKEVENT
]

FAST_TICK = pygame.USEREVENT + 5
pygame.time.set_timer(FAST_TICK, 20)
POS_BTN = (WIDTH - 100, HEIGHT - 75)
mode = 0


def menu_event_loop(screen2: pygame.display, clock, elements, user_events):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                pos = pygame.mouse.get_pos()
                if button_credits.in_hitbox(pos):
                    global mode
                    if mode == 0:
                        mode = 1
                    else:
                        mode = 0

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
                        element.tick_update_100()

                    except AttributeError:
                        pass
                    except TypeError:
                        element.tick_update_100(elements)
        if event.type == user_events[len(user_events) - 1]:
            for key in elements.keys():
                for element in elements[key]:
                    try:
                        element.tick_update()
                    except AttributeError:
                        pass
                    except TypeError:
                        try:
                            element.tick_update(elements)
                        except TypeError:
                            element.tick_update()

        if event.type == FAST_TICK:
            for key in elements.keys():
                for element in elements[key]:
                    try:
                        element.tick_update_fast()
                    except AttributeError:
                        pass
                    except TypeError:
                        element.tick_update_fast(elements)


def display_credits(elements, screen):
    for elem in elements["displayable"]:
        try:
            elem.display(screen)
        except Exception as e:
            pass
    pygame.display.flip()


def menu_display_loop(screen2: pygame.display, elements):
    global mode

    for key in elements.keys():
        if key != "text" or mode == 0:
            for element in elements[key]:
                element.display(screen2)


def tutorial(screen):
    terrain = Terrain()
    player = Player()
    hint = Text((WIDTH / 2, 30), "Utilisez ZQSD pour vous deplacer", size=15, color=(255, 255, 255),
                centerd_around_coords=True)
    mooved = 0
    elements = {
        "terrain": [terrain],
        "pigs": [],
        "zombies": [],
        "player": [player],
        "fries": [],
        "fx_manager": []
    }
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                player.move(event, elements)
                player.update(elements)

                if mooved == 0:
                    mooved = 1
                    elements["pigs"].append(Pig(WIDTH / 2, HEIGHT - 100))
                    hint = Text((WIDTH / 2, 60), "Ramassez les patates et donnez les au cochons avec ESPACE", size=13,
                                color=(255, 255, 255), centerd_around_coords=True)
                if event.key == K_RETURN:
                    return None
        for i in range(3):
            player.update(elements)

        screen.fill((70, 166, 0))
        terrain.display(screen)
        player.display(screen)
        player.digging = False
        hint.display(screen)
        try:
            elements["pigs"][0].display(screen)
            health = elements["pigs"][0].health
            elements["pigs"][0].update(elements)

            if health > 30:
                mooved = 3
                hint = Text((WIDTH / 2, 60), "Appuyez sur entree pour quitter le tutoriel", size=15,
                            color=(255, 255, 255), centerd_around_coords=True)
        except IndexError:
            pass
        pygame.display.flip()


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
    sound_manager.sound_menu(pygame)
    main_title = Text(
        (WIDTH // 2, 100),
        "FRIES NIGHT AT PIGGIES",
        "menu.ttf",
        size=30,
        centerd_around_coords=True,
        floating_effect=True,
        max_grow=1.14
    )
    menu_elements["text"].append(main_title)

    hint = Text((WIDTH // 2, 180), "Appuyez sur Entree pour lancer une partie", "menu.ttf", size=15,
                centerd_around_coords=True, color=(255, 255, 255))
    menu_elements["text"].append(hint)
    global button_credits
    button_credits = Text(POS_BTN, "CREDIT", "menu.ttf", size=15, centerd_around_coords=True, color=(255, 255, 255))
    menu_elements["text"].append(button_credits)
    return menu_elements


def menu_logic_loop(elements):
    for key in elements.keys():
        for element in elements[key]:
            element.update(elements)


def main_menu(screen2: pygame.display = screen, clock=clock, user_events=user_events):
    pygame.font.init()
    menu_elements = init_menu_elements()
    code = None
    global mode
    tutorial(screen)
    credits_elem = {
        "displayable": [
            Text((WIDTH / 2, 60), "CREDIT", size=30, centerd_around_coords=True, color=(255, 255, 255)),
            Text((30, 100), "Developpeurs", size=20, color=(255, 255, 255)),
            Text((40, 150), "ROBERT Marius", size=15, color=(255, 255, 255)),
            Text((40, 200), "MATHIAN Thibault", size=15, color=(255, 255, 255)),
            Text((40, 250), "LEFRANC Nicolas", size=15, color=(255, 255, 255)),
            Text((40, 300), "PIERNAS Loic", size=15, color=(255, 255, 255)),
            Text((30, 400), "Graphisme", size=20, color=(255, 255, 255)),
            Text((40, 450), "Fait maison", size=15, color=(255, 255, 255)),
            Text((30, 550), "Musiques et bruitage", size=20, color=(255, 255, 255)),
            Text((40, 600), "Sound fishing", size=15, color=(255, 255, 255)),
            Text((40, 650), "La sonoteque org", size=15, color=(255, 255, 255)),
            Text(POS_BTN, "Retour ", size=15, centerd_around_coords=True, color=(255, 255, 255))
        ],
    }

    while code is None:
        screen2.fill((70, 166, 0))
        code = menu_event_loop(screen2, clock, menu_elements, user_events)
        menu_logic_loop(menu_elements)

        menu_display_loop(screen2, menu_elements)
        if mode == 1:
            display_credits(credits_elem, screen2)
        clock.tick(60)
        pygame.display.flip()
    return code
