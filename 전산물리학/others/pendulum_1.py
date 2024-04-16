import numpy as np
import matplotlib.pyplot as plt

from numpy.linalg import inv
from math import *

def G(t,y):
    # F[0] = F0 * np.cos(omega * t)
    F[0] = -g * y[1]
    F[1] = y[0]

    return inv_L.dot(F)

def RK4(t, y, delta_t):
    k1 = G(t, y)
    k2 = G(t + 0.5*delta_t, y + 0.5*delta_t * k1)
    k3 = G(t + 0.5*delta_t, y + 0.5*delta_t * k2)
    k4 = G(t + 1.0*delta_t, y + 1.0*delta_t * k3)

    return (k1 + 2.0*k2 + 2.0*k3 + k4)/6.0

g = 9.8
l = 1.0

omega = sqrt(g/l)

delta_t = 0.001
time = np.arange(0,10,delta_t)

theta0 = 60.0 * pi/180
thetadot0 = 0.0

period = 2 * pi * sqrt(l/g)
print ('Period = ', period)

y = np.array([thetadot0,sin(theta0)])
L = np.array([[l,0.0],[0.0,1.0]])
F = np.array([0.0,0.0])

TT = []
VV = []
FF = []

inv_L = inv(L)  #note. inv(A)를 밖에 두어서 연산을 줄여서 최적화 가능 

#time steps 
for t in time:
    y = y + delta_t * RK4(t,y,delta_t)


    # G = (k1+2*k2+2*k3+k4)/6.0

    TT.append(y[1])
    VV.append(y[0])
    FF.append(F[0])

plt.grid(True)
plt.plot(time,TT,'b',time,VV,'r')
plt.show()
