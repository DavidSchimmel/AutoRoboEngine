import sys, pygame
from pygame.draw import circle
from Config import Config
import Constants as C
import Debug
from Robot import Robot
from collision_managment import create_environment, render_environment

config = Config()

pygame.init()

size = width, height = config.BOARD_SIZE
speed = [2, 2]

screen = pygame.display.set_mode(size)

env=create_environment(size, 4) #create an environment with 4 obstacles
robot = Robot(config, pygame, screen, size, env, C.ROBOT_CYAN, [400, 400], 90 , 25)

def render(robot, obstacles):
    robot.draw()

while 1: #simulation loop
    #keyboard input manager
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                robot.acellarate(robot.LEFT,   1)
            elif event.key == pygame.K_o:
                robot.acellarate(robot.RIGHT,  1)
            if event.key == pygame.K_s:
                robot.acellarate(robot.LEFT,  -1)
            elif event.key == pygame.K_l:
                robot.acellarate(robot.RIGHT, -1)
            elif event.key == pygame.K_t:
                robot.acellarate(robot.LEFT,   1)
                robot.acellarate(robot.RIGHT,  1)
            elif event.key == pygame.K_g:
                robot.acellarate(robot.LEFT,  -1)
                robot.acellarate(robot.RIGHT, -1)
            elif event.key == pygame.K_x:
                robot.stop()

    #execute a robot's movement checking the collisions
    robot.move()
    #update the sensors' measurement
    robot.check_sensors()
    #update the graphical representation
    render_environment(screen, pygame, env)
    render(robot, [])
    #if we are working in DEBUG mode, we can see the labels with the sensors' measurement and the robot speed
    if (config.DEBUG):
        Debug.print_debug_info(screen, "v left: {:0.3f}".format(robot.velocity_left), (robot.position[0], robot.position[1] - 10))
        Debug.print_debug_info(screen, "v right: {:0.3f}".format(robot.velocity_right), (robot.position[0], robot.position[1] + 10))
        for sensor in robot.sensors:
            Debug.print_debug_info(screen, "L: {:0.0f}".format(sensor.length), (sensor.direction_vector[0], sensor.direction_vector[1] - 10))

    pygame.display.flip()