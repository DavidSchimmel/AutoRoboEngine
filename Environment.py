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

def render(robot):
    robot.draw()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                robot.acellarate("left")
            elif event.key == pygame.K_k:
                robot.acellarate("right")

    robot.update_position()


    """ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(C.BLACK)
    screen.blit(ball, ballrect)"""

    # update()
    render(robot)

    pygame.display.flip()