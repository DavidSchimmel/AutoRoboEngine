import math

class Config:
    # general
    DEBUG = False
    SHOW = "ALL" #[ALL, BEST, NONE]
    SHOW_INCREMENT_DISTANCE = 3 # number of generations for saving
    KEYBOARD_MOVEMENT = 0 # 0=prohibited, 1=permitted

    # Board
    BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 760, 570
    # FRAMES_PER_SECOND = 30

    OBSTACLE_COLOUR = (255, 255, 0)

    # Robot
    ACCELERATION     = 0.005
    BALL_SIZE        = 30
    MAX_VELOCITY     = 10
    SENSOR_COUNT     = 12
    SENSOR_FREQUENCY = 30
    SENSOR_RANGE     = 75
    SENSOR_COLOUR    = (0, 255, 0)
    MAX_SPEED        = 50

    # Evolutionary Algorithm
    NUMBER_OF_EXPERIMENTS = 3
    POPULATION_SIZE       = 15
    GENERATION_DURATION   = 360
    GENERATION_COUNT      = 12
    VELOCITY_QUEUE_LENGTH = 10
    MUTATION_RATE         = 0.05

    # Controller related variables
    INITIAL_WEIGHT_RANGE = [-1, 1]