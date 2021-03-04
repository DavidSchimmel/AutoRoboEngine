import sys, pygame
from pygame.draw import circle
import multiprocessing as mp
from Config import Config
import Constants as C
import Debug
from Robot import Robot
from collision_managment import create_environment, render_environment

def render(agents):
    if config.SHOW == "ALL":
        for agent in agents:
            agent.draw()
    elif config.SHOW == "BEST":
        agents[0].draw()

def process_agent(agent):
    # calculate movement per controller
    agent.controller_process()
    #execute a robot's movement checking the collisions
    agent.move()
    #update the sensors' measurement
    agent.check_sensors()
    return

if __name__ == '__main__':
    # mp.freeze_support()
    # pool = mp.Pool(mp.cpu_count())

    config = Config()
    pygame.init()


    size = width, height = config.BOARD_SIZE
    speed = [2, 2]

    screen = pygame.display.set_mode(size)

    env=create_environment(size, 4) #create an environment with 4 obstacles

    agents = []
    for k in range (config.POPULATION_SIZE):
        robot = Robot(config, pygame, screen, size, env, C.ROBOT_CYAN, [400, 400], 90 , 25)
        agents.append(robot)


    for tick in range(config.GENERATION_DURATION): #simulation loop
        #keyboard input manager
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if config.KEYBOARD_MOVEMENT==1 and event.type == pygame.KEYDOWN:
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


        #temp = [pool.apply(process_agent, args=(agent)) for agent in agents]
        #pool.map(process_agent, [agent for agent in agents])
        for agent in agents:
            process_agent(agent)

        render_environment(screen, pygame, env)

        #update the graphical representation
        render(agents)

        #if we are working in DEBUG mode, we can see the labels with the sensors' measurement and the robot speed
        if (config.DEBUG):
            for agent in agents:
                Debug.print_debug_info(screen, "v left: {:0.3f}".format(agent.velocity_left), (agent.position[0], agent.position[1] - 10))
                Debug.print_debug_info(screen, "v right: {:0.3f}".format(agent.velocity_right), (agent.position[0], agent.position[1] + 10))
                for sensor in agent.sensors:
                    Debug.print_debug_info(screen, "L: {:0.0f}".format(sensor.length), (sensor.direction_vector[0], sensor.direction_vector[1] - 10))

        pygame.display.flip()

    # pool.close()