from random import random
import Constants as C
from Config import Config
import math
import sys, pygame

config = Config()

#**** Environment obstacles and collisions detection ****#
def create_environment(size, room_number, N_obstacle=4): #create a N_obstacle (random shape, position and dimension) obstacles in the environment
    obstacle_list=[]
    if room_number   == 0:
        pass
    elif room_number == 1:
        obstacle_list.append(('r', (120, size[1]/2 - 50, size[0] - 240 , 20)))
    elif room_number == 2:
        obstacle_list.append(('r', (          160, 100, 20 , size[1] - 200)))
        obstacle_list.append(('r', (size[0] - 180, 100, 20 , size[1] - 200)))
    elif room_number == 3:
        obstacle_list.append(('r', (          160,           120, 60, 60)))
        obstacle_list.append(('r', (          160, size[1] - 160, 60, 60)))
        obstacle_list.append(('r', (size[0] - 200,           120, 60, 60)))
        obstacle_list.append(('r', (size[0] - 200, size[1] - 160, 60, 60)))
    elif room_number == 4: #HIGH evol pressure
        #obstacle_list.append(('r', (400,         400, 20 , 20))) #spam point
        obstacle_list.append(('r', (200,         120, 20 , size[1] - 240)))
        obstacle_list.append(('r', (200,         120, size[1] - 240 , 20)))
        obstacle_list.append(('r', (size[1] - 40,         120, 20 , size[1])))
        obstacle_list.append(('r', (350,         300, 160, 20)))
        obstacle_list.append(('r', (350,         450, 200, 20)))
    elif room_number == 5: #Very easy collision remaining in the spanning place
        #obstacle_list.append(('r', (400,         400, 20 , 20))) #spam point

        obstacle_list.append(('r', (300,         300, 20, size[1]-300)))
        obstacle_list.append(('r', (500,         180, 20, size[1]-180)))
        obstacle_list.append(('r', (170,         180, 330, 20)))
        obstacle_list.append(('r', (170,         180, 20, 160)))
        #obstacle_list.append(('r', (380,         450, 150, 20)))
    else:
        for o in range(N_obstacle):
            if random()<0.0:
                obstacle_list.append(('c',(random()*size[0], random()*size[1]), 10+random()*100))
            else:
                obstacle_list.append(('r',(random()*size[0], random()*size[1], 50+random()*100, 50+random()*100)))

    #add window frame for collision management
    obstacle_list.append(('r', (0, 0, size[0], 2)))
    obstacle_list.append(('r', (0, 0, 2, size[1])))
    obstacle_list.append(('r', (0, size[1]-2, size[0], size[1])))
    obstacle_list.append(('r', (size[0]-2, 0, size[0], size[1])))
    return obstacle_list

def render_environment(screen, pg, ob_list): #print the environment on the screen
    screen.fill(C.BLACK)
    obstacle_color=config.OBSTACLE_COLOUR
    for o in ob_list:
        if o[0]=='r':
            pg.draw.rect(screen, obstacle_color, o[1])
        elif o[0]=='c':
            pg.draw.circle(screen, obstacle_color, o[1], o[2])

def collision_rect(c_start, c, radius, r): #detect a collision with a rectangular obstacle
   left=r[0]
   top=r[1]
   right=left+r[2]
   bottom=top+r[3]
   #check if I'm too close to the obstacle (I'm touching it)
   closestX = left if c[0] < left else (right if c[0] > right else c[0])
   closestY = top if c[1] < top else (bottom if c[1] > bottom else c[1])
   dx = closestX - c[0]
   dy = closestY - c[1]
   if dx==0 and dy==0: return True
   if ( dx * dx + dy * dy ) < radius * radius: return True
   #check if I've jumped the obstacle in one step
   if (get_line_intersection( (c_start,c), ((left, top),(right, top)) )): return True
   if (get_line_intersection( (c_start,c), ((left, bottom),(right, bottom)) )): return True
   if (get_line_intersection( (c_start,c), ((left, top),(left, bottom)) )): return True
   if (get_line_intersection( (c_start,c), ((right, top),(right, bottom)) )): return True
   return False

def collision_circle(c, r, C, R): #detect a collision with a circular obstacle
    dx = c[0] - C[0]
    dy = c[1] - C[1]
    dr = r + R
    if dx==0 and dy==0: return True
    if ( dx * dx + dy * dy ) < dr * dr: return True
    return False


def resolve_collision(start, s, robot_R, ob_list, size): #scan each obstacle in the environment and return True if there is a collision
    for ob in ob_list:
        if ob[0] == 'r':
            if (collision_rect(start, s, robot_R, ob[1])):
                return True
        if ob[0] == 'c':
            if (collision_circle(s, robot_R, ob[1], ob[2])):
                return True
    if s[0]<robot_R or s[0]>size[0]-robot_R or s[1]<0 or s[1]>size[1]-robot_R: return True
    return False

#**** Sensors obstacles collision ****#

def find_intersection(root_vector, direction_vector, radius, obstacle_list): #find a possible intersection with an obstacle
    intersections = []

    for obstacle in obstacle_list:
        if (obstacle[0] != "r"): continue

        left=obstacle[1][0]
        top=obstacle[1][1]
        right=left+obstacle[1][2]
        bottom=top+obstacle[1][3]

        line_1_intersection = get_line_intersection((root_vector, direction_vector), ((left,  bottom), (right, bottom)))
        line_2_intersection = get_line_intersection((root_vector, direction_vector), ((left,  top),    (right, top)))
        line_3_intersection = get_line_intersection((root_vector, direction_vector), ((left,  top),    (left,  bottom)))
        line_4_intersection = get_line_intersection((root_vector, direction_vector), ((right, top),    (right, bottom)))

        if (line_1_intersection != None):# and check_in_range(root_vector, radius, line_1_intersection)):
            intersections.append(line_1_intersection)
        if (line_2_intersection != None):# and check_in_range(root_vector, radius, line_2_intersection)):
            intersections.append(line_2_intersection)
        if (line_3_intersection != None):# and check_in_range(root_vector, radius, line_3_intersection)):
            intersections.append(line_3_intersection)
        if (line_4_intersection != None):# and check_in_range(root_vector, radius, line_4_intersection)):
            intersections.append(line_4_intersection)

    return intersections

def get_line_intersection(line1, line2): #get the intersection between two 2D lines
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if (check_range(x, y, line2[0], line2[1]) and check_range(x, y, line1[0], line1[1])):
        return x, y

    return None

def check_range(x, y, start_point, end_point): #prevent misclarification in the sensor when a collision contact point is exactly in the same position
    epsilon = 0.0000001
    if x + epsilon < min(start_point[0], end_point[0]): return False
    if x - epsilon > max(start_point[0], end_point[0]): return False
    if y + epsilon < min(start_point[1], end_point[1]): return False
    if y - epsilon > max(start_point[1], end_point[1]): return False

    return True

def get_line_normal_form(x1, x2, y1, y2):
    if ((x2 - x1) == 0): # FIXME handle logics for y axis parallels
        a = 0.000000000001
    else:
        a = (y2 - y1) / (x2 - x1)
    b = y1 - (x1 * a)
    return a, b


if __name__=='__main__': #Render a room
    pygame.init()
    screen = pygame.display.set_mode(Config.BOARD_SIZE)
    env = create_environment(Config.BOARD_SIZE, 5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        render_environment(screen, pygame, env)
        pygame.display.flip()