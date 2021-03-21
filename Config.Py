import math

class Config:
    # general
    DEBUG = False
    SHOW = "ALL" #[ALL, BEST, NONE]
    SHOW_INCREMENT_DISTANCE = 1 # number of generations for saving
    KEYBOARD_MOVEMENT = 0 # 0=prohibited, 1=permitted

    # Board
    BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 610, 440
    # FRAMES_PER_SECOND = 30

    OBSTACLE_COLOUR = (255, 255, 0)

    # Robot
    ACCELERATION     = 0.005
    BALL_SIZE        = 25
    MAX_VELOCITY          = 10
    SENSOR_COUNT     = 12
    SENSOR_FREQUENCY = 30
    SENSOR_RANGE          = 50
    SENSOR_COLOUR    = (0, 255, 0)
    MAX_SPEED        = 50

    LANDMARK_RANGE   = 600

    # Evolutionary Algorithm
    NUMBER_OF_EXPERIMENTS = 3
    POPULATION_SIZE       = 22
    GENERATION_DURATION   = 390
    GENERATION_COUNT      = 50
    SAVE_INCREMENT_DISTANCE = 1 #checkpoint
    VELOCITY_QUEUE_LENGTH = 6
    MUTATION_RATE         = 0.05
    RANK_PROPRTIONS       = [8, 6, 4, 2, 1, 1]
    N_ROOM_EVAL           = 6 #number of room on which an individual is tested
    N_BEST                = 3
    COLLISION_VAL         = -0.0001

    # Controller related variables
    NN_LAYER_NODES        = [17,4,2]
    INITIAL_WEIGHT_RANGE  = [-1, 1]
