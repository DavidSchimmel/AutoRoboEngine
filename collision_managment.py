from random import random
import Constants as C
import math

#**** Environment obstacles and collisions recovery ****#
def create_environment(size, N_obstacle): #create a N_obstacle (random shape, position and dimension) obstacles in the environment
    obstacle_list=[]
    for o in range(N_obstacle):
        if random()<0.5:
            obstacle_list.append(('c',(random()*size[0], random()*size[1]), 10+random()*100))
        else:
            obstacle_list.append(('r',(random()*size[0], random()*size[1], 50+random()*100, 50+random()*100)))
    return obstacle_list

def render_environment(screen, pg, ob_list): #print the environment on the screen
    screen.fill(C.BLACK)
    obstacle_color=(0, 255, 0)
    for o in ob_list:
        if o[0]=='r':
            pg.draw.rect(screen, obstacle_color, o[1])
        elif o[0]=='c':
            pg.draw.circle(screen, obstacle_color, o[1], o[2])

def collision_rect(c, radius, r):
   left=r[0]
   top=r[1]
   right=left+r[2]
   bottom=top+r[3]
   closestX = left if c[0] < left else (right if c[0] > right else c[0])
   closestY = top if c[1] < top else (bottom if c[1] > bottom else c[1])
   dx = closestX - c[0]
   dy = closestY - c[1]
   if dx==0 and dy==0: return True
   if ( dx * dx + dy * dy ) < radius * radius: return True
   return False

def collision_circle(c, r, C, R):
    dx = c[0] - C[0]
    dy = c[1] - C[1]
    dr = r + R
    if dx==0 and dy==0: return True
    if ( dx * dx + dy * dy ) < dr * dr: return True
    return False


def resolve_collision(s, robot_R, ob_list, size):
    for ob in ob_list:
        if ob[0] == 'r':
            if (collision_rect(s, robot_R, ob[1])):
                return True
        if ob[0] == 'c':
            if (collision_circle(s, robot_R, ob[1], ob[2])):
                return True
    if s[0]<robot_R or s[0]>size[0]-robot_R or s[1]<0 or s[1]>size[1]-robot_R: return True
    return False