import math

class Config:
    # general
    DEBUG = False
    SHOW = "ALL" #[ALL, BEST, NONE]
    SHOW_INCREMENT_DISTANCE = 10 # number of generations for saving
    KEYBOARD_MOVEMENT = 0 # 0=prohibited, 1=permitted

    # Board
    BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 1024, 760
    # FRAMES_PER_SECOND = 30

    OBSTACLE_COLOUR = (255, 255, 0)

    # Robot
    ACCELERATION     = 0.005
    BALL_SIZE        = 25
    MAX_VELOCITY     = math.inf
    SENSOR_COUNT     = 12
    SENSOR_FREQUENCY = 30
    SENSOR_RANGE     = 200
    SENSOR_COLOUR    = (0, 255, 0)
    MAX_SPEED        = 15

    # Evolutionary Algorithm
    POPULATION_SIZE = 10
    GENERATION_DURATION = 600
    GENERATION_COUNT = 50
    VELOCITY_QUEUE_LENGTH = 30