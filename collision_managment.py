from random import random
import Constants as C
import math

#**** Environment obstacles and collisions recovery ****#
def create_environment(size, N_obstacle): #create a N_obstacle (random shape, position and dimension) obstacles in the environment
    obstacle_list=[]
    for o in range(N_obstacle):
        if random()<0:
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

def collision_rect(c, start, radius, r):
   left=r[0]
   top=r[1]
   right=left+r[2]
   bottom=top+r[3]
   closestX = left if c[0] < left else (right if c[0] > right else c[0])
   closestY = top if c[1] < top else (bottom if c[1] > bottom else c[1])
   closestX_start = left if start[0] < left else (right if start[0] > right else start[0])
   closestY_start = top if start[1] < top else (bottom if start[1] > bottom else start[1])
   if (closestX != closestX_start): closestX=closestX_start
   if (closestY != closestY_start): closestY=closestY_start

   dx = closestX - c[0]
   dy = closestY - c[1]

   collision = False
   if ( dx * dx + dy * dy ) <= radius * radius: #there is a collision
        collision=True

        if dx==0 and dy>=0: theta = math.pi/2
        elif dx==0 and dy<0: theta = -math.pi/2
        else: theta = math.atan(dy/dx)

        delta = radius - math.sqrt(dx*dx + dy*dy)

        d_x = delta*math.cos(theta)
        d_y = delta*math.sin(theta)

        new_x = c[0] - math.copysign(1, dx)*d_x
        new_y = c[1] - math.copysign(1, dy)*d_y
   else:
        new_x=c[0]
        new_y=c[1]
        #v_x=v[0]
        #v_y=v[1]
   return new_x, new_y, collision

def collision_circle(c, radius, v, C, R):
    dx = c[0] - C[0]
    dy = c[1] - C[1]
    dr = radius + R
    collision=False
    if (dx*dx + dy*dy) <= dr * dr: #there is a collision
        collision=True
        v_norm_x = 0 if v[0]==0 else v[0]/math.sqrt(v[0]*v[0]+v[1]*v[1])
        v_norm_y = 0 if v[1]==0 else v[1]/math.sqrt(v[0]*v[0]+v[1]*v[1])
        d = (radius + R) - math.sqrt(dx*dx + dy*dy)
        new_x = c[0] - d * v_norm_x
        new_y = c[1] - d * v_norm_y
        #update velocity
        #n = (new_x - C[0], new_y - C[1])
        #cost = (v[0]*n[0] + v[1]*n[1]) / (math.sqrt(n[0]*n[0]+n[1]*n[1]))
        #v_x = v[0] - cost * n[0]
        #v_y = v[1] - cost * n[1]
    else:
        new_x=c[0]
        new_y=c[1]
        #v_x=v[0]
        #v_y=v[1]
    return new_x, new_y, collision

#to call after every robot update (in the engine, not graphical)
def resolve_collision(start, s, robot_R, ob_list, size):
    s_x=max(robot_R, s[0])
    s_x=min(s_x, size[0]-robot_R)
    s_y=max(robot_R, s[1])
    s_y=min(s_y, size[1]-robot_R)
    m_x=s_x; m_y=s_y
    for ob in ob_list:
        if ob[0] == 'r':
            s_x_tmp, s_y_tmp, collision = collision_rect(s, start, robot_R, ob[1])
        if collision:
            s_x=max(robot_R, s_x_tmp)
            s_x=min(s_x, size[0]-robot_R)
            s_y=max(robot_R, s_y_tmp)
            s_y=min(s_y, size[1]-robot_R)
            if abs(s[0]-s_x)>abs(s[0]-m_x): m_x=s_x
            if abs(s[0]-s_y)>abs(s[0]-m_y): m_y=s_y
    return m_x, m_y