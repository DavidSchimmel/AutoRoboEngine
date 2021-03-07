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
    POPULATION_SIZE = 10 #number of individuals
    GENERATION_DURATION = 600 #steps in simulation
    GENERATION_COUNT = 50
    NUM_GENERATION = 10 #number of generations
    N_ROOM_EVAL = 3 #number of room on which an individual is tested
    VELOCITY_QUEUE_LENGTH = 30
    MUTATION_RATE = 0.1 
    N_BEST = 3
    NN_LAYER_NODES = [15,2]
    COLLISION_VAL = -0.5
     #penalty given for a collision
    