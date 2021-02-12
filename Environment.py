import sys, pygame
from pygame.draw import circle
from Config import Config
import Constants as C
from Robot import Robot

config = Config()

pygame.init()

size = width, height = 1024, 768
speed = [2, 2]

screen = pygame.display.set_mode(size)

robot = Robot(config, pygame, screen, (50,50,100), [100, 700], [0, -1] , 25)


"""ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()"""

def render(robot, obstacles):
    screen.fill(C.BLACK)
    robot.draw()

while 1:
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

    robot.move()

    # update()

    render(robot, [])

    pygame.display.flip()