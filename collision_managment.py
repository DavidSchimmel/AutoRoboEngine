#**** Environment obstacles and collisions recovery ****#
def create_environment(size, N_obstacle): #create a N_obstacle (random shape, position and dimension) obstacles in the environment
    obstacle_list=[]
    for o in range(N_obstacle):
        if random()<0.5:
            obstacle_list.append(('c',(random()*size[0], random()*size[1]), 10+random()*100))
        else:
            obstacle_list.append(('r',(random()*size[0], random()*size[1], 30+random()*100, 30+random()*100)))
    return obstacle_list
def render_environment(screen, pg, ob_list): #print the environment on the screen
    screen.fill(C.BLACK)
    obstacle_color=(0, 255, 0)
    for o in ob_list:
        if o[0]=='r':
            pg.draw.rect(screen, obstacle_color, o[1])
        elif o[0]=='c':
            pg.draw.circle(screen, obstacle_color, o[1], o[2])

def collision_rect(c, radius, v, r):
   left=r[0]
   top=r[1]
   right=left+r[2]
   bottom=top+r[3]
   closestX = left if c[0] < left else (right if c[0] > right else c[0])
   closestY = top if c[1] < top else (bottom if c[1] > bottom else c[1])
   dx = closestX - c[0]
   dy = closestY - c[1]
   if ( dx * dx + dy * dy ) <= radius * radius: #there is a collision
        new_x=c[0]-dx 
        new_y=c[1]-dy 
        v_x=v[0]
        v_y=v[1]
        if (new_x==left-radius and v[0]>0) or (new_x==right+radius and v[0]<0):
            v_x=0
        if (new_y==top-radius and v[1]>0) or (new_y==bottom+radius and v[1]<0):
            v_y=0
   return new_x, new_y, v_x, v_y
def collision_circle(c, radius, v, C, R):
    dx = c[0] - C[0]
    dy = c[1] - C[1]
    dr = radius + R 
    if (dx*dx + dy*dy) <= dr * dr: #there is a collision
        v_norm_x = v[0]/math.sqrt(v[0]*v[0]+v[1]*v[1])
        v_norm_y = v[1]/math.sqrt(v[0]*v[0]+v[1]*v[1])
        d = (radius + R) - math.sqrt(dx*dx + dy*dy) 
        new_x = c[0] - d * v_norm_x 
        new_y = c[1] - d * v_norm_y 
        #update velocity
        n = (new_x - C[0], new_y - C[1])
        cost = (v[0]*n[0] + v[1]*n[1]) / (math.sqrt(n[0]*n[0]+n[1]*n[1]))
        v_x = v[0] - cost * n[0]
        v_y = v[1] - cost * n[1]
    return new_x, new_y, v_x, v_y

#to call after every robot update (in the engine, not graphical)
def resolve_collision(s, v, robot_R, ob_list):
    for ob in ob_list:
        if ob[0] == 'r':
            s[0], s[1], v[0], v[1] = collision_rect(s, robot_R, v, ob[1])
        elif ob[0] == 'c':
            s[0], s[1], v[0], v[1] = collision_circle(s, robot_R, v, ob[1], ob[2])