# General
FPS = 60
SHOW_HITBOX = False
PROB_ZOMBIE_SPAWN = 0.08

# Terrain
SIZE = WIDTH, HEIGHT = 1280, 720
AGE_MAX_TROU = 16
CASE_SIZE = 50
BORDER_SIZE = 5

# Potatoes
CHANCE_POTATO = 1
PROBA_PATATE= 2

# Pigs
NB_ELEM_X = WIDTH // CASE_SIZE
NB_ELEM_Y = HEIGHT // CASE_SIZE

print(NB_ELEM_X, NB_ELEM_Y)

POS_TOUR_1=(round(((NB_ELEM_X//2)-(NB_ELEM_X//6))*CASE_SIZE), round(((NB_ELEM_Y//2)-(NB_ELEM_Y//4))*CASE_SIZE))
POS_TOUR_2=(round(((NB_ELEM_X//2)+(NB_ELEM_X//6))*CASE_SIZE), round(((NB_ELEM_Y//2)-(NB_ELEM_Y//4))*CASE_SIZE))
POS_TOUR_3=(round(((NB_ELEM_X//2)-(NB_ELEM_X//6))*CASE_SIZE), round(((NB_ELEM_Y//2)+(NB_ELEM_Y//4))*CASE_SIZE))
POS_TOUR_4=(round(((NB_ELEM_X//2)+(NB_ELEM_X//6))*CASE_SIZE), round(((NB_ELEM_Y//2)+(NB_ELEM_Y//4))*CASE_SIZE))

#POS_TOUR_1=(9*CASE_SIZE,4*CASE_SIZE)
#POS_TOUR_2=(16*CASE_SIZE,4*CASE_SIZE)
#POS_TOUR_3=(9*CASE_SIZE,9*CASE_SIZE)
#POS_TOUR_4=(16*CASE_SIZE,9*CASE_SIZE)

TOURS = [POS_TOUR_1, POS_TOUR_2, POS_TOUR_3, POS_TOUR_4]

AUTO_DAMAGE_SPEED = 2

# Player
SIZE_PLAYER = CASE_SIZE * 1.1
PLAYER_SPEED = 300 / FPS

# Health bar
DEFAULT_HEALTH_BAR_SIZE = (CASE_SIZE, 10)
DEFAULT_HEALTH_BAR_PADDING = 2

# Zombie

SIZE_ZOMBIE = CASE_SIZE
COLLIDBOX_SIZE = 8
ZOMBIE_SPEED = 1
ZOMBIE_DAMAGE = 10
ZOMBIE_HEALTH = 100

# Fries
HITBOX_FRIES = (10, 10)
FRIES_DAMAGE = 40
FRIES_SIZE = (6, 40)
FRIES_SPEED = 3
