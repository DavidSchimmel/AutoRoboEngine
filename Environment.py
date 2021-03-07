#Simone and David
import sys, pygame
from pygame.draw import circle
import multiprocessing as mp
from Config import Config
import Constants as C
import Debug
from Robot import Robot
from collision_managment import create_environment, render_environment
import numpy as np
from math import sqrt

def render(config, agents):
    if config.SHOW == "ALL":
        for agent in agents:
            agent.draw()
    elif config.SHOW == "BEST":
        agents[0].draw()

def process_agent(agent, board, fitness, a):
    # calculate movement per controller
    agent.controller_process()
    #execute a robot's movement checking the collisions
    _, collision = agent.move()
    if collision:
        fitness[a] = Config.COLLISION_VAL
    clear_room(agent.position, Config.BALL_SIZE, board)
    #update the sensors' measurement
    agent.check_sensors()
    return

def clear_room(c, R, blackboard):
    cx = round(c[0])
    cy = round(c[1])
    #R = round(R*3.7795) #from mm to px
    for x in range(-R, R):
        for y in range( round(-R*sqrt(1-x*x/(R*R))) , round(R*sqrt(1-x*x/(R*R))) ):
            blackboard[ min(blackboard.shape[0]-1, max(0, cx+x)) ][ min(blackboard.shape[1]-1, max(0, cy+y)) ]=1

environments = []
for room_number in range(Config.N_ROOM_EVAL):
    environments.append(create_environment(Config.BOARD_SIZE, room_number, 4))

def simulate_episode(population, show_graphically, generation_counter):
    #population = list of genotype = weights
    config = Config()
    pygame.init()

    size = width, height = config.BOARD_SIZE
    speed = [2, 2]

    screen = pygame.display.set_mode(size)
    all_fitness=[]
    for e in range(Config.N_ROOM_EVAL):
        env=environments[e] #create_environment(size, 4) if we want a new random environment at every execution

        agents = []
        black_board = []
        fitness = []
        norm_term = width*height
        #initialization, we can put it outside if we want to mantain active the pygame instance
        for k in range (config.POPULATION_SIZE):
            robot = Robot(config, \
                pygame, \
                screen, \
                size, \
                env, \
                C.ROBOT_CYAN, \
                [305, 280], \
                90, \
                config.BALL_SIZE, \
                config.MAX_VELOCITY, \
                population[k]) #add parameter population[k] = weights for its nn
            agents.append(robot)
            black_board.append(np.zeros(size, dtype='bool'))
            fitness.append(0)

        for tick in range(config.GENERATION_DURATION): #simulation loop
            flag = False
            for f in fitness:
                if f == 0:
                    flag = True
            if (not flag): #all robot has collided
                break

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
            for a in range(len(agents)):
                if (fitness[a]!=Config.COLLISION_VAL): #If my agent hasn't already collided
                    process_agent(agents[a], black_board[a], fitness, a)

            #if we are working in DEBUG mode, we can see the labels with the sensors' measurement and the robot speed
            if (config.DEBUG):
                for agent in agents:
                    Debug.print_debug_info(screen, "v left: {:0.3f}".format(agent.velocity_left), (agent.position[0], agent.position[1] - 10))
                    Debug.print_debug_info(screen, "v right: {:0.3f}".format(agent.velocity_right), (agent.position[0], agent.position[1] + 10))
                    for sensor in agent.sensors:
                        Debug.print_debug_info(screen, "L: {:0.0f}".format(sensor.length), (sensor.direction_vector[0], sensor.direction_vector[1] - 10))

            if (show_graphically):
                    #update the graphical representation
                    render_environment(screen, pygame, env)
                    render(config, agents)
                    Debug.print_debug_info(screen, "Generation: {:0.3f}".format(generation_counter), (50, 10))
                    pygame.display.flip()

        #finish of the time
        #count board and add the value
        for a in range(len(agents)):
                fitness[a] += np.count_nonzero(black_board[a])/norm_term
        # pool.close()
        all_fitness.append(fitness)

    fitness=np.average(np.array(all_fitness),axis=0).tolist()
    return fitness

if __name__ == '__main__':
    fitness = simulate_episode(0)
    print(fitness)
