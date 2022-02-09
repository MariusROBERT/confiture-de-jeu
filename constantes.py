from json import loads

with open("config.json") as f:
    config = loads(f.read())

# General
FPS = 60
SHOW_HITBOX = config["debug"]
DATAPACK = config["datapack"]
OPACITY_NIGHT = 120
NIGHT_DURATION = 10

# Terrain
SIZE = WIDTH, HEIGHT = 1280, 720
AGE_MAX_TROU = 16
CASE_SIZE = 50
BORDER_SIZE = 5

# Potatoes
CHANCE_POTATO = 1
POTATO_LIFESPAN = 26

# Pigs
NB_ELEM_X = WIDTH // CASE_SIZE
NB_ELEM_Y = HEIGHT // CASE_SIZE

POS_TOUR_1 = (round(((NB_ELEM_X // 2) - (NB_ELEM_X // 6)) * CASE_SIZE),
              round(((NB_ELEM_Y // 2) - (NB_ELEM_Y // 4)) * CASE_SIZE))
POS_TOUR_2 = (round(((NB_ELEM_X // 2) + (NB_ELEM_X // 6)) * CASE_SIZE),
              round(((NB_ELEM_Y // 2) - (NB_ELEM_Y // 4)) * CASE_SIZE))
POS_TOUR_3 = (round(((NB_ELEM_X // 2) - (NB_ELEM_X // 6)) * CASE_SIZE),
              round(((NB_ELEM_Y // 2) + (NB_ELEM_Y // 4)) * CASE_SIZE))
POS_TOUR_4 = (round(((NB_ELEM_X // 2) + (NB_ELEM_X // 6)) * CASE_SIZE),
              round(((NB_ELEM_Y // 2) + (NB_ELEM_Y // 4)) * CASE_SIZE))

TOURS = [POS_TOUR_1, POS_TOUR_2, POS_TOUR_3, POS_TOUR_4]

AUTO_DAMAGE_SPEED = 0.3
DEFAULT_PIG_HEALTH = 30
PIG_MAX_HEALTH = 100

# Player
SIZE_PLAYER = CASE_SIZE * 1.1
PLAYER_SPEED = 300 / FPS
DAMAGE_ZOMBIE_PER_TICK = 0.2

# Health bar
DEFAULT_HEALTH_BAR_SIZE = (CASE_SIZE, 10)
DEFAULT_HEALTH_BAR_PADDING = 2
DEFAULT_HEALTH_BAR_BOTTOM_MARGIN = 5    

# Zombie
SIZE_ZOMBIE = CASE_SIZE
COLLIDBOX_SIZE = 12
DEAD_BODY_LIFESPAN = 10

ZOMBIE_SPEED = 1
ZOMBIE_DAMAGE = 10
ZOMBIE_HEALTH = 100

PROB_ZOMBIE_SPAWN = 0.08
ZOMBIE_SPAWN = 1

# Fries
HITBOX_FRIES = (10, 10)
FRIES_DAMAGE = 20
FRIES_SIZE = (6, 40)
FRIES_SPEED = 10
OVERRIDE_TEA_TIME_ALGORITHM = False
NO_DIRECT_SHOT = False
SPAWN_DELAY = 320
# If True, the tea time algorithm will be disabled
# tea time allow to shoot anticipating zombie movement


# NIGHT

BABY_ZOMBIE_SPAWN_CHANCE = 0.4
BABY_ZOMBIE_SIZE = SIZE_ZOMBIE // 1.4
