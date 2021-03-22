import numpy as np
from math import sin, cos, atan2, sqrt

MAP = [[0,0,1],[1,1,2],[1,2,3],[4,4,4]]

def kalman_filter(mu_t_1, V_t_1, u_t, z_t): #Pose extimation
    A = np.identity(3)
    C = np.identity(3)
    dt = 1
    theta = mu_t_1[2]
    B = np.array([[dt*cos(theta), 0],[dt*sin(theta), 0],[0, dt]])
    R = np.multiply(np.random.randn(3,3),np.eye(3,3))
    Q = np.multiply(np.random.randn(3,3),np.eye(3,3))

    _mu = A.dot(mu_t_1) + B.dot(u_t)
    _V = A.dot(V_t_1).dot(A.T) + R

    if z_t == None:
        return _mu, _V

    K = _V.dot(C.T).dot(np.linalg.inv(C.dot(_V).dot(C.T) + Q))
    mu = _mu + K.dot(z_t - C.dot(_mu))
    V = (np.eye(3,3)-K.dot(C)).dot(_V)
    return mu, V

def calc_features(p, mappa): #Sensor reading
    f = []
    psi = np.random.randn(3)
    for i in range(len(mappa)):
        r = sqrt(pow((mappa[i][0]-p[0]),2)+pow((mappa[i][1]-p[1]),2)) + psi[0]
        phi = atan2(mappa[i][1]-p[1],mappa[i][0]-p[0]) - p[2] + psi[1]
        s = mappa[i][2] + psi[2]
        f.append([r, phi, s])
    return f

def triangulate(P0, P1, P2, r0, r1, r2):
    EPSILON = 0.001
    dx = P1[0] - P0[0]
    dy = P1[1] - P0[1]
    d = sqrt((dy*dy) + (dx*dx))

    a = ((r0*r0) - (r1*r1) + (d*d)) / (2.0 * d)
    point2_x = P0[0] + (dx * a/d)
    point2_y = P0[1] + (dy * a/d)
    h = sqrt((r0*r0) - (a*a))
    rx = -dy * (h/d)
    ry = dx * (h/d)

    intersectionPoint1_x = point2_x + rx
    intersectionPoint2_x = point2_x - rx
    intersectionPoint1_y = point2_y + ry
    intersectionPoint2_y = point2_y - ry

    dx = intersectionPoint1_x - P2[0]
    dy = intersectionPoint1_y - P2[1]
    d1 = sqrt((dy*dy) + (dx*dx))
    dx = intersectionPoint2_x - P2[0]
    dy = intersectionPoint2_y - P2[1]
    d2 = sqrt((dy*dy) + (dx*dx))

    if(abs(d1 - r2) < EPSILON): return intersectionPoint1_x, intersectionPoint1_y
    if(abs(d2 - r2) < EPSILON): return intersectionPoint2_x, intersectionPoint2_y

def estimate_pose(p, mappa): #p=pose_t, return z_t
    if mappa == None or len(mappa) < 3:
        return None

    # get intersection of two circles (gotten from stack overflow https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles)

    x0 = mappa[0][0]
    y0 = mappa[0][1]
    r0 = sqrt((p[0]-x0)**2 + (p[1] - y0)**2)
    x1 = mappa[1][0]
    y1 = mappa[1][1]
    r1 = sqrt((p[0]-x1)**2 + (p[1] - y1)**2)

    d  = sqrt((x1-x0)**2 + (y1-y0)**2)

    a  = (r0**2-r1**2+d**2)/(2*d)
    h  = sqrt(r0**2-a**2)
    x2 = x0+a*(x1-x0)/d
    y2 = y0+a*(y1-y0)/d

    x3 = x2+h*(y1-y0)/d
    y3 = y2-h*(x1-x0)/d

    x4=x2-h*(y1-y0)/d
    y4=y2+h*(x1-x0)/d

    intersection_1 = (x3, y3)
    intersection_2 = (x4, y4)

    # pick the point that is close to the distance of the third landmark

    r_bearing = sqrt((p[0]-mappa[2][0])**2 + (p[1] - mappa[2][1])**2)

    r_int_1 = sqrt((mappa[2][0]-intersection_1[0])**2 + (mappa[2][1] - intersection_1[1])**2)
    r_int_2 = sqrt((mappa[2][0]-intersection_2[0])**2 + (mappa[2][1] - intersection_2[1])**2)

    if abs(r_int_1 - r_bearing) < 0.1:
        return [intersection_1[0], intersection_1[1], p[2]]
    elif abs(r_int_2 - r_bearing) < 0.1:
        return [intersection_2[0], intersection_2[1], p[2]]

    return None


# def estimate_pose(p, mappa): #p=pose_t, return z_t
#     if len(mappa) < 3:
#         return None

#     pose = np.zeros(3)
#     c = 0
#     theta = 0
#     t = 0
#     f = calc_features(p, mappa)
#     for i in range(len(mappa)-2):
#         for j in range(i+1, len(mappa)-1):
#             for k in range(j+1, len(mappa)):
#                 x, y = triangulate([mappa[i][0],mappa[i][1]], [mappa[j][0],mappa[j][1]], [mappa[k][0],mappa[k][1]], f[i][0], f[j][0], f[k][0])
#                 pose[0]+=x
#                 pose[1]+=y
#                 c+=1
#     pose[0] = pose[0]/c
#     pose[1] = pose[1]/c
#     for i in range(len(mappa)):
#         pose[2] += atan2(mappa[i][1]-pose[1], mappa[i][0]-pose[0])-f[1]
#     pose[2] = pose[2]/c
#     return pose

