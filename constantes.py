# General
FPS = 60
SHOW_HITBOX = True
PROB_ZOMBIE_SPAWN = 0.08

# Terrain
SIZE = WIDTH, HEIGHT = 1280, 720
AGE_MAX_TROU = 16
CASE_SIZE = 40
BORDER_SIZE = 5

# Potatoes
CHANCE_POTATO = 2

# Pigs
NB_ELEM_X = WIDTH // CASE_SIZE
NB_ELEM_Y = HEIGHT // CASE_SIZE

POS_TOUR_1 = (5 * CASE_SIZE, 2 * CASE_SIZE)
POS_TOUR_2 = (10 * CASE_SIZE, 2 * CASE_SIZE)
POS_TOUR_3 = (10 * CASE_SIZE, 6 * CASE_SIZE)
POS_TOUR_4 = (5 * CASE_SIZE, 6 * CASE_SIZE)

TOURS = [POS_TOUR_1, POS_TOUR_2, POS_TOUR_3, POS_TOUR_4]
FRIES_SPEED = 16

AUTO_DAMAGE_SPEED = 2


# Player
SIZE_PLAYER = CASE_SIZE/0.8
PLAYER_SPEED = 300 / FPS

# Health bar
DEFAULT_HEALTH_BAR_SIZE     = (CASE_SIZE, 10)
DEFAULT_HEALTH_BAR_PADDING  = 2