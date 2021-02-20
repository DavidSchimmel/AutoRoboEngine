import math

class Config:
    # general
    DEBUG = True

    # Board
    BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 1024, 760
    # FRAMES_PER_SECOND = 30

    OBSTACLE_COLOUR = (255, 255, 0)

    # Robot
    ACCELERATION = 0.005
    BALL_SIZE = 25
    MAX_VELOCITY = math.inf
    SENSOR_COUNT = 12
    SENSOR_FREQUENCY = 30
    SENSOR_RANGE = 200
    SENSOR_COLOUR = (0, 255, 0)
