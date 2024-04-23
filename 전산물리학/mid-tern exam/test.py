import pygame
import sys 

from math import *
import numpy as np
from numpy.linalg import inv

#setting color 
white = pygame.Color('white')
black = pygame.Color('black')

#setting screen  
width , height = 1000, 800
screen = pygame.display.set_mode((width,height))
screen.fill(black)

pygame.display.update()

clock = pygame.time.Clock()

count = 0

ll = 100
a = 0.0

x_center, y_center = width*0.5, height*0.2

#physics parameter 
g = 9.81
m1, m2 = 1.0, 1.0
l1, l2 = 2.0, 1.0

omega1, omega2 = 0.0, 0.0               # 초기 각속도
theta1, theta2 = 0.1, 60 * 3.14 / 180   # 초기 각도 
gamma = 0.5                             # 감쇠 상수

t, delta_t = 0.0, 0.01

y = np.array([omega1, omega2, theta1, theta2])
L = np.array([[ll,0.0],[0.0,1.0]])
F = np.array([0.0,0.0,0.0,0.0])

inv_L = inv(L)

#Slope(G) function
def G(t,y):
    F[0] = -m2 * l2 * y[1] * y[1] * sin(y[2] - y[3]) - (m1 + m2) * air_g * sin(y[2]) - gamma * y[0]
    F[1] = l1 * y[0] * y[0] * sin(y[2] - y[3]) - air_g * sin(y[3]) - gamma * y[1]
    F[2] = y[0]
    F[3] = y[1]

    L = np.array([
        [(m1+m2)*l1         , m2*cos(y[2]-y[3]) ,0  ,0],
        [l1*cos(y[2]-y[3])  , l2                ,0  ,0],
        [0                  , 0                 ,1  ,0],
        [0                  , 0                 ,0  ,1],
        ])
        
    return np.linalg.inv(L).dot(F)

#RK4 function 
def RK4(t, y, delta_t):
    k1 = G(t, y)
    k2 = G(t + 0.5*delta_t, y + 0.5*delta_t * k1)
    k3 = G(t + 0.5*delta_t, y + 0.5*delta_t * k2)
    k4 = G(t + 1.0*delta_t, y + 1.0*delta_t * k3)

    return (k1 + 2.0*k2 + 2.0*k3 + k4)/6.0

def position(angle1, angle2):
    x1 = 100*l1 * sin(angle1) + x_center
    y1 = 100*l1 * cos(angle1) + y_center

    x2 = 100*l2 * sin(angle2) + x1
    y2 = 100*l2 * cos(angle2) + y1

    return (x1, y1), (x2, y2)

def square(x0,y0,x1,y1,length):
    m = (y1 - y0) / (x1 - x0)
    line_angle = np.arctan(m) - 90/180*np.pi

    length_2 = np.sqrt((x1-x0)**2 + (y1-y0)**2)

    x2 = (length*x1 - (length-length_2)*x0) / (length_2) 
    y2 = (length*y1 - (length-length_2)*y0) / (length_2) 
    
    s1 = (x0-length / 2*cos(line_angle),y0-length / 2*sin(line_angle))
    s2 = (x0+length / 2*cos(line_angle),y0+length / 2*sin(line_angle))
    s3 = (x2+length / 2*cos(line_angle),y2+length / 2*sin(line_angle))
    s4 = (x2-length / 2*cos(line_angle),y2-length / 2*sin(line_angle))

    print(np.arctan(m)*180/np.pi, line_angle*180/np.pi)
    return [s1,s2,s3,s4]

def render(position1_xy, position2_xy):
    square_pos = square(x_center, y_center, position1_xy[0], position1_xy[1], 400)

    screen.fill(black)

    # draw square position
    pygame.draw.line(screen,white,(square_pos[0]),(square_pos[1]),3)
    pygame.draw.line(screen,white,(square_pos[1]),(square_pos[2]),3)
    pygame.draw.line(screen,white,(square_pos[0]),(square_pos[3]),3)
    pygame.draw.line(screen,white,(square_pos[2]),(square_pos[3]),3)

    # Pivot point
    pygame.draw.circle(screen, white, (x_center, y_center) , 30)
    pygame.draw.circle(screen, black, (x_center, y_center) , 20) 
    
    # draw pendulum 2 position
    pygame.draw.line(screen, white,(position1_xy[0], position1_xy[1]), (position2_xy[0],position2_xy[1]), 3)
    pygame.draw.circle(screen, white, (position2_xy[0],position2_xy[1]) , 10)

class airplane_gravity():
    # Define the airplane's gravity function
    def cal_hypergravity(time, g):
        val = -0.008 * time**2 + 0.48 * time - 5.4
        return g * val 

    def hypergravity_time(time, g):
        if time < 20:
            return g
        elif 20 <= time < 45:
            return airplane_gravity.cal_hypergravity(time, g)
        elif 40 <= time < 75:
            return 0 
        elif 75 <= time < 100:
            return airplane_gravity.cal_hypergravity(time-60, g)
        elif 100 <= time <= 120:
            return g

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    count += 1

    position1_xy, position2_xy = position(y[2], y[3])
    render(position1_xy, position2_xy)

    t += delta_t
    air_g = airplane_gravity.hypergravity_time(t, 9.8)
    y = y + delta_t * RK4(t, y, delta_t)

    clock.tick(60)
    pygame.display.update()